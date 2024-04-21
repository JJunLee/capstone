import cv2
import numpy as np 

# 딥러닝 기반의 얼굴 감지 모델 로드
face_net = cv2.dnn.readNetFromCaffe('c:\\Users\\uhs\\Desktop\\deploy (1).prototxt', 'c:\\Users\\uhs\\Desktop\\res10_300x300_ssd_iter_140000.caffemodel')

# 웹캠 열기
cap = cv2.VideoCapture(0)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    # 프레임 크기 변경
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    
    # 얼굴 감지
    face_net.setInput(blob)
    detections = face_net.forward()
    
    face_detected = False # 얼굴이 감지되었는지 여부를 나타내는 변수
    
    # 감지된 얼굴에 대해 반복
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        if confidence > 0.5: # 신뢰도가 0.5 이상인 경우
            face_detected = True
            
            # 얼굴 영역 추출
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")
            
            # 얼굴 영역에 사각형 그리기
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
    
    # 얼굴이 감지되지 않았을 경우에 경고 메시지 표시
    if not face_detected:
        cv2.putText(frame, "No face detected!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # 화면 표시
    cv2.imshow('Face Detection', frame)
    
    # 종료 조건: 'p' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break

# 종료
cap.release()
cv2.destroyAllWindows()