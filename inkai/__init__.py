"""
  This module provides facilities for loading data to a database from a .xlsx file.

  The .xlsx file should fit the following schema:

      - Sheet 'Metadata': it contains information about how to bind data on the xlsx
      file to the database schema

      Cell 'A1': name of the table

      Below the Metadata sheet contains information about the relation between field in the database
      table and columns on the Data sheet of the xslx file. For each column in the data sheet there
      will be a column X on the Metadata sheet with the following values:
        - Cell 'X2': number of the data column
        - Cell 'X3': name of the field on the database table
        - Cell 'X4': type of the value. Currenlty, Integer and String are allowed

      - Sheet 'Data': contains the data. First row is dedicated to name the database field that
      we can find in this column

      This module relies on sqlalchemy and openpyxl for accesing database and xslx files
"""
import sqlalchemy
import openpyxl

def load (engine, workbook):
    """ load the workbook into a database using the engine connection """

    table_name = workbook['Metadata']['A1'].value
    fields = []
    data_columns = []
    types = []
    for column in workbook['Metadata'].columns:
        fields.append(column[2].value)
        data_columns.append(column[1].value)
        types.append(column[3].value)

    for row in workbook['Data'].rows:
        insert_values = []
        for cell, domain in zip(row, types):
            value = cell.value
            if domain == 'String':
                value = "'" + value + "'"
            else:
                value = str(value)
            insert_values.append(value)
        with engine.connect() as conn:
            conn.execute(
                sqlalchemy.text(
                    "INSERT INTO " + table_name + "(" + ",".join(fields) + ") " \
                            "VALUES (" + ",".join(insert_values) +")"
                            )
                )
            conn.commit()
