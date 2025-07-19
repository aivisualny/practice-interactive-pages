import os
import glob
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import threading
import sys

class ImageToPdfConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("이미지 to PDF 변환기")
        self.root.geometry("600x460")
        self.root.resizable(True, True)
        
        # 변수들
        self.input_folder = tk.StringVar()
        self.output_file = tk.StringVar()
        self.page_size = tk.StringVar(value="A4")
        self.image_ext = tk.StringVar(value="png")
        self.progress_var = tk.DoubleVar()
        self.cancel_flag = threading.Event()
        self.thread = None
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        ttk.Label(main_frame, text="이미지 폴더 선택:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable=self.input_folder, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="폴더 찾기", command=self.browse_input_folder).grid(row=0, column=2, pady=5)
        ttk.Label(main_frame, text="출력 PDF 파일:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable=self.output_file, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="파일 저장", command=self.browse_output_file).grid(row=1, column=2, pady=5)
        ttk.Label(main_frame, text="페이지 크기:").grid(row=2, column=0, sticky="w", pady=5)
        size_frame = ttk.Frame(main_frame)
        size_frame.grid(row=2, column=1, sticky="w", pady=5)
        ttk.Radiobutton(size_frame, text="A4", variable=self.page_size, value="A4").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(size_frame, text="Letter", variable=self.page_size, value="letter").pack(side=tk.LEFT, padx=10)
        ttk.Label(main_frame, text="이미지 확장자:").grid(row=3, column=0, sticky="w", pady=5)
        ext_frame = ttk.Frame(main_frame)
        ext_frame.grid(row=3, column=1, sticky="w", pady=5)
        ttk.Radiobutton(ext_frame, text="JPG/JPEG", variable=self.image_ext, value="jpg").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(ext_frame, text="PNG", variable=self.image_ext, value="png").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(ext_frame, text="기타", variable=self.image_ext, value="etc").pack(side=tk.LEFT, padx=10)
        self.etc_entry = ttk.Entry(ext_frame, width=8)
        self.etc_entry.pack(side=tk.LEFT, padx=5)
        self.etc_entry.insert(0, "bmp")
        self.etc_entry.config(state='disabled')
        def on_ext_change(*args):
            if self.image_ext.get() == 'etc':
                self.etc_entry.config(state='normal')
            else:
                self.etc_entry.config(state='disabled')
        self.image_ext.trace_add('write', on_ext_change)
        ttk.Label(main_frame, text="진행률:").grid(row=4, column=0, sticky="w", pady=5)
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        self.status_label = ttk.Label(main_frame, text="폴더를 선택하고 변환 버튼을 클릭하세요.")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=10)
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=3, pady=10)
        self.convert_button = ttk.Button(btn_frame, text="PDF 변환 시작", command=self.start_conversion)
        self.convert_button.pack(side=tk.LEFT, padx=10)
        self.cancel_button = ttk.Button(btn_frame, text="중간 취소", command=self.cancel_conversion, state='disabled')
        self.cancel_button.pack(side=tk.LEFT, padx=10)
        log_frame = ttk.LabelFrame(main_frame, text="처리 로그", padding="5")
        log_frame.grid(row=7, column=0, columnspan=3, sticky="nsew", pady=10)
        self.log_text = tk.Text(log_frame, height=8, width=70)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    def browse_input_folder(self):
        folder = filedialog.askdirectory(title="이미지가 있는 폴더를 선택하세요")
        if folder:
            self.input_folder.set(folder)
            folder_name = os.path.basename(folder)
            # 기본 저장 경로를 Downloads로 고정
            downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
            self.output_file.set(os.path.join(downloads, f"{folder_name}_images.pdf"))
            self.log_message(f"입력 폴더 선택: {folder}")
    def browse_output_file(self):
        downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
        file = filedialog.asksaveasfilename(
            title="PDF 파일 저장 위치 선택",
            defaultextension=".pdf",
            initialdir=downloads,
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file:
            self.output_file.set(file)
            self.log_message(f"출력 파일 선택: {file}")
    def log_message(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    def start_conversion(self):
        if not self.input_folder.get():
            messagebox.showerror("오류", "입력 폴더를 선택해주세요.")
            return
        if not self.output_file.get():
            messagebox.showerror("오류", "출력 파일명을 지정해주세요.")
            return
        ext = self.image_ext.get()
        if ext == 'etc':
            ext = self.etc_entry.get().strip()
            if not ext:
                messagebox.showerror("오류", "기타 확장자를 입력해주세요.")
                return
        self.convert_button.config(state='disabled')
        self.cancel_button.config(state='normal')
        self.progress_var.set(0)
        self.cancel_flag.clear()
        self.thread = threading.Thread(target=self.convert_images_to_pdf_pil, args=(ext,))
        self.thread.daemon = True
        self.thread.start()
    def cancel_conversion(self):
        self.cancel_flag.set()
        self.status_label.config(text="변환 취소 중...")
        self.log_message("변환 취소 요청됨.")
    def convert_images_to_pdf_pil(self, ext):
        try:
            input_folder = self.input_folder.get()
            output_pdf = self.output_file.get()
            ext = ext.lower()
            if ext == 'jpg' or ext == 'jpeg':
                image_extensions = ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']
            elif ext == 'png':
                image_extensions = ['*.png', '*.PNG']
            else:
                image_extensions = [f'*.{ext}', f'*.{ext.upper()}']
            image_files = []
            for e in image_extensions:
                image_files.extend(glob.glob(os.path.join(input_folder, e)))
            image_files.sort()
            # 중복 파일 체크 및 제거
            unique_files = list(dict.fromkeys(image_files))
            if len(unique_files) != len(image_files):
                self.log_message(f"중복 파일 발견! 전체: {len(image_files)}, 고유: {len(unique_files)}. 중복을 제거합니다.")
                image_files = unique_files
            else:
                self.log_message(f"중복 없음! 전체: {len(image_files)}, 고유: {len(unique_files)}")
            if not image_files:
                self.log_message(f"'{input_folder}' 폴더에서 이미지 파일을 찾을 수 없습니다.")
                self.cancel_button.config(state='disabled')
                self.convert_button.config(state='normal')
                return
            self.log_message(f"최종 변환 대상 이미지 개수: {len(image_files)}")
            images = []
            for i, file in enumerate(image_files):
                if self.cancel_flag.is_set():
                    self.status_label.config(text="변환이 취소되었습니다.")
                    self.log_message("변환이 중단되었습니다.")
                    self.cancel_button.config(state='disabled')
                    self.convert_button.config(state='normal')
                    return
                img = Image.open(file)
                if img.mode in ('RGBA', 'LA'):
                    bg = Image.new('RGB', img.size, (255, 255, 255))
                    bg.paste(img, mask=img.split()[-1])
                    img = bg
                else:
                    img = img.convert('RGB')
                images.append(img)
                self.log_message(f"이미지 추가: {os.path.basename(file)} ({i+1}/{len(image_files)})")
                progress = (i + 1) / len(image_files) * 100
                self.progress_var.set(progress)
                self.status_label.config(text=f"처리 중: {os.path.basename(file)} ({i+1}/{len(image_files)})")
                self.log_message(f"처리 중: {os.path.basename(file)} ({i+1}/{len(image_files)})")
            # images 리스트 중복 체크
            self.log_message(f"PDF에 저장될 이미지 개수: {len(images)}")
            if not self.cancel_flag.is_set():
                images[0].save(output_pdf, save_all=True, append_images=images[1:])
                self.log_message(f"\nPDF 생성 완료: {output_pdf}")
                self.log_message(f"총 {len(image_files)}개의 이미지가 포함되었습니다.")
                self.status_label.config(text="변환 완료!")
                messagebox.showinfo("완료", f"PDF 변환이 완료되었습니다!\n파일: {output_pdf}\n총 {len(image_files)}개의 이미지가 포함되었습니다.")
        except Exception as e:
            self.log_message(f"오류 발생: {str(e)}")
            messagebox.showerror("오류", f"변환 중 오류가 발생했습니다:\n{str(e)}")
        finally:
            self.cancel_button.config(state='disabled')
            self.convert_button.config(state='normal')

def main():
    root = tk.Tk()
    app = ImageToPdfConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main() 