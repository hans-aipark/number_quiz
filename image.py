import os
import json
import datetime
import numpy as np
from glob import glob

from PIL import Image, ImageDraw, ImageFont
from config import NUM_to_HAN, COLOR, FONT, MATRIX, LANGUAGE_CODE

import logging
logging.getLogger("PIL").setLevel(logging.WARNING)


def draw_text(canvas, n_probs, use_char, use_color, use_font):
    global COLOR, FONT, MATRIX, COLOR_MAP, FONT_MAP
    # 매트릭스 크기, 위치 설정
    matrix_size = MATRIX['size'][str(n_probs)]
    matrix_pos = MATRIX['pos'][str(n_probs)]

    # 행렬 데이터
    matrix_data = np.arange(1, n_probs+1)
    np.random.shuffle(matrix_data)
    # 세로 길이 5칸 고정
    row, col = MATRIX['shape'][str(n_probs)]
    matrix_data = matrix_data.reshape((row, col))

    # 그리기 도구 생성
    draw = ImageDraw.Draw(canvas)

    # 각 셀의 크기
    cell_size = (matrix_size[0] // len(matrix_data[0]), matrix_size[1] // len(matrix_data))

    # 각 셀에 숫자 그리기
    for i in range(len(matrix_data)):
        for j in range(len(matrix_data[i])):
            # 셀 내부에 숫자 그리기
            cell_center = ((j + 0.5) * cell_size[0] + matrix_pos[0], (i + 0.5) * cell_size[1] + matrix_pos[1])
            # 문자 변환 or not
            if use_char and matrix_data[i][j] in NUM_to_HAN and np.random.choice([True, False], p=[0.3, 0.7]):
                text = NUM_to_HAN[matrix_data[i][j]]
            else:
                text = str(matrix_data[i][j])
            # 색상 랜덤 선택 or not
            if use_color:
                p = [0.5] + [0.5/(len(COLOR_MAP)-1)] * (len(COLOR_MAP)-1)
                text_color = tuple(COLOR_MAP[np.random.choice(range(len(COLOR_MAP)), p=p)])
            else:
                text_color = tuple(COLOR_MAP[0])
            # 폰트 랜덤 선택 or not
            if use_font:
                key = np.random.choice(range(len(FONT_MAP)))
                font = ImageFont.truetype(FONT_MAP[key][0], size=FONT_MAP[key][1])
            else:
                font = ImageFont.truetype(FONT_MAP[0][0], size=FONT_MAP[0][1])

            draw.text(cell_center, text, font=font, fill=text_color, anchor='mm')

def make_images(design_path, lang, diff, options, save_dir='outputs'):
    '''
    lang : language
    diff : diffuculty
    '''
    config = json.load(open(os.path.join(design_path, 'config.json'), encoding='utf-8'))
    global COLOR, FONT, MATRIX, COLOR_MAP, FONT_MAP
    COLOR = config['COLOR']
    FONT = config['FONT']
    MATRIX = config['MATRIX']
    TIMER = config['TIMER']
    COLOR_MAP = list(COLOR.values())
    FONT_MAP = [(os.path.join(design_path, v[0]), v[1]) for v in FONT.values()]
    # Background image list
    BGI_LIST = glob(os.path.join(design_path, 'image', '*.png'))

    lang = LANGUAGE_CODE[lang]
    # 60 -->0 까지 역순으로 카운트
    idx_savefile = 0
    for idx, (n_probs, time, use_color, use_char, use_font) in enumerate(options):
        # 외국어에 대해서 문자 변환 불능
        if lang != 'ko':
            use_font = False
        time_images = sorted(glob(os.path.join(f'{design_path}/image/times', '*.png')))
        timer_size = TIMER['size'][str(n_probs)]
        timer_pos = TIMER['pos'][str(n_probs)]
        # 캔버스 생성
        background_img = Image.open(np.random.choice(BGI_LIST))
        prob_matrix = Image.open(f'{design_path}/image/{n_probs}칸/{n_probs}칸-문제지.png')
        prob_question = Image.open(f'{design_path}/image/{n_probs}칸/{n_probs}칸-질문-{lang}.png')
        canvas = Image.composite(prob_matrix, background_img, prob_matrix)
        canvas = Image.composite(prob_question, canvas, prob_question)

        draw_text(canvas, n_probs, use_char, use_color, use_font)
        # 이미지 저장
        new_save_dir = os.path.join(save_dir, f'{idx:04d}')
        os.makedirs(new_save_dir, exist_ok=True)
        for i in range(time, -1, -1):
            # canvas = Image.composite(prob_time, canvas, prob_time)
            prob_time = Image.open(time_images[i]).resize(timer_size)
            prob_time_pos = (timer_pos[0]-timer_size[1]//2, timer_pos[1]-timer_size[1]//2)
            canvas.paste(prob_time, prob_time_pos, prob_time)
            canvas.save(os.path.join(new_save_dir, f'matrix_{idx_savefile:04d}.png'))
            idx_savefile += 1


