from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine, database

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# HTML pages

@app.get("/add_user", response_class=RedirectResponse)
def add_user_form(request: Request):
    return templates.TemplateResponse("add_user.html", {"request": request})

@app.post("/add_user", response_class=RedirectResponse)
def create_user(request: Request, first_name: str = Form(...), last_name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    new_user = schemas.UserCreate(first_name=first_name, last_name=last_name, email=email, password=password)
    db_user = models.User(**new_user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return RedirectResponse("/products", status_code=303)

@app.get("/products", response_class=RedirectResponse)
def read_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

