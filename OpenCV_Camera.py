import cv2
import os

# 녹화할 동영상 파일명과 경로 설정
video_filename = r'C:\Test_folder\video_filename\output_video.avi'
frame_folder = r'C:\Test_folder\frames'

# 폴더가 존재하지 않으면 프레임을 저장할 폴더 생성
if not os.path.exists(frame_folder):
    os.makedirs(frame_folder)

# OpenCV 비디오 캡처 객체 생성
capture = cv2.VideoCapture(0)  # 카메라를 사용할 경우 인덱스 0, 동영상 파일을 사용할 경우 파일 경로 입력

# 캡처 객체가 열려 있는지 확인
if not capture.isOpened():
    print("Error: Could not open video capture.")
    exit()

# 비디오 녹화를 위한 설정
frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 30
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))

# 프레임 저장 카운터 초기화
frame_count = 0

# 비디오 녹화 및 프레임 저장 루프
while True:
    ret, frame = capture.read()  # 새로운 프레임 읽기

    if not ret:
        print("Error: Failed to capture frame.")
        break

    # 프레임을 화면에 출력
    cv2.imshow('Recording', frame)

    # 프레임을 비디오 파일에 추가
    out.write(frame)

    # 프레임을 폴더에 저장
    frame_filename = os.path.join(frame_folder, f"frame_{frame_count}.png")
    cv2.imwrite(frame_filename, frame)

    # 프레임 저장 카운터 증가
    frame_count += 1

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 리소스 해제
capture.release()
out.release()
cv2.destroyAllWindows()
