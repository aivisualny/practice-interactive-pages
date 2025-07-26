import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QDialog, QHBoxLayout, QMessageBox, QProgressBar, QMenu, QMenuBar, QComboBox, QSpinBox, QFormLayout, QDialogButtonBox, QFrame, QGridLayout, QScrollArea
)
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QColor, QFont
from PyQt5.QtCore import QSize, Qt, QPoint, QTimer
from PIL import Image
from pdf2image import convert_from_path
import os

# 다국어 번역 딕셔너리
TRANSLATIONS = {
    "ko": {
        "window_title": "PDF 변환기",
        "settings": "설정",
        "options": "옵션...",
        "add_files": "파일 추가",
        "convert_pdf": "PDF 변환 시작",
        "preview": "미리보기",
        "delete": "삭제",
        "dpi": "PDF 해상도(DPI)",
        "page_size": "페이지 크기",
        "img_quality": "이미지 품질(JPEG)",
        "language": "언어",
        "select_files": "파일 선택",
        "save_pdf": "PDF 저장 위치",
        "preview_error": "미리보기 오류",
        "preview_error_msg": "미리볼 수 없는 항목입니다.",
        "pdf_error": "PDF 오류",
        "convert_error": "PDF 변환 오류",
        "convert_no_files": "변환할 파일이 없습니다.",
        "convert_no_images": "변환할 이미지가 없습니다.",
        "convert_success": "PDF 저장 완료",
        "pdf_page_error": "PDF 페이지를 미리볼 수 없습니다.",
        "unsupported": "지원 안함",
        "image_error": "이미지 오류",
        "file_select": "파일 선택",
        "file_types": "이미지/PDF (*.jpg *.jpeg *.png *.pdf)",
        "pdf_files": "PDF Files (*.pdf)",
        "korean": "한국어",
        "english": "English",
        "select_pages": "페이지 선택",
        "select_all": "전체 선택",
        "deselect_all": "전체 해제",
        "page_range": "페이지 범위",
        "apply": "적용",
        "cancel": "취소",
        "total_pages": "총 {0}페이지",
        "selected_pages": "선택된 페이지: {0}"
    },
    "en": {
        "window_title": "PDF Converter",
        "settings": "Settings",
        "options": "Options...",
        "add_files": "Add Files",
        "convert_pdf": "Convert to PDF",
        "preview": "Preview",
        "delete": "Delete",
        "dpi": "PDF Resolution (DPI)",
        "page_size": "Page Size",
        "img_quality": "Image Quality (JPEG)",
        "language": "Language",
        "select_files": "Select Files",
        "save_pdf": "Save PDF As",
        "preview_error": "Preview Error",
        "preview_error_msg": "Cannot preview this item.",
        "pdf_error": "PDF Error",
        "convert_error": "PDF Conversion Error",
        "convert_no_files": "No files to convert.",
        "convert_no_images": "No images to convert.",
        "convert_success": "PDF saved successfully",
        "pdf_page_error": "Cannot preview PDF page.",
        "unsupported": "Not Supported",
        "image_error": "Image Error",
        "file_select": "Select Files",
        "file_types": "Images/PDF (*.jpg *.jpeg *.png *.pdf)",
        "pdf_files": "PDF Files (*.pdf)",
        "korean": "한국어",
        "english": "English",
        "select_pages": "Select Pages",
        "select_all": "Select All",
        "deselect_all": "Deselect All",
        "page_range": "Page Range",
        "apply": "Apply",
        "cancel": "Cancel",
        "total_pages": "Total {0} pages",
        "selected_pages": "Selected pages: {0}"
    }
}

