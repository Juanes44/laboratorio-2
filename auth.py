import os
import json

USERS_FILE = "users.json"


# =========================
# Persistencia
# =========================

#Asegura que el archivo este creado, si no es asi, lo crea
def _asegurar_archivo():
    #Verifica
    if not os.path.exists(USERS_FILE):
        #Crea
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({"users": []}, f, indent=4)

#Abre el archivo para posteriormente guardarlo en una variable
def _cargar():
    try:                                                                    ########
        #Verifique que exista
        _asegurar_archivo()
        #Abre el archivo
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            #Almacena el contenido en una variable
            datos = json.load(f)
        #Si en el archivo no hay nada, crea un diccionario vacio
        if not isinstance(datos, dict) or "users" not in datos:
            return {"users": []}

        return datos
    except:
        return {"users": []}

#Despues de los cambios en la variable datos, se vuelve a guardar en el archivo
def _guardar(datos):
    #Abre el archivo
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        #Guarda lo puesto en la variable datos
        json.dump(datos, f, indent=4)


# =========================
# Validaciones
# =========================

#Verifica el rol del usuario
def _rol_valido(rol):
    return rol in ("admin", "supervisor", "viewer")


# =========================
# API
# =========================
#Busca al usuario por medio de la variable datos
def findUser(user):
    datos = _cargar()
    for u in datos["users"]:
        if u.get("user") == user:
            return u
    return None

#Registra nuevos usuarios
def registerUser(user, password, role):
    #Si no se puso las variables necesarias, retorna
    if not user or not password or not _rol_valido(role):
        return "invalid data"

    datos = _cargar()
    #Verifica que el usuario ya esta en el sistema, si no es asi, crea el usuario
    for u in datos["users"]:
        if u["user"] == user:
            return "user exists"
    #Crea el usuario
    nuevo_usuario = {
        "user": user,
        "password": password,
        "role": role,
        "session": False
    }
    #Agrega el usuario al diccionario datos
    datos["users"].append(nuevo_usuario)
    _guardar(datos)

    return "ok"

    #Cierra o abre la sesion
def openCloseSession(user, password, flag):
    if not user or not password:
        return "invalid data"

    datos = _cargar()

    for u in datos["users"]:
        if u["user"] == user:
            if u["password"] != password:
                return "wrong credentials"

            u["session"] = flag
            _guardar(datos)
            return "ok"

    return "wrong credentials"

#Verifica que el usuario tenga un rol, si no es asi le da uno con la funcion usuario.get
def hasRole(user, allowed_roles):
    usuario = findUser(user)
    if usuario is None:
        return False
    return usuario.get("role") in allowed_roles
