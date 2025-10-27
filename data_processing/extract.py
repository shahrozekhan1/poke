import requests
import logging
from time import sleep
from constants import (
    POKEAPI_BASE_URL,
    POKEMON_ENDPOINT,
    SPECIES_ENDPOINT,
    EVOLUTION_CHAIN_ENDPOINT,
    API_DELAY,
    LOG_FORMAT,
    LOG_LEVEL,
)
import json

# --------------------------------------------------------------------------- #
# Logging setup (shared across all modules)
# --------------------------------------------------------------------------- #
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)


def fetch_pokemon_data(pokemon_id):
    """Fetch Pokémon data including evolution chain from PokeAPI with full logging."""
    
    # Input validation
    if not isinstance(pokemon_id, int) or pokemon_id <= 0:
        logging.error(f"Invalid Pokémon ID: {pokemon_id}. ID must be a positive integer.")
        return None

    url = f"{POKEAPI_BASE_URL}/{POKEMON_ENDPOINT}/{pokemon_id}/"
    
    # Step 1: Fetch main Pokémon data
    try:
        logging.info(f"Fetching Pokémon data for ID: {pokemon_id}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error for Pokémon ID {pokemon_id}: {err}")
        return None
    except requests.exceptions.ConnectionError:
        logging.error("Connection failed. Check your internet.")
        return None
    except requests.exceptions.Timeout:
        logging.error("Request timed out. PokeAPI may be slow.")
        return None
    except requests.exceptions.RequestException as err:
        logging.error(f"Unexpected error fetching Pokémon {pokemon_id}: {err}")
        return None

    try:
        data = response.json()
    except ValueError:
        logging.error("Failed to parse JSON response from PokeAPI.")
        return None

    # Step 2: Fetch species data
    species_url = data.get("species", {}).get("url")
    if not species_url:
        logging.warning(f"No species URL found for Pokémon ID {pokemon_id}")
        return None

    try:
        logging.info(f"Fetching species data from: {species_url}")
        species_response = requests.get(species_url, timeout=10)
        species_response.raise_for_status()
        species_data = species_response.json()
    except requests.exceptions.RequestException as err:
        logging.error(f"Failed to fetch species data: {err}")
        return None
    except ValueError:
        logging.error("Failed to parse species JSON.")
        return None

    # Step 3: Fetch evolution chain
    evolution_chain_url = species_data.get("evolution_chain", {}).get("url")
    if not evolution_chain_url:
        logging.warning(f"No evolution chain URL for Pokémon ID {pokemon_id}")
        return None

    try:
        logging.info(f"Fetching evolution chain from: {evolution_chain_url}")
        evolution_response = requests.get(evolution_chain_url, timeout=10)
        evolution_response.raise_for_status()
        evolution_data = evolution_response.json()
    except requests.exceptions.RequestException as err:
        logging.error(f"Failed to fetch evolution chain: {err}")
        return None
    except ValueError:
        logging.error("Failed to parse evolution chain JSON.")
        return None

    # Helper: Recursively extract evolution names
    def extract_evolution_names(chain):
        names = [chain["species"]["name"]]
        for evolution in chain.get("evolves_to", []):
            names.extend(extract_evolution_names(evolution))
        return names

    try:
        evolution_chain = extract_evolution_names(evolution_data["chain"])
    except Exception as err:
        logging.error(f"Error parsing evolution chain: {err}")
        evolution_chain = []

    # Determine if evolved
    is_evolved = evolution_chain and evolution_chain[0] != data["name"]

    # Build final Pokémon dict
    pokemon = {
        "name": data["name"],
        "id": data["id"],
        "types": [t["type"]["name"] for t in data["types"]],
        "abilities": [a["ability"]["name"] for a in data["abilities"]],
        "stats": {s["stat"]["name"]: s["base_stat"] for s in data["stats"]},
        "evolution_chain": evolution_chain,
        "is_evolved": is_evolved
    }

    logging.info(f"Successfully fetched data for Pokémon: {pokemon['name'].capitalize()} (ID: {pokemon_id})")
    return pokemon



def fetch_pokemon_example():
    """Fetch a single Pokémon (ID 2 - Ivysaur) for testing. Returns data or None."""
    
    TEST_ID = 2
    pokemon_name = "Ivysaur"  # For logging clarity

    logging.info("--- Starting Test Fetch for Pokémon ID: 2 (Ivysaur) ---")

    # Call the main function
    pokemon = fetch_pokemon_data(TEST_ID)

    if pokemon:
        logging.info(f"SUCCESS: Fetched Pokémon - {pokemon['name'].title()} (ID: {pokemon['id']})")
        print(f"Fetched: {pokemon['name'].title()}")  # Keep simple print for console
        return pokemon
    else:
        logging.error(f"FAILED: Could not fetch test Pokémon (ID: {TEST_ID} - {pokemon_name})")
        print("Failed to fetch test Pokémon.")
        return None



# This block only runs when you execute `python extract.py` directly
if __name__ == "__main__":
    pokemon = fetch_pokemon_example()
    if pokemon:
        print("\n✅ Successfully fetched Pokemon data!\n")
        print(json.dumps(pokemon, indent=2))