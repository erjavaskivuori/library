## Kirjasto

Tietokantasovellukseni on luotu kirjaston käyttämiseen ja hallintaan.

Sovelluksella on seuraavat toiminallisuudet:

Kuka tahansa sivulla voi:
- Nähdä kaikki kirjastossa olevat kirjat
- Nähdä kirjan oman sivun, jossa on tarkempia tietoja kirjasta sekä sille annetut arvostelut
- Hakea kirjoja teoksen nimen, kirjailijan, kategorian tai julkaisuvuoden perusteella
- Luoda uuden tunnuksen

Käyttäjä voi:
- Kirjautua sisään ja ulos
- Lainata ja palauttaa kirjoja
- Antaa arvosteluja kirjoille
- Toivoa uusia kirjoja

Kirjaston työntekijä voi:
- Antaa arvosteluja kirjoille
- Lisätä ja poistaa kirjoja
- Nähdä kirjatoiveet ja toiveen esittäjän käyttäjänimen
- Nähdä lainassa olevat kirjat ja lainaajan käyttäjänimen

Sovellusta voi testata seuraavien ohjeiden avulla:

1. Kloonaa repositorio

2. Luo repositorioon .env-tiedosto, johon lisäät seuraavat muuttujat:
´´´
DATABASE_URL=postgresql:///user     # user tilalle oma psql-käyttäjänimi
SECRET_KEY=                         # luo oma secret key
´´´

3. Luo ´schema.sql´ mukaiset taulut komennolla:
´´´
psql < schema.sql
´´´

4. Asenna vaadittavat riippuvuudet komennolla:
´´´
pip install requirements.txt
´´´

5. Aktivoi virtuaaliympäristö komennolla:
´´´
source venv/bin/activate
´´´

6. Käynnistä sovellus komennolla:
´´´
flask run
´´´