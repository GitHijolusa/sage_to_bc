import json
import pyodbc
import setup
from datetime import datetime

from empleado import Empleado




def getEmpleadosDb():
    conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={setup.ipDb};'
    f'DATABASE={setup.db};'
    f'UID={setup.userDb};'
    f'PWD={setup.passwordDb};'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    rows =''

    try:
        cursor.execute(setup.query)
        rows = cursor.fetchall()
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '28000':
            print("Authentication error. Check your username and password.")
        else:
            print(f"Database error: {ex}")
        
    empleados = []
    for row in rows:

        json_row = {}
        for i, col in enumerate(cursor.description):
            value = row[i]
            if isinstance(value, datetime):
                value = value.isoformat()
            json_row[col[0]] = value

        # print(json.dumps(json_row, indent=4))
        # Create an Empleado object from each row
        empleado = Empleado()
        empleado.__dict__.update(json_row)

        print(f"Processing employee: {empleado.NombreEmpleado}")
        #Process empleado object here, for example:
        empleados.append(empleado)
        empleado.CodigoEmpleado = str(empleado.CodigoEmpleado).zfill(5)
        if empleado.Sexo == 1:
            empleado.Sexo = 'Hombre'
        elif empleado.Sexo == 2:
            empleado.Sexo = 'Mujer'



    cursor.close()
    conn.close()
    print(f"Total number of employees: {len(empleados)}")
    for empleado in empleados:
        print(empleado)
    return empleados



    
