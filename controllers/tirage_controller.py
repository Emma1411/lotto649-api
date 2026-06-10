from fastapi import APIRouter
import psycopg2
import psycopg2.extras
from config.database import get_connection as get_conn
from utils.db_query import DBQuery
from utils.response import success, not_found, paginate, error

router = APIRouter(prefix="/api/v1/tirages", tags=["tirages"])
db = DBQuery("tirage")


# Retourne la liste des tirages avec pagination.
@router.get("")
def list_tirages(page: int = 1, per_page: int = 20):
    try:
        data = db.list(page, per_page)
        total = db.count()
        return paginate(data, total, page, per_page)
    except Exception as e:
        return error(str(e))


# Retourne uniquement le nombre total de tirages enregistrés.
@router.get("/count")
def count_tirages():
    try:
        return success({"total": db.count()})
    except Exception as e:
        return error(str(e))


# Retourne le dernier tirage disponible dans la base.
@router.get("/dernier")
def dernier_tirage():
    try:
        data = db.custom("dernier", many=False)
        if not data:
            return not_found("Aucun tirage trouve")
        return success(data)
    except Exception as e:
        return error(str(e))


# Permet de filtrer les tirages entre deux dates.
@router.get("/filter")
def filter_tirages(
    start_date: str,
    end_date: str,
    page: int = 1,
    per_page: int = 20
):
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute(
            "SELECT * FROM sp_tirage_filter_by_date(%s, %s, %s, %s)",
            (start_date, end_date, page, per_page)
        )
        data = [dict(r) for r in cur.fetchall()]

        cur.execute(
            "SELECT * FROM sp_tirage_count_by_date(%s, %s)",
            (start_date, end_date)
        )
        total = cur.fetchone()["total"]

        cur.close()
        conn.close()

        return paginate(data, total, page, per_page)

    except Exception as e:
        return error(str(e))


# Recherche un tirage précis à partir de sa date.
@router.get("/date/{date}")
def tirage_par_date(date: str):
    try:
        data = db.find(date)

        if not data:
            return not_found(f"Aucun tirage pour la date {date}")

        return success(data)

    except Exception as e:
        return error(str(e))


# Retourne les détails complets d'un tirage.
@router.get("/{date}/details")
def get_tirage_details(date: str):
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute(
            "SELECT * FROM sp_tirage_details_read(%s)",
            (date,)
        )

        data = cur.fetchone()

        cur.close()
        conn.close()

        if not data:
            return not_found("Aucun detail disponible pour ce tirage")

        return success(dict(data))

    except Exception as e:
        return error(str(e))


# Retourne un tirage à partir de son identifiant unique.
@router.get("/{id}")
def read_tirage(id: int):
    try:
        data = db.read(id)

        if not data:
            return not_found(f"Tirage {id} introuvable")

        return success(data)

    except Exception as e:
        return error(str(e))