import unittest

from .context import inkai

import sqlalchemy
import openpyxl

class AcceptanceTest(unittest.TestCase):

    def test_singlerow(self):
        # tests that the application can upload a spreadsheet with a single row
        # ACC03001

        # Test Fixture

        engine_url = 'sqlite+pysqlite:///:memory:'
        engine = sqlalchemy.create_engine(engine_url, echo=True, future=True)
        # fixture - create database
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(
            'singleRowTable',
            metadata,
            sqlalchemy.Column('field1', sqlalchemy.Integer),
            sqlalchemy.Column('field2', sqlalchemy.String(20))
        )
        metadata.create_all(engine)

        # fixture - create spreadsheet
        book = openpyxl.Workbook()
        book.active.title = 'Metadata'
        book.create_sheet('Data')

        book['Metadata']['A1'] = 'singleRowTable'
        book['Metadata']['A2'] = 1
        book['Metadata']['A3'] = 'field1'
        book['Metadata']['B2'] = 2
        book['Metadata']['B3'] = 'field2'
        
        book['Data']['A1'] = 'field1'
        book['Data']['B1'] = 'field2'
        book['Data']['A2'] = 101
        book['Data']['B2'] = 'ejemplo1'
        book['Data']['A3'] = 103
        book['Data']['B3'] = 'ejemplo2'

        # tests

        inkai.load(table, book)

        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text('SELECT field1, field2 FROM singleRowTable'))
            self.assertEqual(result.rowcount, 2)
            row1 = result.first()
            self.assertEqual(row1.field1, 101)
            self.assertEqual(row1.field2, 'ejemplo1')
            row2 = result.fetch()
            self.assertEqual(row2.field1, 103)
            self.assertEqual(row2.field2, 'ejemplo2')

if __name__ == '__main__':
    unittest.main()
