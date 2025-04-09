import time
from google.cloud import vision
from pdf2image import convert_from_path
import os

def detect_text_from_pdf(pdf_path, page_num=0):
    start_time = time.time()  # ⏱ 시작 시각

    client = vision.ImageAnnotatorClient()
    pages = convert_from_path(pdf_path)
    img_pil = pages[page_num]
    image_path = "temp_page.jpg"
    img_pil.save(image_path)

    with open(image_path, "rb") as img_file:
        content = img_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    print("=== 인식된 텍스트 ===")
    for text in texts:
        print(text.description)

    os.remove(image_path)

    if response.error.message:
        raise Exception(f"API 오류 발생: {response.error.message}")

    elapsed_time = time.time() - start_time  # ⏱ 경과 시간
    print(f"\n⏱ 총 실행 시간: {elapsed_time:.2f}초")

if __name__ == "__main__":
    detect_text_from_pdf("/mnt/c/Users/cheon/capstone/document_grading/data/insurance_1_class.pdf")
