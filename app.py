from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_mysqldb import MySQL
import base64
import logging
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import os


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = '123'

# MySQL 설정
app.config['MYSQL_HOST'] = 'project-db-cgi.smhrd.com'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'sc_21K_bigdata11_p3_1'
app.config['MYSQL_PASSWORD'] = 'smhrd1'
app.config['MYSQL_DB'] = 'sc_21K_bigdata11_p3_1'

mysql = MySQL(app)

model = load_model('static/model.h5')

@app.route('/')
def first():
    return render_template('first.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.json
    image_data = data['image']
    image_data = image_data.split(",")[1]  # Remove the "data:image/png;base64," part
    with open("captured_image.png", "wb") as fh:
        fh.write(base64.b64decode(image_data))

    img = cv2.imread('captured_image.png')
    face_cascade = cv2.CascadeClassifier("static/haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(img, 1.1, 4)

    if len(faces) == 0:
        return jsonify({"error": "사진을 다시 찍어주세요"}), 400

    for (x, y, w, h) in faces:
        cropped_face = img[y:y + h, x:x + w]
        cv2.imwrite('cropped_face.png', cropped_face)

        face_img = cv2.resize(cropped_face, (64, 64))
        face_img = face_img.astype("float") / 255.0
        face_img = img_to_array(face_img)
        face_img = np.expand_dims(face_img, axis=0)


        predictions = model.predict(face_img)
        result = np.argmax(predictions, axis=1)
        result[0] = int(result[0])
        session['prediction'] = int(result[0])

    return jsonify({"redirect": url_for('reco')})


@app.route('/reco')
def reco():
    prediction = session.get('prediction', 'No prediction available')

    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT * FROM menu m JOIN menu_reco mr ON m.menu_idx = mr.menu_idx and mr.reco_ages = %s ORDER BY mr.menu_sales DESC;", (prediction,))
    menu_details = cur.fetchall()

    cur.close()

    updated_menu_details = []
    for menu in menu_details:
        image_base64 = menu[5]
        if isinstance(image_base64, bytes):
            menu_image = base64.b64encode(image_base64).decode('utf-8')
            updated_menu = menu[:5] + (menu_image,)
            updated_menu_details.append(updated_menu)
        else:
            app.logger.error(f"Invalid type for image data: {type(image_base64)}")
            updated_menu_details.append(menu)
    return render_template('reco.html', menu_details=updated_menu_details, prediction=prediction)


@app.route('/coffee')
def coffee():
    prediction = session.get('prediction', 'No prediction available')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu where menu_category='커피'")
    menu_details = cur.fetchall()

    cur.close()

    updated_menu_details = []
    for menu in menu_details:
        image_base64 = menu[5]
        if isinstance(image_base64, bytes):
            menu_image = base64.b64encode(image_base64).decode('utf-8')
            updated_menu = menu[:5] + (menu_image,)
            updated_menu_details.append(updated_menu)
        else:
            app.logger.error(f"Invalid type for image data: {type(image_base64)}")
            updated_menu_details.append(menu)
    return render_template('coffee.html', menu_details=updated_menu_details, prediction=prediction)

@app.route('/tea')
def tea():
    prediction = session.get('prediction', 'No prediction available')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu where menu_category='티'")
    menu_details = cur.fetchall()

    cur.close()

    updated_menu_details = []
    for menu in menu_details:
        image_base64 = menu[5]
        if isinstance(image_base64, bytes):
            menu_image = base64.b64encode(image_base64).decode('utf-8')
            updated_menu = menu[:5] + (menu_image,)
            updated_menu_details.append(updated_menu)
        else:
            app.logger.error(f"Invalid type for image data: {type(image_base64)}")
            updated_menu_details.append(menu)
    return render_template('tea.html', menu_details=updated_menu_details, prediction=prediction)


@app.route('/ade')
def food():
    prediction = session.get('prediction', 'No prediction available')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu where menu_category='에이드/주스'")
    menu_details = cur.fetchall()

    cur.close()

    updated_menu_details = []
    for menu in menu_details:
        image_base64 = menu[5]
        if isinstance(image_base64, bytes):
            menu_image = base64.b64encode(image_base64).decode('utf-8')
            updated_menu = menu[:5] + (menu_image,)
            updated_menu_details.append(updated_menu)
        else:
            app.logger.error(f"Invalid type for image data: {type(image_base64)}")
            updated_menu_details.append(menu)
    return render_template('ade.html', menu_details=updated_menu_details, prediction=prediction)


@app.route('/smoothie')
def product():
    prediction = session.get('prediction', 'No prediction available')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu where menu_category='스무디/프라페'")
    menu_details = cur.fetchall()

    cur.close()

    updated_menu_details = []
    for menu in menu_details:
        image_base64 = menu[5]
        if isinstance(image_base64, bytes):
            menu_image = base64.b64encode(image_base64).decode('utf-8')
            updated_menu = menu[:5] + (menu_image,)
            updated_menu_details.append(updated_menu)
        else:
            app.logger.error(f"Invalid type for image data: {type(image_base64)}")
            updated_menu_details.append(menu)
    return render_template('smoothie.html', menu_details=updated_menu_details, prediction=prediction)



@app.route('/decaffeine')
def decaffeine():
    prediction = session.get('prediction', 'No prediction available')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu where menu_category='디카페인'")
    menu_details = cur.fetchall()

    cur.close()

    updated_menu_details = []
    for menu in menu_details:
        image_base64 = menu[5]
        if isinstance(image_base64, bytes):
            menu_image = base64.b64encode(image_base64).decode('utf-8')
            updated_menu = menu[:5] + (menu_image,)
            updated_menu_details.append(updated_menu)
        else:
            app.logger.error(f"Invalid type for image data: {type(image_base64)}")
            updated_menu_details.append(menu)
    return render_template('decaffeine.html', menu_details=updated_menu_details, prediction=prediction)


@app.route('/beverage')
def beverage():
    prediction = session.get('prediction', 'No prediction available')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu where menu_category='음료'")
    menu_details = cur.fetchall()

    cur.close()

    updated_menu_details = []
    for menu in menu_details:
        image_base64 = menu[5]
        if isinstance(image_base64, bytes):
            menu_image = base64.b64encode(image_base64).decode('utf-8')
            updated_menu = menu[:5] + (menu_image,)
            updated_menu_details.append(updated_menu)
        else:
            app.logger.error(f"Invalid type for image data: {type(image_base64)}")
            updated_menu_details.append(menu)
    return render_template('beverage.html', menu_details=updated_menu_details, prediction=prediction)



@app.route('/senior')
def senior():
    prediction = session.get('prediction', 'No prediction available')
    cur = mysql.connection.cursor()
    cur.execute("SELECT m.* FROM menu m JOIN menu_reco mr ON m.menu_idx = mr.menu_idx and mr.reco_ages = %s ORDER BY mr.menu_sales DESC;", (prediction,))
    menu_details = cur.fetchall()

    cur.close()

    updated_menu_details = []
    for menu in menu_details:
        image_base64 = menu[5]
        if isinstance(image_base64, bytes):
            menu_image = base64.b64encode(image_base64).decode('utf-8')
            updated_menu = menu[:5] + (menu_image,) + (menu[6],)
            updated_menu_details.append(updated_menu)
        else:
            app.logger.error(f"Invalid type for image data: {type(image_base64)}")
            updated_menu_details.append(menu)
    return render_template('senior.html', menu_details=updated_menu_details, prediction=prediction)

@app.route('/scoffee')
def scoffee():
    prediction = session.get('prediction', 'No prediction available')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu where menu_category='커피'")
    menu_details = cur.fetchall()

    cur.close()

    updated_menu_details = []
    for menu in menu_details:
        image_base64 = menu[5]
        if isinstance(image_base64, bytes):
            menu_image = base64.b64encode(image_base64).decode('utf-8')
            updated_menu = menu[:5] + (menu_image,) + (menu[6],)
            updated_menu_details.append(updated_menu)
        else:
            app.logger.error(f"Invalid type for image data: {type(image_base64)}")
            updated_menu_details.append(menu)
    return render_template('scoffee.html', menu_details=updated_menu_details, prediction=prediction)

@app.route('/snoncoffee')
def snonoffee():
    prediction = session.get('prediction', 'No prediction available')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu where NOT menu_category='커피'")
    menu_details = cur.fetchall()

    cur.close()

    updated_menu_details = []
    for menu in menu_details:
        image_base64 = menu[5]
        if isinstance(image_base64, bytes):
            menu_image = base64.b64encode(image_base64).decode('utf-8')
            updated_menu = menu[:5] + (menu_image,) + (menu[6],)
            updated_menu_details.append(updated_menu)
        else:
            app.logger.error(f"Invalid type for image data: {type(image_base64)}")
            updated_menu_details.append(menu)
    return render_template('snoncoffee.html', menu_details=updated_menu_details, prediction=prediction)

@app.route('/cart')
def cart():
    prediction = session.get('prediction', 'No prediction available')
    session['cartpage'] = 1
    return render_template('cart.html', prediction=prediction)

@app.route('/pay')
def pay():
    prediction = session.get('prediction', 'No prediction available')
    cartpage = session.get('cartpage', 0)
    return render_template('pay.html', prediction=prediction, cartpage=cartpage)


@app.route('/save', methods=['POST'])
def save():
    # 세션에서 'prediction' 값 가져오기
    prediction = session.get('prediction')
    # 요청 본문에서 'cartData' 값 가져오기
    cart_data = request.json.get('cartData')
    custnum = request.json.get('custnum')

    # MySQL 연결 객체에서 커서 생성
    cur = mysql.connection.cursor()

    total_quantity = sum(int(item['quantity']) for item in cart_data)
    # 적립여부 판별
    if custnum is not None:
        # 적립 시 회원여부 판별
        custsel = cur.execute("SELECT * FROM customer where cust_phone = %s", (custnum,))
        if custsel == 0:
            cur.execute("INSERT INTO customer (cust_phone, cust_stamp, cust_ages) VALUES (%s, %s, %s)",
                        (custnum, total_quantity, prediction))
        else:
            cur.execute("UPDATE customer SET cust_stamp=cust_stamp+%s where cust_phone = %s",
                        (total_quantity, custnum))


    # 장바구니 데이터 반복 처리
    for item in cart_data:
        # 메뉴 테이블에서 해당 메뉴 정보 조회
        sel = cur.execute("SELECT * FROM menu_reco where menu_idx = %s", (item['idx'],))

        # 조회 결과가 없으면 새로 insert
        if sel is None:
            cur.execute("INSERT INTO menu_reco (menu_idx, reco_ages, menu_sales) VALUES (%s, %s, %s)",
                        (item['idx'], prediction, item['quantity']))
        # 조회 결과가 있으면 sales 수량 update
        else:
            cur.execute("UPDATE menu_reco SET menu_sales=menu_sales+%s where menu_idx = %s and reco_ages = %s",
                        (int(item['quantity']), item['idx'], prediction))

        # 변경 사항 커밋
        mysql.connection.commit()

    # 커서 닫기
    cur.close()

    return jsonify({"redirect": url_for('home')})


@app.route('/get_stamp_info', methods=['POST'])
def get_stamp_info():
    data = request.get_json()
    custnum = data['custnum']

    # MySQL 연결 객체에서 커서 생성
    cur = mysql.connection.cursor()
    cur.execute("SELECT cust_stamp FROM customer WHERE cust_phone = %s", (custnum,))
    result = cur.fetchone()
    cur.close()

    if result:
        stamp_count = result[0]
    else:
        stamp_count = 0  # 고객 정보가 없으면 기본값 0 설정

    return jsonify({'stamp_count': stamp_count})

@app.route('/finish')
def finish():
    return render_template('finish.html')

# 업로드 디렉토리 설정
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'success': False, 'message': 'No audio file uploaded'})

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})

    file_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(file_path)


    return jsonify({'success': True})




