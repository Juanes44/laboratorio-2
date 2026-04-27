import os
import json
import csv
from datetime import datetime, date

DB_FILE = "db.json"
CONTRACTS_CSV = "contracts.csv"
TRACKINGS_CSV = "trackings.csv"


# =========================
# Persistencia
# =========================
#Verifica que el archivo exista, si no es asi, lo crea
def _asegurar_db():
    #Verifica 
    if not os.path.exists(DB_FILE):                                     #
        #Crea el archivo
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({"contracts": []}, f, indent=4)

#Guarda el contenido del archivo en una variable
def _cargar_db():
    try:
        #Verifica que este por medio de la funcion _asegurar_db
        _asegurar_db()
        #Abre el archivo y guarda el contenido
        with open(DB_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
        #Si no existe ningun contrato, se crea un diccionario
        if not isinstance(datos, dict) or "contracts" not in datos:         ##########
            return {"contracts": []}

        return datos
    except:
        return {"contracts": []}

#Despues de los cambios hechos, vuelve a guardar el diccionario modificado en el archivo
def _guardar_db(datos):
    #Abre el archivo y guarda
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)


# =========================
# Validaciones
# =========================

#Saca la fecha de hoy
def _parsear_fecha(texto):
    return datetime.strptime(texto, "%d/%m/%Y").date()

#Verifica el correo dado por el usuario
def _correo_valido(correo):
    if not isinstance(correo, str) or " " in correo:                #
        return False
    if correo.count("@") != 1:
        return False
    izq, der = correo.split("@")
    if not izq or not der:
        return False
    if "." not in der:
        return False
    return True

#Mirando las fechas verifica que el estado del contrato
def _estado_valido(estado):
    return estado in ("ACTIVO", "SUSPENDIDO", "TERMINADO")

#Verifica que el numero sea positivo
def _a_float_positivo(valor):                                   #
    try:
        v = float(valor)
        if v > 0:
            return v
        return None
    except:
        return None


def _buscar_contrato(datos, numero):
    for c in datos["contracts"]:
        if c.get("number") == numero:
            return c
    return None


# =========================
# CONTRATOS
# =========================

def registerContract(number, contractor, obj, start, end, value, supervisor, status, email):
    if not all([number, contractor, obj, start, end, value, supervisor, status, email]):        #
        return "invalid data"

    datos = _cargar_db()

    if _buscar_contrato(datos, number):
        return "number already exists"

    if not _estado_valido(status) or not _correo_valido(email):         #
        return "invalid data"

    valor_num = _a_float_positivo(value)                        #
    if valor_num is None:
        return "invalid data"

    try:
        f1 = _parsear_fecha(start)
        f2 = _parsear_fecha(end)
    except:
        return "invalid date format"

    if f1 > f2:
        return "invalid date range"

    nuevo = {
        "number": number,
        "contractor": contractor,
        "object": obj,
        "start": start,
        "end": end,
        "value": valor_num,
        "supervisor": supervisor,
        "status": status,
        "email": email,
        "trackings": []
    }

    datos["contracts"].append(nuevo)
    _guardar_db(datos)

    return "ok"


def listContracts():
    datos = _cargar_db()
    lista = []

    for c in datos["contracts"]:
        copia = c.copy()
        copia.pop("trackings", None)
        lista.append(copia)

    return sorted(lista, key=lambda x: str(x.get("contractor", "")))


def searchContract(number):
    datos = _cargar_db()
    return _buscar_contrato(datos, number)


# =========================
# TRACKINGS
# =========================

def addTracking(number, date_str, desc, progress, obs):
    if not number or not desc:
        return "invalid data"

    try:
        _parsear_fecha(date_str)            ########
    except:
        return "invalid date format"

    try:
        prog = int(progress)
        if prog < 0 or prog > 100:                      #
            return "invalid data"
    except:
        return "invalid data"

    datos = _cargar_db()
    contrato = _buscar_contrato(datos, number)

    if contrato is None:
        return "contract not found"

    seguimientos = contrato.get("trackings", [])
    nuevo_id = len(seguimientos) + 1

    nuevo_seg = {
        "id": nuevo_id,
        "date": date_str,
        "desc": desc,
        "progress": prog,
        "obs": obs
    }

    seguimientos.append(nuevo_seg)
    contrato["trackings"] = seguimientos

    _guardar_db(datos)

    return "ok"


def listTrackings(number):
    if not number:
        return "invalid data"               #

    datos = _cargar_db()
    contrato = _buscar_contrato(datos, number)

    if contrato is None:
        return "contract not found"

    return contrato.get("trackings", [])


def avgProgress(number):
    if not number:
        return "invalid data"

    datos = _cargar_db()
    contrato = _buscar_contrato(datos, number)

    if contrato is None:
        return "contract not found"

    seguimientos = contrato.get("trackings", [])

    if not seguimientos:
        return {"number": number, "count": 0, "avg_progress": 0.0}

    total = sum(s["progress"] for s in seguimientos)
    promedio = round(total / len(seguimientos), 2)

    return {
        "number": number,
        "count": len(seguimientos),
        "avg_progress": promedio
    }


# =========================
# STATS
# =========================

def stats():
    datos = _cargar_db()
    contratos = datos["contracts"]

    total = len(contratos)

    por_estado = {"ACTIVO": 0, "SUSPENDIDO": 0, "TERMINADO": 0}

    valores = [c["value"] for c in contratos] if contratos else []

    for c in contratos:
        if c["status"] in por_estado:
            por_estado[c["status"]] += 1

    total_valor = sum(valores) if valores else 0
    promedio_valor = (total_valor / total) if total > 0 else 0

    max_c = max(contratos, key=lambda x: x["value"]) if contratos else None
    min_c = min(contratos, key=lambda x: x["value"]) if contratos else None

    proximos = []
    hoy = date.today()

    for c in contratos:                                 ########
        try:
            fin = _parsear_fecha(c["end"])
            if 0 <= (fin - hoy).days <= 30:
                proximos.append(c)
        except:
            pass

    return {
        "total_contracts": total,
        "total_by_status": por_estado,
        "total_value": total_valor,
        "avg_value": promedio_valor,
        "max_contract": max_c,
        "min_contract": min_c,
        "contracts_soon_to_end": proximos
    }


# =========================
# EXPORT
# =========================

def exportCsv():
    datos = _cargar_db()
    contratos = datos["contracts"]

    with open(CONTRACTS_CSV, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["number","contractor","object","start","end","value","supervisor","status","email"])

        for c in contratos:
            escritor.writerow([
                c["number"], c["contractor"], c["object"],
                c["start"], c["end"], c["value"],
                c["supervisor"], c["status"], c["email"]
            ])

    with open(TRACKINGS_CSV, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["number","id","date","desc","progress","obs"])

        for c in contratos:
            for t in c.get("trackings", []):
                escritor.writerow([
                    c["number"],
                    t["id"],
                    t["date"],
                    t["desc"],
                    t["progress"],
                    t["obs"]
                ])