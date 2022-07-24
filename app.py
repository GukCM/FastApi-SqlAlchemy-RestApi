#Conda prompt conda create --name fastapi-mysql python=3
#conda prompt conda activate fastapi-mysql
#python -m uvicorn app:app --reload
#-50 -330
from fastapi import FastAPI
from routes.user import user
app = FastAPI()

app.include_router(user)
