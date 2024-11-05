import jwt
from apps.db import schemas
from apps.db import Users
from apps.db import Tokens
from apps.db import SessionDep
from apps.admin.auth import (
    JWTBearer,
    token_required,
    check_and_get_refresh_token,
    check_and_get_access_token,
    decodeJWT,
)
from apps.admin.crypto import (
    get_hashed_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    JWT_SECRET_KEY,
    ALGORITHM,
)
from datetime import datetime, timezone
from sqlmodel import select, delete
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import UJSONResponse


account = APIRouter(
    prefix="/account",
    tags=["Account"],
)


@account.post("/register")
async def register(user: schemas.UserCreate, session: SessionDep):
    existing_user = session.exec(
        select(Users).where(Users.username == user.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    encrypted_password = get_hashed_password(user.pw)
    new_user = Users(
        login_id=user.username,
        pw=encrypted_password,
        player=user.player,
        birthdate=user.birthdate,
        gender=user.gender,
        status=user.status,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "User registered successfully"}


@account.post("/unregister")
@token_required
async def unregister(
    request: schemas.requestdetails,
    session: SessionDep,
    dependencies=Depends(JWTBearer()),
):
    existing_user = session.exec(
        select(Users).where(Users.username == request.username)
    )
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(existing_user)
    session.commit()
    return {"message": "User unregistered successfully"}


@account.post("/login", response_model=schemas.TokenSchema)
async def login(request: schemas.requestdetails, session: SessionDep):
    existing_user = session.exec(
        select(Users).where(Users.username == request.username)
    ).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")

    hashed_pass = existing_user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access = create_access_token(subject=request.username, uuid=existing_user.uuid)
    refresh = create_refresh_token(subject=request.username, uuid=existing_user.uuid)

    token_db = Tokens(
        uuid=existing_user.uuid,
        user_id=request.username,
        access_token=access,
        refresh_token=refresh,
        status=True,
        created_date=str(datetime.now(timezone.utc)),
    )

    session.add(token_db)
    session.commit()
    session.refresh(token_db)
    response = UJSONResponse(
        status_code=200,
        content={
            "access_token": access,
            "refresh_token": refresh,
        },
    )
    response.set_cookie(key="access_token", value=access, secure=True)
    response.set_cookie(key="refresh_token", value=refresh, secure=True)
    return response


@account.post("/refresh-token", response_model=schemas.TokenSchema)
async def refresh_token(
    session: SessionDep,
    refresh_token: str = Depends(check_and_get_refresh_token),
    access_token: str = Depends(check_and_get_access_token),
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Access Token not provided")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not provided")

    access_token_payload = decodeJWT(access_token)
    refresh_token_payload = decodeJWT(refresh_token)
    refresh_token_exp = refresh_token_payload["exp"]
    access_token_exp = access_token_payload["exp"]
    if access_token_exp < datetime.now(timezone.utc):
        if refresh_token_exp < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Refresh token expired")
        else:
            exisiting_user = session.exec(
                select(Tokens).where(Tokens.username == refresh_token_payload["sub"])
            ).first()
            if not exisiting_user:
                raise HTTPException(status_code=400, detail="Invalid access token")

            access = create_access_token(
                refresh_token_payload["sub"], refresh_token_payload["uuid"]
            )
            refresh = create_refresh_token(
                refresh_token_payload["sub"], refresh_token_payload["uuid"]
            )

            token_db = Tokens(
                uuid=refresh_token_payload["uuid"],
                user_id=refresh_token_payload["sub"],
                access_token=access,
                refresh_token=refresh,
                status=True,
                created_date=str(datetime.now(timezone.utc)),
            )

            session.add(token_db)
            session.commit()
            session.refresh(token_db)
            response = UJSONResponse(
                status_code=200,
                content={
                    "access_token": access,
                    "refresh_token": refresh,
                },
            )
            response.set_cookie(key="access_token", value=access, secure=True)
            response.set_cookie(key="refresh_token", value=refresh, secure=True)
            return response
    else:
        raise HTTPException(status_code=401, detail="Access token not expired")


@account.get("/getusers")
@token_required
async def getusers(session: SessionDep, dependencies=Depends(JWTBearer())):
    user = session.exec(select(Users)).all()
    return user


@account.post("/change-password")
async def change_password(request: schemas.changepassword, session: SessionDep):
    existing_user = session.exec(
        select(Users).where(Users.username == request.username)
    ).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(request.old_password, existing_user.password):
        raise HTTPException(status_code=400, detail="Invalid old password")

    encrypted_password = get_hashed_password(request.new_password)
    existing_user.password = encrypted_password
    session.add(existing_user)
    session.commit()
    return {"message": "Password changed successfully"}


@account.post("/logout")
@token_required
async def logout(session: SessionDep, dependencies=Depends(JWTBearer())):
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    username = payload["sub"]
    token_record = session.exec(select(Tokens)).all()
    info = []
    for record in token_record:
        print("record", record)
        if (
            datetime.now(timezone.utc)
            - record.created_date.replace(tzinfo=timezone.utc)
        ).days > 1:
            info.append(record.username)
    if info:
        existing_token = session.exec(delete(Tokens).where(Tokens.username == info))
        session.commit()

    existing_token = session.exec(
        select(Tokens).where(Tokens.username == username, Tokens.access_token == token)
    ).first()
    if existing_token:
        existing_token.status = False
        session.add(existing_token)
        session.commit()
    return {"message": "Logout Successfully"}
