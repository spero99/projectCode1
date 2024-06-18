import os
from flask_socketio import SocketIO, send , emit
import compress
from flask import Flask, render_template,flash,request,redirect, url_for


def create_app(test_config=None):
    # create and configure the app
    UPLOAD_FOLDER = 'C:/test'
    ALLOWED_EXTENSIONS = {'txt'}

    app = Flask(__name__, instance_relative_config=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),

    )
    socket = SocketIO(app)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route("/")
    def main():
        return render_template("main.html")

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], "data.txt"))
                with open('C:/test/data.txt', 'r') as file:
                    data = file.read().replace('\n', '')
                compress.compressing(data)
                socket.send(encoded_message)

        return
    @socket.on('message')
    def handle_message(msg):
        socket.send("test")


    @socket.on('receive_file')
    def handle_file(file):
        socket.send("testfile")

    @socket.on('receive_json')
    def handle_the_json(json):
        print('received json: ' + str(json))

    if __name__ == "__main__":
        socket.run(app)

    return app