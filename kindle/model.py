import pyodbc
import pandas as pd

DRIVER = ''
SERVER = ''
DB = ''
USER = ''
PASSWORD = ''


class GenericTable:
    def __init__(self, name: str, schema: str = 'dbo', default_table_reference: str = 'table'):
        self.name = name
        self.schema = schema
        self.default_table_reference = default_table_reference
        self.connection = None
        self._login()

    def _login(self, driver: str = DRIVER, server: str = SERVER, database: str = DB, user: str = USER, password: str = PASSWORD):
        self.connection = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}')

    def execut(self):
        pass

    def select(self):
        pass

    def execute_and_return(self):
        pass
