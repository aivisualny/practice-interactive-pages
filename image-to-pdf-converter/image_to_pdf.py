import os
import glob
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import argparse

def convert_images_to_pdf(input_folder, output_pdf, page_size='A4', ext='jpg'):
    """
    지정된 폴더의 모든 이미지를 이름 오름차순으로 정렬하여 PDF로 변환합니다.
    Args:
        input_folder (str): 이미지가 있는 폴더 경로
        output_pdf (str): 출력 PDF 파일명
        page_size (str): 페이지 크기 ('A4' 또는 'letter')
        ext (str): 이미지 확장자 (jpg, png 등)
    """
    # 지원하는 이미지 확장자
    ext = ext.lower()
    if ext == 'jpg' or ext == 'jpeg':
        image_extensions = ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']
    elif ext == 'png':
        image_extensions = ['*.png', '*.PNG']
    else:
        image_extensions = [f'*.{ext}', f'*.{ext.upper()}']

    # 모든 이미지 파일 찾기
    image_files = []
    for e in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_folder, e)))
    image_files.sort()

    if not image_files:
        print(f"'{input_folder}' 폴더에서 이미지 파일을 찾을 수 없습니다.")
        return

    print(f"총 {len(image_files)}개의 이미지 파일을 찾았습니다.")

    # 페이지 크기 설정
    if page_size.upper() == 'A4':
        pagesize = A4
    else:
        pagesize = letter

    c = canvas.Canvas(output_pdf, pagesize=pagesize)
    width, height = pagesize

    for i, image_path in enumerate(image_files):
        try:
            img = Image.open(image_path)
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height
            margin = 50
            max_width = width - 2 * margin
            max_height = height - 2 * margin
            if aspect_ratio > 1:
                new_width = min(max_width, img_width)
                new_height = new_width / aspect_ratio
                if new_height > max_height:
                    new_height = max_height
                    new_width = new_height * aspect_ratio
            else:
                new_height = min(max_height, img_height)
                new_width = new_height * aspect_ratio
                if new_width > max_width:
                    new_width = max_width
                    new_height = new_width / aspect_ratio
            x = (width - new_width) / 2
            y = (height - new_height) / 2
            # PNG는 투명 배경이 있을 수 있으니 RGB로 변환
            if img.mode in ('RGBA', 'LA'):
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[-1])
                img = bg
                img.save('_temp_img_for_pdf.jpg', 'JPEG')
                c.drawImage('_temp_img_for_pdf.jpg', x, y, width=new_width, height=new_height)
                os.remove('_temp_img_for_pdf.jpg')
            else:
                c.drawImage(image_path, x, y, width=new_width, height=new_height)
            print(f"처리 중: {os.path.basename(image_path)} ({i+1}/{len(image_files)})")
            if i < len(image_files) - 1:
                c.showPage()
        except Exception as e:
            print(f"오류: {image_path} 처리 중 문제 발생 - {str(e)}")
            continue
    c.save()
    print(f"\nPDF 생성 완료: {output_pdf}")
    print(f"총 {len(image_files)}개의 이미지가 포함되었습니다.")

def main():
    parser = argparse.ArgumentParser(description='이미지들을 PDF로 변환합니다.')
    parser.add_argument('input_folder', help='이미지가 있는 폴더 경로')
    parser.add_argument('-o', '--output', default='output.pdf', help='출력 PDF 파일명 (기본값: output.pdf)')
    parser.add_argument('-s', '--size', choices=['A4', 'letter'], default='A4', help='페이지 크기 (기본값: A4)')
    parser.add_argument('-e', '--ext', default='jpg', help='이미지 확장자 (기본값: jpg, 예: png, jpeg 등)')
    args = parser.parse_args()
    if not os.path.exists(args.input_folder):
        print(f"오류: '{args.input_folder}' 폴더가 존재하지 않습니다.")
        return
    convert_images_to_pdf(args.input_folder, args.output, args.size, args.ext)

if __name__ == "__main__":
    main() 