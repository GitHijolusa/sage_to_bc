# from db_query import empleados
from bc_requests import business_central_request
import db_query
from datetime import datetime
from empleado import Empleado
from setup import urlEmpleados, urlEmpleadosCentro, direct_unit_cost, indirect_cost_percent

postEmpleados = []
postEmpleadosCentro = []
patchEmpleados = []
empleadosDB = []
empleadosBc = []
empleadoCentroMaquina = []

def getEmpleadosBC():
    """
    Retrieves employee data from Business Central.

    This function sends a GET request to the Business Central API to retrieve a list of employees.
    It then parses the JSON response and creates Empleado objects for each employee found.
    The employee data is stored in the global empleadosBc list.

    """
    """
    Obtiene los códigos de empleado de Business Central.

    Args:
        url (str): La URL del servicio web.
        username (str): El nombre de usuario para la autenticación NTLM.
        password (str): La contraseña para la autenticación NTLM.

    Returns:
        list: Una lista con los códigos de empleado.
    """
    
    try:
        responseData = business_central_request(url=urlEmpleados, method='GET')
        print(responseData)
        if responseData:
            for item in responseData['value']:
                empleado = Empleado()
                empleado.CodigoEmpleado = item.get('No')
                empleado.NombreEmpleado = item.get('Name')
                empleado.PrimerApellidoEmpleado = item.get('First_Family_Name')
                empleado.SegundoApellidoEmpleado = item.get('Second_Family_Name')
                empleado.DireccionCompleta = item.get('Address')
                empleado.CodigoPostal = item.get('Post_Code')
                empleado.Municipio = item.get('City')
                empleado.Provincia = item.get('County')
                empleado.Telefono = item.get('Phone_No_2')
                empleado.TelefonoMovil = item.get('Mobile_Phone_No')
                empleado.EMail1 = item.get('E_Mail')
                empleado.FechaNacimiento = item.get('Birth_Date')
                empleado.Dni = item.get('CifNif_MPX_LDR')
                empleado.IBANReceptor = item.get('Bank_Account_No')
                empleado.Sexo = item.get('Gender')
                empleado.FechaInicioContrato = item.get('Employment_Date')
                empleado.FechaFinalContrato = item.get('Termination_Date')
                empleado.SiglaNacion = item.get('Country_Region_Code')
                empleado.ProvNumSoe = item.get('Social_Security_No')
                empleado.odata_etag = item.get('@odata.etag')
                empleado.estado = item.get('Status')
                # ... asignar otros atributos si es necesario ...

                empleadosBc.append(empleado)                

    except TypeError as e:
        print(f"Error: {e}")
    # print (f"Empleados en BC: {len(listaEmpleadosBC)} ")
    #for empleado in empleadosBc:
        #print(empleado)
    return empleadosBc

def getEmpleadosCentroMaquina():
    """
    Retrieves employee data from the "Centro Maquina" endpoint in Business Central.

    This function sends a GET request to the Business Central API to retrieve a list of employees
    from the "Centro Maquina" endpoint. It then parses the JSON response and creates Empleado
    objects for each employee found. The employee data is stored in the global
    empleadoCentroMaquina list.
    """
        
    try:        
        responseData = business_central_request(url=urlEmpleadosCentro, method='GET')
        print(responseData)
        if responseData:
            for item in responseData['value']:
                empleado = Empleado()
                empleado.CodigoEmpleado = item.get('No')
                empleado.NombreEmpleado = item.get('Name')
                empleado.estado = item.get('Status')               
                empleado.direct_unit_cost = item.get('Direct_Unit_Cost')
                empleado.indirect_cost_percent = item.get('Indirect_Cost_Percent')

                empleadoCentroMaquina.append(empleado)                

    except TypeError as e:
        print(f"Error: {e}")
    return empleadoCentroMaquina

def getEmpleadosDB():
    """
    Retrieves employee data from the database.

    This function calls the getEmpleadosDb function from the db_query module to retrieve
    employee data from the database. The retrieved data is stored in the global empleadosDB list.
    """
    global empleadosDB
    empleadosDB = db_query.getEmpleadosDb()