class ThumbnailWidget(QFrame):
    def __init__(self, icon, text, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(2)
        self.setMidLineWidth(1)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 3px solid #e0e0e0;
                border-radius: 16px;
                padding: 16px;
                margin: 8px;
            }
            QFrame:hover {
                border: 3px solid #2196F3;
                background-color: #f8f9fa;
                transform: scale(1.02);
            }
            QFrame:selected {
                border: 3px solid #1976D2;
                background-color: #E3F2FD;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 썸네일 이미지 - 크게 증가
        self.icon_label = QLabel()
        self.icon_label.setPixmap(icon.pixmap(QSize(280, 360)))  # 2배 크기로 증가
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.icon_label)
        
        # 파일명 - 더 큰 폰트
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setWordWrap(True)
        self.text_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: #212121;
                font-size: 16px;
                font-weight: 600;
                font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
                padding: 8px;
                line-height: 1.4;
            }
        """)
        layout.addWidget(self.text_label)
        
        self.setLayout(layout)
        self.setFixedSize(320, 440)  # 크기 증가
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent().select_thumbnail(self)
            # 클릭 시 바로 미리보기 표시
            self.parent().preview_thumbnail(self)
        elif event.button() == Qt.RightButton:
            self.parent().show_context_menu(event.globalPos(), self)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent().preview_thumbnail(self)
        super().mouseDoubleClickEvent(event)

class ThumbnailGrid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.thumbnails = []
        self.selected_thumbnails = []
        self.drag_start_pos = None
        self.dragged_thumbnail = None
        
        self.layout = QGridLayout()
        self.layout.setSpacing(20)  # 간격 증가
        self.layout.setContentsMargins(32, 32, 32, 32)  # 여백 증가
        self.setLayout(self.layout)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                border: none;
            }
        """)
        
        self.setAcceptDrops(True)

    def add_thumbnail(self, icon, text, data):
        thumbnail = ThumbnailWidget(icon, text, data, self)
        self.thumbnails.append(thumbnail)
        self.update_layout()
        return thumbnail

    def remove_thumbnail(self, thumbnail):
        if thumbnail in self.thumbnails:
            self.thumbnails.remove(thumbnail)
            thumbnail.deleteLater()
            self.update_layout()

    def update_layout(self):
        # 기존 위젯들 제거
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        
        # 새로운 레이아웃으로 배치 - 더 큰 썸네일에 맞게 조정
        cols = max(1, self.width() // 360)  # 썸네일 너비(320) + 간격(40)에 맞춤
        for i, thumbnail in enumerate(self.thumbnails):
            row = i // cols
            col = i % cols
            self.layout.addWidget(thumbnail, row, col)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        QTimer.singleShot(100, self.update_layout)

    def select_thumbnail(self, thumbnail):
        modifiers = QApplication.keyboardModifiers()
        if modifiers & Qt.ControlModifier:
            if thumbnail in self.selected_thumbnails:
                self.selected_thumbnails.remove(thumbnail)
                thumbnail.setStyleSheet(thumbnail.styleSheet().replace(":selected", ""))
            else:
                self.selected_thumbnails.append(thumbnail)
                thumbnail.setStyleSheet(thumbnail.styleSheet() + " QFrame:selected { border: 3px solid #1976D2; background-color: #E3F2FD; }")
        else:
            for t in self.selected_thumbnails:
                t.setStyleSheet(t.styleSheet().replace(":selected", ""))
            self.selected_thumbnails = [thumbnail]
            thumbnail.setStyleSheet(thumbnail.styleSheet() + " QFrame:selected { border: 3px solid #1976D2; background-color: #E3F2FD; }")

    def show_context_menu(self, pos, thumbnail):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                font-weight: 500;
                font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
            }
            QMenu::item {
                padding: 10px 20px;
                border-radius: 4px;
                color: #212121;
            }
            QMenu::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
        """)
        preview_action = menu.addAction(self.parent.tr("preview"))
        delete_action = menu.addAction(self.parent.tr("delete"))
        action = menu.exec_(pos)
        if action == preview_action:
            self.parent.preview_thumbnail(thumbnail)
        elif action == delete_action:
            self.remove_thumbnail(thumbnail)

    def preview_thumbnail(self, thumbnail):
        self.parent.preview_thumbnail(thumbnail)

    def get_thumbnail_data(self):
        return [t.data for t in self.thumbnails]

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.pos()
            self.dragged_thumbnail = self.childAt(event.pos())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragged_thumbnail and self.drag_start_pos:
            distance = (event.pos() - self.drag_start_pos).manhattanLength()
            if distance >= QApplication.startDragDistance():
                self.start_drag()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.drag_start_pos = None
        self.dragged_thumbnail = None
        super().mouseReleaseEvent(event)

    def start_drag(self):
        if isinstance(self.dragged_thumbnail, ThumbnailWidget):
            # 드래그 시작
            mime_data = self.dragged_thumbnail.data
            # 여기서 드래그 액션을 처리할 수 있습니다

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        # 드롭 위치 계산 및 썸네일 순서 변경
        drop_pos = event.pos()
        target_thumbnail = self.childAt(drop_pos)
        if isinstance(target_thumbnail, ThumbnailWidget) and self.dragged_thumbnail:
            # 썸네일 순서 변경 로직
            old_index = self.thumbnails.index(self.dragged_thumbnail)
            new_index = self.thumbnails.index(target_thumbnail)
            if old_index != new_index:
                self.thumbnails.pop(old_index)
                self.thumbnails.insert(new_index, self.dragged_thumbnail)
                self.update_layout()
        event.acceptProposedAction()

class SettingsDialog(QDialog):
    def __init__(self, dpi, page_size, img_quality, language, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.language = language
        self.setWindowTitle(self.tr("settings"))
        self.setStyleSheet("""
            QDialog {
                background-color: #fafafa;
                font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
            }
            QLabel {
                font-weight: 600;
                color: #212121;
                font-size: 14px;
                padding: 4px 0;
            }
            QSpinBox, QComboBox {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
                font-weight: 500;
                color: #212121;
                min-height: 20px;
            }
            QSpinBox:focus, QComboBox:focus {
                border-color: #2196F3;
                outline: none;
            }
            QPushButton {
                padding: 12px 24px;
                border: 2px solid #2196F3;
                border-radius: 8px;
                background-color: #2196F3;
                color: white;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #1976D2;
                border-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        layout = QFormLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # DPI 설정
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(50, 600)
        self.dpi_spin.setValue(dpi)
        layout.addRow(self.tr("dpi"), self.dpi_spin)
        
        # 페이지 크기 설정
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["A4", "Letter"])
        self.page_size_combo.setCurrentText(page_size)
        layout.addRow(self.tr("page_size"), self.page_size_combo)
        
        # 이미지 품질 설정
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(img_quality)
        layout.addRow(self.tr("img_quality"), self.quality_spin)
        
        # 언어 설정
        self.language_combo = QComboBox()
        self.language_combo.addItems([self.tr("korean"), self.tr("english")])
        self.language_combo.setCurrentText(self.tr("korean") if language == "ko" else self.tr("english"))
        layout.addRow(self.tr("language"), self.language_combo)
        
        # 버튼
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)
    
    def tr(self, key):
        return TRANSLATIONS[self.language].get(key, key)
    
    def get_values(self):
        lang = "ko" if self.language_combo.currentText() == self.tr("korean") else "en"
        return self.dpi_spin.value(), self.page_size_combo.currentText(), self.quality_spin.value(), lang

