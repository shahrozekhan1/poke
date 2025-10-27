import sqlite3
from sqlite3 import Error
import logging
from constants import DATABASE_FILE, LOG_FORMAT, LOG_LEVEL

logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)



def create_connection(db_file):
    """Create a connection to SQLite database with logging and error handling."""
    
    if not db_file or not isinstance(db_file, str):
        logging.error("Invalid database file path: must be a non-empty string.")
        return None

    conn = None
    try:
        logging.info(f"Attempting to connect to SQLite database: {db_file}")
        conn = sqlite3.connect(db_file)
        
        # Enable foreign key support
        conn.execute("PRAGMA foreign_keys = ON")
        
        logging.info(f"Successfully connected to {db_file} (SQLite version: {sqlite3.version})")
        return conn

    except sqlite3.Error as e:
        logging.error(f"SQLite error occurred while connecting to {db_file}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error connecting to database {db_file}: {e}")
    
    # Only reaches here on error
    if conn:
        try:
            conn.close()
        except:
            pass
    logging.warning(f"Failed to connect to database: {db_file}")
    return None




def create_tables(conn):
    """Create all required tables in the SQLite database with detailed logging."""
    
    if not conn:
        logging.error("Cannot create tables: Database connection is None.")
        return False

    # List of (table_name, sql) tuples for clarity and logging
    table_definitions = [
        ("pokemon", """
            CREATE TABLE IF NOT EXISTS pokemon (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                is_evolved BOOLEAN NOT NULL
            );
        """),
        ("types", """
            CREATE TABLE IF NOT EXISTS types (
                name TEXT PRIMARY KEY
            );
        """),
        ("abilities", """
            CREATE TABLE IF NOT EXISTS abilities (
                name TEXT PRIMARY KEY
            );
        """),
        ("stats", """
            CREATE TABLE IF NOT EXISTS stats (
                name TEXT PRIMARY KEY
            );
        """),
        ("pokemon_types", """
            CREATE TABLE IF NOT EXISTS pokemon_types (
                pokemon_id INTEGER,
                type_name TEXT,
                PRIMARY KEY (pokemon_id, type_name),
                FOREIGN KEY (pokemon_id) REFERENCES pokemon (id),
                FOREIGN KEY (type_name) REFERENCES types (name)
            );
        """),
        ("pokemon_abilities", """
            CREATE TABLE IF NOT EXISTS pokemon_abilities (
                pokemon_id INTEGER,
                ability_name TEXT,
                PRIMARY KEY (pokemon_id, ability_name),
                FOREIGN KEY (pokemon_id) REFERENCES pokemon (id),
                FOREIGN KEY (ability_name) REFERENCES abilities (name)
            );
        """),
        ("pokemon_stats", """
            CREATE TABLE IF NOT EXISTS pokemon_stats (
                pokemon_id INTEGER,
                stat_name TEXT,
                base_stat INTEGER NOT NULL,
                PRIMARY KEY (pokemon_id, stat_name),
                FOREIGN KEY (pokemon_id) REFERENCES pokemon (id),
                FOREIGN KEY (stat_name) REFERENCES stats (name)
            );
        """),
        ("evolution_chains", """
            CREATE TABLE IF NOT EXISTS evolution_chains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chain_identifier TEXT UNIQUE NOT NULL
            );
        """),
        ("evolution_links", """
            CREATE TABLE IF NOT EXISTS evolution_links (
                chain_id INTEGER,
                pokemon_name TEXT,
                stage INTEGER,
                PRIMARY KEY (chain_id, pokemon_name),
                FOREIGN KEY (chain_id) REFERENCES evolution_chains (id)
            );
        """)
    ]

    cursor = None
    success_count = 0

    try:
        cursor = conn.cursor()
        logging.info("Starting table creation...")

        for table_name, sql in table_definitions:
            sql = sql.strip()
            try:
                cursor.execute(sql)
                logging.info(f"Table '{table_name}' created or already exists.")
                success_count += 1
            except Error as e:
                logging.error(f"Failed to create table '{table_name}': {e}")

        # Only commit if at least one table was processed
        if success_count > 0:
            conn.commit()
            logging.info(f"Successfully committed {success_count}/{len(table_definitions)} tables.")
        else:
            logging.warning("No tables were created. Rolling back any changes.")
            conn.rollback()

        return success_count == len(table_definitions)  # True if ALL succeeded

    except Error as e:
        logging.error(f"Critical database error in create_tables(): {e}")
        try:
            conn.rollback()
            logging.info("Transaction rolled back due to critical error.")
        except:
            pass
        return False
    except Exception as e:
        logging.error(f"Unexpected error in create_tables(): {e}")
        try:
            conn.rollback()
        except:
            pass
        return False
    finally:
        if cursor:
            cursor.close()
            
            

