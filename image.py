import os
import datetime
import numpy as np
from glob import glob

from PIL import Image, ImageDraw, ImageFont
from text import NUM_to_HAN

import logging
logging.getLogger("PIL").setLevel(logging.WARNING)

COLOR_MAP = [(103, 89, 79), (100, 163, 111), (172, 13, 13), (255, 183, 64)]

def draw_text(canvas, n_probs, use_char, use_color, font):
    # 매트릭스 크기, 위치 설정
    matrix_size = (1250, 740)
    matrix_pos = (320, 210)
    
    # 행렬 데이터
    matrix_data = np.arange(1, n_probs+1)
    np.random.shuffle(matrix_data)
    matrix_data = matrix_data.reshape((n_probs//5, 5))

    # 그리기 도구 생성
    draw = ImageDraw.Draw(canvas)

    # 각 셀의 크기
    cell_size = (matrix_size[0] // len(matrix_data[0]), matrix_size[1] // len(matrix_data))

    # 각 셀에 숫자 그리기
    for i in range(len(matrix_data)):
        for j in range(len(matrix_data[i])):
            # 셀 내부에 숫자 그리기
            cell_center = ((j + 0.5) * cell_size[0] + matrix_pos[0], (i + 0.5) * cell_size[1] + matrix_pos[1])
            # 숫자 변환 or not
            if use_char and matrix_data[i][j] in NUM_to_HAN and np.random.choice([True, False], p=[0.3, 0.7]):
                text = NUM_to_HAN[matrix_data[i][j]]
            else:
                text = str(matrix_data[i][j])
            # 색상 랜덤 선택 or not
            if use_color:
                text_color = COLOR_MAP[np.random.choice(range(len(COLOR_MAP)), p=[0.55, 0.15, 0.15, 0.15])]
            else:
                text_color = COLOR_MAP[0]

            draw.text(cell_center, text, font=font, fill=text_color, anchor='mm')

def make_images(options, save_dir='outputs'):

    os.makedirs(save_dir, exist_ok=True)
    # 60 -->0 까지 역순으로 카운트
    time_images = sorted(glob(os.path.join('datas/image/25칸/times', '*.png')), reverse=True)
    for idx, (n_probs, use_color, use_char) in enumerate(options):
        # 캔버스 생성
        background_img = Image.open('datas/image/배경.png')
        prob_matrix = Image.open('datas/image/25칸/25칸-문제지.png')
        prob_question = Image.open('datas/image/25칸/25칸-질문-ko.png')
        canvas = Image.composite(prob_matrix, background_img, prob_matrix)
        canvas = Image.composite(prob_question, canvas, prob_question)

        # 폰트 설정
        font = ImageFont.truetype('datas/font/TMONBlack.ttf', size=70)

        draw_text(canvas, n_probs, use_char, use_color, font)
        # 이미지 저장
        # new_save_dir = os.path.join(save_dir, f'{idx}번째 문제')
        for i in range(60):
            prob_time = Image.open(time_images[i])
            canvas = Image.composite(prob_time, canvas, prob_time)
            canvas.save(os.path.join(save_dir, f'matrix_{60*idx+i}.png'))


