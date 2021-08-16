"""
Acceptance tests
"""

import unittest

from .context import inkai

import sqlalchemy
import openpyxl

class AcceptanceTest(unittest.TestCase):
    """ Acceptance Test """

    def test_singlerow(self):
        """
        tests that the application can upload a spreadsheet with a single row
        # ACC03001
        """

        # Test Fixture

        engine_url = 'sqlite+pysqlite:///:memory:'
        engine = sqlalchemy.create_engine(engine_url, echo=True, future=True)
        # fixture - create database
        metadata = sqlalchemy.MetaData()
        sqlalchemy.Table(
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
        book['Metadata']['A4'] = 'Integer'
        book['Metadata']['B2'] = 2
        book['Metadata']['B3'] = 'field2'
        book['Metadata']['B4'] = 'String'

        book['Data']['A1'] = 101
        book['Data']['B1'] = 'ejemplo1'

        # tests

        inkai.load(engine, book)

        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text('SELECT COUNT(*) FROM singleRowTable'))
            self.assertEqual(result.scalar(), 1)
            result = conn.execute(sqlalchemy.text('SELECT field1, field2 FROM singleRowTable'))
            row1 = result.mappings().first()
            self.assertEqual(row1.field1, 101)
            self.assertEqual(row1.field2, 'ejemplo1')

if __name__ == '__main__':
    unittest.main()
