
import os
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Garmin Health+",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "app": "Garmin Health+",
        "status": "online",
        "garmin_connected": False
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/garmin/status")
def garmin_status():
    return {
        "connected": False,
        "message": "Garmin integration not configured"
    }
