import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.email import send_verification_email
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.db.dynamodb import (
    get_user_by_email,
    get_user_by_id,
    get_user_by_verification_token,
    put_user,
    update_user,
)
from app.dependencies import get_current_user
from app.models.user import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserProfile,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest):
    if get_user_by_email(body.email):
        raise HTTPException(status_code=409, detail="Email already registered")

    user_id = str(uuid.uuid4())
    verification_token = str(uuid.uuid4())
    expires_at = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    now = datetime.now(timezone.utc).isoformat()

    put_user(
        {
            "user_id": user_id,
            "email": body.email,
            "password_hash": hash_password(body.password),
            "email_verified": False,
            "verification_token": verification_token,
            "verification_token_expires_at": expires_at,
            "created_at": now,
        }
    )

    send_verification_email(body.email, verification_token)
    return {"message": "Registration successful. Check your email to verify your account."}


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    user = get_user_by_email(body.email)
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.get("email_verified"):
        raise HTTPException(status_code=403, detail="Email not verified")

    access_token = create_access_token(user["user_id"])
    refresh_token = create_refresh_token(user["user_id"])

    update_user(
        user["user_id"],
        "SET refresh_token = :rt",
        {":rt": refresh_token},
    )

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.get("/verify-email")
def verify_email(token: str):
    user = get_user_by_verification_token(token)
    if not user:
        raise HTTPException(status_code=410, detail="Invalid or expired verification link")

    expires_at = user.get("verification_token_expires_at", "")
    if datetime.now(timezone.utc) > datetime.fromisoformat(expires_at):
        raise HTTPException(status_code=410, detail="Verification link has expired")

    update_user(
        user["user_id"],
        "SET email_verified = :v REMOVE verification_token, verification_token_expires_at",
        {":v": True},
    )
    return {"message": "Email verified successfully. You can now log in."}


@router.post("/refresh", response_model=TokenResponse)
def refresh(body: RefreshRequest):
    from jose import JWTError

    try:
        payload = decode_token(body.refresh_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    user_id = payload.get("sub")
    user = get_user_by_id(user_id)
    if not user or user.get("refresh_token") != body.refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token revoked or not found")

    new_access = create_access_token(user_id)
    new_refresh = create_refresh_token(user_id)

    update_user(user_id, "SET refresh_token = :rt", {":rt": new_refresh})
    return TokenResponse(access_token=new_access, refresh_token=new_refresh)


@router.get("/me", response_model=UserProfile)
def me(user: dict = Depends(get_current_user)):
    return UserProfile(
        user_id=user["user_id"],
        email=user["email"],
        email_verified=user["email_verified"],
        created_at=user["created_at"],
    )
