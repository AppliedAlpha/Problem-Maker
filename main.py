import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QGridLayout, QFileDialog, QTableWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from qtcode.codeeditor import CodeEditor
from qt_material import apply_stylesheet
from datetime import datetime

class ProblemMaker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Problem Maker")
        layout = QGridLayout()

        self.title = QLabel("Problem Maker")
        # self.title.font().setPointSize(80)

        self.folder_path_lbl = QLabel("출력 위치")
        self.folder_path_txt = QLineEdit()
        self.folder_path_open_btn = QPushButton("위치 지정...")

        self.problem_statement_lbl = QLabel("문제 지문")
        self.answer_code_lbl = QLabel("정답 코드")

        self.problem_statement_text = QTextEdit()
        self.problem_statement_text.setAcceptRichText(False)

        self.answer_code_text = CodeEditor()

        self.input_example_lbl = QLabel("입력 예시")
        self.output_example_lbl = QLabel("출력 예시")

        self.input_example_text = QTextEdit()
        self.output_example_text = QTextEdit()

        self.get_output_from_code_btn = QPushButton("정답 코드로 출력 예시 생성")
        self.add_case_btn = QPushButton("채점 케이스 추가")
        self.remove_case_btn = QPushButton("채점 케이스 삭제")
        self.create_problem_btn = QPushButton("문제 만들기")

        self.case_table = QTableWidget()
        self.log = QTextEdit()

        self.case_table.setEnabled(False)
        self.log.setReadOnly(False)

        layout.addWidget(self.title, 0, 0, 1, 9, Qt.AlignCenter)

        layout.addWidget(self.folder_path_lbl, 1, 0, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.folder_path_txt, 1, 1, 1, 5)
        layout.addWidget(self.folder_path_open_btn, 1, 6, 1, 3)

        layout.addWidget(self.problem_statement_lbl, 2, 0, 1, 5)
        layout.addWidget(self.answer_code_lbl, 2, 5, 1, 4)

        layout.addWidget(self.problem_statement_text, 3, 0, 1, 5)
        layout.addWidget(self.answer_code_text, 3, 5, 5, 4)

        layout.addWidget(self.input_example_lbl, 4, 0, 1, 2, Qt.AlignCenter)
        layout.addWidget(self.output_example_lbl, 4, 2, 1, 2, Qt.AlignCenter)

        layout.addWidget(self.input_example_text, 5, 0, 3, 2)
        layout.addWidget(self.output_example_text, 5, 2, 3, 2)

        layout.addWidget(self.get_output_from_code_btn, 4, 4)
        layout.addWidget(self.add_case_btn, 5, 4)
        layout.addWidget(self.remove_case_btn, 6, 4)
        layout.addWidget(self.create_problem_btn, 7, 4)

        layout.addWidget(self.case_table, 8, 0, 1, 5)
        layout.addWidget(self.log, 8, 5, 1, 4)

        layout.setRowMinimumHeight(0, 30)
        layout.setRowMinimumHeight(8, 250)

        layout.setColumnMinimumWidth(5, 300)
        layout.setColumnMinimumWidth(6, 200)

        self.setLayout(layout)

        self.folder_path_open_btn.clicked.connect(self.open_folder_dialog)

        # after init
        self.print_log("초기화 완료.")

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "폴더 열기", "")
        if folder_path:
            self.folder_path_txt.setText(folder_path)

    def print_log(self, text):
        now = datetime.now().strftime("[%m/%d %H:%M:%S.%f")[:-3]

        current_text = self.log.toPlainText()
        if current_text:
            current_text += "\n"
        
        self.log.setText(current_text + f"{now}] -- " + str(text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProblemMaker()

    apply_stylesheet(app, theme='light_blue.xml')
    window.show()
    sys.exit(app.exec_())