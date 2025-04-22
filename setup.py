import json
import os

urlEmpleados = None
urlEmpleadosCentro = None
usernameBC = None
passwordBC = None
userDb = None
passwordDb = None
ipDb = None
db = None
query = None

def load_setup_from_json(filepath=os.path.join(os.path.dirname(__file__), "setup.json")):
    
    rutaJson = "dist/setup.json"
    try:
        with open(rutaJson, 'r') as f:
            data = json.load(f)
            global urlEmpleados, urlEmpleadosCentro, usernameBC, passwordBC, userDb, passwordDb, ipDb, db, query
            urlEmpleados = data.get('urlEmpleados', urlEmpleados)  
            urlEmpleadosCentro = data.get('urlEmpleadosCentroMaquina', urlEmpleadosCentro)           
            usernameBC = data.get('usernameBC', usernameBC)            
            passwordBC = data.get('passwordBC', passwordBC)            
            userDb = data.get('userDb', userDb)            
            passwordDb = data.get('passwordDb', passwordDb)            
            ipDb = data.get('ipDb', ipDb)            
            db = data.get('db', db)            
            query = data.get('query', query)            
        print("Configuración cargada correctamente ")
    except FileNotFoundError:
        print("Error: json not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in json.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
load_setup_from_json()
