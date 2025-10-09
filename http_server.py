from flask import Flask, request, send_file, abort

app = Flask(__name__)

@app.route('/', methods=['POST'])
def download():
    file_path = "payloadk-mitm.apk"
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        abort(404)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
