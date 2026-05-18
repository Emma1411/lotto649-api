import psycopg2.extras
from config.database import get_connection


class DBQuery:

    def __init__(self, table: str):
        self.table = table

    def _exec(self, sql: str, params: tuple = ()):

        # ouvre une connexion PostgreSQL
        conn = get_connection()

        # retourne directement des dicts au lieu de tuples
        cur = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        # exécution de la requête
        cur.execute(sql, params)

        try:
            # récupération des résultats
            result = cur.fetchall()

            # conversion propre en liste de dictionnaires
            result = [dict(r) for r in result]

        except Exception:
            # certaines procédures ne retournent rien
            result = []

        # commit pour appliquer les changements
        conn.commit()

        # fermeture propre
        cur.close()
        conn.close()

        return result

    def _exec_one(self, sql: str, params: tuple = ()):

        # récupère seulement le premier résultat
        result = self._exec(sql, params)

        return result[0] if result else None

    # retourne une liste paginée
    def list(self, page: int = 1, per_page: int = 20, paginate: int = 1):

        return self._exec(
            f"SELECT * FROM sp_{self.table}_list(%s, %s, %s)",
            (page, per_page, paginate)
        )

    # retourne un élément par id
    def read(self, id: int):

        return self._exec_one(
            f"SELECT * FROM sp_{self.table}_read(%s)",
            (id,)
        )

    # recherche via une valeur
    def find(self, value):

        return self._exec_one(
            f"SELECT * FROM sp_{self.table}_find(%s)",
            (value,)
        )

    # insertion
    def create(self, *args):

        # génère automatiquement:
        # %s, %s, %s ...
        placeholders = ", ".join(["%s"] * len(args))

        return self._exec_one(
            f"SELECT * FROM sp_{self.table}_create({placeholders})",
            args
        )

    # mise à jour
    def update(self, *args):

        placeholders = ", ".join(["%s"] * len(args))

        return self._exec_one(
            f"SELECT * FROM sp_{self.table}_update({placeholders})",
            args
        )

    # suppression par id
    def delete(self, id: int):

        return self._exec_one(
            f"SELECT * FROM sp_{self.table}_delete(%s)",
            (id,)
        )

    # retourne le total
    def count(self):

        result = self._exec_one(
            f"SELECT * FROM sp_{self.table}_count()"
        )

        return result["total"] if result else 0

    # pour les procédures custom/spéciales
    def custom(
        self,
        action: str,
        params: tuple = (),
        many: bool = True
    ):

        sql = f"SELECT * FROM sp_{self.table}_{action}"

        # ajoute automatiquement les paramètres
        if params:

            placeholders = ", ".join(["%s"] * len(params))
            sql += f"({placeholders})"

        else:
            sql += "()"

        # retourne plusieurs lignes
        if many:
            return self._exec(sql, params)

        # retourne une seule ligne
        return self._exec_one(sql, params)