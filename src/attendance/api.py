import json
import qrcode

from io import BytesIO
from fastapi import APIRouter, status, HTTPException
from datetime import datetime, timedelta
from fastapi.responses import StreamingResponse

from src.user.models import UserRoles
from src.user.utils.deps import is_authorized_for
from src.attendance.crud import attendance_crud
from src.attendance.enums import AttendanceEnum
from src.attendance.schemas import AttendanceUpdateSchema, AttendanceBaseSchema, AttendanceRequestSchema

attendance_router = APIRouter()

@attendance_router.post("/attendance", status_code=status.HTTP_201_CREATED, response_model=AttendanceBaseSchema)
def create_attendance(request: AttendanceRequestSchema, user_db: is_authorized_for([UserRoles.STUDENT.value, UserRoles.SUPER_ADMIN.value])):
    try:
        user, db = user_db
        
        is_exist = attendance_crud.get_by_user_and_qr_id(db=db, student_id=request.student_id, qr_code_id=request.qr_code_id)
        if is_exist:
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="Already present")

        attendance = attendance_crud.create(db=db, obj_in=AttendanceBaseSchema(created_by=user.id, updated_by=user.id, status=AttendanceEnum.PRESENT.value, **request.model_dump(exclude_unset=True)))
        return attendance
    except HTTPException:
        raise
    except Exception as e:
        pass