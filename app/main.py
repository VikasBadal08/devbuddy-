from fastapi import FastAPI
from sqlalchemy import text 

from app.core.db import engine 

app= FastAPI(title="DevBuddy")

@app.get("/")
def root():
    return {
        "message":"DevBuddy is running"
    }

@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

            return {
                "status":"healthy",
                "database":"connected"
            }
    except Exception:
        return {
            "status":"unhealthy",
            "database":"disconnected"
        }