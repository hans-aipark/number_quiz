import os
import sys
from glob import glob

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from generation import GenarationDialog

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

DATAS = 'datas'

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.selectedList = [0]
        self.design_list = sorted(os.listdir(DATAS))
        # 5의 배수로 설정
        self.problem_list = []
        self.problem_times = ['40', '50', '60']
        self.table_columns = ['문제 수', '제한 시간', '색상', '문자', '폰트']
        self.foreign_languages = ['전체 선택', '한국어', '영어', '중국어', '일본어', '스페인어', '인도네시아어', '포르투갈어']
        self.initUI()

    def initUI(self):
        self.initDialog()

        self.setWindowTitle('Number Quiz Automation Tool')
        self.setMinimumWidth(500)
        # initial vbox
        vbox = QVBoxLayout()

        # 디자인 선택 탭
        label = QLabel('디자인 선택')
        vbox.addWidget(label)
        scrollArea = QScrollArea()
        scrollArea.setFixedHeight(55)
        gb = QGroupBox()
        gb.setMinimumWidth(460)
        gb.setMaximumHeight(100)
        vvbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.btns_design = QButtonGroup()
        for i, dir in enumerate(self.design_list, start=1):
            btn = QRadioButton(dir)
            self.btns_design.addButton(btn, i-1)
            hbox.addWidget(btn)
            if i % 3 == 0:
                vvbox.addLayout(hbox)
                hbox = QHBoxLayout()
        vvbox.addLayout(hbox)
        gb.setLayout(vvbox)
        scrollArea.setWidget(gb)
        vbox.addWidget(scrollArea)
        

        # 언어 선택 탭
        label = QLabel('언어 선택')
        vbox.addWidget(label)

        scrollArea = QScrollArea()
        scrollArea.setFixedHeight(70)
        gb = QGroupBox()
        gb.setMinimumWidth(460)
        gb.setMaximumHeight(100)
        vvbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.btns_foreign = QButtonGroup()
        self.btns_foreign.setExclusive(False)
        for i, lan in enumerate(self.foreign_languages, start=1):
            btn = QCheckBox(lan)
            self.btns_foreign.addButton(btn, i-1)
            hbox.addWidget(btn)
            if i % 3 == 0:
                vvbox.addLayout(hbox)
                hbox = QHBoxLayout()
            if i == 1:
                btn.clicked.connect(self.check_foreign)
        vvbox.addLayout(hbox)
        gb.setLayout(vvbox)
        scrollArea.setWidget(gb)
        vbox.addWidget(scrollArea)

        # 난이도 선택 탭
        hbox = QHBoxLayout()
        label = QLabel('난이도 선택')
        vbox.addWidget(label)
        difficulty = ['상', '중', '하']
        self.btns_diff = QButtonGroup()
        for i, d in enumerate(difficulty):
            btn = QPushButton(d)
            btn.setCheckable(True)
            self.btns_diff.addButton(btn, i)
            hbox.addWidget(btn)
        vbox.addLayout(hbox)

        # 퀴즈 테이블
        self.table_quiz = QTableWidget(0, len(self.table_columns))
        header = self.table_quiz.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_quiz.setHorizontalHeaderLabels(self.table_columns)
        self.table_quiz.itemSelectionChanged.connect(self.table_changed)
        vbox.addWidget(self.table_quiz)

        hbox = QHBoxLayout()
        btn_plus = QPushButton('+1')
        btn_plus.clicked.connect(lambda: self.add_row(1))
        btn_plus_n = QPushButton('+n')
        btn_plus_n.clicked.connect(lambda: self.dialog_add_row.show())
        btn_minus = QPushButton('-')
        btn_minus.clicked.connect(self.remove_row)
        hbox.addWidget(btn_plus)
        hbox.addWidget(btn_plus_n)
        hbox.addWidget(btn_minus)
        vbox.addLayout(hbox)

        # 생성 버튼
        btn_generation = QPushButton('생성')
        btn_generation.clicked.connect(self.generate)
        vbox.addWidget(btn_generation)

        # 마지막 적용 탭
        self.setLayout(vbox)
        self.show()

    def initDialog(self):
        # ----------------------------------------------------------------
        # +n 버튼 dialog
        self.dialog_add_row = QDialog(self)
        self.dialog_add_row.setWindowTitle('Add row')
        self.dialog_add_row.resize(200, 100)
        vbox = QVBoxLayout()
        line = QLineEdit()
        line.setPlaceholderText('추가할 개수를 입력하세요.')
        vbox.addWidget(line)
        btn = QPushButton('OK')
        btn.clicked.connect(lambda: self.add_row(line.text()))
        btn.clicked.connect(lambda: self.dialog_add_row.close())
        vbox.addWidget(btn)
        self.dialog_add_row.setLayout(vbox)
        # ----------------------------------------------------------------

    def table_changed(self):
        self.selectedList.clear()        
        for item in self.table_quiz.selectedIndexes():
            self.selectedList.append(item.row())
         
        self.selectedList = list(set(self.selectedList))
         
        if self.table_quiz.rowCount()!=0 and len(self.selectedList) == 0:
            self.selectedList.append(0)

    def check_foreign(self):
        state = self.btns_foreign.button(0).isChecked()
        for btn in self.btns_foreign.buttons()[1:]:
            btn.setChecked(state)

    def add_row(self, iteration=1):
        # 디자인 선택 혹은 언어 선택을 하지 않으면 실행 안 함
        if self.check_btns() is False:
            return
        contents_dir = self.btns_design.checkedButton().text()

        self.problem_list = [os.path.basename(path)[:-1] for path in sorted(glob(os.path.join(DATAS, contents_dir, 'image', '*칸')))]

        print(iteration)
        try:
            iteration = int(iteration)
        except:
            return
        
        for _ in range(iteration):
            n_items = self.table_quiz.rowCount()
            self.table_quiz.setRowCount(n_items+1)

            btn_cnt = QComboBox()
            btn_cnt.addItems(self.problem_list)
            btn_cnt.setCurrentIndex(0)
            btn_time = QComboBox()
            btn_time.addItems(self.problem_times)
            btn_time.setCurrentIndex(2)
            btn_col = QPushButton('단일')
            btn_text = QPushButton('단일')
            btn_font = QPushButton('단일')
            btn_col.setCheckable(True)
            btn_text.setCheckable(True)
            btn_font.setCheckable(True)
            btn_col.pressed.connect(self.press_btn)
            btn_text.pressed.connect(self.press_btn)
            btn_font.pressed.connect(self.press_btn)

            if n_items >= 1:
                cur_btn_cnt = self.table_quiz.cellWidget(n_items-1, 0)
                cur_btn_time = self.table_quiz.cellWidget(n_items-1, 1)
                cur_btn_col = self.table_quiz.cellWidget(n_items-1, 2)
                cur_btn_text = self.table_quiz.cellWidget(n_items-1, 3)
                cur_btn_font = self.table_quiz.cellWidget(n_items-1, 4)

                btn_cnt.setCurrentIndex(cur_btn_cnt.currentIndex())
                btn_time.setCurrentIndex(cur_btn_time.currentIndex())
                btn_col.setChecked(cur_btn_col.isChecked())
                btn_text.setChecked(cur_btn_text.isChecked())
                btn_font.setChecked(cur_btn_font.isChecked())
                if cur_btn_col.isChecked():
                     btn_col.setText('랜덤')
                if cur_btn_text.isChecked():
                    btn_text.setText('랜덤')
                if cur_btn_font.isChecked():
                    btn_font.setText('랜덤')

            self.table_quiz.setCellWidget(n_items, 0, btn_cnt)
            self.table_quiz.setCellWidget(n_items, 1, btn_time)
            self.table_quiz.setCellWidget(n_items, 2, btn_col)
            self.table_quiz.setCellWidget(n_items, 3, btn_text)
            self.table_quiz.setCellWidget(n_items, 4, btn_font)

    def remove_row(self):
        n_items = self.table_quiz.rowCount()
        if n_items < 1: return
        for i, selected in enumerate(sorted(self.selectedList, reverse=True), start=1):
            self.table_quiz.removeRow(selected)
            self.table_quiz.setRowCount(n_items-i)
        self.selectedList = [self.table_quiz.rowCount()]

    def press_btn(self):
        if self.sender().isChecked():
            self.sender().setText('단일')
        else:
            self.sender().setText('랜덤')

    def generate(self):
        # 디자인 선택 혹은 언어 선택을 하지 않으면 실행 안 함
        if self.check_btns() is False:
            return

        # 디자인 체크 인덱스 
        design_id = self.btns_design.checkedId()
        design_path = os.path.join(DATAS, self.design_list[design_id])
        print('design_path: %s' % design_path)

        # 언어 체크 리스트 추출
        lang = [btn.text() for btn in self.btns_foreign.buttons() if btn.isChecked() and btn.text() != '전체 선택']

        diff = self.btns_diff.checkedId()
        n_items = self.table_quiz.rowCount()
        if n_items < 1: return
        options = []
        for i in range(n_items):
            n_prob = self.table_quiz.cellWidget(i, 0).currentIndex()
            n_prob = int(self.problem_list[n_prob])
            time_prob = self.table_quiz.cellWidget(i, 1).currentIndex()
            time_prob = int(self.problem_times[time_prob])

            use_color = self.table_quiz.cellWidget(i, 2).isChecked()
            use_char  = self.table_quiz.cellWidget(i, 3).isChecked()
            use_font  = self.table_quiz.cellWidget(i, 4).isChecked()
            options.append((n_prob, time_prob, use_color, use_char, use_font))
        genDialog = GenarationDialog(self, design_path, lang, diff, options)
        genDialog.exec()

    def check_btns(self):
        # 디자인 버튼이 하나도 선택되지 않으면 False
        for btn in self.btns_design.buttons():
            if btn.isChecked():
                break
        else:
            return False
        # 언어 박스가 하나도 선택되지 않으면 False
        for btn in self.btns_foreign.buttons():
            if btn.isChecked():
                break
        else:
            return False
        return True
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())