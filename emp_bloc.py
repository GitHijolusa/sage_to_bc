# from db_query import empleados
from bc_requests import business_central_request
import db_query
from datetime import datetime
from empleado import Empleado
# import setup
postEmpleados = []
patchEmpleados = []
empleadosDB = []
empleadosBc = []

def getEmpleadosBC():
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
        responseData = business_central_request(method='GET')
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
                # ... asignar otros atributos si es necesario ...

                empleadosBc.append(empleado)

    except TypeError as e:
        print(f"Error: {e}")
    # print (f"Empleados en BC: {len(listaEmpleadosBC)} ")
    for empleado in empleadosBc:
        print(empleado)
    return empleadosBc

def getEmpleadosDB():
    global empleadosDB
    empleadosDB = db_query.getEmpleadosDb()

def getdiffEmpleados():
    print(f"empleados en BC: {len(empleadosBc)}")
    print(f"empleados en DB: {len(empleadosDB)}")

    for empleadoDB in empleadosDB:
        if empleadoDB.Sexo == "Hombre":
            empleadoDB.Sexo = "Male"
        elif empleadoDB.Sexo == "Mujer":
            empleadoDB.Sexo = "Female"
            
    for empleadoDB in empleadosDB:
        found = False
        for empleadoBC in empleadosBc:
                if empleadoDB.__dict__ != empleadoBC.__dict__ :
                    empleadoDB.odata_etag = empleadoBC.odata_etag
                    empleadoDB.CodigoEmpleado = empleadoBC.CodigoEmpleado                    
                    if empleadoDB.CodigoEmpleado not in [emp.CodigoEmpleado for emp in patchEmpleados]:
                        patchEmpleados.append(empleadoDB)
                    found = True
                    break
                elif empleadoDB.CodigoEmpleado == empleadoBC.CodigoEmpleado:
                    found = True
                    break
        if not found:
            postEmpleados.append(empleadoDB)

    print(f"Total number of new employees: {len(postEmpleados)}")

    
    print(f"Total number of patch employees: {len(patchEmpleados)}")
import openpyxl

def generarExcel(empleados, nombreArchivo):

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
    generarExcel(postEmpleados, "empleados_nuevos.xlsx")
    generarExcel(patchEmpleados, "empleados_modificados.xlsx")


def postEmpleadosBC():
    """ This function iterates through the list of Empleado objects retrieved by getEmpleadosDB().
      For each employee, it constructs a dictionary data containing the employee's information,
        mapping field names from the database to corresponding fields in Business Central. 
        It then calls the business_central_request function (with a POST request) 
        to create the new employee in Business Central, passing the data dictionary as the request body. 
        The function includes error handling and prints success/failure messages for each employee creation attempt. """
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
                "Bank_Account_No": empleado.IBANReceptor
            }
            if empleado.Sexo == "Hombre":
                data["Gender"] = "Male"
            elif empleado.Sexo == "Mujer":
                data["Gender"] = "Female"

            if isinstance(empleado.FechaNacimiento, datetime):
                data["Birth_Date"] = empleado.FechaNacimiento.strftime('%Y-%m-%dT%H:%M:%SZ')
            else:
                data["Birth_Date"] = None
            if empleado.CodigoEmpleado not in empleados_codigos or len(empleados_codigos) == 0:
                response = business_central_request(data=data)
                if response:
                    print(f"Empleado {empleado.NombreEmpleado} con codigo {empleado.CodigoEmpleado} creado correctamente en Business Central.")
                else:
                    print(f"Error al crear el empleado {empleado.NombreEmpleado} en Business Central.")
            else:
                print(f"El empleado {empleado.NombreEmpleado} con código {empleado.CodigoEmpleado} ya existe en Business Central.")
            
        except Exception as e:
            print(f"Error al procesar el empleado {empleado.NombreEmpleado}: {e}")

        
def patchEmpleadosBC():
    """ This function iterates through the list of Empleado objects that need to be updated in Business Central.
        For each employee, it constructs a dictionary data containing the employee's information,
        mapping field names from the database to corresponding fields in Business Central.
        It then calls the business_central_request function (with a PATCH request)
        to update the employee in Business Central, passing the data dictionary as the request body.
        The function includes error handling and prints success/failure messages for each employee update attempt. """
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
                "Birth_Date": empleado.FechaNacimiento,
                "Social_Security_No": empleado.ProvNumSoe,
                "Bank_Account_No": empleado.IBANReceptor
            }
            if empleado.Sexo == "Hombre":
                data["Gender"] = "Male"
            elif empleado.Sexo == "Mujer":
                data["Gender"] = "Female"
            
            if isinstance(empleado.FechaNacimiento, datetime):
                data["Birth_Date"] = empleado.FechaNacimiento.strftime('%Y-%m-%dT%H:%M:%SZ')
            else:
                data["Birth_Date"] = None

            response = business_central_request(method='PATCH', data=data, etag=empleado.odata_etag, id=empleado.CodigoEmpleado)
            if response:
                print(f"Empleado {empleado.NombreEmpleado} actualizado correctamente en Business Central.")
            else:
                print(f"Error al actualizar el empleado {empleado.NombreEmpleado} en Business Central.")
        except Exception as e:
            print(f"Error al procesar el empleado {empleado.NombreEmpleado}: {e}")
