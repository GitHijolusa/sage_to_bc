# from db_query import empleados
from bc_requests import business_central_request
import db_query
from empleado import Empleado
# import setup




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
    listaEmpleadosActualesBC = []
    try:
        responseData = business_central_request(method='GET')
        print(responseData)
        if responseData:
            for item in responseData['value']:
                empleado = Empleado(**item)
                listaEmpleadosActualesBC.append(empleado)

    except TypeError as e:
        print(f"Error: {e}")
    print (f"Empleados en BC: {len(listaEmpleadosActualesBC)} ")
    print(listaEmpleadosActualesBC)
    return listaEmpleadosActualesBC

def getEmpleadosDB():
    empleados = db_query.getEmpleadosDb()
    return empleados



def postEmpleadosBC():
    """ This function iterates through the list of Empleado objects retrieved by getEmpleadosDB().
      For each employee, it constructs a dictionary data containing the employee's information,
        mapping field names from the database to corresponding fields in Business Central. 
        It then calls the business_central_request function (with a POST request) 
        to create the new employee in Business Central, passing the data dictionary as the request body. 
        The function includes error handling and prints success/failure messages for each employee creation attempt. """
    # for empleado in empleados:
    #     try:
    #         data = {
    #             "No": empleado.CodigoEmpleado,
    #             "Name": empleado.NombreEmpleado,
    #             "First_Family_Name": empleado.PrimerApellidoEmpleado,
    #             "Last_Family_Name": empleado.SegundoApellidoEmpleado,
    #             "Address": empleado.DireccionCompleta,
    #             "PostCode": empleado.CodigoPostal,
    #             "City": empleado.Municipio,
    #             "County": empleado.Provincia,
    #             "PhoneNo": empleado.Telefono,
    #             "MobilePhoneNo": empleado.TelefonoMovil,
    #             "E_Mail": empleado.EMail1,
    #             "BirthDate": empleado.FechaNacimiento,
    #             "SSN": empleado.Dni,
    #             "IBAN": empleado.IBANReceptor,
    #             "Gender": empleado.Sexo,
    #             "JobTitle": "Empleado",
    #             "StartDate": empleado.FechaInicioContrato,
    #             "EndDate": empleado.FechaFinalContrato,
    #             "Nationality": empleado.SiglaNacion
    #         }
    #         response = business_central_request(data=data)
    #         if response:
    #             print(f"Empleado {empleado.NombreEmpleado} creado correctamente en Business Central.")
    #         else:
    #             print(f"Error al crear el empleado {empleado.NombreEmpleado} en Business Central.")
    #     except Exception as e:
    #         print(f"Error al procesar el empleado {empleado.NombreEmpleado}: {e}")
    data = {
    "No": "0003",
    "Name": "John",
    "First_Family_Name": "Does"
    }
    business_central_request(data=data)



