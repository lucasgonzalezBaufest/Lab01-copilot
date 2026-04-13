from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import BaseModel

from app.auth import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
)

app = FastAPI(
    title="JWT Auth API",
    description="FastAPI application with JWT authentication (access + refresh tokens).",
    version="0.1.0",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- Response models ---

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


# --- Endpoints ---

@app.post("/token", response_model=TokenResponse, summary="Obtain JWT tokens")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate with **username** and **password**.

    - username: `admin`
    - password: `admin123`

    Returns an access token (expires in 300 s) and a refresh token (expires in 3600 s).
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user["username"]})
    refresh_token = create_refresh_token(data={"sub": user["username"]})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )


@app.post("/token/refresh", response_model=TokenResponse, summary="Refresh JWT tokens")
def refresh_token(body: RefreshRequest):
    """
    Provide a valid **refresh_token** to obtain a new access token and refresh token pair.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(body.refresh_token)
    except JWTError:
        raise credentials_exception

    if payload.get("type") != "refresh":
        raise credentials_exception

    username: str = payload.get("sub")
    if not username:
        raise credentials_exception

    access_token = create_access_token(data={"sub": username})
    new_refresh_token = create_refresh_token(data={"sub": username})

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )


@app.get("/me", summary="Get current user")
def read_current_user(token: str = Depends(oauth2_scheme)):
    """
    Returns the username of the currently authenticated user.
    Requires a valid **access_token** in the `Authorization: Bearer <token>` header.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
    except JWTError:
        raise credentials_exception

    if payload.get("type") != "access":
        raise credentials_exception

    username: str = payload.get("sub")
    if not username:
        raise credentials_exception

    return {"username": username}
