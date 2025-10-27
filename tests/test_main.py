# tests/test_main.py

import unittest
from unittest.mock import patch, MagicMock
from main import run_etl_pipeline


class TestMain(unittest.TestCase):

    @patch("main.POKEMON_TO_FETCH", 2)  # Patch main's copy!
    @patch("main.sleep")
    @patch("main.load_pokemon")
    @patch("main.transform_pokemon_data")
    @patch("main.fetch_pokemon_data")
    @patch("main.create_tables")
    @patch("main.create_connection")
    def test_pipeline_success(
        self, mock_create_conn, mock_create_tables,
        mock_fetch, mock_transform, mock_load, mock_sleep
    ):
        # ---- mocks ----
        conn = MagicMock()
        mock_create_conn.return_value = conn
        mock_create_tables.return_value = True

        mock_fetch.side_effect = [
            {"id": 1, "name": "bulbasaur", "is_evolved": False,
             "types": [], "abilities": [], "stats": {}, "evolution_chain": ["bulbasaur"]},
            {"id": 2, "name": "ivysaur", "is_evolved": True,
             "types": [], "abilities": [], "stats": {}, "evolution_chain": ["bulbasaur", "ivysaur"]}
        ]

        mock_transform.side_effect = lambda d: {
            "main": {"id": d["id"], "name": d["name"], "is_evolved": d["is_evolved"]},
            "types": [], "abilities": [], "stats": [],
            "evolution_chain_identifier": d["evolution_chain"][0],
            "evolution_links": [{"name": n, "stage": i + 1} for i, n in enumerate(d["evolution_chain"])]
        }

        mock_load.return_value = True

        # ---- run ----
        result = run_etl_pipeline()

        self.assertTrue(result)
        self.assertEqual(mock_fetch.call_count, 2)
        self.assertEqual(mock_transform.call_count, 2)
        self.assertEqual(mock_load.call_count, 2)

    @patch("main.create_connection")
    def test_pipeline_db_failure(self, mock_conn):
        mock_conn.return_value = None
        self.assertFalse(run_etl_pipeline())


if __name__ == "__main__":
    unittest.main()