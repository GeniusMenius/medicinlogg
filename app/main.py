# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from collections import defaultdict
import os

# 🚀 Skapa Flask-appen och konfigurera databasen
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mediciner.db"
db = SQLAlchemy(app)

# 💊 Tabell: Medicin
class Medicin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100), unique=True, nullable=False)
    gräns_i_timmar = db.Column(db.Integer, default=24)
    färgklass = db.Column(db.String(20), default="standard")
    visa_nästa_dos = db.Column(db.Boolean, default=True)

# 🕒 Tabell: Intag
class Intag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100))
    tidpunkt = db.Column(db.DateTime, default=datetime.now)

# 👤 Tabell: Profil
class Profil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100), nullable=False)

# 📦 Initiera databasen vid första körning
with app.app_context():
    if not os.path.exists("mediciner.db"):
        db.create_all()
        db.session.add(Profil(namn="Användare"))
        db.session.commit()

# 📘 Loggsida
@app.route("/logg")
def logg():
    intag = Intag.query.order_by(Intag.tidpunkt.desc()).all()
    profil = Profil.query.first()
    return render_template("logg.html", intag=intag, profil=profil)

# 📊 Statistikvy
@app.route("/statistik")
def statistik():
    intervall = request.args.get("intervall", "vecka")
    diagramtyp = request.args.get("diagramtyp", "bar")
    profil = Profil.query.first()

    nu = datetime.now()
    if intervall == "månad":
        gräns = nu - timedelta(days=30)
    elif intervall == "år":
        gräns = nu - timedelta(days=365)
    else:
        gräns = nu - timedelta(days=7)

    intag = Intag.query.filter(Intag.tidpunkt >= gräns).all()

    data = defaultdict(int)
    for rad in intag:
        data[rad.namn] += 1

    labels = list(data.keys())
    värden = list(data.values())

    return render_template("statistik.html",
                           data=data,
                           labels=labels,
                           värden=värden,
                           intervall=intervall,
                           diagramtyp=diagramtyp,
                           profil=profil)

# 🧹 Rensa senaste intaget
@app.route("/rensa_senaste")
def rensa_senaste():
    senaste = Intag.query.order_by(Intag.tidpunkt.desc()).limit(1).all()
    for rad in senaste:
        db.session.delete(rad)
    db.session.commit()
    return redirect("/logg")

# 🏠 Startsidan – medicinschema
@app.route("/", methods=["GET", "POST"])
def index():
    mediciner = Medicin.query.all()
    senaste = {}
    profil = Profil.query.first()

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

    return render_template("index.html", mediciner=mediciner, senaste=senaste, datetime=datetime, profil=profil)

# ⚙️ Inställningar – namn & mediciner
@app.route("/inställningar", methods=["GET", "POST"])
def inställningar():
    mediciner = Medicin.query.order_by(Medicin.namn).all()
    profil = Profil.query.first()

    if request.method == "POST":
        if "profilnamn" in request.form:
            profil.namn = request.form.get("profilnamn") or "Användare"
            db.session.commit()

        elif "radera_id" in request.form:
            medicin = Medicin.query.get(int(request.form["radera_id"]))
            db.session.delete(medicin)
            db.session.commit()

        elif "ändra_id" in request.form:
            medicin = Medicin.query.get(int(request.form["ändra_id"]))
            medicin.namn = request.form.get("namn")
            medicin.gräns_i_timmar = int(request.form.get("gräns") or 24)
            medicin.färgklass = request.form.get("färgklass") or "standard"
            medicin.visa_nästa_dos = bool(request.form.get("visa_nästa_dos"))
            db.session.commit()

        else:
            namn = request.form.get("namn")
            gräns = int(request.form.get("gräns") or 24)
            färg = request.form.get("färgklass") or "standard"
            visa_dos = bool(request.form.get("visa_nästa_dos"))
            if namn:
                db.session.add(Medicin(
                    namn=namn,
                    gräns_i_timmar=gräns,
                    färgklass=färg,
                    visa_nästa_dos=visa_dos
                ))
                db.session.commit()

        return redirect("/inställningar")

    return render_template("inställningar.html", mediciner=mediciner, profil=profil)

# 🚀 Kör appen
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
