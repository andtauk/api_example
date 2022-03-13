import uvicorn
import time
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

try:
    from .database import engine
    from . import models
    from .routers import post, user, auth
    
except:
    from database import engine
    import models
    from routers import post, user, auth
    

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fast_api",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Connected to the database")
        break

    except Exception as e:
        print("Unable to connect to the database")
        print("Error: ", e)
        time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hellow World"}



if __name__ == "__main__":
    uvicorn.run("__main__:app", host="127.0.0.1", reload=True, port=8000)

    