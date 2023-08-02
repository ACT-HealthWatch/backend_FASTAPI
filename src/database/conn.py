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
        self.USERNAME: str = "localplayer0"
        self.PASSWORD: str = "hello_neighbor123"
        self.ENDPOINT: str = "hoshi-kirby.xyz"
        self.DBNAME: str = "develop"
        self.PORT: str = "3306"
        self.rds = create_engine(
                f"mysql+pymysql://{self.USERNAME}:{self.PASSWORD}@{self.ENDPOINT}:{self.PORT}/{self.DBNAME}?charset=utf8",
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


conn = CONNECT()
Session = conn.rdsSession()