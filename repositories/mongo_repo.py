from config.database import get_mongo_db
from datetime import datetime


class MongoRepo:

    def __init__(self):
        # connexion à la base MongoDB
        self.db = get_mongo_db()

    # sauvegarde une prédiction en base
    def sauvegarder_prediction(self, data: dict):
        data["created_at"] = datetime.now()
        result = self.db.predictions.insert_one(data)
        return str(result.inserted_id)

    # récupère la dernière prédiction enregistrée
    def get_derniere_prediction(self):
        result = self.db.predictions.find_one(
            sort=[("created_at", -1)]
        )

        # conversion de l'id Mongo en string pour API
        if result:
            result["_id"] = str(result["_id"])

        return result

    # enregistre un log de pipeline
    def logger_pipeline(self, log: dict):
        log["timestamp"] = datetime.now()
        self.db.pipeline_logs.insert_one(log)

    # récupère les derniers logs du pipeline
    def get_derniers_logs(self, limit: int = 20):
        logs = list(self.db.pipeline_logs.find(
            sort=[("timestamp", -1)],
            limit=limit
        ))

        # conversion des ObjectId en string
        for log in logs:
            log["_id"] = str(log["_id"])

        return logs