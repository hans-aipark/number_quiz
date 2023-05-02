import os
import math
from glob import glob
from moviepy.editor import AudioFileClip, CompositeAudioClip, ImageClip, ImageSequenceClip, VideoFileClip, concatenate_videoclips, concatenate_audioclips

INTRO_PATH = os.path.join('datas', 'video', 'intro_남자.mp4')
OUTRO_PATH = os.path.join('datas', 'video', 'outro_남자.mp4')
# BGM_PATH = os.path.join('datas', 'sound', 'background.wav')
BGM_PATH = os.path.join('datas', 'sound')

def image_and_audio_to_video(image_dir, audio_path, output_path, language, times):
    # 파일 명의 숫자 부분을 필터링하여 오름차순으로 정렬
    image_paths = sorted(glob(os.path.join(image_dir, '*.png')), key=lambda x: int(''.join(filter(str.isdigit, x))))
    # print(image_paths)
    image_clip = ImageSequenceClip(image_paths, fps=1)
    # image_clip.write_videofile(output_path)

    # 배경음
    clips = []
    clips.append(AudioFileClip(os.path.join(BGM_PATH, f'{language}_1.wav')).set_start(0.2))
    time_sum = times[0]
    for time in times[1:-1]:
        clips.append(AudioFileClip(os.path.join(BGM_PATH, f'{language}_2.wav')).set_start(time_sum + 0.2))
        time_sum += time
    if len(times) >= 2:
        clips.append(AudioFileClip(os.path.join(BGM_PATH, f'{language}_3.wav')).set_start(time_sum + 0.2))
    audio_clip = CompositeAudioClip(clips)
    final_clip = image_clip.set_audio(audio_clip)
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
    final_clip.write_videofile(output_path)