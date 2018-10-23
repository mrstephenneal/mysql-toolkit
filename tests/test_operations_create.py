import os
import shutil
import unittest
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

    # def tearDown(self):
    #     self.sql.truncate_database()
    #     self.sql.execute_script(SQL_SCRIPT)

    def test_drop_empty_tables(self):
        rows = self.sql.select_all('employees')

        ct = self.sql.create_table('workers', rows, self.sql.get_columns('employees'))
        self.assertIn('workers', self.sql.tables)
        self.assertEqual(self.sql.get_primary_key('workers'), 'employeeNumber')


if __name__ == '__main__':
    unittest.main()