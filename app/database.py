from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

try:
    from .config import settings
except:
    from config import settings

# import psycopg2
# from psycopg2.extras import RealDictCursor

SQLALQUEMY_DATABASE_URL = f"""postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"""

engine = create_engine(SQLALQUEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, )

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

##para usar raw sql ao invés de sqlalchemy
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fast_api",
#             user="postgres",
#             password="postgres",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Connected to the database")
#         break

#     except Exception as e:
#         print("Unable to connect to the database")
#         print("Error: ", e)
#         time.sleep(2)
        