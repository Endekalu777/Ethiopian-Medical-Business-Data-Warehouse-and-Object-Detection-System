from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from my_project import crud, models, schemas
from my_project.database import SessionLocal, engine,get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Object Detection API"}


@app.post("/detections/", response_model=schemas.ObjectDetection)
def create_detection(detection: schemas.ObjectDetectionCreate, db: Session = Depends(get_db)):
    return crud.create_detection(db=db, detection=detection)

@app.get("/detections/", response_model=list[schemas.ObjectDetection])
def read_detections(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    detections = crud.get_detections(db, skip=skip, limit=limit)
    return detections
