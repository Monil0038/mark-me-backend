from src.qr_code.models import QRCode
from src.qr_code.schema import QrCodeBaseSchema, QrCodeUpdateSchema

from utils.crud.base import CRUDBase

class QrCodeCRUD(CRUDBase[QRCode, QrCodeBaseSchema, QrCodeUpdateSchema]):
    pass

qr_code_crud = QrCodeCRUD(QRCode)