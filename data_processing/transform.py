import logging
from constants import LOG_FORMAT, LOG_LEVEL

logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)


def transform_pokemon_data(pokemon_data: dict) -> dict | None:
    """
    Transform raw Pokémon API data into a structured format for database loading.
    Returns dict on success, None on validation/transform error.
    """
    if not pokemon_data or not isinstance(pokemon_data, dict):
        logging.error("transform_pokemon_data: Input 'pokemon_data' is None or not a dictionary.")
        return None

    pokemon_id = pokemon_data.get("id")
    pokemon_name = pokemon_data.get("name", "Unknown")

    logging.info(f"Transforming data for Pokémon: {pokemon_name} (ID: {pokemon_id})")

    try:
        # === 1. Main Pokémon data ===
        if "id" not in pokemon_data or "name" not in pokemon_data or "is_evolved" not in pokemon_data:
            logging.error(f"Missing required main fields in Pokémon {pokemon_id}: need 'id', 'name', 'is_evolved'")
            return None

        pokemon_main = {
            "id": pokemon_data["id"],
            "name": pokemon_data["name"],
            "is_evolved": bool(pokemon_data["is_evolved"])  # Ensure boolean
        }

        # === 2. Types & Abilities (must be lists) ===
        types = pokemon_data.get("types", [])
        if not isinstance(types, list):
            logging.warning(f"Types is not a list for Pokémon {pokemon_id}. Converting to list.")
            types = [types] if types else []

        abilities = pokemon_data.get("abilities", [])
        if not isinstance(abilities, list):
            logging.warning(f"Abilities is not a list for Pokémon {pokemon_id}. Converting to list.")
            abilities = [abilities] if abilities else []

        # === 3. Stats (must be dict) ===
        raw_stats = pokemon_data.get("stats")
        if not isinstance(raw_stats, dict):
            logging.error(f"Stats must be a dictionary for Pokémon {pokemon_id}, got: {type(raw_stats)}")
            return None

        pokemon_stats = [
            {"stat_name": name, "base_stat": int(value)}
            for name, value in raw_stats.items()
            if isinstance(value, (int, float))  # Only valid numbers
        ]

        if len(pokemon_stats) == 0:
            logging.warning(f"No valid stats found for Pokémon {pokemon_id}")

        # === 4. Evolution Chain (must be non-empty list) ===
        evolution_chain = pokemon_data.get("evolution_chain", [])
        if not evolution_chain or not isinstance(evolution_chain, list) or len(evolution_chain) == 0:
            logging.error(f"Evolution chain is missing or empty for Pokémon {pokemon_id}")
            return None

        evolution_chain_identifier = evolution_chain[0]  # First in chain
        evolution_links = [
            {"name": name, "stage": i + 1}  # Stage starts at 1
            for i, name in enumerate(evolution_chain)
            if isinstance(name, str)
        ]

        if len(evolution_links) == 0:
            logging.error(f"No valid names in evolution chain for Pokémon {pokemon_id}")
            return None

        # === Build final result ===
        transformed = {
            "main": pokemon_main,
            "types": types,
            "abilities": abilities,
            "stats": pokemon_stats,
            "evolution_chain_identifier": evolution_chain_identifier,
            "evolution_links": evolution_links
        }

        logging.info(f"Successfully transformed Pokémon '{pokemon_name}' (ID: {pokemon_id})")
        return transformed

    except Exception as e:
        logging.error(f"Unexpected error transforming Pokémon {pokemon_id}: {e}")
        return None

if __name__ == "__main__":
    # Example of what the transform function does
    print("--- Testing Transform Function ---")
    
    # Example data for Pikachu (what extract.py would provide)
    pikachu_raw_data = {
        'name': 'pikachu',
        'id': 25,
        'types': ['electric'],
        'abilities': ['static', 'lightning-rod'],
        'stats': {'hp': 35, 'attack': 55, 'defense': 40, 
                  'special-attack': 50, 'special-defense': 50, 'speed': 90},
        'evolution_chain': ['pichu', 'pikachu', 'raichu'],
        'is_evolved': True
    }
    
    transformed = transform_pokemon_data(pikachu_raw_data)
    
    import json
    print(json.dumps(transformed, indent=2))