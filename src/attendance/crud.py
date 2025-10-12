from typing import Optional
from sqlalchemy.orm import Session

from src.attendance.models import Attendance
from src.attendance.schemas import AttendanceBaseSchema, AttendanceUpdateSchema

from utils.crud.base import CRUDBase

class AttendanceCRUD(CRUDBase[Attendance, AttendanceBaseSchema, AttendanceUpdateSchema]):
    def get_by_user_and_qr_id(self, db: Session, student_id: str, qr_code_id: str) -> Optional[Attendance]:
        return (
            db.query(self.model)
            .filter(self.model.student_id == student_id, self.model.qr_code_id == qr_code_id)
            .first()
        )

attendance_crud = AttendanceCRUD(Attendance)