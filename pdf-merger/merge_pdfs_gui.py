import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger

# 다운로드 폴더 경로 (Windows 기준)
def get_downloads_folder():
    return str(Path.home() / "Downloads")

def merge_pdfs_in_folder(folder_path, output_path):
    pdf_files = []
    for entry in os.scandir(folder_path):
        if entry.is_file() and entry.name.lower().endswith(".pdf"):
            pdf_files.append((entry.stat().st_ctime, entry.path))
    if not pdf_files:
        return False, "PDF 파일이 없습니다."
    pdf_files.sort()
    merger = PdfMerger()
    for _, pdf_path in pdf_files:
        merger.append(pdf_path)
    merger.write(output_path)
    merger.close()
    return True, f"병합 완료! 결과: {output_path}"

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 병합기 (GUI)")
        self.folder_path = tk.StringVar()
        self.status = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="PDF 폴더 선택:").pack(pady=5)
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Entry(frame, textvariable=self.folder_path, width=40).pack(side=tk.LEFT)
        tk.Button(frame, text="찾아보기", command=self.browse_folder).pack(side=tk.LEFT, padx=5)
        tk.Button(self.root, text="PDF 병합", command=self.merge_pdfs).pack(pady=10)
        tk.Label(self.root, textvariable=self.status, fg="blue").pack(pady=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def merge_pdfs(self):
        folder = self.folder_path.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("오류", "유효한 폴더를 선택하세요.")
            return
        downloads = get_downloads_folder()
        output_pdf = os.path.join(downloads, "merged.pdf")
        self.status.set("병합 중...")
        self.root.update()
        ok, msg = merge_pdfs_in_folder(folder, output_pdf)
        self.status.set(msg)
        if ok:
            messagebox.showinfo("완료", msg)
        else:
            messagebox.showerror("실패", msg)

def main():
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 