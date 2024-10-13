from pydantic import BaseModel

class DetectionBase(BaseModel):
    image_name: str
    object_class: str
    confidence: float
    x_min: float
    y_min: float
    x_max: float
    y_max: float

class DetectionCreate(DetectionBase):
    pass

class Detection(DetectionBase):
    id: int

    class Config:
        orm_mode = True
