from cv2 import cv2
import mediapipe as mp

import utils
import config as cfg

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(3, cfg.WIDTH)
cap.set(4, cfg.HEIGHT)

THUMB_TIP = mp_hands.HandLandmark.THUMB_TIP
INDEX_FINGER_TIP = mp_hands.HandLandmark.INDEX_FINGER_TIP


def put_text(frame, obj):
    y_coord = 15
    for key in obj:
        text = f'{key}: {"  ".join([str(round(x, 2)) for x in obj[key]])}'
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame = cv2.putText(frame, text, (15, y_coord), font, 0.6, (0, 128, 255))
        y_coord += y_coord + 3
    return frame


with mp_hands.Hands(min_tracking_confidence=0.8) as hands:
    while cap.isOpened():
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)

        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame)

        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                # координаты польцев
                thumb_tip_landmark = hand_landmarks.landmark[THUMB_TIP]
                thumb_tip_coords = [thumb_tip_landmark.x, thumb_tip_landmark.y]

                index_finger_tip_landmark = hand_landmarks.landmark[INDEX_FINGER_TIP]
                index_finger_tip_coords = [index_finger_tip_landmark.x, index_finger_tip_landmark.y]

                # расстояние мужду указательным и большим
                distance = utils.count_distance(
                    (thumb_tip_coords[0] * cfg.WIDTH, thumb_tip_coords[1] * cfg.HEIGHT),
                    (index_finger_tip_coords[0] * cfg.WIDTH, index_finger_tip_coords[1] * cfg.HEIGHT)
                )
                utils.set_volume(distance)

                # линия соединения
                pt1 = (int(thumb_tip_coords[0] * cfg.WIDTH), int(thumb_tip_coords[1] * cfg.HEIGHT))
                pt2 = (int(index_finger_tip_coords[0] * cfg.WIDTH), int(index_finger_tip_coords[1] * cfg.HEIGHT))

                frame = cv2.line(frame, pt1, pt2, (0, 128, 255), 3)

                obj = {'Thumb': thumb_tip_coords,
                       'Index': index_finger_tip_coords,
                       'Distance': [distance * 100, 0.0]}

                frame = put_text(frame, obj)

                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        cv2.imshow('Frame', frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
