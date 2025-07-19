# Changelog

Alla större ändringar i detta projekt dokumenteras här.

## [Unreleased]

### Docker & Containerisering
- Uppdaterad `Dockerfile` så hela `app/` kopieras, men utan att inkludera `mediciner.db`
- Lagt till `.dockerignore` med korrekt sökväg `app/instance/mediciner.db` för att förhindra att databasen följer med i bild
- Skapat separata volymnamn för dev och prod (`medicin_dev_data`, `medicin_prod_data`)
- Förbättrad `docker-compose.yml` med Portainer–kompatibelt upplägg och portstyrning via `FLASK_PORT`
- Dev–stacken körs på port `7171`, prod körs på `5000` förtillfället
- Volym `app/instance` används för att persistera SQLite–databasen
- Volymen rensas vid behov för att starta dev från tom databas

### Flask-applikationen
- Ändrat `main.py` så Flask startar på port från miljövariabel: `os.environ.get("FLASK_PORT", 7000)`
- Databasen skapas automatiskt endast om den saknas (`mediciner.db`)
- Lagt till möjlighet att köra flera miljöer (local, dev, prod) parallellt utan portkrock

### Deployment & Git
- Förberett pushflöde för dev–imagen till Docker Hub med tydlig taggning (`medicinlogg:dev`)
- Genomfört manual push efter rensning av `.dockerignore` och rebuild av image

### UI / Web (planerat)
- Förberett flytt av knappar till undersidan via CSS `position: fixed; bottom: 0;` (ej implementerat ännu)
- Beslut att commit skickas först innan frontend–ändringar

## [2025-07-19] - Initial Setup

- Startade projektet med grundläggande Flask-app
- Första Docker–imagen skapad
- SQLite–databas `mediciner.db` byggs automatiskt om den saknas
