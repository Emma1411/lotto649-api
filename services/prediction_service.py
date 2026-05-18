import pickle
import pandas as pd
import random
from datetime import datetime
from config.settings import MODEL_PATH, POOL_PATH
from repositories.mongo_repo import MongoRepo


class PredictionService:

    def __init__(self):
        # connexion Mongo + chargement du modèle
        self.mg = MongoRepo()
        self._load_model()

    # chargement du modèle ML + pool de numéros
    def _load_model(self):
        try:
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)

            self.pool = pd.read_csv(POOL_PATH)

            print("Modèle ML chargé")

        except Exception as e:
            print(f"Modèle non chargé : {e}")
            self.model = None
            self.pool = None

    # retourne le pool de numéros brut
    def get_pool(self):
        if self.pool is None:
            return []

        return self.pool.to_dict(orient="records")

    # génération des grilles de prédiction
    def generer_grilles(self, nb_tickets: int, strategie: str):

        if self.pool is None:
            raise Exception("Modèle ML non disponible")

        numeros = list(self.pool["numero"].astype(int))

        # choix de la stratégie
        if strategie == "chaud":
            grilles = self._chaud(numeros, nb_tickets)

        elif strategie == "couverture":
            grilles = self._couverture(numeros, nb_tickets)

        else:
            grilles = self._equilibre(numeros, nb_tickets)

        # sauvegarde en base MongoDB
        self.mg.sauvegarder_prediction({
            "date": datetime.now().isoformat(),
            "strategie": strategie,
            "nb_tickets": nb_tickets,
            "grilles": grilles
        })

        return {
            "strategie": strategie,
            "nb_tickets": nb_tickets,
            "cout_total": nb_tickets * 3,
            "grilles": grilles
        }

    # stratégie équilibrée : tirage aléatoire
    def _equilibre(self, pool, n):
        return [
            {"ticket": i + 1, "numeros": sorted(random.sample(pool, 6))}
            for i in range(n)
        ]

    # stratégie "chaud" : prend les numéros les plus fréquents
    def _chaud(self, pool, n):
        top = pool[:10]

        return [
            {"ticket": i + 1, "numeros": sorted(random.sample(top, 6))}
            for i in range(n)
        ]

    # stratégie couverture : limite la répétition des numéros
    def _couverture(self, pool, n):
        used = {}
        grilles = []

        for i in range(n):

            # trie selon la fréquence d’utilisation
            scored = sorted(pool, key=lambda x: used.get(x, 0))
            nums = sorted(scored[:6])

            # mise à jour des usages
            for num in nums:
                used[num] = used.get(num, 0) + 1

            grilles.append({"ticket": i + 1, "numeros": nums})

        return grilles