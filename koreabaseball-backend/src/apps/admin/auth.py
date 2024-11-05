import jwt
from functools import wraps
from config import SECRET_KEY, REFRESH_SECRET_KEY
from apps.db import Tokens
from sqlmodel import select
from jwt.exceptions import InvalidTokenError
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = SECRET_KEY
JWT_REFRESH_SECRET_KEY = REFRESH_SECRET_KEY


async def check_and_get_access_token(request: Request):
    cookie = request.cookies
    if not cookie:
        return None
    if cookie.get("access_token"):
        return cookie.get("access_token")


async def check_and_get_refresh_token(request: Request):
    cookie = request.cookies
    if not cookie:
        return None
    if cookie.get("refresh_token"):
        return cookie.get("refresh_token")


def decodeJWT(jwtoken: str):
    try:
        # Decode and verify the token
        payload = jwt.decode(jwtoken, JWT_SECRET_KEY, ALGORITHM)
        return payload
    except InvalidTokenError:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except Exception:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


def token_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        payload = jwt.decode(kwargs["dependencies"], JWT_SECRET_KEY, ALGORITHM)
        user_id = payload["sub"]
        data = (
            kwargs["session"]
            .exec(
                select(Tokens).filter_by(
                    user_id=user_id, access_token=kwargs["dependencies"], status=True
                )
            )
            .first()
        )
        if data:
            return await func(
                dependencies=kwargs["dependencies"], session=kwargs["session"]
            )

        else:
            return {"msg": "Token blocked"}

    return wrapper


jwt_bearer = JWTBearer()
