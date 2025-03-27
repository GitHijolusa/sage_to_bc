import json
import pymssql
import setup
from datetime import datetime

from empleado import Empleado




def getEmpleadosDb():
    try:
        conn = pymssql.connect(server=setup.ipDb, user=setup.userDb, password=setup.passwordDb, database=setup.db)
        cursor = conn.cursor(as_dict=True)
        rows =''
    except pymssql.Error as e:
        print(f"Error connecting to the database: {e}")
        return []

    try:
        cursor.execute(setup.query)        
        rows = cursor.fetchall()        
    except pymssql.Error as ex:
        if '28000' in str(ex):
            print(f"Authentication error: {ex}")
        elif '18456' in str(ex):
            print(f"Login failed for user: {ex}")
        else:
            print(f"Database error: {ex}")
        
    empleados = []
    for row in rows:

        json_row = {}
        for key, value in row.items():
            if isinstance(value, datetime):
                value = value.isoformat()
            json_row[key] = value

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



    
