from sqlalchemy.orm import Session
import models, schemas

def get_detections(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Detection).offset(skip).limit(limit).all()

def create_detection(db: Session, detection: schemas.ObjectDetectionCreate):
    db_detection = models.Detection(**detection.dict())
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    return db_detection
