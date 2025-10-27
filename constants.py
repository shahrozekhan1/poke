# constants.py
# Centralised configuration for the Pokémon ETL pipeline

# --------------------------------------------------------------------------- #
# API & Network
# --------------------------------------------------------------------------- #
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
POKEMON_ENDPOINT = "pokemon"
SPECIES_ENDPOINT = "pokemon-species"
EVOLUTION_CHAIN_ENDPOINT = "evolution-chain"



API_DELAY = 0.5           # sleep between calls (rate-limit friendliness)

# --------------------------------------------------------------------------- #
# Database
# --------------------------------------------------------------------------- #
DATABASE_FILE = "db/pokemon_database.db"

# --------------------------------------------------------------------------- #
# ETL Behaviour
# --------------------------------------------------------------------------- #
POKEMON_TO_FETCH = 12             # default for tests / dev; override in prod if needed

# --------------------------------------------------------------------------- #
# Logging (shared format)
# --------------------------------------------------------------------------- #
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"