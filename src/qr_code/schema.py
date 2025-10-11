from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel

from utils.schemas.base import BaseSchema

class QrCodeUpdateSchema(BaseModel):
    name: Optional[str] = None
    qr_code_data: Optional[Dict] = None
    expiry_time: Optional[datetime] = None
    regenerate_interval_seconds: Optional[float] = None

class QrCodeBaseSchema(BaseSchema, QrCodeUpdateSchema):
    updated_by: str

class QrCodeRequestSchema(BaseModel):
    name: str
    expiry_time: datetime
    regenerate_interval_seconds: float