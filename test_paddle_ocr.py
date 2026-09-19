from pathlib import Path

from app.integrations.paddle_ocr import PaddleOCR


image_path = Path("app/data/test.png")

document_bytes = image_path.read_bytes()

ocr = PaddleOCR()

# response = ocr.submit_document(
#     document_bytes,
#     image_path.name
# )

# print(response)

status_response = ocr.get_job_status('94709901829120000')
print(status_response)

# res = ocr.get_result("https://paddleocr-store-4.bj.bcebos.com/v1/job/fc0a151ce7673b2bb3c1dd6d1dcebaa8314ce3d1983e9d80db2d1d1e52eabbff/json/e9106f40afad0077ca8ca6978e167b55.json?authorization=bce-auth-v1%2FALTAKDN8mY5KlNI7zaRpLmOqrw%2F2026-09-16T22%3A02%3A24Z%2F604800%2F%2Fa8f8f2bae08a4618e18651b0cc79d021168752f04a185ee3b592232908af0cc7")
# text = ocr.extract_text(res)

# print(text)