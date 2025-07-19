import os
import sys
from pathlib import Path
from PyPDF2 import PdfMerger

# 다운로드 폴더 경로 (Windows 기준)
def get_downloads_folder():
    return str(Path.home() / "Downloads")

# PDF 병합 함수
def merge_pdfs_in_folder(folder_path, output_path):
    pdf_files = []
    for entry in os.scandir(folder_path):
        if entry.is_file() and entry.name.lower().endswith(".pdf"):
            pdf_files.append((entry.stat().st_ctime, entry.path))
    if not pdf_files:
        print("PDF 파일이 없습니다.")
        return False
    # 생성된 시간 순서대로 정렬
    pdf_files.sort()
    merger = PdfMerger()
    for _, pdf_path in pdf_files:
        merger.append(pdf_path)
    merger.write(output_path)
    merger.close()
    return True

def main():
    print("PDF 병합기")
    folder = input("PDF 파일들이 들어있는 폴더 경로를 입력하세요 (엔터=현재폴더): ").strip()
    if not folder:
        folder = os.getcwd()
    if not os.path.isdir(folder):
        print("폴더가 존재하지 않습니다.")
        sys.exit(1)
    downloads = get_downloads_folder()
    output_pdf = os.path.join(downloads, "merged.pdf")
    ok = merge_pdfs_in_folder(folder, output_pdf)
    if ok:
        print(f"병합 완료! 결과: {output_pdf}")
    else:
        print("병합 실패.")

if __name__ == "__main__":
    main() 