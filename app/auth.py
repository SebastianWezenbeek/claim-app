# backend/auth.py
import os, hashlib, hmac
from fastapi import Depends, HTTPException, Request, Response
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from sqlmodel import Session, select
from .models import Merchant
from .db import get_session

SECRET = os.getenv("SECRET_KEY", "dev-secret")
serializer = URLSafeTimedSerializer(SECRET)

def hash_pw(pw: str) -> str:
    return hashlib.scrypt(pw.encode(), salt=b"claims", n=2**14, r=8, p=1).hex()

def verify_pw(pw: str, hashed: str) -> bool:
    return hmac.compare_digest(hash_pw(pw), hashed)

def set_session(resp: Response, merchant_id: int):
    token = serializer.dumps({"merchant_id": merchant_id})
    resp.set_cookie("session", token, httponly=True, samesite="lax")

def current_merchant(
    request: Request, session: Session = Depends(get_session)
) -> Merchant:
    token = request.cookies.get("session")
    if not token:
        raise HTTPException(401)
    try:
        data = serializer.loads(token, max_age=60*60*24*7)
    except (BadSignature, SignatureExpired):
        raise HTTPException(401)
    merchant = session.get(Merchant, data["merchant_id"])
    if not merchant:
        raise HTTPException(401)
    return merchant
