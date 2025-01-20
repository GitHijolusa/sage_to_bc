import setup
from setup import load_setup_from_json
import db_query
import emp_bloc


load_setup_from_json()
empleadosDB = db_query.getEmpleadosDb()
# empleadosbc = emp_bloc.getEmpleadosBC()
# emp_bloc.postEmpleadosBC()





