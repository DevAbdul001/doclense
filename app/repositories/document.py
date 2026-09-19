from sqlalchemy.orm import Session;
from app.models.document import Document, OCRStatus;

class DocumentRepository:

    def get_by_id(self, db: Session, document_id: int):
        return db.query(Document).filter(Document.id == document_id).first();

    def create(self, db: Session, document: Document):
        db.add(document);
        db.commit();
        db.refresh(document);

        return document;
    
    def update(self, db: Session, document_id: int, ocr_status: OCRStatus):
        doc = db.query(Document).filter(Document.id == document_id).first();

        if doc is None:
            return;

        doc.ocr_status = ocr_status;

        db.commit();
        db.refresh(doc);

        return doc;

    def get_all(self, db: Session):
        documents = db.query(Document).all();

        return documents;

    def delete(self, db: Session, document_id: int):
        doc = db.query(Document).filter(Document.id == document_id).first();

        if doc is None:
            return;

        deleted_id = doc.id;

        db.delete(doc);
        db.commit();

        return deleted_id;
