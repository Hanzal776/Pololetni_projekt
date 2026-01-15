# Herní Skóre - Flask Aplikace

Jednoduchá webová aplikace na počítání herního skóre postavená na Flask s databází SQLite.

## Funkce

- **Správa hráčů**: Přidávání a mazání hráčů
- **Zaznamenávání skóre**: Záznam skóre pro každého hráče
- **Leaderboard**: Zobrazení hráčů seřazeného podle celkového skóre
- **Statistiky**: Celkové skóre, počet her a průměr skóre pro každého hráče

## Struktura Databáze

### Tabulka Players
- `id` - ID hráče (primární klíč)
- `name` - Jméno hráče (unikátní)
- `total_score` - Celkové skóre
- `games_played` - Počet odehraných her

### Tabulka Scores
- `id` - ID záznamu (primární klíč)
- `player_id` - ID hráče (cizí klíč → Players.id)
- `score` - Zaznamenané skóre
- `game_date` - Datum a čas zaznamenání
- `notes` - Poznámka k zápasu

## Instalace

1. Nainstalujte závislosti:
```bash
pip install -r requirements.txt
```

2. Spusťte aplikaci:
```bash
python app.py
```

3. Otevřete prohlížeč a přejděte na `http://localhost:5000`

## Technologie

- **Backend**: Flask 2.3.3, SQLAlchemy 2.0.21
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## API Endpoints

- `GET /api/players` - Seznam všech hráčů
- `POST /api/players` - Přidat nového hráče
- `DELETE /api/players/<id>` - Smazat hráče
- `POST /api/scores` - Zaznamenat skóre
- `GET /api/players/<id>/scores` - Skóre hráče
- `GET /api/leaderboard` - Leaderboard (seřazeno podle skóre)

## Použití

1. Nejprve přidejte hráče do aplikace
2. Vyberte hráče a zaznamenejte jeho skóre
3. Sledujte aktuální leaderboard s medailemi pro top 3 hráče
