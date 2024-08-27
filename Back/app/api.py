from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints.router import router
import subprocess

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

subprocess.run(["python", "Back/app/db/mainDB.py"])