import os
import shutil
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal

from image import make_images
from video import image_and_audio_to_video

OUTPUT_ROOT_DIR = 'outputs'
TEMP_DIR = 'temp'
class GenarationDialog(QDialog):
    def __init__(self, w, lang, diff, options):
        super().__init__(w)
        self.lang = lang
        # 난이도
        self.diff = diff
        self.options = options
        self.genThread = GenThread()
        self.initUI()

    def initUI(self):
        self.resize(200, 100)
        vbox = QVBoxLayout()
        line = QLineEdit()
        line.setPlaceholderText('생성 횟수를 입력해주세요.')
        vbox.addWidget(line)
        btn = QPushButton('OK')
        btn.clicked.connect(lambda: self.generation(line.text()))
        btn.clicked.connect(lambda: self.close())
        vbox.addWidget(btn)
        self.setLayout(vbox)


    def generation(self, times):
        try:
            times = int(times)
        except:
            print('wrong input :', times)
            return
        self.genThread.setup(self.lang, self.diff, self.options, times)
        self.genThread.start()

class GenThread(QThread):
    '''실제 생성 부'''
    pSignal = pyqtSignal(int)
    def ___init__(self):
        super().__init__()

    def setup(self, lang, diff, options, times):
        self.lang = lang
        self.diff = diff
        self.options = options
        self.times = times

    def run(self):
        # 현재 시간
        time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        for i in range(self.times):
            image_dir = os.path.join(TEMP_DIR, time_str)
            if os.path.exists(image_dir):
                shutil.rmtree(image_dir)
            # 문제에 해당하는 이미지 생성
            make_images(self.options, image_dir)
            # 이미지와 오디오를 합쳐서 비디오 생성
            video_path = os.path.join(OUTPUT_ROOT_DIR, time_str, f'{i+1}번째_영상.mp4')
            times = [60 for option in self.options]
            print(times)
            image_and_audio_to_video(image_dir, None, video_path, '한국어', times)


            