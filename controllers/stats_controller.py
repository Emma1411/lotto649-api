from fastapi import APIRouter
from utils.db_query import DBQuery
from utils.response import success, not_found, error


# routes stats
router = APIRouter(
    prefix="/api/v1/stats",
    tags=["stats"]
)

db = DBQuery("stats")


# liste globale des stats
@router.get("")
def list_stats():

    try:
        data = db.custom("list", many=True)
        return success(data)

    except Exception as e:
        return error(str(e))


# heatmap des numéros
@router.get("/heatmap")
def heatmap():

    try:
        data = db.custom("heatmap", many=True)
        return success(data)

    except Exception as e:
        return error(str(e))


# numéros les plus fréquents
@router.get("/chauds")
def numeros_chauds(limit: int = 15):

    try:
        data = db.custom(
            "chauds",
            params=(limit,),
            many=True
        )
        return success(data)

    except Exception as e:
        return error(str(e))


# numéros les moins fréquents
@router.get("/froids")
def numeros_froids(limit: int = 15):

    try:
        data = db.custom(
            "froids",
            params=(limit,),
            many=True
        )
        return success(data)

    except Exception as e:
        return error(str(e))


# total stats en base
@router.get("/count")
def count_stats():

    try:
        total = db.count()
        return success({"total": total})

    except Exception as e:
        return error(str(e))


# stats d’un numéro précis
@router.get("/{numero}")
def read_stats(numero: int):

    try:
        data = db.custom(
            "read",
            params=(numero,),
            many=False
        )

        if not data:
            return not_found(
                f"Numéro {numero} introuvable"
            )

        return success(data)

    except Exception as e:
        return error(str(e))