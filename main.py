
import os
import secrets

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI(
    title="Garmin Health+",
    version="1.1.0",
    docs_url=None,
    redoc_url=None
)

bearer = HTTPBearer(auto_error=False)


def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(bearer)
):
    expected = os.environ.get("HEALTH_API_TOKEN")

    if not expected or len(expected) < 32:
        raise HTTPException(
            status_code=503,
            detail="Authentication not configured"
        )

    if (
        credentials is None
        or not secrets.compare_digest(
            credentials.credentials, expected
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return True


@app.get("/")
def home():
    return {
        "app": "Garmin Health+",
        "status": "online"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/garmin/status")
def garmin_status(authorized=Depends(require_auth)):
    return {
        "connected": False,
        "message": "Garmin integration pending"
    }
