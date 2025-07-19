✨ Fleranvändarstöd med Flask–Login + användarspecifik datamodell

- Lagt till användarsystem med Flask–Login (login, logout, register)
- Skapat User–modell med lösenordshashning via Werkzeug
- Kopplat Medicin och Intag–modeller till user_id
- Skyddat alla vyer med @login_required
- Uppdaterat logg, statistik och startsida för användarspecifik visning
- Ny inställningsvy per användare (mediciner + namn)
- Lagt till login.html och register.html i templates/
- Rensat gamla profilmodellen
- Säker initialisering av demo-användare
