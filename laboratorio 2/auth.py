
"""
# Autenticación simple con JSON (users.json)
# Estructura esperada:
# {
#   "users": [
#     {"user":"admin1","password":"adm","role":"admin","session":false}
#   ]
# }
"""
import os
import json

USERS_FILE = "users.json"



# Funciones auxiliares de persistencia

def _ensure_users_file():
    """
    Si el archivo users.json no existe, debe crearlo
    con la estructura inicial:
    {"users": []}
    """
    pass


def _load():
    """
    Debe cargar y devolver el contenido del archivo users.json.

    Reglas:
    - Si el archivo no existe, debe crearlo primero.
    - Si ocurre algún error leyendo el archivo,
      debe devolver {"users": []}
    - Si la estructura no es válida, debe devolver {"users": []}
    """
    pass


def _save(data):
    """
    Debe guardar en users.json la información recibida en data.
    El archivo debe guardarse con indentación para que sea legible.
    """
    pass



# Validaciones

def _valid_role(role):
    """
    Debe validar si el rol es permitido.

    Roles válidos:
    - admin
    - supervisor
    - viewer

    Retorna:
    - True  si el rol es válido
    - False en caso contrario
    """
    pass


# API principal de autenticación

def findUser(user):
    """
    Debe buscar un usuario por nombre.

    Parámetro:
    - user: nombre del usuario

    Retorna:
    - el diccionario del usuario si existe
    - None si no existe
    """
    pass


def registerUser(user, password, role):
    """
    Debe registrar un nuevo usuario en users.json.

    Validaciones:
    - user no vacío
    - password no vacío
    - role válido
    - no debe existir ya un usuario con el mismo nombre

    Retorna:
    - "ok"
    - "invalid data"
    - "user exists"
    """
    pass


def openCloseSession(user, password, flag):
    """
    Debe abrir o cerrar sesión para un usuario.

    Parámetros:
    - user: nombre del usuario
    - password: contraseña
    - flag:
        True  -> abrir sesión
        False -> cerrar sesión

    Validaciones:
    - user y password no vacíos
    - el usuario debe existir
    - la contraseña debe coincidir

    Retorna:
    - "ok"
    - "invalid data"
    - "wrong credentials"
    """
    pass


def hasRole(user, allowed_roles):
    """
    Debe verificar si el usuario tiene uno de los roles permitidos.

    Parámetros:
    - user: nombre del usuario
    - allowed_roles: tupla o lista de roles permitidos

    Retorna:
    - True  si el usuario existe y su rol está permitido
    - False en caso contrario
    """
    pass
