import sqlite3
from time import sleep
import logging
from tqdm import tqdm

from data_processing.extract import fetch_pokemon_data
from data_processing.transform import transform_pokemon_data
from data_processing.load import create_connection, create_tables, load_pokemon

from constants import (
    DATABASE_FILE,
    POKEMON_TO_FETCH,
    API_DELAY,
    LOG_FORMAT,
    LOG_LEVEL,
)



logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)


# --- Configuration ---
DATABASE_FILE = "db/pokemon_database.db" 


def run_etl_pipeline():
    """Run the full ETL pipeline: Extract → Transform → Load."""
    
    conn = None
    success_count = 0
    failure_count = 0

    try:
        # === 1. Database Setup ===
        logging.info("Starting ETL pipeline setup...")
        conn = create_connection(DATABASE_FILE)
        if not conn:
            raise Exception("Failed to connect to database.")

        if not create_tables(conn):
            logging.warning("Some tables failed to create. Continuing anyway...")

        logging.info(f"Starting ETL for first {POKEMON_TO_FETCH} Pokémon")

        # === 2. Main ETL Loop with Progress Bar ===
        # Use tqdm for nice progress bar (fallback to range if not installed)
        try:
            pbar = tqdm(range(1, POKEMON_TO_FETCH + 1), desc="Processing Pokémon", unit="poke")
        except:
            pbar = range(1, POKEMON_TO_FETCH + 1)

        for i in pbar:
            pokemon_name = f"ID:{i}"

            try:
                # --- EXTRACT ---
                logging.debug(f"Extracting Pokémon ID: {i}")
                raw_data = fetch_pokemon_data(i)

                if not raw_data:
                    logging.warning(f"Could not fetch data for ID: {i}")
                    failure_count += 1
                    if isinstance(pbar, tqdm):
                        pbar.set_postfix({"Last": "Not Fetched", "Success": success_count, "Fail": failure_count})
                    continue

                pokemon_name = raw_data["name"].title()

                # --- TRANSFORM ---
                transformed_data = transform_pokemon_data(raw_data)
                if not transformed_data:
                    logging.warning(f"Transformation failed for {pokemon_name} (ID: {i})")
                    failure_count += 1
                    if isinstance(pbar, tqdm):
                        pbar.set_postfix({"Last": pokemon_name, "Success": success_count, "Fail": failure_count})
                    continue

                # --- LOAD ---
                if load_pokemon(conn, transformed_data):
                    success_count += 1
                    logging.info(f"Successfully loaded {pokemon_name} (ID: {i})")
                else:
                    failure_count += 1
                    logging.error(f"Failed to load {pokemon_name} (ID: {i})")

                # Update progress bar
                if isinstance(pbar, tqdm):
                    pbar.set_postfix({"Last": pokemon_name, "Success": success_count, "Fail": failure_count})

            except Exception as e:
                failure_count += 1
                logging.error(f"Unexpected error processing Pokémon ID {i}: {e}")
                if isinstance(pbar, tqdm):
                    pbar.set_postfix({"Last": pokemon_name, "Success": success_count, "Fail": failure_count})

            # Respect API rate limit
            sleep(API_DELAY)

        # === 3. Summary ===
        total = success_count + failure_count
        logging.info("=" * 50)
        logging.info("ETL PIPELINE COMPLETE")
        logging.info(f"Total Processed : {total}")
        logging.info(f"Successfully Loaded  : {success_count}")
        logging.info(f"Failed           : {failure_count}")
        logging.info("=" * 50)

    except Exception as e:
        logging.critical(f"CRITICAL ERROR in ETL pipeline: {e}")
        return False
    finally:
        if conn:
            try:
                conn.close()
                logging.info("Database connection closed.")
            except:
                logging.error("Failed to close database connection.")
    
    return success_count > 0

if __name__ == "__main__":
    run_etl_pipeline()
    
    
    