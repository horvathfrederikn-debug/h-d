from flask import Flask, request, send_file
import io

app = Flask(__name__)

# Itt tároljuk ideiglenesen a legfrissebb képet a memóriában
latest_image = None

@app.route('/upload', methods=['POST'])
def upload():
    global latest_image
    file = request.files.get('image')
    if file:
        latest_image = file.read()
        return "OK", 200
    return "No image", 400

@app.route('/image', methods=['GET'])
def get_image():
    global latest_image
    if latest_image:
        return send_file(
            io.BytesIO(latest_image),
            mimetype='image/jpeg'
        )
    return "No image available", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)