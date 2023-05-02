import os
import math
from glob import glob
from moviepy.editor import AudioFileClip, CompositeAudioClip, ImageClip, ImageSequenceClip, VideoFileClip, concatenate_videoclips, concatenate_audioclips

INTRO_PATH = os.path.join('datas', 'video', 'intro_남자.mp4')
OUTRO_PATH = os.path.join('datas', 'video', 'outro_남자.mp4')
BRIDGE_PATH = os.path.join('datas', 'video', 'bridge.mp4')
# BGM_PATH = os.path.join('datas', 'sound', 'background.wav')
BGM_PATH = os.path.join('datas', 'sound')

def image_and_audio_to_video(image_dir, audio_path, output_path, language, times):
    clips = []
    bridge_clip = VideoFileClip(BRIDGE_PATH)
    audio_clip1 = AudioFileClip(os.path.join(BGM_PATH, f'{language}_1.wav'))
    audio_clip2 = AudioFileClip(os.path.join(BGM_PATH, f'{language}_2.wav'))
    audio_clip3 = AudioFileClip(os.path.join(BGM_PATH, f'{language}_3.wav'))
    for i, prob_dir in enumerate(sorted(os.listdir(image_dir))):
        # 파일 명의 숫자 부분을 필터링하여 오름차순으로 정렬
        image_paths = sorted(glob(os.path.join(image_dir, prob_dir, '*.png')), key=lambda x: int(''.join(filter(str.isdigit, x))))
        image_clip = ImageSequenceClip(image_paths, fps=1)
        if i == 0:
            image_clip = image_clip.set_audio(audio_clip1)
        elif i == len(os.listdir(image_dir)) - 1:
            image_clip = image_clip.set_audio(audio_clip3)
        else:
            image_clip = image_clip.set_audio(audio_clip2)
        clips.append(image_clip)
        clips.append(bridge_clip)


    # bgm = AudioFileClip(BGM_PATH)
    # audio_clip_length = len(image_paths) + 2
    # repeated_bgm = concatenate_audioclips([bgm] * math.ceil(audio_clip_length/bgm.duration))
    # audio_clip = repeated_bgm.subclip(0, audio_clip_length)

    # # 배경음과 이미지 클립 합치기
    # video_clip = image_clip.set_audio(audio_clip)
    # video_clip.duration = audio_clip.duration
    # video_clip.fps = 1

    # # 인트로 아웃트로 붙여서 저장하기
    # intro_video_clip = VideoFileClip(INTRO_PATH).audio_fadeout(1)
    # outro_video_clip = VideoFileClip(OUTRO_PATH)
    # final_clip = concatenate_videoclips([intro_video_clip, video_clip, outro_video_clip])
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path)