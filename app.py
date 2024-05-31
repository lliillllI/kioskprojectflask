from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_mysqldb import MySQL
import base64
import logging
import cv2


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# MySQL 설정
app.config['MYSQL_HOST'] = 'project-db-campus.smhrd.com'
app.config['MYSQL_PORT'] = 3312
app.config['MYSQL_USER'] = 'sc_21K_bigdata11_p3_1'
app.config['MYSQL_PASSWORD'] = 'smhrd1'
app.config['MYSQL_DB'] = 'sc_21K_bigdata11_p3_1'

mysql = MySQL(app)


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

    return jsonify({"redirect": url_for('reco')})


@app.route('/reco')
def reco():
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
    return render_template('reco.html', menu_details=updated_menu_details)


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








if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000,
            ssl_context=('C:/Users/smart/cert.pem', 'C:/Users/smart/key_no_pass.pem'))
