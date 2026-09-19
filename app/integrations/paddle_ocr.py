import requests;

from app.config.settings import PADDLEOCR_ACCESS_TOKEN


class PaddleOCR:

    def __init__(self):
        self.url = "https://paddleocr.aistudio-app.com/api/v2/ocr/jobs"
        self.headers = {
            "Authorization": f"Bearer {PADDLEOCR_ACCESS_TOKEN}"
        }

    def submit_document(self, document_bytes: bytes, filename: str):

        files = {
            "file": (filename, document_bytes)
        }

        data = {
            "model": "PP-OCRv5"
        }

        response = requests.post(
            self.url,
            headers=self.headers,
            files=files,
            data=data
        )

        return response.json()

    def get_job_status(self, job_id: str):

        url = f"{self.url}/{job_id}"

        response = requests.get(
            url,
            headers=self.headers
        )

        return response.json()

    def get_result(self, result_url: str):

        response = requests.get(result_url)

        return response.json()
    

    def extract_text(self, result: dict):

        ocr_results = result["result"]["ocrResults"]

        text = []

        for ocr_result in ocr_results:
            rec_texts = ocr_result["prunedResult"]["rec_texts"]
            text.extend(rec_texts)

        return "\n".join(text)