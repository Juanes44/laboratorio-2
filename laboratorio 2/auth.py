import os
import json

USERS_FILE = "users.json"


# =========================
# FUNCIONES AUXILIARES
# =========================

def _ensure_users_file():
    """
    Si el archivo users.json no existe, debe crearlo
    con la estructura inicial:
    {"users": []}
    """
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as archivo:
            json.dump({"users": []}, archivo, indent=4)


def _load():
    """
    Debe cargar y devolver el contenido del archivo users.json.
    """
    _ensure_users_file()

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)

        if not isinstance(data, dict) or "users" not in data:
            return {"users": []}

        if not isinstance(data["users"], list):
            return {"users": []}

        return data

    except Exception:
        return {"users": []}


def _save(data):
    """
    Debe guardar en users.json la información recibida en data.
    """
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as archivo:
            json.dump(data, archivo, indent=4)
    except Exception:
        print("Error al guardar el archivo")


# =========================
# VALIDACIONES
# =========================

def _valid_role(role):
    """
    Debe validar si el rol es permitido.
    """
    if role == "admin" or role == "supervisor" or role == "viewer":
        return True
    else:
        return False


# =========================
# API PRINCIPAL
# =========================

def findUser(user):
    data = _load()

    for u in data["users"]:
        if u["user"] == user:
            return u

    return None


def registerUser(user, password, role):

    if user == "" or password == "" or role == "":
        return "invalid data"

    if not _valid_role(role):
        return "invalid data"

    data = _load()

    for u in data["users"]:
        if u["user"] == user:
            return "user exists"

    nuevo = {
        "user": user,
        "password": password,
        "role": role,
        "session": False
    }

    data["users"].append(nuevo)
    _save(data)

    return "ok"


def openCloseSession(user, password, flag):

    if user == "" or password == "":
        return "invalid data"

    data = _load()

    for u in data["users"]:
        if u["user"] == user:

            if u["password"] != password:
                return "wrong credentials"

            u["session"] = flag
            _save(data)
            return "ok"

    return "wrong credentials"


def hasRole(user, allowed_roles):

    data = _load()

    for u in data["users"]:
        if u["user"] == user:
            if u["role"] in allowed_roles:
                return True
            else:
                return False

    return False