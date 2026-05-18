# middlewares/cors.py

from fastapi.middleware.cors import CORSMiddleware
from config.settings import FRONTEND_URL


def add_cors(app):

    app.add_middleware(

        CORSMiddleware,

        # domaines autorisés à appeler l'API
        allow_origins=[
            FRONTEND_URL,
            "http://localhost:5173",  # vite
            "http://localhost:3000",  # react classique
        ],

        # autorise les cookies / tokens / sessions
        allow_credentials=True,

        # autorise toutes les méthodes HTTP
        allow_methods=["*"],

        # autorise tous les headers
        allow_headers=["*"],
    )