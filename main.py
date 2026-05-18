from fastapi import FastAPI
from config.database import test_connections
from config.settings import APP_NAME, API_VERSION
from middlewares.cors import add_cors
from controllers.tirage_controller import router as tirage_router
from controllers.stats_controller import router as stats_router
from controllers.prediction_controller import router as prediction_router
from controllers.ticket_controller import router as ticket_router
from controllers.backtesting_controller import router as backtesting_router


# création de l'application FastAPI
app = FastAPI(
    title=APP_NAME,
    version=API_VERSION,
    description="API backend pour le projet Lotto 6/49 IA"
)


# activation du CORS
# permet au frontend d'appeler l'API
add_cors(app)


# enregistrement des routes/controllers
app.include_router(tirage_router)
app.include_router(stats_router)
app.include_router(prediction_router)
app.include_router(ticket_router)
app.include_router(backtesting_router)


# route simple pour vérifier si l'API fonctionne
@app.get("/")
def root():

    return {
        "app": APP_NAME,
        "version": API_VERSION,
        "status": "running"
    }


# démarrage du serveur
@app.on_event("startup")
def startup():

    print(f"{APP_NAME} démarré")

    # test des connexions base de données
    test_connections()