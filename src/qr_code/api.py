import json
import qrcode
import logging

from typing import List
from io import BytesIO
from fastapi import APIRouter, status, HTTPException
from datetime import datetime, timedelta
from fastapi.responses import StreamingResponse

from src.user.models import UserRoles
from src.user.utils.deps import is_authorized_for
from src.qr_code.crud import qr_code_crud
from src.qr_code.schema import QrCodeBaseSchema, QrCodeRequestSchema, QrCodeUpdateSchema

qr_code = APIRouter()

@qr_code.post("/generate/qr_code", status_code=status.HTTP_201_CREATED)
async def register_student_by_csv(
    request: QrCodeRequestSchema, user_db: is_authorized_for([UserRoles.ADMIN.value, UserRoles.SUPER_ADMIN.value])
):
    try:
        user, db = user_db
        # Current and end times
        start_time = datetime.now()
        end_time = request.expiry_time

        # Data to encode inside the QR
        data = {
            "name": request.name,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "regenerate_interval_seconds": int(request.regenerate_interval_seconds),
        }

        qr_code = qr_code_crud.create(db=db, obj_in=QrCodeBaseSchema(
                name=request.name,
                qr_code_data=data,
                expiry_time=end_time,
                regenerate_interval_seconds=int(request.regenerate_interval_seconds),
                created_by=user.id,
                updated_by=user.id
            )
        )

        data["qr_code_id"] = qr_code.id

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(json.dumps(data, separators=(",", ":")))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save image in memory
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        # Return as image
        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        logging.exception("===REASON===: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong"
        )

@qr_code.get("/qr_code", response_model=List[QrCodeBaseSchema],status_code=status.HTTP_200_OK)
async def retrieve_students(user_db: is_authorized_for([UserRoles.ADMIN.value, UserRoles.SUPER_ADMIN.value])):
    try:
        user, db = user_db

        students = qr_code_crud.get_multi(db)
        
        return students
    except Exception as e:
        logging.exception("===REASON===: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong"
        )

@qr_code.get("/qr_code/{id}", response_model=QrCodeBaseSchema,status_code=status.HTTP_200_OK)
async def retrieve_students(id: str, user_db: is_authorized_for([UserRoles.ADMIN.value, UserRoles.SUPER_ADMIN.value])):
    try:
        user, db = user_db

        students = qr_code_crud.get(db, id)

        return students
    except Exception as e:
        logging.exception("===REASON===: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong"
        )