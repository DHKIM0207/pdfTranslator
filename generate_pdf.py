#!/usr/bin/env python3
"""
번역된 내용으로 PDF 생성
"""
import json
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import glob

def create_korean_pdf():
    """번역된 내용으로 한국어 PDF 생성"""

    output_file = "Weaviate-Context-Engineering-ebook-Korean.pdf"

    # PDF 문서 생성
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    # 한글 폰트 등록
    try:
        pdfmetrics.registerFont(TTFont('NotoSansKR', 'NotoSansKR.ttf'))
        korean_font = 'NotoSansKR'
        print("✓ Noto Sans KR 폰트 로드 완료")
    except:
        korean_font = 'Helvetica'
        print("⚠ 한글 폰트 로드 실패, 기본 폰트 사용")

    # 스타일 설정
    styles = getSampleStyleSheet()

    # 한국어 지원을 위한 스타일
    korean_style = ParagraphStyle(
        'Korean',
        parent=styles['Normal'],
        fontName=korean_font,
        fontSize=10,
        leading=15,
        spaceAfter=10,
        alignment=TA_LEFT
    )

    title_style = ParagraphStyle(
        'KoreanTitle',
        parent=styles['Title'],
        fontName=korean_font,
        fontSize=20,
        leading=28,
        spaceAfter=20,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'KoreanHeading',
        parent=styles['Heading1'],
        fontName=korean_font,
        fontSize=14,
        leading=18,
        spaceAfter=12,
        spaceBefore=12
    )

    # Story (PDF 내용) 빌드
    story = []

    # 표지
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Context Engineering", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("컨텍스트 엔지니어링", title_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("모델에 어떤 정보가 전달되고<br/>어떻게 일관성을 유지하는지를 제어하는<br/>시스템 설계", korean_style))
    story.append(PageBreak())

    # 번역된 페이지들 추가
    translated_files = sorted(glob.glob('pages_translated/page_*.txt'))

    print(f"번역된 페이지 {len(translated_files)}개를 PDF에 추가합니다...")

    for i, filepath in enumerate(translated_files, 1):
        page_num = os.path.basename(filepath).replace('page_', '').replace('.txt', '')
        print(f"  페이지 {page_num} 처리 중...")

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 페이지 내용 추가
        if content.strip():
            # 간단한 단락 분할
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    # 특수 문자 이스케이프
                    para_clean = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    para_clean = para_clean.replace('\n', '<br/>')

                    try:
                        story.append(Paragraph(para_clean, korean_style))
                        story.append(Spacer(1, 0.2*inch))
                    except:
                        # 파라그래프 생성 실패 시 건너뛰기
                        pass

        # 페이지별로 이미지 추가
        image_pattern = f'extracted_images/page_{page_num}_img_*.png'
        images = glob.glob(image_pattern)

        for img_path in images[:3]:  # 페이지당 최대 3개 이미지
            try:
                img = Image(img_path, width=4*inch, height=3*inch, kind='proportional')
                story.append(img)
                story.append(Spacer(1, 0.2*inch))
            except:
                pass

        # 페이지 구분
        if i < len(translated_files):
            story.append(PageBreak())

    # PDF 빌드
    print("\nPDF 생성 중...")
    doc.build(story)

    print(f"\n✓ PDF 생성 완료: {output_file}")
    print(f"  - 파일 크기: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")

    return output_file

if __name__ == '__main__':
    create_korean_pdf()
