class HerokuUtils:
    @staticmethod
    def parse_postgres_dialect(db_url: str) -> str:
        """
        Fixes an issue with the now deprecated postgres dialect that Heroku gives back
        :param db_url: valid DB URL
        :return: DB URL with the correct dialect
        """
        if db_url.startswith("postgres://"):
            return db_url.replace("postgres://", "postgresql://", 1)
        else:
            return db_url
