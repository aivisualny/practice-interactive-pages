import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import random
from datetime import datetime

class EnglishQuizGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("영어 단어 시험지 생성기")
        self.root.geometry("800x600")
        
        # 단어 데이터 저장
        self.words = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="영어 단어 시험지 생성기", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 입력 프레임
        input_frame = ttk.LabelFrame(main_frame, text="단어 입력", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 영어 단어 입력
        ttk.Label(input_frame, text="영어 단어:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.word_entry = ttk.Entry(input_frame, width=30)
        self.word_entry.grid(row=0, column=1, padx=(0, 10))
        
        # 뜻 입력
        ttk.Label(input_frame, text="한글 뜻:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.meaning_entry = ttk.Entry(input_frame, width=50)
        self.meaning_entry.grid(row=1, column=1, padx=(0, 10))
        
        # 추가 버튼
        add_btn = ttk.Button(input_frame, text="단어 추가", command=self.add_word)
        add_btn.grid(row=0, column=2, rowspan=2, padx=(10, 0))
        
        # 단어 목록 프레임
        list_frame = ttk.LabelFrame(main_frame, text="입력된 단어 목록", padding="10")
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 트리뷰 생성
        columns = ("영어 단어", "한글 뜻")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        # 컬럼 설정
        self.tree.heading("영어 단어", text="영어 단어")
        self.tree.heading("한글 뜻", text="한글 뜻")
        self.tree.column("영어 단어", width=200)
        self.tree.column("한글 뜻", width=400)
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        # 삭제 버튼
        delete_btn = ttk.Button(button_frame, text="선택된 단어 삭제", command=self.delete_word)
        delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 전체 삭제 버튼
        clear_btn = ttk.Button(button_frame, text="전체 삭제", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # PDF 생성 버튼
        generate_btn = ttk.Button(button_frame, text="PDF 생성", command=self.generate_pdf)
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 단어 섞기 버튼
        shuffle_btn = ttk.Button(button_frame, text="단어 섞기", command=self.shuffle_words)
        shuffle_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 단어 개수 표시
        self.count_label = ttk.Label(button_frame, text="총 0개 단어")
        self.count_label.pack(side=tk.RIGHT)
        
        # 그리드 가중치 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Enter 키 바인딩
        self.word_entry.bind('<Return>', lambda e: self.meaning_entry.focus())
        self.meaning_entry.bind('<Return>', lambda e: self.add_word())
        
    def add_word(self):
        word = self.word_entry.get().strip()
        meaning = self.meaning_entry.get().strip()
        
        if not word or not meaning:
            messagebox.showwarning("경고", "영어 단어와 뜻을 모두 입력해주세요.")
            return
            
        # 중복 확인
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == word:
                messagebox.showwarning("경고", "이미 존재하는 단어입니다.")
                return
        
        # 트리뷰에 추가
        self.tree.insert("", "end", values=(word, meaning))
        
        # 입력 필드 초기화
        self.word_entry.delete(0, tk.END)
        self.meaning_entry.delete(0, tk.END)
        self.word_entry.focus()
        
        # 개수 업데이트
        self.update_count()
        
    def delete_word(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("경고", "삭제할 단어를 선택해주세요.")
            return
            
        self.tree.delete(selected)
        self.update_count()
        
    def clear_all(self):
        if messagebox.askyesno("확인", "모든 단어를 삭제하시겠습니까?"):
            self.tree.delete(*self.tree.get_children())
            self.update_count()
            
    def update_count(self):
        count = len(self.tree.get_children())
        self.count_label.config(text=f"총 {count}개 단어")
        
    def shuffle_words(self):
        """단어 목록을 랜덤하게 섞습니다."""
        items = list(self.tree.get_children())
        if len(items) < 2:
            messagebox.showinfo("알림", "섞을 단어가 2개 이상 필요합니다.")
            return
            
        # 현재 단어들을 가져와서 섞기
        words = []
        for item in items:
            values = self.tree.item(item)['values']
            words.append((values[0], values[1]))
        
        # 단어들을 랜덤하게 섞기
        random.shuffle(words)
        
        # 트리뷰를 비우고 섞인 단어들을 다시 추가
        self.tree.delete(*self.tree.get_children())
        for word, meaning in words:
            self.tree.insert("", "end", values=(word, meaning))
            
        messagebox.showinfo("완료", "단어들이 섞였습니다!")
        
    def generate_pdf(self):
        words = []
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            words.append((values[0], values[1]))
            
        if not words:
            messagebox.showwarning("경고", "단어를 입력해주세요.")
            return
            
        # 저장 경로 선택
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="PDF 파일 저장"
        )
        
        if not file_path:
            return
            
        try:
            self.create_pdf(file_path, words)
            messagebox.showinfo("성공", f"PDF가 생성되었습니다.\n저장 위치: {file_path}")
        except Exception as e:
            messagebox.showerror("오류", f"PDF 생성 중 오류가 발생했습니다: {str(e)}")
            
    def create_pdf(self, file_path, words):
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        story = []
        
        # 한글 폰트 등록
        try:
            # Windows 기본 한글 폰트들 시도
            font_paths = [
                "C:/Windows/Fonts/malgun.ttf",  # 맑은 고딕
                "C:/Windows/Fonts/gulim.ttc",   # 굴림
                "C:/Windows/Fonts/batang.ttc",  # 바탕
                "C:/Windows/Fonts/dotum.ttc",   # 돋움
                "C:/Windows/Fonts/NanumGothic.ttf",  # 나눔고딕
                "C:/Windows/Fonts/NanumBarunGothic.ttf",  # 나눔바른고딕
            ]
            
            korean_font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('Korean', font_path))
                        korean_font = 'Korean'
                        print(f"한글 폰트 등록 성공: {font_path}")
                        break
                    except Exception as font_error:
                        print(f"폰트 등록 실패 {font_path}: {font_error}")
                        continue
            
            if korean_font is None:
                # 한글 폰트를 찾지 못한 경우 기본 폰트 사용
                korean_font = 'Helvetica'
                print("한글 폰트를 찾지 못해 기본 폰트를 사용합니다.")
                
        except Exception as e:
            print(f"폰트 등록 오류: {e}")
            korean_font = 'Helvetica'
        
        # 스타일 설정
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            alignment=1,  # 중앙 정렬
            fontName=korean_font
        )
        
        # === 시험지 페이지 (1-2페이지) ===
        # 제목 추가
        title = Paragraph("영어 단어 시험지", title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # 테이블 데이터 준비
        table_data = []
        
        # 헤더
        table_data.append(["영어 단어", "뜻", "영어 단어", "뜻"])
        
        # 단어들을 2열로 배치 (섞인 순서 그대로 사용)
        for i in range(0, len(words), 2):
            row = []
            row.append(words[i][0])  # 첫 번째 영어 단어
            row.append("")  # 첫 번째 뜻 공백
            if i + 1 < len(words):
                row.append(words[i + 1][0])  # 두 번째 영어 단어
                row.append("")  # 두 번째 뜻 공백
            else:
                row.append("")  # 빈 칸
                row.append("")  # 빈 칸
            table_data.append(row)
            
        # 테이블 생성
        table = Table(table_data, colWidths=[2*inch, 2*inch, 2*inch, 2*inch])
        
        # 테이블 스타일
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), korean_font),  # 헤더에도 한글 폰트 적용
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), korean_font),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        table.setStyle(style)
        
        story.append(table)
        
        # === 정답지 페이지 (3-4페이지) ===
        # 첫 번째 페이지 나누기 (시험지 끝)
        story.append(PageBreak())
        
        # 두 번째 페이지 나누기 (공백 페이지)
        story.append(PageBreak())
        
        # 정답지 제목
        answer_title = Paragraph("정답지", title_style)
        story.append(answer_title)
        story.append(Spacer(1, 20))
        
        # 정답 테이블 데이터 (시험지와 동일한 순서 사용)
        answer_data = []
        answer_data.append(["영어 단어", "뜻", "영어 단어", "뜻"])
        
        for i in range(0, len(words), 2):
            row = []
            row.append(words[i][0])  # 첫 번째 영어 단어
            row.append(words[i][1])  # 첫 번째 뜻
            if i + 1 < len(words):
                row.append(words[i + 1][0])  # 두 번째 영어 단어
                row.append(words[i + 1][1])  # 두 번째 뜻
            else:
                row.append("")  # 빈 칸
                row.append("")  # 빈 칸
            answer_data.append(row)
            
        # 정답 테이블 생성
        answer_table = Table(answer_data, colWidths=[2*inch, 2*inch, 2*inch, 2*inch])
        
        # 정답 테이블 스타일
        answer_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), korean_font),  # 헤더에도 한글 폰트 적용
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), korean_font),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        answer_table.setStyle(answer_style)
        
        story.append(answer_table)
        
        # PDF 생성
        doc.build(story)

def main():
    root = tk.Tk()
    app = EnglishQuizGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 