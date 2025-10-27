import unittest
from data_processing.transform import transform_pokemon_data


class TestTransform(unittest.TestCase):

    def test_transform_full(self):
        raw = {
            "id": 25,
            "name": "pikachu",
            "is_evolved": True,
            "types": ["electric"],
            "abilities": ["static", "lightning-rod"],
            "stats": {"hp": 35, "attack": 55},
            "evolution_chain": ["pichu", "pikachu", "raichu"]
        }
        out = transform_pokemon_data(raw)

        self.assertEqual(out["main"]["id"], 25)
        self.assertEqual(out["main"]["name"], "pikachu")
        self.assertTrue(out["main"]["is_evolved"])

        self.assertEqual(out["types"], ["electric"])
        self.assertEqual(out["abilities"], ["static", "lightning-rod"])

        self.assertEqual(len(out["stats"]), 2)
        self.assertIn({"stat_name": "hp", "base_stat": 35}, out["stats"])

        self.assertEqual(out["evolution_chain_identifier"], "pichu")
        self.assertEqual(len(out["evolution_links"]), 3)
        self.assertEqual(out["evolution_links"][1]["name"], "pikachu")
        self.assertEqual(out["evolution_links"][1]["stage"], 2)

    def test_missing_required_fields(self):
        raw = {"id": 1, "name": "missing_is_evolved"}
        self.assertIsNone(transform_pokemon_data(raw))

    def test_empty_evolution_chain(self):
        raw = {
            "id": 1, "name": "test", "is_evolved": False,
            "types": [], "abilities": [], "stats": {}, "evolution_chain": []
        }
        self.assertIsNone(transform_pokemon_data(raw))

    def test_non_list_types(self):
        raw = {
            "id": 1, "name": "test", "is_evolved": False,
            "types": "fire", "abilities": [], "stats": {}, "evolution_chain": ["a"]
        }
        out = transform_pokemon_data(raw)
        self.assertEqual(out["types"], ["fire"])


if __name__ == "__main__":
    unittest.main()