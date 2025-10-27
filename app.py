from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
import sqlite3
from main import run_etl_pipeline, DATABASE_FILE

app = FastAPI()

@app.get("/")
async def root():
    return FileResponse("index.html")


@app.get("/pokemon")
async def get_pokemon():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute("SELECT name FROM pokemon ORDER BY id")
        rows = cur.fetchall()
        return [row["name"] for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# ✅ NEW: Pokémon Filtering API
@app.get("/pokemon/filter")
async def filter_pokemon(
    is_evolved: bool | None = Query(None),
    hp_min: int | None = Query(None),
    attack_min: int | None = Query(None),
    type_name: str | None = Query(None)
):
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        # Base query
        query = """
        SELECT DISTINCT p.name
        FROM pokemon p
        LEFT JOIN pokemon_stats s_hp ON p.id = s_hp.pokemon_id AND s_hp.stat_name = 'hp'
        LEFT JOIN pokemon_stats s_atk ON p.id = s_atk.pokemon_id AND s_atk.stat_name = 'attack'
        LEFT JOIN pokemon_types pt ON p.id = pt.pokemon_id
        WHERE 1=1
        """

        params = []

        if is_evolved is not None:
            query += " AND p.is_evolved = ?"
            params.append(1 if is_evolved else 0)

        if hp_min is not None:
            query += " AND s_hp.base_stat >= ?"
            params.append(hp_min)

        if attack_min is not None:
            query += " AND s_atk.base_stat >= ?"
            params.append(attack_min)

        if type_name:
            query += " AND pt.type_name = ?"
            params.append(type_name.lower())

        query += " ORDER BY p.id"

        cur.execute(query, params)
        rows = cur.fetchall()

        return [row["name"] for row in rows]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.post("/etl/run-pipeline")
async def run_pipeline():
    print("ETL Pipeline STARTED")
    run_etl_pipeline()
    print("ETL Pipeline FINISHED")
    return {"detail": "Pipeline completed."}
