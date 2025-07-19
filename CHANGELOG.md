# 📘 Changelog – Medicinlogg

Alla större ändringar och förbättringar i Micha-appen dokumenteras här.

---

## [v1.3.0] – 2025-07-19

### ✨ Nytt
- Inför `base.html` som grundmall för alla sidor → enklare layout och färre dupliceringar
- Visuellt mörkt/ljust läge med ikonväxling och lokal lagring via `localStorage`
- Funktion för att markera mediciner som “💤 Vid behov”
- Backend tolkar “Vid behov” och undviker gränsvarningar, men behåller statistik
- “Senaste intag” visas med datum/klockslag för behovsmediciner
- Statistik visar “💭”-notis för behovsmediciner direkt i tabellen
- Tillägg av `Dockerfile`, `.dockerignore` och push till Docker Hub (`geniusmenius/medicinlogg:dev`)
- README.md med appbeskrivning och installationssteg

### 🧼 Fix
- HTML-fel med script-in-script i gamla `statistik.html`
- Rensat duplicerade script från varje sida, nu i gemensam mall

---

## [v1.2.0] – Tidigare version

### 🛠 Funktioner
- Registrering av medicinintag via formulär
- Spara senaste intag i databas
- Visuell dosgräns–indikator med färgklass
- Statistik i Chart.js
- Inställningssida för profil och mediciner
