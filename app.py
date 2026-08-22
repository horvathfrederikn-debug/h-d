from flask import Flask, request

app = Flask(__name__)

# Itt tároljuk a parancsot és a választ
tarolo = {"parancs": "", "valasz": ""}


@app.route("/kuld", methods=["POST"])
def parancsot_fogad():
  adat = request.json
  tarolo["parancs"] = adat.get("parancs", "")
  return "OK"


@app.route("/leker", methods=["GET"])
def parancsot_keres():
  return tarolo["parancs"]


@app.route("/valasz", methods=["POST"])
def valaszt_fogad():
  adat = request.json
  tarolo["valasz"] = adat.get("valasz", "")
  return "OK"


@app.route("/eredmeny", methods=["GET"])
def valaszt_keres():
  return tarolo["valasz"]


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=10000)