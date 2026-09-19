from sqlalchemy.orm import Session;
from fastapi import UploadFile;
import asyncio;

from app.repositories.document import DocumentRepository;
from app.integrations.paddle_ocr import PaddleOCR;
from app.models.document import Document, OCRStatus;
from app.exceptions.document import DocumentCreationError, DocumentNotFoundError, DocumentStatusUpdateError, DocumentDeletionError, OcrError;

class DocumentService:

    def __init__(self):
        self.repository= DocumentRepository();
        self.ocr = PaddleOCR();

    def create_document(
            self,
            db: Session,
            filename: str,
            mime_type: str,
            file_size_bytes: int
            ):
        document = Document(
            original_filename=filename,
            mime_type=mime_type,
            file_size_bytes=file_size_bytes,
            ocr_status=OCRStatus.PENDING
        );
        try:
           return self.repository.create(db, document);
        except Exception as e:
            print(e); 
            raise DocumentCreationError("Failed to create document");

    def update_document(
            self,
            db: Session,
            document_id: int,
            ocr_status: OCRStatus
    ):
        document = self.repository.get_by_id(db, document_id);

        if document is None:
            raise DocumentNotFoundError("Document not found");

        try:
            return self.repository.update(db, document_id, ocr_status);
        except Exception as e:
            print(e);
            raise DocumentStatusUpdateError("Failed to update document");


    def get_all_documents(
            self, db: Session
    ):
       try:
            documents = self.repository.get_all(self, db)
            return documents;
       except Exception as e:
           print(e);

    def get_by_id(
            self, db: Session, document_id: int
    ):
        try:
            return self.repository.get_by_id(self, db, document_id)
        except Exception as e:
            print(e);


    def delete(
            self, db: Session, document_id: int
    ):
        exists = self.repository.get_by_id(self, db, document_id);

        if exists is None:
            raise DocumentNotFoundError("Document not found");

        try:
            deleted_id = self.repository.delete(self, db, document_id);
            if deleted_id is None:
                raise DocumentDeletionError("Failed to delete document");
        except Exception as e:
            print(e);

    async def upload_document(
            self, file: UploadFile, db: Session
    ):
        document_bytes = await file.read();
        size = len(document_bytes);
        mime_type = file.content_type;

        document = self.create_document(db, file.filename, mime_type, size);
        status = document.ocr_status;
        ocr_response = None;

        try:
            result = self.ocr.submit_document( document_bytes, file.filename);
            job_id = result["data"]["jobId"];

            self.update_document(db, document.id, OCRStatus.PROCESSING);
            status = OCRStatus.PROCESSING;

            while status == OCRStatus.PENDING or status == OCRStatus.PROCESSING:
                ocr_response = self.ocr.get_job_status(job_id);
                ocr_status = ocr_response["data"]["state"]
                

                if ocr_status == "done" :
                    status = OCRStatus.COMPLETED;
                    self.update_document(db, document.id, status)
                    break;

                elif ocr_status == "failed" :
                    status = OCRStatus.FAILED;
                    self.update_document(db, document.id, status);
                    print("Ocr status: failed")
                    raise OcrError("OCR error");
                else:
                    await  asyncio.sleep(2)

            ocr_result = self.ocr.get_result(
                ocr_response["data"]["resultUrl"]["jsonUrl"])
            text = self.ocr.extract_text(ocr_result);   

            return text;
        except OcrError:
            raise
        except Exception as e:
            print(e); 
            raise OcrError("OCR error");

        

        
            
        