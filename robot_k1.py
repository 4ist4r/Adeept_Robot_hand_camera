import cv2
import mediapipe as mp
import serial
import time
import math

# Inicializar conexión con Arduino (ajustar 'COM3' si es necesario)
arduino = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)

# Inicializar MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Iniciar cámara
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Voltear imagen
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Obtener puntos clave
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            thumb_cmc = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
            pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # 🔹 1. ROTACIÓN LATERAL DE LA MUÑECA (Servo 9)
            wrist_rotation = pinky_mcp.y - thumb_cmc.y  # Diferencia vertical entre pulgar y meñique
            servo_9_angle = int((wrist_rotation + 0.2) * (180 / 0.4))  # Normalizar a rango 0-180
            servo_9_angle = max(0, min(180, servo_9_angle))

            # 🔹 2. POSICIÓN DE LA MUÑECA (Servos 6, 5, 3)
            wrist_y = wrist.y * 100
            wrist_position = int((wrist_y - 30) * (180 / 40))
            wrist_position = max(0, min(180, wrist_position))

            # 🔹 3. APERTURA Y CIERRE DE LA MANO (Servo 11)
            finger_distance = math.dist([index_tip.x, index_tip.y], [thumb_tip.x, thumb_tip.y])
            servo_11_angle = int(finger_distance * 300)
            servo_11_angle = max(0, min(180, servo_11_angle))

            # Enviar valores al Arduino
            command = f"{servo_9_angle},{wrist_position},{servo_11_angle}\n"
            arduino.write(command.encode())

            # Dibujar en pantalla
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.putText(frame, f"Rot: {servo_9_angle}  Muneca: {wrist_position}  Mano: {servo_11_angle}",
                        (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Hand Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
