from fastapi import APIRouter, Depends, UploadFile;
from sqlalchemy.orm import Session;

from app.services.document import DocumentService;
from app.database.connection import get_db;

router = APIRouter();

def get_document_service():
    return DocumentService()

@router.post("/upload")
async def upload_document(
    file: UploadFile,
    db: Session = Depends(get_db),
    service: DocumentService = Depends(get_document_service)
):
    return await service.upload_document(file, db);

