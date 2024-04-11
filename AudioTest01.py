import cv2
import speech_recognition as sr
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from moviepy.editor import VideoFileClip
import pygame

# 음성 인식기 객체 생성
r = sr.Recognizer()

# 마이크로부터 오디오를 가져오는 함수
def record_audio():
    with sr.Microphone() as source:
        print("말해주세요.")
        audio = r.listen(source)
    return audio

# 음성을 텍스트로 변환하는 함수
def speech_to_text(audio):
    try:
        text = r.recognize_google(audio, language="ko-KR")
        return text
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
        return ""
    except sr.RequestError as e:
        print("Google Speech Recognition API에 접근할 수 없습니다. {0}".format(e))
        return ""

# 영상에서 소리를 추출하는 함수
def extract_audio(video_path, output_path):
    # 동영상 파일을 VideoFileClip 객체로 불러옵니다.
    video = VideoFileClip(video_path)
    
    # 동영상 파일로부터 오디오를 추출합니다.
    audio = video.audio
    
    # 오디오를 파일로 출력합니다.
    audio.write_audiofile(output_path)
    
    # VideoFileClip 객체와 연결된 자원을 해제합니다.
    video.close()

def main():
    # 영상 재생 함수 호출
    video_path = "C:\\Users\\jjlee\\OneDrive\\바탕 화면\\KakaoTalk_20240312_220206853.mp4"  # 실제 영상 파일 경로로 변경
    audio_path = "C:\\Users\\jjlee\\OneDrive\\바탕 화면\\extracted_audio.wav"  # 추출된 오디오 파일 경로
    stop_time = 5 # 예시: 5초에 영상을 멈춤
    
    # 영상에서 소리를 추출
    extract_audio(video_path, audio_path)
    
    # 영상 재생 함수 호출
    play_video(video_path, audio_path, stop_time)

# 영상 재생 함수 정의
def play_video(video_path, audio_path, stop_time, window_name='Video'):
    # 동영상 파일 열기
    cap = cv2.VideoCapture(video_path)

    # 오디오 파일 열기
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    
    # # 영상의 총 길이 가져오기
    # total_time = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)

    answers = ["안녕", "숫자 2", "잘가","-1"]
    questions = ["인사할 때 뭐라고 하나요?", "1 더하기 1은 뭔가요?", "헤어질 때 뭐라고 하나요?","-1"]
    times = [3, 10, 1000000]

    # 한글 폰트 로드
    font_path = "C:\\Windows\\Fonts\\H2GTRM"  # 다운로드한 한글 폰트 파일 경로로 변경
    font = ImageFont.truetype(font_path, 50)

    while questions:
        ret, frame = cap.read()
        if not ret:
            break

        # 현재 프레임의 시간 정보 가져오기
        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

        # 특정 시간에 도달하면 영상 멈춤
        if current_time >= stop_time:
            print("영상이 멈춘 상태입니다.")

            # 문구 화면에 표시
            question = questions.pop(0)
            answer = answers.pop(0)
            image_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(image_pil)
            draw.text((50, 50), question, font=font, fill=(0, 0, 255))
            frame = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
            cv2.imshow(window_name, frame)
            cv2.waitKey(0)  # 키 입력을 대기합니다.

            # 사용자가 정답을 맞출 때까지 대기
            while True:
                audio_input = record_audio()
                text_output = speech_to_text(audio_input)
                print("음성 입력:", text_output)
                if text_output == answer:
                    print("정답입니다.")
                    print("영상을 멈춘 시점에서 다시 재생합니다.")
                    # 멈춘 시간을 기준으로 다시 재생 시작
                    cap.set(cv2.CAP_PROP_POS_MSEC, stop_time * 1000)  # stop_time초부터 다시 재생
                    pygame.mixer.music.play()
                    break
                else:
                    print("틀렸습니다.")

            stop_time += times.pop(0)  # 다음 멈추는 시간 설정

        # 영상 재생
        cv2.imshow(window_name, frame)

        if cv2.waitKey(25) != -1:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
