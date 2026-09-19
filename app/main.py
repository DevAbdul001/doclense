from fastapi import FastAPI, Depends;
from app.database.connection import get_db;
from app.controller.document import router;
from sqlalchemy.orm import Session;
from sqlalchemy import text;

app = FastAPI(
        title = "Doclense",
        description ="OCR backend service",
        version = "1.0.0"
        );

app.include_router(router, prefix="/documents")

@app.get("/")
def test(db: Session = Depends(get_db)):
    test = db.execute(text("SELECT 1"));
    return {"result": test.scalar()};

