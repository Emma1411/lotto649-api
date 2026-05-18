from fastapi import APIRouter
from utils.response import success, error
from services.prediction_service import PredictionService


# routes predictions
router = APIRouter(
    prefix="/api/v1/predictions",
    tags=["predictions"]
)

# service métier pour générer les prédictions
service = PredictionService()


# génération de grilles de prédiction
@router.get("/generer")
def generer_predictions(nb_tickets: int = 3, strategie: str = "equilibre"):

    try:
        data = service.generer_grilles(nb_tickets, strategie)
        return success(data)

    except Exception as e:
        return error(str(e))


# récupération du pool de numéros utilisés pour la prédiction
@router.get("/pool")
def get_pool():

    try:
        data = service.get_pool()
        return success(data)

    except Exception as e:
        return error(str(e))


# dernière prédiction générée
@router.get("/derniere")
def derniere_prediction():

    try:
        from repositories.mongo_repo import MongoRepo

        mg = MongoRepo()
        data = mg.get_derniere_prediction()

        return success(data)

    except Exception as e:
        return error(str(e))