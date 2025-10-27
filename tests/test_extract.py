import unittest
from unittest.mock import patch, Mock
from data_processing.extract import fetch_pokemon_data


class TestExtract(unittest.TestCase):

    @patch("data_processing.extract.requests.get")
    def test_fetch_success(self, mock_get):
        pokemon_resp = {
            "id": 25,
            "name": "pikachu",
            "types": [{"type": {"name": "electric"}}],
            "abilities": [{"ability": {"name": "static"}}],
            "stats": [{"stat": {"name": "hp"}, "base_stat": 35}],
            "species": {"url": "https://pokeapi.co/api/v2/pokemon-species/25/"}
        }
        species_resp = {
            "evolution_chain": {"url": "https://pokeapi.co/api/v2/evolution-chain/10/"}
        }
        evo_resp = {
            "chain": {
                "species": {"name": "pichu"},
                "evolves_to": [{
                    "species": {"name": "pikachu"},
                    "evolves_to": [{
                        "species": {"name": "raichu"},
                        "evolves_to": []
                    }]
                }]
            }
        }

        mock_get.side_effect = [
            Mock(status_code=200, json=lambda: pokemon_resp),
            Mock(status_code=200, json=lambda: species_resp),
            Mock(status_code=200, json=lambda: evo_resp),
        ]

        result = fetch_pokemon_data(25)

        expected = {
            "id": 25,
            "name": "pikachu",
            "types": ["electric"],
            "abilities": ["static"],
            "stats": {"hp": 35},
            "evolution_chain": ["pichu", "pikachu", "raichu"],
            "is_evolved": True
        }
        self.assertEqual(result, expected)

    @patch("data_processing.extract.requests.get")
    def test_fetch_http_error(self, mock_get):
        mock_resp = Mock(status_code=404)
        mock_resp.raise_for_status.side_effect = (
            __import__("requests").exceptions.HTTPError("404 Not Found")
        )
        mock_get.return_value = mock_resp

        self.assertIsNone(fetch_pokemon_data(99999))

    def test_invalid_id(self):
        self.assertIsNone(fetch_pokemon_data(-1))
        self.assertIsNone(fetch_pokemon_data("abc"))


if __name__ == "__main__":
    unittest.main()