def getdiffEmpleados():
    """
    Compares employee data between the database, Business Central, and Centro Maquina.

    This function compares the employee data in empleadosDB, empleadosBc, and empleadoCentroMaquina
    to identify new employees, modified employees, and employees that need to be added to Centro Maquina.
    """
    
    print(f"empleados en DB: {len(empleadosDB)}")
    print(f"empleados en BC: {len(empleadosBc)}")
    print(f"empleados en centro maquina: {len(empleadoCentroMaquina)}")

    for empleadoDB in empleadosDB:
        if empleadoDB.Sexo == "Hombre":            
            empleadoDB.Sexo = "Male"            
        elif empleadoDB.Sexo == "Mujer":            
            empleadoDB.Sexo = "Female" 
            
    empleadosBc_dict = {emp.CodigoEmpleado: emp for emp in empleadosBc}

    for empleadoDB in empleadosDB:
        codigo_empleado_db = empleadoDB.CodigoEmpleado
        empleadoBC = empleadosBc_dict.get(codigo_empleado_db)

        if empleadoBC:
            # Se encontró el empleado en Business Central, verificamos si algún campo necesita actualización
            campos_a_verificar = [
                "NombreEmpleado:", "PrimerApellidoEmpleado:", "SegundoApellidoEmpleado:",
                "DireccionCompleta:", "Municipio:", "CodigoPostal:", "Provincia:",
                "Telefono:", "TelefonoMovil:", "EMail1:", "FechaNacimiento:",
                "Dni:", "Sexo:", "FechaInicioContrato:", "FechaFinalContrato:",
                "SiglaNacion:", "ProvNumSoe:", "Estado:"
            ]

            necesita_actualizacion = False
            for campo in campos_a_verificar:
                valor_db = getattr(empleadoDB, campo, None)
                valor_bc = getattr(empleadoBC, campo, None)

                if campo == "FechaNacimiento" or campo == "FechaInicioContrato" or campo == "FechaFinalContrato":
                    fecha_db = str(valor_db)[:10].strip() if valor_db else ""
                    fecha_bc = str(valor_bc)[:10].strip() if valor_bc else ""
                    
                    if fecha_db != fecha_bc and fecha_bc != "0001-01-01":
                        necesita_actualizacion = True
                elif str(valor_db).strip() != str(valor_bc).strip():
                    print(f"Campo diferente: {campo} - Valor en DB: {valor_db}, Valor en BC: {valor_bc} - Empleado: {codigo_empleado_db}")
                    necesita_actualizacion = str(valor_db).strip() != str(valor_bc).strip()
                    break  # Si encontramos una diferencia, no es necesario seguir verificando

            if necesita_actualizacion:
                empleado_modificado = Empleado()  # Creamos un nuevo objeto para el PATCH
                empleado_modificado.CodigoEmpleado = codigo_empleado_db
                empleado_modificado.odata_etag = empleadoBC.odata_etag
                # Copiamos todos los campos del empleado de la base de datos al objeto modificado
                empleado_modificado.__dict__.update({k: v for k, v in empleadoDB.__dict__.items() if k != 'odata_etag'})

                # Verificamos si ya está en la lista de PATCH para evitar duplicados
                if empleado_modificado.CodigoEmpleado not in [emp.CodigoEmpleado for emp in patchEmpleados]:
                    patchEmpleados.append(empleado_modificado)


    for empleadoBC in empleadosBc:
        found_centro = False
        for empleadoCentro in empleadoCentroMaquina:
            if empleadoBC.CodigoEmpleado == empleadoCentro.CodigoEmpleado:
                found_centro = True
                break
        
        if empleadoBC.estado == "Active" and not found_centro:
            postEmpleadosCentro.append(empleadoBC)
                

    print(f"Total number of new employees in centro maquina: {len(postEmpleadosCentro)}")
    print(f"Total number of new employees: {len(postEmpleados)}")
    print(f"Total number of patch employees: {len(patchEmpleados)}")
import openpyxl

def contar_empleados_activos_db():
    """
    Cuenta el número de empleados inactivos en la base de datos.

    Returns:
        int: El número de empleados inactivos.
    """
    empleados_inactivos = [empleado for empleado in empleadosDB if empleado.estado == "Active"]
    print(f"Total number of active employees: {len(empleados_inactivos)}")
    return len(empleados_inactivos)

def get_empleado_db(codigo_empleado):
    """
    Retrieves a specific employee from the database by their code.

    Args:
        codigo_empleado (str): The code of the employee to retrieve.

    Returns:
        Empleado: An Empleado object representing the employee, or None if not found.
    """
    for empleado in empleadosDB:
        if empleado.CodigoEmpleado == codigo_empleado:
            print(empleado)
            return empleado
    return None



def generarExcel(empleados, nombreArchivo):
    """
    Generates an Excel file from a list of employee objects.

    Args:
        empleados (list): A list of Empleado objects.
        nombreArchivo (str): The name of the Excel file to be created.

    """

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Escribir encabezados
    if empleados:
        encabezados = list(empleados[0].__dict__.keys())
        sheet.append(encabezados)

        # Escribir datos
        for empleado in empleados:
            fila = [str(getattr(empleado, header)) for header in encabezados]
            sheet.append(fila)

        workbook.save(nombreArchivo)

    workbook.save(nombreArchivo)

