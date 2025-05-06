import json
import os
import sys

def get_resource_path():

    if hasattr(sys, 'frozen'):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(__file__)

def load_setup_from_json():
    
    rutaJson = os.path.join(get_resource_path(), "dist", "setup.json")
    
    try:
        with open(rutaJson, 'r') as f:
            data = json.load(f)
            global urlEmpleados, urlEmpleadosCentro, usernameBC, passwordBC, userDb, passwordDb, ipDb, db, query, direct_unit_cost, indirect_cost_percent
            urlEmpleados = data.get('urlEmpleados', urlEmpleados)  
            urlEmpleadosCentro = data.get('urlEmpleadosCentro', urlEmpleadosCentro)           
            usernameBC = data.get('usernameBC', usernameBC)            
            passwordBC = data.get('passwordBC', passwordBC)            
            userDb = data.get('userDb', userDb)            
            passwordDb = data.get('passwordDb', passwordDb)            
            ipDb = data.get('ipDb', ipDb)            
            db = data.get('db', db)            
            query = data.get('query', query)
            direct_unit_cost = data.get('Direct_Unit_Cost', direct_unit_cost)
            indirect_cost_percent = data.get('Indirect_Cost_Percent', indirect_cost_percent)
        print("Configuración cargada correctamente ")
    except FileNotFoundError:
        print("Error: json not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in json.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
urlEmpleados = None
urlEmpleadosCentro = None
usernameBC = None
passwordBC = None
userDb = None
passwordDb = None
ipDb = None
db = None
query = None
direct_unit_cost = None
indirect_cost_percent = None
        

load_setup_from_json()
