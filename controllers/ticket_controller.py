from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from utils.db_query import DBQuery
from utils.response import success, created, not_found, error, paginate


# routes tickets
router = APIRouter(
    prefix="/api/v1/tickets",
    tags=["tickets"]
)

db = DBQuery("ticket")


# modèle création ticket
class TicketCreate(BaseModel):
    date_achat: date
    strategie: str
    numeros_joues: List[int]
    cout_ticket: float = 3.00
    date_tirage: Optional[date] = None


# modèle update ticket
class TicketUpdate(BaseModel):
    statut: str


# liste des tickets avec pagination
@router.get("")
def list_tickets(page: int = 1, per_page: int = 20):

    try:
        data = db.list(page, per_page)
        total = db.count()
        return paginate(data, total, page, per_page)

    except Exception as e:
        return error(str(e))


# total des tickets
@router.get("/count")
def count_tickets():

    try:
        total = db.count()
        return success({"total": total})

    except Exception as e:
        return error(str(e))


# suivi des tickets (requête custom)
@router.get("/suivi")
def suivi_tickets():

    try:
        data = db.custom("suivi", many=True)
        return success(data)

    except Exception as e:
        return error(str(e))


# lecture d’un ticket par id
@router.get("/{id}")
def read_ticket(id: int):

    try:
        data = db.read(id)

        if not data:
            return not_found(f"Ticket {id} introuvable")

        return success(data)

    except Exception as e:
        return error(str(e))


# création d’un ticket
@router.post("")
def create_ticket(ticket: TicketCreate):

    try:
        data = db.create(
            ticket.date_achat,
            ticket.strategie,
            ticket.numeros_joues,
            ticket.cout_ticket,
            ticket.date_tirage
        )
        return created(data)

    except Exception as e:
        return error(str(e))


# mise à jour du statut
@router.put("/{id}")
def update_ticket(id: int, ticket: TicketUpdate):

    try:
        data = db.update(id, ticket.statut)

        if not data:
            return not_found(f"Ticket {id} introuvable")

        return success(data)

    except Exception as e:
        return error(str(e))


# suppression d’un ticket
@router.delete("/{id}")
def delete_ticket(id: int):

    try:
        data = db.delete(id)

        if not data:
            return not_found(f"Ticket {id} introuvable")

        return success({"deleted": True, "id": id})

    except Exception as e:
        return error(str(e))