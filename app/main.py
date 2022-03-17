from multiprocessing import allow_connection_pickling
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# try:
from .database import engine
from . import models
from .routers import post, user, auth, vote
from .config import settings
    
# except:
#     from database import engine
#     import models
#     from routers import post, user, auth, vote
#     from config import settings    

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello 13:24 tutorial"}

# if __name__ == "__main__":
#     uvicorn.run("__main__:app", host="127.0.0.1", reload=True, port=8000)

    