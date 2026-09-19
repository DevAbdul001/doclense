from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, func
from app.database.base import Base;



class OCRStatus(Enum):
    PENDING = "PENDING";
    PROCESSING = "PROCESSING";
    COMPLETED = "COMPLETED";
    FAILED = "FAILED";

class Document(Base):
    __tablename__="documents";

    id = Column(Integer,primary_key=True);
    original_filename = Column(String(255), nullable=False);
    mime_type = Column(String(50), nullable=False);
    file_size_bytes = Column(Integer, nullable=False);
    ocr_status = Column(SQLEnum(OCRStatus), nullable=False);
    created_at = Column(DateTime, nullable=False, server_default=func.now())