## 사운드처리
import librosa
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
from pydub import AudioSegment

@app.route('/predict_command')
def predict_command():
    file_path = 'uploads/recording.wav'
    soundmodel = load_model('static/soundmodel.h5')

    # AudioSegment를 로드합니다
    audio = AudioSegment.from_file(file_path)

    # 오디오 샘플링 레이트를 16000으로 변경합니다
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": 16000
    })

    # AudioSegment를 numpy 배열로 변환합니다
    signal = np.array(audio.get_array_of_samples(), dtype=np.float32)
    if audio.channels == 2:  # 스테레오 오디오인 경우
        signal = signal.reshape((-1, 2)).mean(axis=1)  # 모노로 변환

    sr = 16000

    # 정규화 (16비트 PCM의 최대값으로 나누어 -1.0에서 1.0 사이의 값으로 변환)
    signal /= np.iinfo(np.int16).max

    # 멜 스펙트로그램을 계산합니다
    mel_spec = librosa.feature.melspectrogram(y=signal, sr=sr, n_mels=256, n_fft=1024, hop_length=512)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

    # 패딩 또는 잘라내기
    max_length = 256
    if mel_spec_db.shape[1] > max_length:
        mel_spec_db = mel_spec_db[:, :max_length]
    else:
        pad_width = max_length - mel_spec_db.shape[1]
        mel_spec_db = np.pad(mel_spec_db, ((0, 0), (0, pad_width)), mode='constant')

    mel_spec_db = mel_spec_db[..., np.newaxis]  # 채널 차원 추가
    mel_spec_db = np.expand_dims(mel_spec_db, axis=0)  # 배치 차원 추가

    # 모델 예측
    prediction = soundmodel.predict(mel_spec_db)
    class_names = ['(ICE)아메리카노', '딸기라떼', '수박 주스']
    predicted_class = np.argmax(prediction)
    predicted_command = class_names[predicted_class]

    return predicted_command

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000,
            ssl_context=('C:/Users/smart/cert.pem', 'C:/Users/smart/key_no_pass.pem'))
