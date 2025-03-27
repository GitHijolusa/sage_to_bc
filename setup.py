import json
import os


urlEmpleados = "http://192.168.1.231:7048/BC_Test/ODataV4/Company('AGRICOLA%20VILLENA%20SL')/Empleados"  # Replace with your actual endpoint
usernameBC = "SQL-NAV-PRE\\ALFREDO.BLANCO"  # Replace with your Business Central username. Note the double backslash.
passwordBC = "Rol62357"  # Replace with your Business Central password

userDb= 'alfredo.blanco'
passwordDb = 'Rol62357'
ipDb = '192.168.1.221'
db = 'LOGIC'

query="""
SELECT DISTINCT 
    p.[SiglaNacion],
    p.[Dni],
    n.CodigoEmpleado,
    [NombreEmpleado],
    [ProvNumSoe],
    [PrimerApellidoEmpleado],
    [SegundoApellidoEmpleado],
    pd.[CodigoPostal],
    pd.DireccionCompleta,
    pd.[Telefono],
    pd.[TelefonoMovil],
    pd.[Municipio],
    pd.[Provincia],
    [Sexo],
    [FechaNacimiento],
    p.[EMail1],
    [FechaInicioContrato],
    [FechaFinalContrato],
    co.[IBANReceptor]
FROM 
    [LOGIC].[dbo].[Personas] AS p
JOIN (
    SELECT 
        Dni, 
        CodigoEmpleado, 
        FechaInicioContrato,
        FechaFinalContrato,
        ROW_NUMBER() OVER (PARTITION BY CodigoEmpleado ORDER BY FechaInicioContrato DESC) AS rn 
    FROM 
        dbo.EmpleadoNomina
) AS n ON p.Dni = n.Dni AND n.rn = 1
LEFT JOIN (
    SELECT 
        CodigoEmpleado, 
        IBANReceptor,
        ROW_NUMBER() OVER (PARTITION BY CodigoEmpleado ORDER BY FechaAlta DESC) AS rn 
    FROM 
        dbo.EmpleadoCobro
) AS co ON n.CodigoEmpleado = co.CodigoEmpleado AND co.rn = 1
LEFT JOIN (
    SELECT 
        [Dni]
        ,[ViaPublica]
        ,[Numero1]
        ,[Numero2]
        ,[Escalera]
        ,[Piso]
        ,[Puerta]
        ,[Letra]
        ,[CodigoPostal]
        ,[Telefono]
        ,[TelefonoMovil]
        ,[Municipio]
        ,[Provincia]
        ,[IdDomicilio]
        ,CASE 
            WHEN [ViaPublica] IS NOT NULL THEN [ViaPublica] + ' ' ELSE '' END +
            CASE 
            WHEN [Numero1] IS NOT NULL THEN [Numero1] + ' ' ELSE '' END +
            CASE 
            WHEN [Numero2] IS NOT NULL THEN [Numero2] + ' ' ELSE '' END +
            CASE 
            WHEN [Escalera] IS NOT NULL THEN [Escalera] + ' ' ELSE '' END +
            CASE 
            WHEN [Piso] IS NOT NULL THEN [Piso] + ' ' ELSE '' END +
            CASE 
            WHEN [Puerta] IS NOT NULL THEN [Puerta] + ' ' ELSE '' END +
            CASE 
            WHEN [Letra] IS NOT NULL THEN [Letra] + ' ' ELSE '' END AS DireccionCompleta,
        ROW_NUMBER() OVER (PARTITION BY [Dni] ORDER BY [IdDomicilio] DESC) AS RowNum
    FROM [LOGIC].[dbo].[PersonasDomicilios]
) AS pd ON p.Dni = pd.Dni AND pd.RowNum = 1
ORDER BY 
    n.CodigoEmpleado
"""

def load_setup_from_json(filepath=os.path.join(os.path.dirname(__file__), "setup.json")):
    
    rutaJson = "setup.json"
    try:
        with open(rutaJson, 'r') as f:
            data = json.load(f)
            global urlEmpleados, usernameBC, passwordBC, userDb, passwordDb, ipDb, db, query
            urlEmpleados = data.get('urlEmpleados', urlEmpleados)            
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
