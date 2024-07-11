from fastapi import FastAPI
from router import api_routers
from engine.db_connection import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(api_routers.router)
