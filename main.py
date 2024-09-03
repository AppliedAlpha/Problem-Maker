import os
import sys
import tempfile
import subprocess

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QGridLayout, QFileDialog, QTableWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
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

        self.problem_name_lbl = QLabel("문제 이름 (ex. 실습문제02-01)")
        self.problem_name_txt = QLineEdit()

        self.problem_statement_lbl = QLabel("문제 지문")
        self.answer_code_lbl = QLabel("정답 코드")
        self.answer_code_clear_btn = QPushButton("지우기")

        self.problem_statement_text = QTextEdit()
        self.problem_statement_text.setAcceptRichText(False)

        self.answer_code_text = CodeEditor()

        self.input_example_lbl = QLabel("입력 예시")
        self.output_example_lbl = QLabel("출력 예시")

        self.input_example_text = QTextEdit()
        self.output_example_text = QTextEdit()

        self.input_example_text.setAcceptRichText(False)
        self.output_example_text.setAcceptRichText(False)

        self.get_output_from_code_btn = QPushButton("정답 코드로 출력 예시 생성")
        self.add_case_btn = QPushButton("채점 케이스 추가")
        self.remove_case_btn = QPushButton("채점 케이스 삭제")
        self.create_problem_btn = QPushButton("문제 만들기")

        self.case_table = QTableWidget()
        self.log = QTextEdit()

        self.case_table.setColumnCount(2)
        self.case_table.setHorizontalHeaderLabels(["입력", "출력"])
        self.case_table.verticalHeader().setFixedWidth(50)

        self.log.setReadOnly(True)

        layout.addWidget(self.title, 0, 0, 1, 9, Qt.AlignCenter)

        layout.addWidget(self.folder_path_lbl, 1, 0, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.folder_path_txt, 1, 1, 1, 5)
        layout.addWidget(self.folder_path_open_btn, 1, 6, 1, 3)

        layout.addWidget(self.problem_name_lbl, 2, 0, 1, 2, Qt.AlignCenter)
        layout.addWidget(self.problem_name_txt, 2, 2, 1, 7)

        layout.addWidget(self.problem_statement_lbl, 3, 0, 1, 5)
        layout.addWidget(self.answer_code_lbl, 3, 5, 1, 3)

        layout.addWidget(self.problem_statement_text, 4, 0, 1, 5)
        layout.addWidget(self.answer_code_text, 4, 5, 5, 4)

        layout.addWidget(self.input_example_lbl, 5, 0, 1, 2, Qt.AlignCenter)
        layout.addWidget(self.output_example_lbl, 5, 2, 1, 2, Qt.AlignCenter)

        layout.addWidget(self.input_example_text, 6, 0, 3, 2)
        layout.addWidget(self.output_example_text, 6, 2, 3, 2)

        layout.addWidget(self.get_output_from_code_btn, 5, 4)
        layout.addWidget(self.add_case_btn, 6, 4)
        layout.addWidget(self.remove_case_btn, 7, 4)
        layout.addWidget(self.create_problem_btn, 8, 4)

        layout.addWidget(self.case_table, 9, 0, 1, 5)
        layout.addWidget(self.log, 9, 5, 1, 4)

        layout.setRowMinimumHeight(0, 30)
        layout.setRowMinimumHeight(4, 150)
        layout.setRowMinimumHeight(9, 250)

        layout.setColumnMinimumWidth(5, 300)
        layout.setColumnMinimumWidth(6, 200)

        self.setLayout(layout)

        self.folder_path_open_btn.clicked.connect(self.open_folder_dialog)
        self.answer_code_clear_btn.clicked.connect(self.answer_code_clear)
        self.get_output_from_code_btn.clicked.connect(self.get_output_from_code)
        self.add_case_btn.clicked.connect(self.add_case)
        self.remove_case_btn.clicked.connect(self.remove_case)
        self.create_problem_btn.clicked.connect(self.create_problem)

        # after init
        self.print_log("초기화 완료.")

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "폴더 열기", "")
        if folder_path:
            self.folder_path_txt.setText(folder_path)

    def print_log(self, text):
        text = str(text)
        now = datetime.now().strftime("[%m/%d %H:%M:%S.%f")[:-3]

        current_text = self.log.toPlainText()
        if current_text:
            current_text += "\n"
        
        self.log.setText(current_text + f"{now}] -- " + str(text))
        self.log.moveCursor(QTextCursor.End)
        self.log.ensureCursorVisible()

    def answer_code_clear(self):
        self.answer_code_text.setPlainText("")

    def add_case(self):
        if not (self.input_example_text.toPlainText().strip() or self.output_example_text.toPlainText().strip()):
            QMessageBox.warning(self, "Problem Maker", "입출력 예시가 비어있습니다.")
            return

        row_idx = self.case_table.rowCount()
        
        self.case_table.insertRow(row_idx)
        self.case_table.setItem(row_idx, 0, QTableWidgetItem(self.input_example_text.toPlainText().strip()))
        self.case_table.setItem(row_idx, 1, QTableWidgetItem(self.output_example_text.toPlainText().strip()))

        self.input_example_text.setText("")
        self.output_example_text.setText("")

        self.resize_table()

    def remove_case(self):
        row_idx = self.case_table.rowCount()

        if not row_idx:
            QMessageBox.warning(self, "Problem Maker", "삭제할 케이스가 없습니다.")
            return

        self.case_table.removeRow(row_idx - 1)

    def get_output_from_code(self):
        if not self.answer_code_text.toPlainText():
            QMessageBox.warning(self, "Problem Maker", "정답 코드가 비어있습니다.")
            return
        
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w+t", encoding="utf-8", delete=True) as temp_file:
            temp_file.write(self.answer_code_text.toPlainText())
            # temp_file.seek(0)
            path = temp_file.name
            self.print_log(f"코드를 다음 파일에 저장했습니다. > (TEMP_PATH)/{path.split('/')[-1]}")

            temp_file.read()

            process = subprocess.Popen(
                ["python" if os.name == "nt" else "python3", path], 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )

            stdin = self.input_example_text.toPlainText()
            stdout, stderr = process.communicate(stdin)
            # print(stdin)
            # print(stdout)

            if stderr:
                self.print_log(stderr)
                QMessageBox.critical(self, "Problem Maker", "실행 중 오류가 발생했습니다.\n\n" + stderr)
                return
            
            if self.output_example_text.toPlainText().strip() == stdout.strip():
                QMessageBox.information(self, "Problem Maker", "실행 결과가 출력 케이스와 동일합니다.")
                return
            
            self.output_example_text.setPlainText(stdout.strip())
            self.print_log("출력 케이스를 작성했습니다.")

    def create_problem(self):
        try:
            path = self.folder_path_txt.text()
            name = self.problem_name_txt.text().strip()
            code = self.answer_code_text.toPlainText()
            statement = self.problem_statement_text.toPlainText().strip()

            if not path:
                QMessageBox.warning(self, "Problem Maker", "경로가 설정되지 않았습니다.")
                return
            
            if not name:
                QMessageBox.warning(self, "Problem Maker", "문제 이름이 비어있습니다.")
                return
            
            if not statement:
                QMessageBox.warning(self, "Problem Maker", "문제 지문이 비어있습니다.")
                return
            
            if not self.case_table.rowCount():
                QMessageBox.warning(self, "Problem Maker", "채점 데이터가 없습니다.")
                return
            
            in_example_item = self.case_table.item(0, 0)
            out_example_item = self.case_table.item(0, 1)

            in_example_text = in_example_item.text() if in_example_item else ""
            out_example_text = out_example_item.text() if out_example_item else ""

            statement += f"\n\n[입력 예시]\n{in_example_text}\n\n[출력 예시]{out_example_text}\n"
            
            # 문제가 들어갈 폴더 만들기
            path += f"/{name}"
            os.mkdir(path)

            _statement = open(path + f"/{name}.txt", "w+t", encoding="utf-8")
            _statement.write(statement)
            _statement.close()

            self.print_log(f"[{name}] 문제 지문 내보내기 완료.")

            _code = open(path + f"/{name}.py", "w+t", encoding="utf-8")
            _code.write(code)
            _code.close()

            self.print_log(f"[{name}] 문제 코드 내보내기 완료.")

            # 테스트 케이스 생성
            case_path = path + "/Case"
            os.mkdir(case_path)

            for idx in range(self.case_table.rowCount()):
                input_item = self.case_table.item(idx + 1, 0)
                output_item = self.case_table.item(idx + 1, 1)

                input_text = input_item.text() if input_item else ""
                output_text = output_item.text() if output_item else ""

                _in = open(case_path + f"/{idx + 1}.in", "w+t", encoding="utf-8")
                _in.write(input_text)
                _in.close()

                _out = open(case_path + f"/{idx + 1}.out", "w+t", encoding="utf-8")
                _out.write(output_text)
                _out.close()

                self.print_log(f"[{name}] {idx+1}번 입출력 내보내기 완료.")

            # 문제 생성 완료
            QMessageBox.information(self, "Problem Maker", f"[{name}]\n\n문제를 성공적으로 생성했습니다.")

        except Exception as err:
            err = err.with_traceback()
            self.print_log(err)
            QMessageBox.critical(self, "Problem Maker", "실행 중 오류가 발생했습니다.\n\n" + err)
            return

    def resize_table(self):
        column_width = (self.case_table.width() - self.case_table.verticalHeader().width()) // 2 - 1
        self.case_table.setColumnWidth(0, column_width)
        self.case_table.setColumnWidth(1, column_width)
        self.case_table.resizeRowsToContents()

    def resizeEvent(self, event):
        self.resize_table()
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProblemMaker()

    apply_stylesheet(app, theme='light_blue.xml')
    window.show()
    sys.exit(app.exec_())