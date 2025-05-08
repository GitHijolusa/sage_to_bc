import requests
from requests_ntlm import HttpNtlmAuth
import json
import logging
from setup import usernameBC, passwordBC
import requests

logging.basicConfig(filename='business_central_api.log', level=logging.ERROR)

def business_central_request(url=None, username=usernameBC, password=passwordBC, data=None, method='POST', etag=None, id=None):
    """
    Realiza una solicitud a un servicio web de Business Central.

    Args:
        url (str): La URL del servicio web.
        username (str): El nombre de usuario para la autenticación NTLM.
        password (str): La contraseña para la autenticación NTLM.
        data (dict, optional): Los datos a enviar en la solicitud. 
                                 Por defecto es None.
        method (str, optional): El método HTTP ('GET' o 'POST'). 
                                 Por defecto es 'POST'.
        url (str, optional): La URL del servicio web.

    Returns:
        dict: La respuesta JSON del servidor si la solicitud es exitosa.
        None: Si la solicitud falla.
    """
    headers = {'Content-Type': 'application/json'}
    auth = HttpNtlmAuth(username, password)

    try:
        if url is None:
            raise ValueError("URL is required.")
        
        if method == 'GET':
            response = requests.get(url, headers=headers, auth=auth)
            print(response.text)
            print(response.status_code) 
        elif method == 'POST':
            response = requests.post(url, headers=headers, auth=auth, data=json.dumps(data))
            print(response.text)
            print(response.status_code)        
        elif method == 'PATCH':
            headers['If-Match'] = etag
            response = requests.patch(f"{url}('{id}')", headers=headers, auth=auth, data=json.dumps(data))
            print(f"Response text: {response.text}")            
            print(f"Response status code: {response.status_code}")            
        else:
            raise ValueError("Método HTTP inválido. Debe ser 'GET' o 'POST'")

        response.raise_for_status()  # Genera una excepción si el código de estado no es 2xx
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error en la solicitud: {e}")
        return None
    except json.decoder.JSONDecodeError as e:
        logging.error(f"Error al decodificar la respuesta JSON: {e}")
        logging.error(f"Contenido de la respuesta: {response.text}")
        return None