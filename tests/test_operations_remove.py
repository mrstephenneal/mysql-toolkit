import os
import shutil
import unittest
from looptools import Timer
from differentiate import diff
from mysql.toolkit import MySQL
from tests import config


SQL_SCRIPT = os.path.join(os.path.dirname(__file__), 'data', 'models.sql')
FAILS_DIR = os.path.join(os.path.dirname(__file__), 'data', 'fails')


class TestOperationsRemove(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sql = MySQL(config('testing_models'))

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(FAILS_DIR):
            shutil.rmtree(FAILS_DIR)
        cls.sql.disconnect()

    def tearDown(self):
        self.sql.truncate_database()
        self.sql.execute_script(SQL_SCRIPT)

    @Timer.decorator
    def test_truncate(self):
        table = 'payments'
        self.sql.truncate(table)
        self.assertEqual(self.sql.count_rows(table), 0)

    @Timer.decorator
    def test_truncate_database(self):
        self.sql.truncate_database()
        self.assertEqual(len(self.sql.tables), 0)

    @Timer.decorator
    def test_drop(self):
        tables = ['orders', 'payments']
        existing = self.sql.tables
        self.sql.drop(tables)
        modified = self.sql.tables
        difference = diff(existing, modified)

        self.assertEqual(len(difference), 2)

    @Timer.decorator
    def test_drop_empty_tables(self):
        existing = self.sql.tables

        table = 'payments'
        self.sql.truncate(table)
        self.assertEqual(self.sql.count_rows(table), 0)
        self.sql.drop_empty_tables()

        modified = self.sql.tables
        difference = diff(existing, modified)
        self.assertEqual(len(difference), 1)


if __name__ == '__main__':
    unittest.main()