def generarExcels():
    """
    Generates Excel files for new and modified employees.

    This function calls generarExcel to create two Excel files: one for new employees and one for modified employees.
    """
    generarExcel(postEmpleados, "empleados_nuevos.xlsx")
    generarExcel(patchEmpleados, "empleados_modificados.xlsx")
    generarExcel(empleadoCentroMaquina, "empleados_centro_maquina.xlsx")
    

def postEmpleadosBC():
    """ This function iterates through the list of Empleado objects retrieved by getEmpleadosDB().
      For each employee, it constructs a dictionary data containing the employee's information,
    Posts new employees to Business Central.

    This function iterates through the list of Empleado objects in postEmpleados.
    For each employee, it constructs a dictionary data containing the employee's information,
    mapping field names from the database to corresponding fields in Business Central.
    It then calls the business_central_request function (with a POST request)
    to create the new employee in Business Central, passing the data dictionary as the request body.
    """
        
    empleados_codigos = [empleado.CodigoEmpleado for empleado in empleadosBc]

    for empleado in postEmpleados:
        try:
            data = {
                "No": empleado.CodigoEmpleado,
                "CifNif_MPX_LDR": empleado.Dni,
                "Name": empleado.NombreEmpleado,
                "First_Family_Name": empleado.PrimerApellidoEmpleado,
                "Second_Family_Name": empleado.SegundoApellidoEmpleado,
                "Phone_No_2": empleado.Telefono,
                "Address": empleado.DireccionCompleta,
                "City": empleado.Municipio,
                "County": empleado.Provincia,
                "Post_Code": empleado.CodigoPostal,
                "Country_Region_Code": empleado.SiglaNacion,
                "Mobile_Phone_No": empleado.TelefonoMovil,
                "E_Mail": empleado.EMail1,
                "Birth_Date": empleado.FechaNacimiento,
                "Social_Security_No": empleado.ProvNumSoe,
                "Bank_Account_No": empleado.IBANReceptor,
                "Status": empleado.estado,
                "Gender": empleado.Sexo,
                "Employment_Date": empleado.FechaInicioContrato,
                "Termination_Date": empleado.FechaFinalContrato
            }
            if empleado.Sexo == "Hombre":
                data["Gender"] = "Male"
            elif empleado.Sexo == "Mujer":
                data["Gender"] = "Female"
                
            data["Birth_Date"] = empleado.FechaNacimiento if empleado.FechaNacimiento else None
            
            if empleado.FechaFinalContrato is None:
                data["Termination_Date"] = None
            else:
                data["Termination_Date"] = empleado.FechaFinalContrato
            
            if empleado.FechaInicioContrato is None:
                data["Employment_Date"] = None
            else:
                data["Employment_Date"] = empleado.FechaInicioContrato

            if empleado.CodigoEmpleado not in empleados_codigos or len(empleados_codigos) == 0:
                response = business_central_request(url=urlEmpleados, method='POST', data=data)
                if response is not None:                    
                    print(f"Empleado {empleado.NombreEmpleado} con codigo {empleado.CodigoEmpleado} creado correctamente en Business Central.")
                else:
                    print(f"Error al crear el empleado {empleado.NombreEmpleado} en Business Central.")
            else:
                print(f"El empleado {empleado.NombreEmpleado} con código {empleado.CodigoEmpleado} ya existe en Business Central.")
            
        except Exception as e:
            print(f"Error al procesar el empleado {empleado.NombreEmpleado}: {e}")


def postEmpleadosCentroMaquina():
    """
    Posts new employees to the "Centro Maquina" endpoint in Business Central.

    This function iterates through the list of Empleado objects in postEmpleadosCentro.
    For each employee, it constructs a dictionary data containing the employee's information,
    mapping field names from the database to corresponding fields in Business Central.
    It then calls the business_central_request function (with a POST request)
    to create the new employee in Business Central, passing the data dictionary as the request body.
    """
    
    empleados_codigos = [empleado.CodigoEmpleado for empleado in empleadoCentroMaquina]
    

    for empleado in postEmpleadosCentro:
        try:
            data = {
                "No": empleado.CodigoEmpleado,
                "Name":empleado.NombreEmpleado,
                "Direct_Unit_Cost": direct_unit_cost,
                "Indirect_Cost_Percent": indirect_cost_percent
            }

            if empleado.CodigoEmpleado not in empleados_codigos or len(empleados_codigos) == 0:
                response = business_central_request(url=urlEmpleadosCentro, method='POST', data=data)
                if response is not None:                    
                    print(f"Empleado {empleado.NombreEmpleado} con codigo {empleado.CodigoEmpleado} creado correctamente en Business Central.")
                else:
                    print(f"Error al crear el empleado {empleado.NombreEmpleado} en Business Central.")
            else:
                print(f"El empleado {empleado.NombreEmpleado} con código {empleado.CodigoEmpleado} ya existe en Business Central.")
            
        except Exception as e:
            print(f"Error al procesar el empleado {empleado.NombreEmpleado}: {e}")

        