def load_pokemon(conn, transformed_data: dict):
    """
    Load one Pokémon's transformed data into the database.
    Idempotent using INSERT OR IGNORE.
    Returns True on success, False on any error.
    """
    if not conn:
        logging.error("Cannot load Pokémon: Database connection is None.")
        return False

    if not transformed_data or "main" not in transformed_data:
        logging.error("Invalid transformed_data: missing 'main' section.")
        return False

    pokemon_id = transformed_data["main"].get("id")
    pokemon_name = transformed_data["main"].get("name", "Unknown")

    logging.info(f"Starting load for Pokémon: {pokemon_name} (ID: {pokemon_id})")

    cursor = None
    try:
        cursor = conn.cursor()

        # === 1. Insert into Lookup Tables ===
        try:
            types = [(t,) for t in transformed_data.get("types", [])]
            if types:
                cursor.executemany("INSERT OR IGNORE INTO types (name) VALUES (?)", types)
                logging.debug(f"Inserted {len(types)} type(s).")

            abilities = [(a,) for a in transformed_data.get("abilities", [])]
            if abilities:
                cursor.executemany("INSERT OR IGNORE INTO abilities (name) VALUES (?)", abilities)
                logging.debug(f"Inserted {len(abilities)} ability(s).")

            stats = [(s["stat_name"],) for s in transformed_data.get("stats", [])]
            if stats:
                cursor.executemany("INSERT OR IGNORE INTO stats (name) VALUES (?)", stats)
                logging.debug(f"Inserted {len(stats)} stat name(s).")
        except Error as e:
            logging.error(f"Failed to insert lookup data for Pokémon {pokemon_id}: {e}")
            conn.rollback()
            return False

        # === 2. Insert Evolution Chain ===
        try:
            chain_id = transformed_data.get("evolution_chain_identifier")
            if not chain_id:
                logging.warning(f"No evolution chain identifier for Pokémon {pokemon_id}")
            else:
                cursor.execute("INSERT OR IGNORE INTO evolution_chains (chain_identifier) VALUES (?)", (chain_id,))
                cursor.execute("SELECT id FROM evolution_chains WHERE chain_identifier = ?", (chain_id,))
                row = cursor.fetchone()
                if row:
                    chain_db_id = row[0]
                    links = [(chain_db_id, link["name"], link["stage"]) 
                             for link in transformed_data.get("evolution_links", [])]
                    if links:
                        cursor.executemany("INSERT OR IGNORE INTO evolution_links (chain_id, pokemon_name, stage) VALUES (?, ?, ?)", links)
                        logging.debug(f"Inserted {len(links)} evolution link(s).")
                else:
                    logging.warning(f"Could not retrieve chain_db_id for chain_identifier: {chain_id}")
        except Error as e:
            logging.error(f"Failed to insert evolution chain for Pokémon {pokemon_id}: {e}")
            conn.rollback()
            return False

        # === 3. Insert Main Pokémon ===
        try:
            main = transformed_data["main"]
            cursor.execute(
                "INSERT OR IGNORE INTO pokemon (id, name, is_evolved) VALUES (?, ?, ?)",
                (main["id"], main["name"], main["is_evolved"])
            )
            if cursor.rowcount > 0:
                logging.debug(f"Inserted main Pokémon: {main['name']}")
        except Error as e:
            logging.error(f"Failed to insert main Pokémon {pokemon_id}: {e}")
            conn.rollback()
            return False

        # === 4. Insert Junction Tables ===
        try:
            # Types
            type_data = [(pokemon_id, t) for t in transformed_data.get("types", [])]
            if type_data:
                cursor.executemany("INSERT OR IGNORE INTO pokemon_types (pokemon_id, type_name) VALUES (?, ?)", type_data)

            # Abilities
            ability_data = [(pokemon_id, a) for a in transformed_data.get("abilities", [])]
            if ability_data:
                cursor.executemany("INSERT OR IGNORE INTO pokemon_abilities (pokemon_id, ability_name) VALUES (?, ?)", ability_data)

            # Stats
            stat_data = [(pokemon_id, s["stat_name"], s["base_stat"]) for s in transformed_data.get("stats", [])]
            if stat_data:
                cursor.executemany("INSERT OR IGNORE INTO pokemon_stats (pokemon_id, stat_name, base_stat) VALUES (?, ?, ?)", stat_data)

            logging.debug(f"Inserted junction data: {len(type_data)} types, {len(ability_data)} abilities, {len(stat_data)} stats")

        except Error as e:
            logging.error(f"Failed to insert junction tables for Pokémon {pokemon_id}: {e}")
            conn.rollback()
            return False

        # === Commit ===
        conn.commit()
        logging.info(f"SUCCESS: Fully loaded Pokémon '{pokemon_name}' (ID: {pokemon_id})")
        return True

    except Exception as e:
        logging.error(f"Unexpected error loading Pokémon {pokemon_id}: {e}")
        try:
            conn.rollback()
            logging.info("Transaction rolled back due to error.")
        except:
            pass
        return False
    finally:
        if cursor:
            cursor.close()