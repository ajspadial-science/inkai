import sqlalchemy
import openpyxl

def load (engine, workbook):
    tableName = workbook['Metadata']['A1'].value
    fields = []
    dataColumns = []
    types = []
    column = 'A'
    for c in workbook['Metadata'].columns:
        fields.append(c[2].value)
        dataColumns.append(c[1].value)
        types.append(c[3].value)
        column = chr(ord(column) + 1)

    for r in workbook['Data'].rows:
        insertValues = []
        for cell, t in zip(r, types):
            value = cell.value
            if t == 'String':
                value = "'" + value + "'"
            else:
                value = str(value)
            insertValues.append(value)
        with engine.connect() as conn:
            conn.execute(
                sqlalchemy.text("INSERT INTO " + tableName + "(" + ",".join(fields) + ") VALUES (" + ",".join(insertValues) +")")
                )
            conn.commit()


