from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine, get_db
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def welcome(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

@app.get("/detections/", response_class=HTMLResponse)
def display_detections(request: Request, db: Session = Depends(get_db)):
    detections = crud.get_detections(db)  
    return templates.TemplateResponse("detections.html", {"request": request, "detections": detections})