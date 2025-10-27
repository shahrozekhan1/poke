from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import sqlite3
from database import get_db
from schemas import PokemonOut, PokemonStat, EvolutionLink

router = APIRouter(prefix="/pokemon", tags=["pokemon"])

def fetch_pokemon_from_db(conn, pokemon_id):
    """Helper function to fetch and construct a single Pokemon object."""
    
    # 1. Fetch main data
    main_cursor = conn.execute("SELECT * FROM pokemon WHERE id = ?", (pokemon_id,))
    pokemon = main_cursor.fetchone()
    if not pokemon:
        return None

    # 2. Fetch types
    types_cursor = conn.execute(
        "SELECT type_name FROM pokemon_types WHERE pokemon_id = ?", (pokemon_id,)
    )
    types = [row['type_name'] for row in types_cursor.fetchall()]
    
    # 3. Fetch abilities
    abilities_cursor = conn.execute(
        "SELECT ability_name FROM pokemon_abilities WHERE pokemon_id = ?", (pokemon_id,)
    )
    abilities = [row['ability_name'] for row in abilities_cursor.fetchall()]
    
    # 4. Fetch stats
    stats_cursor = conn.execute(
        "SELECT stat_name, base_stat FROM pokemon_stats WHERE pokemon_id = ?", (pokemon_id,)
    )
    stats = [PokemonStat(stat_name=row['stat_name'], base_stat=row['base_stat']) for row in stats_cursor.fetchall()]
    
    # 5. Fetch evolution chain
    # This is a bit more complex, we need to find the chain, then get all links
    evo_cursor = conn.execute(
        """
        SELECT el.pokemon_name, el.stage
        FROM evolution_links el
        JOIN evolution_chains ec ON el.chain_id = ec.id
        WHERE ec.chain_identifier = (
            SELECT chain_identifier FROM evolution_chains ec2
            JOIN evolution_links el2 ON ec2.id = el2.chain_id
            WHERE el2.pokemon_name = ?
        )
        ORDER BY el.stage
        """, (pokemon['name'],)
    )
    evolutions = [EvolutionLink(name=row['pokemon_name'], stage=row['stage']) for row in evo_cursor.fetchall()]

    # Construct the final Pydantic object
    pokemon_out = PokemonOut(
        id=pokemon['id'],
        name=pokemon['name'],
        is_evolved=bool(pokemon['is_evolved']),
        types=types,
        abilities=abilities,
        stats=stats,
        evolution_chain=evolutions
    )
    return pokemon_out


@router.get("/", response_model=List[PokemonOut])
def get_all_pokemon(
    search: Optional[str] = Query(None, description="Search by name"),
    type: Optional[str] = Query(None, description="Filter by type"),
    db: sqlite3.Connection = Depends(get_db)
):
    """
    Get a list of all Pokémon, with optional search and type filtering.
    """
    query = "SELECT id FROM pokemon"
    params = []
    
    if search or type:
        query += " WHERE 1=1" # Start where clause
    
    if search:
        query += " AND name LIKE ?"
        params.append(f"%{search.lower()}%")
        
    if type:
        # Join with pokemon_types to filter by type
        query += """
            AND id IN (
                SELECT pokemon_id FROM pokemon_types WHERE type_name = ?
            )
        """
        params.append(type.lower())
        
    query += " ORDER BY id"
    
    try:
        id_cursor = db.execute(query, tuple(params))
        pokemon_ids = [row['id'] for row in id_cursor.fetchall()]
        
        # Now fetch the full data for each matched ID
        pokemon_list = []
        for pid in pokemon_ids:
            pokemon_data = fetch_pokemon_from_db(db, pid)
            if pokemon_data:
                pokemon_list.append(pokemon_data)
                
        return pokemon_list
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")

@router.get("/{pokemon_id}", response_model=PokemonOut)
def get_pokemon_by_id(
    pokemon_id: int,
    db: sqlite3.Connection = Depends(get_db)
):
    """
Two files in public folder:

index.html
app.js

    Get a single Pokémon by its ID.
    """
    try:
        pokemon = fetch_pokemon_from_db(db, pokemon_id)
        if not pokemon:
            raise HTTPException(status_code=404, detail="Pokemon not found")
        return pokemon
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {e}")
