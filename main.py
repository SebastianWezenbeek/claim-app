# backend/main.py
import os
from fastapi import FastAPI, Request, Depends, Form, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from starlette.middleware.sessions import SessionMiddleware
from app.db import init_db, get_session
from app.models import Claim, Merchant
from app.schemas import ClaimCreate
# from .auth import set_session, current_merchant, hash_pw, verify_pw

app = FastAPI(title="Claim App")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY","dev-secret"))

BASE_DIR = os.path.dirname(__file__)
print(BASE_DIR)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.on_event("startup")
def on_startup():
    init_db()

# ---------- Customer pages ----------
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("claim_form.html", {"request": request})

@app.post("/claim")
def submit_claim(
    request: Request,
    order_id: str = Form(...),
    customer_email: str = Form(...),
    reason: str = Form(...),
    details: str = Form("")
    , session: Session = Depends(get_session)
):
    claim = Claim(order_id=order_id, customer_email=customer_email, reason=reason, details=details)
    session.add(claim); session.commit()
    return templates.TemplateResponse("claim_form.html", {
        "request": request, "success": True
    })

# ---------- Merchant auth ----------
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("merchant_login.html", {"request": request})

# @app.post("/login")
# def login(email: str = Form(...), password: str = Form(...), response: Response = None,
#           session: Session = Depends(get_session)):
#     merchant = session.exec(select(Merchant).where(Merchant.email == email)).first()
#     if not merchant or not verify_pw(password, merchant.password_hash):
#         raise HTTPException(401, "Invalid credentials")
#     set_session(response, merchant.id)
#     response.headers["HX-Redirect"] = "/dashboard"
#     return Response(status_code=204)  # HTMX redirect

# ---------- Merchant dashboard ----------
# @app.get("/dashboard")
# def dashboard(request: Request, merchant: Merchant = Depends(current_merchant),
#               session: Session = Depends(get_session)):
#     claims = session.exec(select(Claim).order_by(Claim.created_at.desc())).all()
#     return templates.TemplateResponse("merchant_dashboard.html",
#                                       {"request": request, "claims": claims, "merchant": merchant})

# @app.post("/claims/{claim_id}/status")
# def update_status(claim_id: int, status: str = Form(...),
#                   merchant: Merchant = Depends(current_merchant),
#                   session: Session = Depends(get_session)):
#     claim = session.get(Claim, claim_id)
#     if not claim:
#         raise HTTPException(404)
#     claim.status = status
#     session.add(claim); session.commit(); session.refresh(claim)
#     # return partial row fragment for HTMX to swap
#     from fastapi.responses import HTMLResponse
#     row = f"""
#     <tr id="claim-{claim.id}">
#       <td>{claim.id}</td><td>{claim.order_id}</td><td>{claim.customer_email}</td>
#       <td>{claim.reason}</td><td>{claim.status}</td>
#       <td>
#         <form hx-post="/claims/{claim.id}/status" hx-target="#claim-{claim.id}" hx-swap="outerHTML">
#           <select name="status">
#             <option {"selected" if claim.status=="new" else ""}>new</option>
#             <option {"selected" if claim.status=="in_review" else ""}>in_review</option>
#             <option {"selected" if claim.status=="approved" else ""}>approved</option>
#             <option {"selected" if claim.status=="rejected" else ""}>rejected</option>
#           </select>
#           <button type="submit">Save</button>
#         </form>
#       </td>
#     </tr>
#     """
#     return HTMLResponse(row)
#
# # Seed one merchant on first run (dev only)
# @app.post("/seed-merchant")
# def seed_merchant(email: str = Form("admin@example.com"), password: str = Form("admin"),
#                   session: Session = Depends(get_session)):
#     if session.exec(select(Merchant).where(Merchant.email==email)).first():
#         return {"ok": True}
#     session.add(Merchant(email=email, password_hash=hash_pw(password))); session.commit()
#     return {"ok": True}
