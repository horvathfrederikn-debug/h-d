from flask import Flask, jsonify, request

app = Flask(__name__)

latest_image = None
latest_click = {}


@app.route("/upload", methods=["POST"])
def upload():
  global latest_image
  if "image" in request.files:
    latest_image = request.files["image"].read()
    return "OK", 200
  return "No image", 400


@app.route("/image", methods=["GET"])
def get_image():
  global latest_image
  if latest_image:
    return latest_image, 200, {"Content-Type": "image/jpeg"}
  return "No image yet", 404


@app.route("/click", methods=["POST", "GET"])
def handle_click():
  global latest_click
  if request.method == "POST":
    data = request.json
    if data:
      latest_click = data
    return "OK", 200
  else:
    click_data = latest_click
    latest_click = {}  # Töröljük, hogy ne kattintson újra
    return jsonify(click_data), 200


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=10000)