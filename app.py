from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

x_accum = []
y_accum = []

from camera import Camera

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/default")
def default():
    return render_template("default.html")

@app.route("/drawing")
def drawing():
    return render_template("drawing.html")

def gen(camera, flag):
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while True:
            success, image = camera.video.read()
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    if flag == 0:
                        default(image, hand_landmarks)
                    elif flag == 1:
                        hand_draw(camera, image, hand_landmarks)
                    else:
                        print('error')

            image = cv2.flip(image, 1)
            ret, frame = cv2.imencode('.jpg', image)
            if frame is not None:
                yield (b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame.tobytes() + b"\r\n")
            else:
                print("frame is none")

def default(image, hand_landmarks):
    mp_drawing.draw_landmarks(
        image,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style())

def hand_draw(camera, image, hand_landmarks):
    height = camera.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = camera.video.get(cv2.CAP_PROP_FRAME_WIDTH)

    x2, y2 = hand_landmarks.landmark[2].x * width, hand_landmarks.landmark[2].y * height
    x4, y4 = hand_landmarks.landmark[4].x * width, hand_landmarks.landmark[4].y * height
    x8, y8 = hand_landmarks.landmark[8].x * width, hand_landmarks.landmark[8].y * height
    x17, y17 = hand_landmarks.landmark[17].x * width, hand_landmarks.landmark[17].y * height
    x20, y20 = hand_landmarks.landmark[20].x * width, hand_landmarks.landmark[20].y * height

    if x2 >= x4: # 親指曲げ
        x_accum.append(x8)
        y_accum.append(y8)
        cv2.circle(image, (int(x8), int(y8)), 5, (0, 255, -255), -1)
    else:
        x_accum.append(0)
        y_accum.append(0)
        cv2.circle(image, (int(x8), int(y8)), 5, (255, 0, -255), -1)

    for i in range(1, len(x_accum)):
        if (x_accum[i-1] == 0) or (x_accum[i] == 0):
            continue
        cv2.line(image, (int(x_accum[i-1]), int(y_accum[i-1])), (int(x_accum[i]), int(y_accum[i])), (0, 0, 255), thickness=4)

    if y20 >= y17: # 小指曲げ
        x_accum.clear()
        y_accum.clear()

@app.route("/video_feed/<flag>")
def video_feed(flag):
    return Response(gen(Camera(), int(flag)),
            mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)