# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from collections import defaultdict
import os

# 🚀 Skapa app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mediciner.db"
app.config["SECRET_KEY"] = "micha-hemlig-nyckel"  # 🔐 Sessionsnyckel
db = SQLAlchemy(app)

# 🔐 Setup Flask–Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Omdirigera till /login om ej inloggad

# 🧍 Användarmodell
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    lösenord = db.Column(db.String(255), nullable=False)
    namn = db.Column(db.String(100), nullable=False, default="Micha")

# 💊 Mediciner kopplade till användare
class Medicin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100), nullable=False)
    gräns_i_timmar = db.Column(db.Integer, default=24)
    färgklass = db.Column(db.String(20), default="standard")
    visa_nästa_dos = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 🔗 Kopplad till user

# 📋 Dosintag kopplade till användare
class Intag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100))
    tidpunkt = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

# 🔐 Ladda användare från session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 📦 Initiera databas och demoanvändare (om inte finns)
with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="demo@demo.se").first():
        demo = User(email="demo@demo.se", namn="Micha", lösenord=generate_password_hash("1234"))
        db.session.add(demo)
        db.session.commit()

# 🏠 Startsida – medicinschema (endast egna mediciner)
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    mediciner = Medicin.query.filter_by(user_id=current_user.id).all()
    senaste = {}

    for med in mediciner:
        senaste_intag = Intag.query.filter_by(namn=med.namn, user_id=current_user.id).order_by(Intag.tidpunkt.desc()).first()
        if senaste_intag:
            senaste[med.namn] = senaste_intag.tidpunkt

    if request.method == "POST":
        for med in mediciner:
            if request.form.get(med.namn):
                db.session.add(Intag(namn=med.namn, user_id=current_user.id))
        db.session.commit()
        return redirect("/")

    return render_template("index.html",
                           mediciner=mediciner,
                           senaste=senaste,
                           datetime=datetime)

# 📘 Loggvy – visar endast egna intag
@app.route("/logg")
@login_required
def logg():
    intag = Intag.query.filter_by(user_id=current_user.id).order_by(Intag.tidpunkt.desc()).all()
    return render_template("logg.html", intag=intag)

# 📊 Statistik – personligt filtrerad
@app.route("/statistik")
@login_required
def statistik():
    intervall = request.args.get("intervall", "vecka")
    diagramtyp = request.args.get("diagramtyp", "bar")
    mediciner = Medicin.query.filter_by(user_id=current_user.id).order_by(Medicin.namn).all()

    nu = datetime.now()
    gräns = nu - timedelta(days=7 if intervall == "vecka" else 30 if intervall == "månad" else 365)

    intag = Intag.query.filter(Intag.tidpunkt >= gräns, Intag.user_id == current_user.id).all()
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
                           mediciner=mediciner)

# 🧹 Rensa senaste intag (endast egna)
@app.route("/rensa_senaste")
@login_required
def rensa_senaste():
    senaste = Intag.query.filter_by(user_id=current_user.id).order_by(Intag.tidpunkt.desc()).limit(1).all()
    for rad in senaste:
        db.session.delete(rad)
    db.session.commit()
    return redirect("/logg")

# ⚙️ Inställningar för mediciner och profil
@app.route("/inställningar", methods=["GET", "POST"])
@login_required
def inställningar():
    mediciner = Medicin.query.filter_by(user_id=current_user.id).order_by(Medicin.namn).all()

    if request.method == "POST":
        form = request.form

        if "profilnamn" in form:
            current_user.namn = form.get("profilnamn") or "Användare"
            db.session.commit()

        elif "radera_id" in form:
            medicin = Medicin.query.get(int(form["radera_id"]))
            if medicin and medicin.user_id == current_user.id:
                db.session.delete(medicin)
                db.session.commit()

        elif "ändra_id" in form:
            medicin = Medicin.query.get(int(form["ändra_id"]))
            if medicin and medicin.user_id == current_user.id:
                medicin.namn = form.get("namn")
                medicin.färgklass = form.get("färgklass") or "standard"
                medicin.gräns_i_timmar = 0 if "vid_behov" in form else int(form.get("gräns") or 24)
                medicin.visa_nästa_dos = "visa_nästa_dos" in form
                db.session.commit()

        else:
            namn = form.get("namn")
            färg = form.get("färgklass") or "standard"
            gräns = 0 if "vid_behov" in form else int(form.get("gräns") or 24)
            visa_dos = False if "vid_behov" in form else "visa_nästa_dos" in form

            if namn:
                ny = Medicin(namn=namn,
                             gräns_i_timmar=gräns,
                             färgklass=färg,
                             visa_nästa_dos=visa_dos,
                             user_id=current_user.id)
                db.session.add(ny)
                db.session.commit()

        return redirect("/inställningar")

    return render_template("inställningar.html",
                           mediciner=mediciner,
                           profilnamn=current_user.namn)

# 👤 Inloggning
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        lösen = request.form.get("lösenord")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.lösenord, lösen):
            login_user(user)
            return redirect("/")
    return render_template("login.html")

# 👤 Registrering
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        namn = request.form.get("namn")
        lösen = generate_password_hash(request.form.get("lösenord"))
        if not User.query.filter_by(email=email).first():
            db.session.add(User(email=email, namn=namn, lösenord=lösen))
            db.session.commit()
            return redirect("/login")
    return render_template("register.html")

# 👤 Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

# 🚀 Kör appen
if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 7000))
    app.run(host="0.0.0.0", port=port)
