# 💊 Medicinlogg

En personlig webbaserad medicinapp som hjälper dig att:

- Logga medicinintag
- Få dosgräns–varningar
- Se statistik och grafer över intag
- Växla mellan mörkt och ljust läge
- Hantera mediciner och inställningar

---

## 🌟 Funktioner

- ✅ Daglig dosregistrering med färgkodad varning
- 📊 Statistik med stöd för stapel-, cirkel- och linjediagram (Chart.js)
- 🌙 Mörkt/ljust läge med lokal lagring via `localStorage`
- 🔧 Profilinställningar och medicinredigering
- 🔐 Lokal lagring, ingen användardata skickas vidare

---

## 🧑‍⚕️ Så använder du Medicinlogg

Medicinlogg är en användarvänlig webbtjänst där du loggar dina mediciner, följer dina dosintervaller och får statistik över hur du följer din behandlingsplan.

Varje användare har sitt eget konto och sin egen medicinvärld – helt privat och lättanvänd!

---

### 🆕 Skapa konto & logga in

Gå till appens startsida:

> 🌐 **https://medicinlogg.se** (eller valfri huvud–URL)

Där kan du:

- 🔐 Logga in med e-post och lösenord
- 🆕 Skapa ett nytt konto via registreringsformulär

💡 För testning finns ett **demo–konto**:
- E-post: `demo@demo.se`
- Lösenord: `1234`

---

### ➕ Lägg till mediciner

Navigera till fliken `⚙️ Inställningar`.

- Skriv medicinens namn
- Välj dosintervall (ex: 6 timmar)
- Välj färgklass för visuell markering (ex: 🔴, 🟢, 🟡)
- Välj om medicinen ska ha dosindikator
- Markera som “vid behov” om dosintervall saknas

Du kan ändra mediciner när som helst – direkt i listan.

---

### 💊 Registrera dosintag

Gå till `🏠 Startsidan`. Där listas dina egna mediciner.

- Tryck på en medicin för att registrera intag
- Medicinen loggas med tidpunkt och namn
- Endast dina egna mediciner visas

---

### 📘 Se logg

Fliken `📘 Logg` visar din doshistorik:

- Senaste intag högst upp
- Visar datum, tid och medicinnamn
- Du kan även radera det senaste intaget

---

### 📊 Statistik

Gå till fliken `📊 Statistik` för att se din personliga medicinanvändning.

- Välj intervall: vecka, månad, år
- Välj diagramtyp: stapel eller cirkel
- Endast dina egna intag analyseras

---

### ⚙️ Inställningar

Under `⚙️ Inställningar` kan du:

- Byta profilnamn
- Lägga till, ändra eller ta bort mediciner
- Ställa in visuell dosindikator
- Markera mediciner som “vid behov”

Allt är kopplat till ditt eget konto – inga andra användare påverkas.

---

### 🔐 Sekretess & säkerhet

- Lösenord lagras krypterat
- Endast du ser dina mediciner och doser
- Sessions hanteras säkert med Flask–Login

---

## 🐳 Docker–installation

För att köra Medicinlogg med Docker, använd följande `docker-compose.yml`:

```yaml
version: '3.8'

services:
  medicinlogg:
    image: geniusmenius/medicinlogg:dev
    container_name: medicinlogg-dev
    ports:
      - "7171:7171"
    environment:
      - FLASK_PORT=7171
    volumes:
      - medicin_data:/app/instance
    restart: unless-stopped

volumes:
  medicin_data:
```
----


🚀 Kom igång
bash
git clone https://github.com/geniusmenius/medicinlogg.git
docker compose up -d


-----
📦 Teknisk info
Backend: Flask + SQLite

Inloggning: Flask–Login

Frontend: Jinja2 + HTML + CSS

Statistik: Chart.js

All data är användarspecifik via user_id


----

🧠 Licens
Projektet är fritt att använda för personligt bruk. Konsultera alltid läkare innan medicinska beslut.


---

👩‍👧 Team
Skapat av Tim Med stöd från Micha & Jonna 👨‍👧‍👧


