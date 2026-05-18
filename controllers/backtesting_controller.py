from fastapi import APIRouter
from utils.db_query import DBQuery
from utils.response import success, error, paginate


# routes backtesting
router = APIRouter(
    prefix="/api/v1/backtesting",
    tags=["backtesting"]
)

db = DBQuery("backtesting")


# liste des backtests avec pagination
@router.get("")
def list_backtesting(page: int = 1, per_page: int = 20):

    try:
        data = db.list(page, per_page)
        total = db.count()
        return paginate(data, total, page, per_page)

    except Exception as e:
        return error(str(e))


# total des backtests
@router.get("/count")
def count_backtesting():

    try:
        total = db.count()
        return success({"total": total})

    except Exception as e:
        return error(str(e))


# stats globales du backtesting
@router.get("/stats")
def stats_backtesting():

    try:
        data = db.custom("stats", many=False)
        return success(data)

    except Exception as e:
        return error(str(e))


# liste des performances
@router.get("/performances")
def list_performances():

    try:
        db_perf = DBQuery("performance")
        data = db_perf.custom("list", many=True)
        return success(data)

    except Exception as e:
        return error(str(e))


# dernière performance enregistrée
@router.get("/performances/derniere")
def derniere_performance():

    try:
        db_perf = DBQuery("performance")
        data = db_perf.custom("derniere", many=False)
        return success(data)

    except Exception as e:
        return error(str(e))