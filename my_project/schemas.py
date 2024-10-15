from pydantic import BaseModel

class TelegramDataBase(BaseModel):
    channel_name: str
    message_text: str
    timestamp: str

class TelegramDataCreate(TelegramDataBase):
    pass

class TelegramData(TelegramDataBase):
    id: int

    class Config:
        from_attributes = True 

class ObjectDetectionBase(BaseModel):
    image_name: str
    class_name: str
    confidence: float
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    source: str

class ObjectDetectionCreate(ObjectDetectionBase):
    pass

class ObjectDetection(ObjectDetectionBase):
    id: int

    class Config:
        from_attributes = True  