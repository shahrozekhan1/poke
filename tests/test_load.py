import unittest
from unittest.mock import MagicMock, patch
import sqlite3
from data_processing.load import create_connection, create_tables, load_pokemon


class TestLoad(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("PRAGMA foreign_keys = ON")

    def tearDown(self):
        self.conn.close()

    def test_create_connection_success(self):
        conn = create_connection(":memory:")
        self.assertIsInstance(conn, sqlite3.Connection)
        conn.close()

    def test_create_tables_all(self):
        ok = create_tables(self.conn)
        self.assertTrue(ok)
        tables = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        ).fetchall()
        expected = {
            "pokemon", "types", "abilities", "stats",
            "pokemon_types", "pokemon_abilities", "pokemon_stats",
            "evolution_chains", "evolution_links"
        }
        self.assertSetEqual({t[0] for t in tables}, expected)

    def test_load_full_pokemon(self):
        create_tables(self.conn)

        transformed = {
            "main": {"id": 25, "name": "pikachu", "is_evolved": True},
            "types": ["electric"],
            "abilities": ["static"],
            "stats": [{"stat_name": "hp", "base_stat": 35}],
            "evolution_chain_identifier": "pichu",
            "evolution_links": [
                {"name": "pichu", "stage": 1},
                {"name": "pikachu", "stage": 2},
                {"name": "raichu", "stage": 3}
            ]
        }

        success = load_pokemon(self.conn, transformed)
        self.assertTrue(success)

        cur = self.conn.cursor()

        cur.execute("SELECT * FROM pokemon WHERE id=25")
        self.assertEqual(cur.fetchone()[1], "pikachu")

        cur.execute("SELECT type_name FROM pokemon_types WHERE pokemon_id=25")
        self.assertEqual(cur.fetchone()[0], "electric")

        cur.execute("SELECT base_stat FROM pokemon_stats WHERE pokemon_id=25 AND stat_name='hp'")
        self.assertEqual(cur.fetchone()[0], 35)

        cur.execute("""
            SELECT pokemon_name, stage 
            FROM evolution_links 
            WHERE chain_id=(SELECT id FROM evolution_chains WHERE chain_identifier='pichu') 
            ORDER BY stage
        """)
        rows = cur.fetchall()
        self.assertEqual(rows, [("pichu", 1), ("pikachu", 2), ("raichu", 3)])

    def test_load_idempotent(self):
        create_tables(self.conn)
        transformed = {
            "main": {"id": 1, "name": "bulbasaur", "is_evolved": False},
            "types": [], "abilities": [], "stats": [],
            "evolution_chain_identifier": "bulba",
            "evolution_links": [{"name": "bulbasaur", "stage": 1}]
        }
        self.assertTrue(load_pokemon(self.conn, transformed))
        self.assertTrue(load_pokemon(self.conn, transformed))

    def test_load_missing_main(self):
        self.assertFalse(load_pokemon(self.conn, {}))


if __name__ == "__main__":
    unittest.main()