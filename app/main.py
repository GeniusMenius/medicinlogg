# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from collections import defaultdict
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mediciner.db"
db = SQLAlchemy(app)

# 💊 Tabeller
class Medicin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100), unique=True, nullable=False)
    gräns_i_timmar = db.Column(db.Integer, default=24)
    färgklass = db.Column(db.String(20), default="standard")
    visa_nästa_dos = db.Column(db.Boolean, default=True)

class Intag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100))
    tidpunkt = db.Column(db.DateTime, default=datetime.now)

class Profil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100), nullable=False)

# 📦 Initiera databasen
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
    mediciner = Medicin.query.order_by(Medicin.namn).all()

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
                           profil=profil,
                           mediciner=mediciner)

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
    profil = Profil.query.first()
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

    return render_template("index.html",
                           mediciner=mediciner,
                           senaste=senaste,
                           datetime=datetime,
                           profil=profil)

# ⚙️ Inställningar
@app.route("/inställningar", methods=["GET", "POST"])
def inställningar():
    mediciner = Medicin.query.order_by(Medicin.namn).all()
    profil = Profil.query.first()

    if request.method == "POST":
        form = request.form

        if "profilnamn" in form:
            profil.namn = form.get("profilnamn") or "Användare"
            db.session.commit()

        elif "radera_id" in form:
            medicin = Medicin.query.get(int(form["radera_id"]))
            db.session.delete(medicin)
            db.session.commit()

        elif "ändra_id" in form:
            medicin = Medicin.query.get(int(form["ändra_id"]))
            medicin.namn = form.get("namn")
            medicin.färgklass = form.get("färgklass") or "standard"

            if "vid_behov" in form:
                medicin.gräns_i_timmar = 0
                medicin.visa_nästa_dos = False
            else:
                medicin.gräns_i_timmar = int(form.get("gräns") or 24)
                medicin.visa_nästa_dos = "visa_nästa_dos" in form

            db.session.commit()

        else:
            namn = form.get("namn")
            färg = form.get("färgklass") or "standard"

            if "vid_behov" in form:
                gräns = 0
                visa_dos = False
            else:
                gräns = int(form.get("gräns") or 24)
                visa_dos = "visa_nästa_dos" in form

            if namn:
                db.session.add(Medicin(
                    namn=namn,
                    gräns_i_timmar=gräns,
                    färgklass=färg,
                    visa_nästa_dos=visa_dos
                ))
                db.session.commit()

        return redirect("/inställningar")

    return render_template("inställningar.html",
                           mediciner=mediciner,
                           profil=profil)

# 🚀 Kör appen
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
