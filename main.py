import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QGridLayout, QFileDialog
from qtcode.codeeditor import CodeEditor
from qt_material import apply_stylesheet

class ProblemMaker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Problem Maker")
        layout = QGridLayout()

        # 첫 번째 줄 - 출력 위치 지정
        self.label_output = QLabel("출력 위치")
        self.folder_path = QLineEdit()
        self.open_folder_path_btn = QPushButton("위치 지정...")

        layout.addWidget(self.label_output, 0, 0)
        layout.addWidget(self.folder_path, 0, 1)
        layout.addWidget(self.open_folder_path_btn, 0, 2)

        # 두 번째 줄 - 문제 지문 텍스트
        label_problem_statement = QLabel("문제 지문")
        layout.addWidget(label_problem_statement, 1, 0, 1, 3)

        # 세 번째 줄 - 문제 지문 입력 공간
        self.text_edit_problem_statement = CodeEditor()
        # self.text_edit_problem_statement.setAcceptRichText(False)
        layout.addWidget(self.text_edit_problem_statement, 2, 0, 1, 3)

        # 네 번째 줄 - 입력 예시 텍스트
        label_input_example = QLabel("입력 예시")
        label_output_example = QLabel("출력 예시")

        layout.addWidget(label_input_example, 3, 0)
        layout.addWidget(label_output_example, 3, 1)

        # 다섯 번째 줄 - 입력 예시, 출력 예시 입력 공간
        self.text_edit_input_example = QTextEdit()
        self.text_edit_output_example = QTextEdit()

        layout.addWidget(self.text_edit_input_example, 4, 0)
        layout.addWidget(self.text_edit_output_example, 4, 1)

        # 레이아웃을 위젯에 설정
        self.setLayout(layout)

        # 버튼 이벤트 연결
        self.open_folder_path_btn.clicked.connect(self.open_folder_dialog)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "폴더 열기", "")
        if folder_path:
            self.folder_path.setText(folder_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProblemMaker()

    apply_stylesheet(app, theme='light_blue.xml')
    window.show()
    sys.exit(app.exec_())