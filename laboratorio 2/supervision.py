import os
import json
import csv
from datetime import datetime, date, timedelta

DB_FILE = "db.json"
CONTRACTS_CSV = "contracts.csv"
TRACKINGS_CSV = "trackings.csv"


# =========================
# Persistencia
# =========================

def _ensure_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({"contracts": []}, f, indent=4)


def _load_db():
    try:
        _ensure_db()
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "contracts" not in data or not isinstance(data["contracts"], list):
            return {"contracts": []}

        return data
    except:
        return {"contracts": []}


def _save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# =========================
# Validaciones auxiliares
# =========================

def _parse_date_ddmmyyyy(s):
    return datetime.strptime(s, "%d/%m/%Y").date()


def _valid_email(e):
    if not isinstance(e, str):
        return False
    if " " in e:
        return False
    if e.count("@") != 1:
        return False

    left, right = e.split("@")
    if not left or not right:
        return False
    if "." not in right:
        return False

    return True


def _valid_status(s):
    return s in ["ACTIVO", "SUSPENDIDO", "TERMINADO"]


def _to_positive_float(x):
    try:
        val = float(x)
        if val > 0:
            return val
    except:
        pass
    return None


def _find_contract(data, number):
    for c in data["contracts"]:
        if c["number"] == number:
            return c
    return None


# =========================
# API contratos
# =========================

def registerContract(number, contractor, obj, start, end, value, supervisor, status, email):
    if not all([number, contractor, obj, start, end, supervisor, status, email]):
        return "invalid data"

    data = _load_db()

    if _find_contract(data, number):
        return "number already exists"

    if not _valid_status(status):
        return "invalid data"

    if not _valid_email(email):
        return "invalid data"

    value = _to_positive_float(value)
    if value is None:
        return "invalid data"

    try:
        start_d = _parse_date_ddmmyyyy(start)
        end_d = _parse_date_ddmmyyyy(end)
    except:
        return "invalid date format"

    if start_d > end_d:
        return "invalid date range"

    contract = {
        "number": number,
        "contractor": contractor,
        "object": obj,
        "start": start,
        "end": end,
        "value": value,
        "supervisor": supervisor,
        "status": status,
        "email": email,
        "trackings": []
    }

    data["contracts"].append(contract)
    _save_db(data)

    return "ok"


def listContracts():
    data = _load_db()

    result = []
    for c in data["contracts"]:
        result.append({
            "number": c["number"],
            "contractor": c["contractor"],
            "object": c["object"],
            "start": c["start"],
            "end": c["end"],
            "value": c["value"],
            "supervisor": c["supervisor"],
            "status": c["status"],
            "email": c["email"]
        })

    return sorted(result, key=lambda x: x["contractor"])


def searchContract(number):
    data = _load_db()
    return _find_contract(data, number)


# =========================
# API seguimientos
# =========================

def addTracking(number, date_str, desc, progress, obs):
    if not number or not desc:
        return "invalid data"

    try:
        _parse_date_ddmmyyyy(date_str)
    except:
        return "invalid date format"

    try:
        progress = int(progress)
        if progress < 0 or progress > 100:
            return "invalid data"
    except:
        return "invalid data"

    data = _load_db()
    contract = _find_contract(data, number)

    if not contract:
        return "contract not found"

    new_id = len(contract["trackings"]) + 1

    tracking = {
        "id": new_id,
        "date": date_str,
        "desc": desc,
        "progress": progress,
        "obs": obs
    }

    contract["trackings"].append(tracking)
    _save_db(data)

    return "ok"


def listTrackings(number):
    if not number:
        return "invalid data"

    data = _load_db()
    contract = _find_contract(data, number)

    if not contract:
        return "contract not found"

    return contract["trackings"]


def avgProgress(number):
    if not number:
        return "invalid data"

    data = _load_db()
    contract = _find_contract(data, number)

    if not contract:
        return "contract not found"

    trackings = contract["trackings"]

    if not trackings:
        return {"number": number, "count": 0, "avg_progress": 0.0}

    total = sum(t["progress"] for t in trackings)
    avg = total / len(trackings)

    return {"number": number, "count": len(trackings), "avg_progress": avg}


# =========================
# Estadísticas
# =========================

def stats():
    data = _load_db()
    contracts = data["contracts"]

    total_contracts = len(contracts)

    total_by_status = {"ACTIVO": 0, "SUSPENDIDO": 0, "TERMINADO": 0}
    total_value = 0

    for c in contracts:
        total_by_status[c["status"]] += 1
        total_value += c["value"]

    avg_value = total_value / total_contracts if total_contracts > 0 else 0

    max_contract = max(contracts, key=lambda x: x["value"], default=None)
    min_contract = min(contracts, key=lambda x: x["value"], default=None)

    today = date.today()
    soon_limit = today + timedelta(days=30)

    contracts_soon_to_end = []
    for c in contracts:
        try:
            end_date = _parse_date_ddmmyyyy(c["end"])
            if today <= end_date <= soon_limit:
                contracts_soon_to_end.append(c)
        except:
            pass

    return {
        "total_contracts": total_contracts,
        "total_by_status": total_by_status,
        "total_value": total_value,
        "avg_value": avg_value,
        "max_contract": max_contract,
        "min_contract": min_contract,
        "contracts_soon_to_end": contracts_soon_to_end
    }


# =========================
# Exportación CSV
# =========================

def exportCsv():
    data = _load_db()

    # contracts.csv
    with open(CONTRACTS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["number", "contractor", "object", "start", "end", "value", "supervisor", "status", "email"])

        for c in data["contracts"]:
            writer.writerow([
                c["number"], c["contractor"], c["object"],
                c["start"], c["end"], c["value"],
                c["supervisor"], c["status"], c["email"]
            ])

    # trackings.csv
    with open(TRACKINGS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["number", "id", "date", "desc", "progress", "obs"])

        for c in data["contracts"]:
            for t in c["trackings"]:
                writer.writerow([
                    c["number"], t["id"], t["date"],
                    t["desc"], t["progress"], t["obs"]
                ])