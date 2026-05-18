from fastapi import APIRouter
from utils.db_query import DBQuery
from utils.response import (
    success,
    not_found,
    paginate,
    error
)


router = APIRouter(
    prefix="/api/v1/tirages",
    tags=["tirages"]
)

db = DBQuery("tirage")

# retourne la liste des tirages avec pagination
@router.get("")
def list_tirages(
    page: int = 1,
    per_page: int = 20
):

    try:

        data = db.list(page, per_page)

        # nombre total de tirages
        total = db.count()

        # réponse paginée standardisée
        return paginate(
            data,
            total,
            page,
            per_page
        )

    except Exception as e:

        # gestion simple des erreurs
        return error(str(e))


# retourne uniquement le nombre total de tirages
@router.get("/count")
def count_tirages():

    try:

        total = db.count()

        return success({
            "total": total
        })

    except Exception as e:

        return error(str(e))


# retourne le dernier tirage disponible
@router.get("/dernier")
def dernier_tirage():

    try:

        # appel procédure custom:
        # sp_tirage_dernier()
        data = db.custom(
            "dernier",
            many=False
        )

        if not data:
            return not_found(
                "Aucun tirage trouvé"
            )

        return success(data)

    except Exception as e:

        return error(str(e))


# recherche un tirage par date
@router.get("/date/{date}")
def tirage_par_date(date: str):

    try:

        data = db.find(date)

        if not data:

            return not_found(
                f"Aucun tirage pour la date {date}"
            )

        return success(data)

    except Exception as e:

        return error(str(e))


# retourne un tirage via son id
@router.get("/{id}")
def read_tirage(id: int):

    try:

        data = db.read(id)

        if not data:

            return not_found(
                f"Tirage {id} introuvable"
            )

        return success(data)

    except Exception as e:

        return error(str(e))