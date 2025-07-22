import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QDialog, QHBoxLayout, QMessageBox, QProgressBar, QMenu, QMenuBar, QComboBox, QSpinBox, QFormLayout, QDialogButtonBox
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt, QPoint
from PIL import Image
from pdf2image import convert_from_path
import os

class SettingsDialog(QDialog):
    def __init__(self, dpi, page_size, img_quality, parent=None):
        super().__init__(parent)
        self.setWindowTitle("설정")
        layout = QFormLayout()
        # DPI 설정
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(50, 600)
        self.dpi_spin.setValue(dpi)
        layout.addRow("PDF 해상도(DPI)", self.dpi_spin)
        # 페이지 크기 설정
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["A4", "Letter"])
        self.page_size_combo.setCurrentText(page_size)
        layout.addRow("페이지 크기", self.page_size_combo)
        # 이미지 품질 설정
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(img_quality)
        layout.addRow("이미지 품질(JPEG)", self.quality_spin)
        # 버튼
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)
    def get_values(self):
        return self.dpi_spin.value(), self.page_size_combo.currentText(), self.quality_spin.value()

class PreviewDialog(QDialog):
    def __init__(self, pixmap, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(400, 400)
        layout = QVBoxLayout()
        label = QLabel()
        label.setPixmap(pixmap.scaled(600, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("이미지+PDF to PDF 변환기")
        self.setGeometry(100, 100, 900, 600)

        # 설정값
        self.pdf_dpi = 200
        self.page_size = "A4"
        self.img_quality = 90

        # 메뉴바
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("설정")
        settings_action = settings_menu.addAction("옵션...")
        settings_action.triggered.connect(self.open_settings)

        # 파일 추가 버튼
        self.add_btn = QPushButton("파일 추가")
        self.add_btn.clicked.connect(self.add_files)

        # 썸네일 리스트
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setIconSize(QSize(100, 140))
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        self.list_widget.itemDoubleClicked.connect(self.preview_item)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

        # PDF 변환 버튼
        self.convert_btn = QPushButton("PDF 변환 시작")
        self.convert_btn.clicked.connect(self.convert_to_pdf)

        # 진행률 바
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        # 레이아웃
        layout = QVBoxLayout()
        layout.addWidget(self.add_btn)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.convert_btn)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_settings(self):
        dlg = SettingsDialog(self.pdf_dpi, self.page_size, self.img_quality, self)
        if dlg.exec_() == QDialog.Accepted:
            self.pdf_dpi, self.page_size, self.img_quality = dlg.get_values()

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "파일 선택", "", "이미지/PDF (*.jpg *.jpeg *.png *.pdf)")
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in [".jpg", ".jpeg", ".png"]:
                # 이미지 파일 썸네일 생성
                try:
                    img = Image.open(file)
                    img.thumbnail((100, 140))
                    thumb_path = file + "_thumb.png"
                    img.save(thumb_path)
                    icon = QIcon(thumb_path)
                    item = QListWidgetItem(icon, os.path.basename(file))
                    # 데이터: (파일경로, None)
                    item.setData(Qt.UserRole, (file, None))
                    self.list_widget.addItem(item)
                    os.remove(thumb_path)
                except Exception as e:
                    item = QListWidgetItem(f"[이미지 오류] {os.path.basename(file)}")
                    self.list_widget.addItem(item)
            elif ext == ".pdf":
                # PDF 모든 페이지 썸네일 생성
                try:
                    pages = convert_from_path(file, dpi=70)
                    for i, page in enumerate(pages):
                        page.thumbnail((100, 140))
                        thumb_path = f"{file}_thumb_{i+1}.png"
                        page.save(thumb_path)
                        icon = QIcon(thumb_path)
                        item = QListWidgetItem(icon, f"{os.path.basename(file)} ({i+1}p)")
                        # 데이터: (파일경로, 페이지번호)
                        item.setData(Qt.UserRole, (file, i+1))
                        self.list_widget.addItem(item)
                        os.remove(thumb_path)
                except Exception as e:
                    item = QListWidgetItem(f"[PDF 오류] {os.path.basename(file)}")
                    self.list_widget.addItem(item)
            else:
                item = QListWidgetItem(f"[지원 안함] {os.path.basename(file)}")
                self.list_widget.addItem(item)

    def preview_item(self, item):
        data = item.data(Qt.UserRole)
        if data is None:
            QMessageBox.warning(self, "미리보기 오류", "미리볼 수 없는 항목입니다.")
            return
        file, page = data
        ext = os.path.splitext(file)[1].lower()
        try:
            if ext in [".jpg", ".jpeg", ".png"]:
                pixmap = QPixmap(file)
                dlg = PreviewDialog(pixmap, os.path.basename(file), self)
                dlg.exec_()
            elif ext == ".pdf" and page is not None:
                # 해당 페이지 이미지를 다시 생성
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
                    QMessageBox.warning(self, "미리보기 오류", "PDF 페이지를 미리볼 수 없습니다.")
            else:
                QMessageBox.warning(self, "미리보기 오류", "미리볼 수 없는 항목입니다.")
        except Exception as e:
            QMessageBox.warning(self, "미리보기 오류", str(e))

    def show_context_menu(self, pos: QPoint):
        item = self.list_widget.itemAt(pos)
        if item is None:
            return
        menu = QMenu(self)
        preview_action = menu.addAction("미리보기")
        delete_action = menu.addAction("삭제")
        action = menu.exec_(self.list_widget.mapToGlobal(pos))
        if action == preview_action:
            self.preview_item(item)
        elif action == delete_action:
            row = self.list_widget.row(item)
            self.list_widget.takeItem(row)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            selected = self.list_widget.selectedItems()
            for item in selected:
                row = self.list_widget.row(item)
                self.list_widget.takeItem(row)
        else:
            super().keyPressEvent(event)

    def convert_to_pdf(self):
        if self.list_widget.count() == 0:
            QMessageBox.warning(self, "PDF 변환", "변환할 파일이 없습니다.")
            return
        save_path, _ = QFileDialog.getSaveFileName(self, "PDF 저장 위치", "output.pdf", "PDF Files (*.pdf)")
        if not save_path:
            return
        images = []
        temp_files = []
        total = self.list_widget.count()
        self.progress_bar.setValue(0)
        try:
            for idx in range(total):
                item = self.list_widget.item(idx)
                data = item.data(Qt.UserRole)
                if data is None:
                    continue
                file, page = data
                ext = os.path.splitext(file)[1].lower()
                if ext in [".jpg", ".jpeg", ".png"]:
                    img = Image.open(file).convert("RGB")
                    img = self.resize_to_page(img)
                    images.append(img)
                elif ext == ".pdf" and page is not None:
                    pages = convert_from_path(file, first_page=page, last_page=page, dpi=self.pdf_dpi)
                    if pages:
                        img = pages[0].convert("RGB")
                        img = self.resize_to_page(img)
                        temp_path = f"{file}_convert_{page}.jpg"
                        img.save(temp_path, quality=self.img_quality)
                        images.append(Image.open(temp_path).convert("RGB"))
                        temp_files.append(temp_path)
                self.progress_bar.setValue(int((idx + 1) / total * 100))
                QApplication.processEvents()
            if not images:
                QMessageBox.warning(self, "PDF 변환", "변환할 이미지가 없습니다.")
                self.progress_bar.setValue(0)
                return
            images[0].save(save_path, save_all=True, append_images=images[1:], quality=self.img_quality)
            QMessageBox.information(self, "PDF 변환", f"PDF 저장 완료: {save_path}")
            self.progress_bar.setValue(100)
        except Exception as e:
            QMessageBox.warning(self, "PDF 변환 오류", str(e))
            self.progress_bar.setValue(0)
        finally:
            for f in temp_files:
                if os.path.exists(f):
                    os.remove(f)

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