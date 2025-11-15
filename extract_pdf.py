#!/usr/bin/env python3
"""
PDF 텍스트 및 이미지 추출 스크립트
"""
import fitz  # PyMuPDF
import json
import os
from PIL import Image
import io

def extract_pdf_content(pdf_path):
    """PDF에서 텍스트, 이미지, 표 정보 추출"""

    doc = fitz.open(pdf_path)

    content = {
        'metadata': {
            'title': doc.metadata.get('title', ''),
            'author': doc.metadata.get('author', ''),
            'pages': len(doc)
        },
        'pages': []
    }

    # 이미지 저장 디렉토리 생성
    img_dir = 'extracted_images'
    os.makedirs(img_dir, exist_ok=True)

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_content = {
            'page_number': page_num + 1,
            'text': '',
            'images': [],
            'tables': []
        }

        # 텍스트 추출
        page_content['text'] = page.get_text()

        # 이미지 추출
        image_list = page.get_images()
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # 이미지 저장
            img_filename = f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
            img_path = os.path.join(img_dir, img_filename)

            with open(img_path, "wb") as img_file:
                img_file.write(image_bytes)

            page_content['images'].append({
                'filename': img_filename,
                'path': img_path,
                'width': base_image.get('width', 0),
                'height': base_image.get('height', 0)
            })

        content['pages'].append(page_content)

    doc.close()

    return content

if __name__ == '__main__':
    pdf_file = 'Weaviate-Context-Engineering-ebook.pdf'

    print(f"PDF 처리 시작: {pdf_file}")
    content = extract_pdf_content(pdf_file)

    # 결과를 JSON으로 저장
    with open('extracted_content.json', 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

    print(f"\n추출 완료:")
    print(f"- 총 페이지: {content['metadata']['pages']}")
    print(f"- 추출된 텍스트 저장: extracted_content.json")
    print(f"- 추출된 이미지: extracted_images/ 디렉토리")

    # 전체 텍스트를 별도 파일로 저장
    with open('extracted_text.txt', 'w', encoding='utf-8') as f:
        for page in content['pages']:
            f.write(f"\n{'='*80}\n")
            f.write(f"Page {page['page_number']}\n")
            f.write(f"{'='*80}\n\n")
            f.write(page['text'])
            f.write('\n\n')

    print(f"- 전체 텍스트 저장: extracted_text.txt")
