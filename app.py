from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_mysqldb import MySQL
import base64
import logging
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

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
    cur.execute("SELECT * FROM menu")
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
    return render_template('coffee.html', menu_details=updated_menu_details)

@app.route('/tea')
def tea():
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
    return render_template('tea.html', menu_details=updated_menu_details)


@app.route('/ade')
def food():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu where menu_category='에이드&주스'")
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
    return render_template('ade.html', menu_details=updated_menu_details)


@app.route('/smoothie')
def product():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu where menu_category='스무디&프라페'")
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
    return render_template('smoothie.html', menu_details=updated_menu_details)



@app.route('/decaffeine')
def decaffeine():
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
    return render_template('decaffeine.html', menu_details=updated_menu_details)


@app.route('/beverage')
def beverage():
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
    return render_template('beverage.html', menu_details=updated_menu_details)



@app.route('/senior')
def senior():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu")
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
    return render_template('senior.html', menu_details=updated_menu_details)

@app.route('/scoffee')
def scoffee():
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
    return render_template('scoffee.html', menu_details=updated_menu_details)

@app.route('/snoncoffee')
def snonoffee():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu where NOT menu_category='커피'")
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
    return render_template('snoncoffee.html', menu_details=updated_menu_details)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/pay')
def pay():
    return render_template('pay.html')


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

    print(total_quantity)
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



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000,
            ssl_context=('C:/Users/smart/cert.pem', 'C:/Users/smart/key_no_pass.pem'))
