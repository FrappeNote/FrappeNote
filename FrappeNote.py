import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel,
    QHBoxLayout, QMessageBox, QSizeGrip
)
from PyQt5.QtGui import QFont


class FrappeNoteApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FrappeNote")
        self.setGeometry(100, 100, 500, 300)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.unsaved_changes = False
        self.dragging = False
        self.always_on_top = False  # Track whether the window is always on top or not

        self.init_ui()

    def init_ui(self):
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Header
        self.header = QWidget(self)
        self.header.setFixedHeight(40)
        self.header.setStyleSheet("""
            background-color: #1e1e1e; border-top-left-radius: 10px; border-top-right-radius: 10px;
        """)
        self.header_layout = QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(5, 5, 5, 5)

        # Header Label
        self.header_label = QLabel("📒 FrappeNote", self.header)
        self.header_label.setStyleSheet("color: white; font-size: 14px;")
        self.header_label.setAlignment(Qt.AlignLeft)

        # Header Buttons
        self.minimize_button = self.create_header_button("➖", self.showMinimized)
        self.close_button = self.create_header_button("✖️", self.prompt_save_before_exit)

        self.header_layout.addWidget(self.header_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.minimize_button)
        self.header_layout.addWidget(self.close_button)

        # Word/Character Counter
        self.counter_widget = QWidget(self)
        self.counter_widget.setFixedHeight(30)
        self.counter_widget.setStyleSheet("background-color: #1e1e1e;")
        self.counter_layout = QHBoxLayout(self.counter_widget)
        self.counter_layout.setContentsMargins(10, 0, 10, 0)

        self.word_count_label = QLabel("Words: 0", self.counter_widget)
        self.word_count_label.setStyleSheet("color: white; font-size: 12px;")
        self.char_count_label = QLabel("Characters: 0", self.counter_widget)
        self.char_count_label.setStyleSheet("color: white; font-size: 12px;")

        self.counter_layout.addWidget(self.word_count_label)
        self.counter_layout.addStretch()
        self.counter_layout.addWidget(self.char_count_label)

        # Content Layout
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        self.sidebar = QWidget(self)
        self.sidebar.setFixedWidth(50)
        self.sidebar.setStyleSheet("""
            background-color: #1e1e1e;
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
        """)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(5, 10, 5, 10)
        self.sidebar_layout.setSpacing(10)

        # Sidebar Buttons
        self.clear_button = self.create_sidebar_button("🗑️", "Clear All Notes", self.clear_all_notes)
        self.open_button = self.create_sidebar_button("📂", "Open Note", self.open_note)
        self.save_button = self.create_sidebar_button("💾", "Save Note", self.save_note)
        self.about_button = self.create_sidebar_button("ℹ️", "About", self.about_app)
        self.always_on_top_button = self.create_sidebar_button("🔝", "Always On Top", self.toggle_always_on_top)

        self.sidebar_layout.addWidget(self.clear_button)
        self.sidebar_layout.addWidget(self.open_button)
        self.sidebar_layout.addWidget(self.save_button)
        self.sidebar_layout.addWidget(self.about_button)
        self.sidebar_layout.addWidget(self.always_on_top_button)
        self.sidebar_layout.addStretch()

        # Main Content Area
        self.content_area = QWidget(self)
        self.content_area.setStyleSheet("""
            background-color: #2d2d2d;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """)
        self.text_edit = QTextEdit(self.content_area)
        self.text_edit.setFont(QFont("Helvetica", 14))
        self.text_edit.setStyleSheet("""
            background-color: #1e1e1e;
            color: white;
            border-radius: 8px;
            padding: 10px;
        """)
        self.text_edit.textChanged.connect(self.update_word_char_count)

        # Resizable Corner Grip
        self.resizer = QSizeGrip(self.content_area)

        content_inner_layout = QVBoxLayout(self.content_area)
        content_inner_layout.addWidget(self.text_edit)

        self.content_layout.addWidget(self.sidebar)
        self.content_layout.addWidget(self.content_area)

        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.counter_widget)
        self.main_layout.addLayout(self.content_layout)

    def create_sidebar_button(self, text, tooltip, function):
        button = QPushButton(text, self.sidebar)
        button.setFixedSize(40, 40)
        button.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)
        button.clicked.connect(function)
        button.setToolTip(tooltip)
        return button

    def create_header_button(self, text, function):
        button = QPushButton(text, self.header)
        button.setFixedSize(30, 30)
        button.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)
        button.clicked.connect(function)
        return button

    def update_word_char_count(self):
        text = self.text_edit.toPlainText()
        words = len(text.split())
        chars = len(text)
        self.word_count_label.setText(f"Words: {words}")
        self.char_count_label.setText(f"Characters: {chars}")

    def clear_all_notes(self):
        confirmation = QMessageBox.question(
            self, "Clear All", "Are You Sure?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmation == QMessageBox.Yes:
            self.text_edit.clear()

    def open_note(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Note", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:  # Open with UTF-8 encoding
                    content = file.read()
                    self.text_edit.setText(content)
            except UnicodeDecodeError:
                # If UTF-8 fails, try opening with a different encoding
                try:
                    with open(file_path, 'r', encoding='cp1252') as file:
                        content = file.read()
                        self.text_edit.setText(content)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to open the file. Error: {e}")

    def save_note(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Note", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:  # Save with UTF-8 encoding
                content = self.text_edit.toPlainText()
                file.write(content)
        self.unsaved_changes = False

    def about_app(self):
        QMessageBox.about(self, "About FrappeNote", "📒 FrappeNote\nThe Best Notes App!")

    def prompt_save_before_exit(self):
        if self.unsaved_changes:
            save_prompt = QMessageBox.question(
                self, "Save Note", "You have unsaved changes. Do you want to save before exiting?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            if save_prompt == QMessageBox.Yes:
                self.save_note()
                self.close()
            elif save_prompt == QMessageBox.No:
                self.close()
        else:
            self.close()

    def toggle_always_on_top(self):
        self.always_on_top = not self.always_on_top
        if self.always_on_top:
            self.setWindowFlag(Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlag(Qt.Widget)
        self.show()  # Refresh the window
        self.always_on_top_button.setText("🔝" if not self.always_on_top else "🔙")  # Change the button text

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False


# Main function
def main():
    app = QApplication(sys.argv)
    window = FrappeNoteApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
