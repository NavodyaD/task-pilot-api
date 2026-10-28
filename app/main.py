from fastapi import FastAPI
from app.config.database import engine, Base

# Import models
from app.models.user_model import User

# Import controllers
from app.controller.user_controller import router as user_router

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# register routes
app.include_router(user_router)

@app.get("/")
def home():
    return {"message": "FastAPI running successfully"}