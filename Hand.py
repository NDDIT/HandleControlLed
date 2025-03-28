import cv2
import mediapipe as mp
import blynklib
import requests

# Thông tin Blynk
BLYNK_AUTH = "iVvuG0xatpOYcFI-8YW9QtkwpemEDj4J"
BLYNK_URL = f"https://blynk.cloud/external/api/update?token={BLYNK_AUTH}"

# Khởi tạo Mediapipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Mở camera
cap = cv2.VideoCapture(0)

def send_to_blynk(virtual_pin, value):
    """Gửi tín hiệu đến Blynk"""
    url = f"{BLYNK_URL}&V{virtual_pin}={value}"
    requests.get(url)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Chuyển ảnh sang RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Lấy tọa độ các đầu ngón tay
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
            
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]

            # Kiểm tra nếu ngón nào đang giơ lên (tip cao hơn DIP)
            index_up = index_tip.y < index_dip.y  # Ngón trỏ giơ lên
            middle_up = middle_tip.y < middle_dip.y  # Ngón giữa giơ lên

            # Điều khiển LED 1
            if index_up:
                send_to_blynk(1, 1)  # Bật đèn 1
                cv2.putText(frame, "LED 1 ON", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                send_to_blynk(1, 0)  # Tắt đèn 1
                cv2.putText(frame, "LED 1 OFF", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Điều khiển LED 2
            if middle_up:
                send_to_blynk(2, 1)  # Bật đèn 2
                cv2.putText(frame, "LED 2 ON", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                send_to_blynk(2, 0)  # Tắt đèn 2
                cv2.putText(frame, "LED 2 OFF", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Hand Gesture", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
