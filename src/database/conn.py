import os
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CONNECT:
    """
    Returns:
        각 연결 세션
    """

    def __init__(self):
        # rds settings
        # self.USERNAME: str = "localplayer0"
        # self.PASSWORD: str = "hello_neighbor123"
        # self.ENDPOINT: str = "hoshi-kirby.xyz"
        # self.DBNAME: str = "develop"
        # self.PORT: str = "3306"
        # self.url_db = os.environ.get("JAWSDB_URL")
        self.USERNAME: str = os.environ.get("USERNAME")
        self.PASSWORD: str = os.environ.get("PASSWORD")
        self.ENDPOINT: str = os.environ.get("ENDPOINT")
        self.DBNAME: str = "develop"
        self.PORT: str = "3306"
        self.url_db = f"mysql+pymysql://{self.USERNAME}:{self.PASSWORD}@{self.ENDPOINT}:{self.PORT}/{self.DBNAME}"

        self.REDIS_HOSTNAME: str = os.environ.get("REDIS")
        self.REDIS_PORT: str = "6379"
        self.REDIS_DBNAME: int = 0

        self.rds = create_engine(
            self.url_db,
            echo=True
        )

        self.session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.rds
        )

    def engineData(self):
        return self.rds

    def rdsSession(self):
        try:
            return self.session
        except Exception as e:
            return str(e)

    def redisConnect(self, dbname: str):
        """
        Args:
            dbname (str): 사용할 db명
        """
        try:
            conn = redis.StrictRedis(
                host=self.REDIS_HOSTNAME,
                port=self.REDIS_PORT,
                db=self.REDIS_DBNAME
            )

            return conn

        except Exception as e:
            return (str(e))


conn = CONNECT()
redisController = conn.redisConnect(0)
Session = conn.rdsSession()