def patchEmpleadosBC():
    """
    Updates existing employees in Business Central.

    This function iterates through the list of Empleado objects that need to be updated in Business Central.
    For each employee, it constructs a dictionary data containing the employee's information,
    mapping field names from the database to corresponding fields in Business Central.
    It then calls the business_central_request function (with a PATCH request)
    to update the employee in Business Central, passing the data dictionary as the request body.
    The function includes error handling and prints success/failure messages for each employee update attempt. 
    """
    for empleado in patchEmpleados:
        try:
            data = {
                "No": empleado.CodigoEmpleado,
                "CifNif_MPX_LDR": empleado.Dni,
                "Name": empleado.NombreEmpleado,
                "First_Family_Name": empleado.PrimerApellidoEmpleado,
                "Second_Family_Name": empleado.SegundoApellidoEmpleado,
                "Phone_No_2": empleado.Telefono,
                "Address": empleado.DireccionCompleta,
                "City": empleado.Municipio,
                "County": empleado.Provincia,
                "Post_Code": empleado.CodigoPostal,
                "Country_Region_Code": empleado.SiglaNacion,
                "Mobile_Phone_No": empleado.TelefonoMovil,
                "E_Mail": empleado.EMail1,
                "Social_Security_No": empleado.ProvNumSoe,
                "Bank_Account_No": empleado.IBANReceptor,
                "Birth_Date": empleado.FechaNacimiento,
                "Status": empleado.estado,                
                "Gender": empleado.Sexo
            }
            if empleado.Sexo == "Hombre":
                data["Gender"] = "Male"
            elif empleado.Sexo == "Mujer":
                data["Gender"] = "Female"
            
            if empleado.FechaFinalContrato is None:
                data["Termination_Date"] = None
            else:
                data["Termination_Date"] = empleado.FechaFinalContrato
            
            if empleado.FechaInicioContrato is None:
                data["Employment_Date"] = None
            else:
                data["Employment_Date"] = empleado.FechaInicioContrato

            response = business_central_request(url=urlEmpleados, method='PATCH', data=data, etag=empleado.odata_etag, id=empleado.CodigoEmpleado)            
            if response:
                print(f"Empleado {empleado.NombreEmpleado} actualizado correctamente en Business Central.")
            else:
                print(f"Error al actualizar el empleado {empleado.NombreEmpleado} en Business Central.")
        except Exception as e:
            print(f"Error al procesar el empleado {empleado.NombreEmpleado}: {e}")

def deleteAllEmpleadosBC():
    """
    Deletes all employee records from the Business Central web service.

    This function retrieves all employees from Business Central, then iterates through them,
    sending a DELETE request for each employee to remove them from the system.
    """
    empleados = getEmpleadosBC()
    if empleados:
        for empleado in empleados:
            try:
                # Assuming DELETE operation is supported and the URL structure is similar to PATCH
                response = business_central_request(url=urlEmpleados, method='DELETE', id=empleado.CodigoEmpleado)
                if response:
                    print(f"Empleado {empleado.NombreEmpleado} (ID: {empleado.CodigoEmpleado}) eliminado correctamente de Business Central.")
                else:
                    print(f"Error al eliminar el empleado {empleado.NombreEmpleado} (ID: {empleado.CodigoEmpleado}) de Business Central.")
            except Exception as e:
                print(f"Error al procesar la eliminación del empleado {empleado.NombreEmpleado} (ID: {empleado.CodigoEmpleado}): {e}")
    else:
        print("No se encontraron empleados en Business Central.")

def get_etag_for_employee(employee_id):
    """
    Retrieves the ETag for a specific employee from Business Central.

    Args:
        employee_id (str): The ID of the employee to retrieve the ETag for.

    Returns:
        str: The ETag of the employee, or None if the employee is not found or an error occurs.
    """
    try:
        # Construct the URL for the specific employee
        employee_url = f"{urlEmpleados}('{employee_id}')"
        
        # Make a GET request to retrieve the employee data
        response = business_central_request(url=employee_url, method='GET')
        
        if response and '@odata.etag' in response:
            print(f"ETag for employee {employee_id}: {response['@odata.etag']}")
            return response['@odata.etag']
            
        else:
            print(f"Employee with ID {employee_id} not found or ETag not available.")
            return None
    except Exception as e:
        print(f"Error retrieving ETag for employee {employee_id}: {e}")
        return None
