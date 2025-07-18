from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mediciner.db"
db = SQLAlchemy(app)

# --- Datamodeller ---
class Medicin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100), unique=True, nullable=False)
    gräns_i_timmar = db.Column(db.Integer, default=24)
    färgklass = db.Column(db.String(20), default="standard")

class Intag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100))
    tidpunkt = db.Column(db.DateTime, default=datetime.now)

# --- Skapa tabeller i rätt kontext ---
with app.app_context():
    db.create_all()





# 📜 Visa logg
@app.route("/logg")
def logg():
    intag = Intag.query.order_by(Intag.tidpunkt.desc()).all()
    return render_template("logg.html", intag=intag)

# 📊 Veckostatistik (senaste 7 dagar)
@app.route("/statistik")
def statistik():
    gräns = datetime.now() - timedelta(days=7)
    data = defaultdict(int)
    intag = Intag.query.filter(Intag.tidpunkt >= gräns).all()
    for rad in intag:
        data[rad.namn] += 1
    return render_template("statistik.html", data=data)


@app.route("/rensa_senaste")
def rensa_senaste():
    senaste = Intag.query.order_by(Intag.tidpunkt.desc()).limit(1).all()
    for rad in senaste:
        db.session.delete(rad)
    db.session.commit()
    return redirect("/logg")

@app.route("/", methods=["GET", "POST"])
def index():
    mediciner = Medicin.query.all()
    senaste = {}

    for med in mediciner:
        senaste_intag = Intag.query.filter_by(namn=med.namn).order_by(Intag.tidpunkt.desc()).first()
        if senaste_intag:
            senaste[med.namn] = senaste_intag.tidpunkt

    if request.method == "POST":
        for med in mediciner:
            if request.form.get(med.namn):
                db.session.add(Intag(namn=med.namn))
        db.session.commit()
        return redirect("/")

    return render_template("index.html", mediciner=mediciner, senaste=senaste, datetime=datetime)


@app.route("/inställningar", methods=["GET", "POST"])
def inställningar():
    if request.method == "POST":
        if "radera_id" in request.form:
            medicin = Medicin.query.get(int(request.form["radera_id"]))
            db.session.delete(medicin)
            db.session.commit()
        elif "ändra_id" in request.form:
            medicin = Medicin.query.get(int(request.form["ändra_id"]))
            medicin.namn = request.form.get("namn")
            medicin.gräns_i_timmar = int(request.form.get("gräns") or 24)
            medicin.färgklass = request.form.get("färgklass") or "standard"
            db.session.commit()
        else:
            namn = request.form.get("namn")
            gräns = int(request.form.get("gräns") or 24)
            färg = request.form.get("färgklass") or "standard"
            if namn:
                db.session.add(Medicin(namn=namn, gräns_i_timmar=gräns, färgklass=färg))
                db.session.commit()

        return redirect("/inställningar")

    mediciner = Medicin.query.order_by(Medicin.namn).all()
    return render_template("inställningar.html", mediciner=mediciner)







if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
