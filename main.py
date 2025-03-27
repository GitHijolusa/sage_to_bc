import setup
from setup import load_setup_from_json
import db_query
import emp_bloc
import bc_requests


load_setup_from_json()
emp_bloc.getEmpleadosDB()
emp_bloc.getEmpleadosBC()
emp_bloc.getdiffEmpleados()
emp_bloc.generarExcels()



emp_bloc.postEmpleadosBC()
emp_bloc.patchEmpleadosBC()