class PreviewDialog(QDialog):
    def __init__(self, pixmap, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(1200, 1400)  # 크기 증가
        self.resize(1400, 1600)  # 기본 크기 설정
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
            }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)  # 여백 증가
        
        # 제목 라벨 추가
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #212121;
                font-size: 20px;
                font-weight: 700;
                padding: 16px;
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                margin-bottom: 16px;
            }
        """)
        layout.addWidget(title_label)
        
        # 이미지 라벨
        label = QLabel()
        # 더 큰 크기로 스케일링
        scaled_pixmap = pixmap.scaled(1200, 1400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                background-color: white; 
                border: 3px solid #e0e0e0; 
                border-radius: 16px; 
                padding: 24px;
            }
        """)
        layout.addWidget(label)
        
        self.setLayout(layout)

class PageSelectionDialog(QDialog):
    def __init__(self, pdf_path, parent=None):
        super().__init__(parent)
        self.pdf_path = pdf_path
        self.parent = parent
        self.language = parent.language if parent else "ko"
        
        # PDF 페이지 수 확인
        try:
            from pdf2image import convert_from_path
            pages = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=70)
            self.total_pages = len(pages)
        except:
            self.total_pages = 1
        
        self.setWindowTitle(self.tr("select_pages"))
        self.setMinimumSize(600, 500)
        self.resize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
            }
            QLabel {
                font-weight: 600;
                color: #212121;
                font-size: 16px;
                padding: 8px 0;
            }
            QSpinBox, QComboBox {
                padding: 16px;
                border: 3px solid #e0e0e0;
                border-radius: 12px;
                background-color: white;
                font-size: 16px;
                font-weight: 500;
                color: #212121;
                min-height: 24px;
            }
            QSpinBox:focus, QComboBox:focus {
                border-color: #2196F3;
                outline: none;
            }
            QPushButton {
                padding: 16px 32px;
                border: 3px solid #2196F3;
                border-radius: 12px;
                background-color: #2196F3;
                color: white;
                font-weight: 700;
                font-size: 16px;
                min-height: 24px;
            }
            QPushButton:hover {
                background-color: #1976D2;
                border-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
            QCheckBox {
                font-size: 16px;
                font-weight: 500;
                color: #212121;
                spacing: 12px;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
                border: 3px solid #e0e0e0;
                border-radius: 6px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #2196F3;
                border-color: #2196F3;
            }
            QScrollArea {
                border: 3px solid #e0e0e0;
                border-radius: 12px;
                background-color: white;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(32, 32, 32, 32)

        # 파일명 표시
        filename_label = QLabel(f"파일: {os.path.basename(pdf_path)}")
        filename_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #1976D2;")
        layout.addWidget(filename_label)

        # 총 페이지 수 라벨
        total_pages_label = QLabel(self.tr("total_pages").format(self.total_pages))
        layout.addWidget(total_pages_label)

        # 페이지 선택 방식
        selection_layout = QHBoxLayout()
        
        # 전체 선택/해제 버튼
        button_layout = QVBoxLayout()
        select_all_btn = QPushButton(self.tr("select_all"))
        select_all_btn.clicked.connect(self.select_all_pages)
        button_layout.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton(self.tr("deselect_all"))
        deselect_all_btn.clicked.connect(self.deselect_all_pages)
        button_layout.addWidget(deselect_all_btn)
        
        selection_layout.addLayout(button_layout)
        
        # 페이지 체크박스 영역
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        self.checkbox_layout = QVBoxLayout()
        scroll_widget.setLayout(self.checkbox_layout)
        
        # 체크박스 생성
        self.page_checkboxes = []
        for i in range(1, self.total_pages + 1):
            checkbox = QCheckBox(f"페이지 {i}")
            checkbox.setChecked(True)  # 기본적으로 모든 페이지 선택
            self.page_checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox)
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        selection_layout.addWidget(scroll_area)
        
        layout.addLayout(selection_layout)

        # 버튼
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.apply_btn = QPushButton(self.tr("apply"))
        self.apply_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.apply_btn)
        self.cancel_btn = QPushButton(self.tr("cancel"))
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def tr(self, key):
        return TRANSLATIONS[self.language].get(key, key)

    def select_all_pages(self):
        for checkbox in self.page_checkboxes:
            checkbox.setChecked(True)

    def deselect_all_pages(self):
        for checkbox in self.page_checkboxes:
            checkbox.setChecked(False)

    def get_selected_pages(self):
        selected = []
        for i, checkbox in enumerate(self.page_checkboxes):
            if checkbox.isChecked():
                selected.append(i + 1)
        return selected

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = "ko"
        self.setWindowTitle(self.tr("window_title"))
        self.setGeometry(100, 100, 1600, 1000)  # 윈도우 크기 증가
        self.setMinimumSize(1200, 800)  # 최소 크기 증가

        # 설정값
        self.pdf_dpi = 200
        self.page_size = "A4"
        self.img_quality = 90

        # 스타일 설정
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
            }
            QPushButton {
                padding: 20px 40px;
                border: 3px solid #2196F3;
                border-radius: 12px;
                background-color: #2196F3;
                color: white;
                font-weight: 700;
                font-size: 18px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #1976D2;
                border-color: #1976D2;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
            QProgressBar {
                border: 3px solid #e0e0e0;
                border-radius: 12px;
                text-align: center;
                font-weight: 700;
                font-size: 16px;
                color: #212121;
                background-color: white;
                min-height: 30px;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 9px;
            }
        """)

        # 메뉴바
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #1976D2;
                color: white;
                font-weight: 700;
                font-size: 16px;
                font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
                padding: 12px;
            }
            QMenuBar::item {
                padding: 12px 20px;
                border-radius: 8px;
            }
            QMenuBar::item:selected {
                background-color: #1565C0;
            }
        """)
        settings_menu = menubar.addMenu(self.tr("settings"))
        settings_action = settings_menu.addAction(self.tr("options"))
        settings_action.triggered.connect(self.open_settings)

        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(32, 32, 32, 32)
        
        # 상단 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        self.add_btn = QPushButton(self.tr("add_files"))
        self.add_btn.clicked.connect(self.add_files)
        button_layout.addWidget(self.add_btn)
        
        button_layout.addStretch()
        
        self.convert_btn = QPushButton(self.tr("convert_pdf"))
        self.convert_btn.clicked.connect(self.convert_to_pdf)
        button_layout.addWidget(self.convert_btn)
        
        main_layout.addLayout(button_layout)
        
        # 썸네일 그리드 (스크롤 영역)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 3px solid #e0e0e0;
                border-radius: 16px;
                background-color: white;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 20px;
                border-radius: 10px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 10px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        
        self.thumbnail_grid = ThumbnailGrid(self)
        scroll_area.setWidget(self.thumbnail_grid)
        main_layout.addWidget(scroll_area)
        
        # 진행률 바
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        main_layout.addWidget(self.progress_bar)
        
        central_widget.setLayout(main_layout)

    def tr(self, key):
        return TRANSLATIONS[self.language].get(key, key)

    def update_ui_language(self):
        self.setWindowTitle(self.tr("window_title"))
        self.menuBar().actions()[0].setText(self.tr("settings"))
        self.menuBar().actions()[0].menu().actions()[0].setText(self.tr("options"))
        self.add_btn.setText(self.tr("add_files"))
        self.convert_btn.setText(self.tr("convert_pdf"))

    def open_settings(self):
        dlg = SettingsDialog(self.pdf_dpi, self.page_size, self.img_quality, self.language, self)
        if dlg.exec_() == QDialog.Accepted:
            self.pdf_dpi, self.page_size, self.img_quality, new_language = dlg.get_values()
            if new_language != self.language:
                self.language = new_language
                self.update_ui_language()

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, self.tr("select_files"), "", self.tr("file_types"))
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in [".jpg", ".jpeg", ".png"]:
                try:
                    img = Image.open(file)
                    img.thumbnail((280, 360))  # 썸네일 크기 증가
                    thumb_path = file + "_thumb.png"
                    img.save(thumb_path)
                    icon = QIcon(thumb_path)
                    self.thumbnail_grid.add_thumbnail(icon, os.path.basename(file), (file, None))
                    os.remove(thumb_path)
                except Exception as e:
                    pass
            elif ext == ".pdf":
                try:
                    # PDF 파일을 하나의 항목으로 처리
                    # 첫 번째 페이지만 썸네일로 사용
                    pages = convert_from_path(file, first_page=1, last_page=1, dpi=70)
                    if pages:
                        page = pages[0]
                        page.thumbnail((280, 360))  # 썸네일 크기 증가
                        thumb_path = f"{file}_thumb.png"
                        page.save(thumb_path)
                        icon = QIcon(thumb_path)
                        
                        # PDF 페이지 수 확인
                        try:
                            all_pages = convert_from_path(file, dpi=70)
                            page_count = len(all_pages)
                            display_name = f"{os.path.basename(file)} ({page_count}페이지)"
                        except:
                            display_name = f"{os.path.basename(file)}"
                        
                        self.thumbnail_grid.add_thumbnail(icon, display_name, (file, "pdf"))
                        os.remove(thumb_path)
                except Exception as e:
                    pass

    def preview_thumbnail(self, thumbnail):
        data = thumbnail.data
        if data is None:
            QMessageBox.warning(self, self.tr("preview_error"), self.tr("preview_error_msg"))
            return
        file, page = data
        ext = os.path.splitext(file)[1].lower()
        try:
            if ext in [".jpg", ".jpeg", ".png"]:
                pixmap = QPixmap(file)
                dlg = PreviewDialog(pixmap, os.path.basename(file), self)
                dlg.exec_()
            elif ext == ".pdf":
                if page == "pdf":
                    # PDF 파일인 경우 페이지 선택 창 표시
                    dlg = PageSelectionDialog(file, self)
                    if dlg.exec_() == QDialog.Accepted:
                        selected_pages = dlg.get_selected_pages()
                        if selected_pages:
                            # 선택된 첫 번째 페이지 미리보기
                            pages = convert_from_path(file, first_page=selected_pages[0], last_page=selected_pages[0], dpi=150)
                            if pages:
                                img = pages[0]
                                temp_path = f"{file}_preview_{selected_pages[0]}.png"
                                img.save(temp_path)
                                pixmap = QPixmap(temp_path)
                                dlg = PreviewDialog(pixmap, f"{os.path.basename(file)} (페이지 {selected_pages[0]})", self)
                                dlg.exec_()
                                os.remove(temp_path)
                elif page is not None:
                    # 개별 페이지 미리보기 (기존 방식)
                    pages = convert_from_path(file, first_page=page, last_page=page, dpi=150)
                    if pages:
                        img = pages[0]
                        temp_path = f"{file}_preview_{page}.png"
                        img.save(temp_path)
                        pixmap = QPixmap(temp_path)
                        dlg = PreviewDialog(pixmap, f"{os.path.basename(file)} ({page}p)", self)
                        dlg.exec_()
                        os.remove(temp_path)
                    else:
                        QMessageBox.warning(self, self.tr("preview_error"), self.tr("pdf_page_error"))
            else:
                QMessageBox.warning(self, self.tr("preview_error"), self.tr("preview_error_msg"))
        except Exception as e:
            QMessageBox.warning(self, self.tr("preview_error"), str(e))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for thumbnail in self.thumbnail_grid.selected_thumbnails[:]:
                self.thumbnail_grid.remove_thumbnail(thumbnail)
        else:
            super().keyPressEvent(event)

    def convert_to_pdf(self):
        thumbnails_data = self.thumbnail_grid.get_thumbnail_data()
        if not thumbnails_data:
            QMessageBox.warning(self, self.tr("convert_error"), self.tr("convert_no_files"))
            return

        # 변환할 이미지와 PDF 페이지들을 수집
        images = []
        temp_files = []
        total_items = 0
        
        # 먼저 총 아이템 수 계산
        for file, page in thumbnails_data:
            ext = os.path.splitext(file)[1].lower()
            if ext in [".jpg", ".jpeg", ".png"]:
                total_items += 1
            elif ext == ".pdf":
                if page == "pdf":
                    # PDF 파일인 경우 페이지 선택 창 표시
                    dlg = PageSelectionDialog(file, self)
                    if dlg.exec_() == QDialog.Accepted:
                        selected_pages = dlg.get_selected_pages()
                        total_items += len(selected_pages)
                        # 선택된 페이지들을 임시로 저장
                        temp_files.append((file, selected_pages))
                    else:
                        continue  # 취소된 경우 건너뛰기
                elif page is not None:
                    total_items += 1
        
        if total_items == 0:
            QMessageBox.warning(self, self.tr("convert_error"), self.tr("convert_no_images"))
            return

        save_path, _ = QFileDialog.getSaveFileName(self, self.tr("save_pdf"), "output.pdf", self.tr("pdf_files"))
        if not save_path:
            return

        self.progress_bar.setValue(0)
        current_item = 0
        
        try:
            for file, page in thumbnails_data:
                ext = os.path.splitext(file)[1].lower()
                if ext in [".jpg", ".jpeg", ".png"]:
                    # 이미지 파일 처리
                    img = Image.open(file).convert("RGB")
                    img = self.resize_to_page(img)
                    images.append(img)
                    current_item += 1
                    self.progress_bar.setValue(int(current_item / total_items * 100))
                    QApplication.processEvents()
                    
                elif ext == ".pdf":
                    if page == "pdf":
                        # PDF 파일에서 선택된 페이지들 처리
                        for temp_file, selected_pages in temp_files:
                            if temp_file == file:
                                for page_num in selected_pages:
                                    pages = convert_from_path(file, first_page=page_num, last_page=page_num, dpi=self.pdf_dpi)
                                    if pages:
                                        img = pages[0].convert("RGB")
                                        img = self.resize_to_page(img)
                                        images.append(img)
                                        current_item += 1
                                        self.progress_bar.setValue(int(current_item / total_items * 100))
                                        QApplication.processEvents()
                                break
                    elif page is not None:
                        # 개별 페이지 처리 (기존 방식)
                        pages = convert_from_path(file, first_page=page, last_page=page, dpi=self.pdf_dpi)
                        if pages:
                            img = pages[0].convert("RGB")
                            img = self.resize_to_page(img)
                            images.append(img)
                            current_item += 1
                            self.progress_bar.setValue(int(current_item / total_items * 100))
                            QApplication.processEvents()

            if not images:
                QMessageBox.warning(self, self.tr("convert_error"), self.tr("convert_no_images"))
                self.progress_bar.setValue(0)
                return

            # PDF 저장
            images[0].save(save_path, save_all=True, append_images=images[1:], quality=self.img_quality)
            QMessageBox.information(self, self.tr("convert_error"), f"{self.tr('convert_success')}: {save_path}")
            self.progress_bar.setValue(100)
            
        except Exception as e:
            QMessageBox.warning(self, self.tr("convert_error"), str(e))
            self.progress_bar.setValue(0)

    def resize_to_page(self, img):
        if self.page_size == "A4":
            width = int(210 / 25.4 * self.pdf_dpi)
            height = int(297 / 25.4 * self.pdf_dpi)
        elif self.page_size == "Letter":
            width = int(8.5 * self.pdf_dpi)
            height = int(11 * self.pdf_dpi)
        else:
            return img
        return img.resize((width, height), Image.LANCZOS)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 