from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel

from utils.schemas.base import BaseSchema
from src.attendance.enums import AttendanceEnum

class AttendanceUpdateSchema(BaseModel):
    student_id: Optional[str] = None
    qr_code_id: Optional[str] = None
    attendance_time: Optional[datetime] = None
    status: Optional[AttendanceEnum] = None

class AttendanceBaseSchema(BaseSchema, AttendanceUpdateSchema):
    pass

class AttendanceRequestSchema(BaseModel):
    student_id: str
    qr_code_id: str
    status: Optional[AttendanceEnum] = None
