from fastapi import APIRouter
import psycopg2
import psycopg2.extras
from config.database import get_connection as get_conn
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from utils.db_query import DBQuery
from utils.response import success, created, not_found, error, paginate

router = APIRouter(prefix="/api/v1/tickets", tags=["tickets"])
db = DBQuery("ticket")


class TicketCreate(BaseModel):
    date_achat: date
    strategie: str
    numeros_joues: List[int]
    cout_ticket: float = 3.00
    date_tirage: Optional[date] = None


class TicketUpdate(BaseModel):
    statut: str


@router.get("/groupes")
def tickets_groupes(page: int = 1, per_page: int = 10):
    try:
        conn = get_conn()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute(
            "SELECT * FROM sp_ticket_group_by_date(%s, %s)",
            (page, per_page)
        )
        data = [dict(r) for r in cur.fetchall()]

        cur.execute("SELECT * FROM sp_ticket_group_count()")
        total = cur.fetchone()["total"]

        cur.close()
        conn.close()
        return paginate(data, total, page, per_page)
    except Exception as e:
        return error(str(e))


@router.get("/groupes/filter")
def tickets_groupes_filter(
    start_date: str,
    end_date:   str,
    page:       int = 1,
    per_page:   int = 10
):
    try:
        conn = get_conn()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute(
            "SELECT * FROM sp_ticket_group_by_date_filter(%s, %s, %s, %s)",
            (start_date, end_date, page, per_page)
        )
        data = [dict(r) for r in cur.fetchall()]

        cur.execute(
            "SELECT * FROM sp_ticket_group_count_filter(%s, %s)",
            (start_date, end_date)
        )
        total = cur.fetchone()["total"]

        cur.close()
        conn.close()
        return paginate(data, total, page, per_page)
    except Exception as e:
        return error(str(e))

# Retourne tous les tickets d'une date précise
@router.get("/date/{date}")
def tickets_par_date(date: str):
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute(
            "SELECT * FROM sp_ticket_by_date(%s)",
            (date,)
        )

        data = [dict(r) for r in cur.fetchall()]

        cur.close()
        conn.close()

        return success(data)

    except Exception as e:
        return error(str(e))


# Liste paginée de tous les tickets
@router.get("")
def list_tickets(page: int = 1, per_page: int = 20):
    try:
        data = db.list(page, per_page)
        total = db.count()

        return paginate(data, total, page, per_page)

    except Exception as e:
        return error(str(e))


# Affiche le résumé financier des tickets
@router.get("/suivi")
def suivi_tickets():
    try:
        data = db.custom("suivi", many=True)
        return success(data)

    except Exception as e:
        return error(str(e))


# Retourne le nombre total de tickets
@router.get("/count")
def count_tickets():
    try:
        return success({"total": db.count()})

    except Exception as e:
        return error(str(e))


# Filtre les tickets selon une plage de dates
@router.get("/filter")
def filter_tickets(start_date: str, end_date: str, page: int = 1, per_page: int = 20):
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute(
            "SELECT * FROM sp_ticket_filter_by_date(%s, %s, %s, %s)",
            (start_date, end_date, page, per_page)
        )

        data = [dict(r) for r in cur.fetchall()]

        cur.execute(
            "SELECT * FROM sp_ticket_count_by_date(%s, %s)",
            (start_date, end_date)
        )

        total = cur.fetchone()["total"]

        cur.close()
        conn.close()

        return paginate(data, total, page, per_page)

    except Exception as e:
        return error(str(e))


# Retourne un ticket à partir de son identifiant
@router.get("/{id}")
def read_ticket(id: int):
    try:
        data = db.read(id)

        if not data:
            return not_found(f"Ticket {id} introuvable")

        return success(data)

    except Exception as e:
        return error(str(e))


# Crée un nouveau ticket
@router.post("/store")
def create_ticket(ticket: TicketCreate):
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute(
            "SELECT * FROM sp_ticket_create(%s, %s, %s, %s, %s)",
            (
                ticket.date_achat,
                ticket.strategie,
                ticket.numeros_joues,
                ticket.cout_ticket,
                ticket.date_tirage,
            )
        )

        result = cur.fetchone()

        conn.commit()

        cur.close()
        conn.close()

        return created(dict(result) if result else None)

    except Exception as e:
        return error(str(e))


# Met à jour le statut d'un ticket
@router.put("/update/{id}")
def update_ticket(id: int, ticket: TicketUpdate):
    try:
        data = db.update(id, ticket.statut)

        if not data:
            return not_found(f"Ticket {id} introuvable")

        return success(data)

    except Exception as e:
        return error(str(e))


# Supprime un ticket
@router.delete("/delete/{id}")
def delete_ticket(id: int):
    try:
        data = db.delete(id)

        if not data:
            return not_found(f"Ticket {id} introuvable")

        return success({
            "deleted": True,
            "id": id
        })

    except Exception as e:
        return error(str(e))

