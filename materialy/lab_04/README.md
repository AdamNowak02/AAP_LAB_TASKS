# lab_04 — Instrukcja uruchomienia

Krótko: w tym folderze znajdują się rozwiązania zadań z Lab 04:

- `zadanie_1.ipynb` — zapis 30 użytkowników z RandomUser do PostgreSQL (jeśli ustawisz `DATABASE_URL`) lub fallback do SQLite.
- `zadanie_2.ipynb` — pobranie sieci z GeckoTerminal i zapis do MongoDB (jeśli ustawisz `MONGO_URI`) lub fallback do JSON.
- `zadanie_3_bonus.ipynb` — demonstracja pgvector; jeśli brak PG/pgvector, używa numpy jako fallback.
- `run_zadanie_1.py`, `run_zadanie_2.py`, `run_zadanie_3.py` — proste skrypty uruchamiające logikę fallbackową (łatwe do uruchomienia bez Jupyter).

Wymagania (zalecane): Python 3.8+, virtualenv.

Instalacja (PowerShell):

```powershell
& .venv\Scripts\Activate.ps1
python -m ensurepip --upgrade
pip install --upgrade pip
pip install nbconvert nbformat nbclient requests numpy
# opcjonalnie dla prawdziwych DB:
pip install psycopg2-binary pymongo
```

Uruchomienie (fallbacks):

```powershell
python materialy/lab_04/run_zadanie_1.py
python materialy/lab_04/run_zadanie_2.py
python materialy/lab_04/run_zadanie_3.py
```

Uruchomienie notebooków (wykonane kopie zapisywane w folderze):

```powershell
python -m nbconvert --to notebook --execute materialy/lab_04/zadanie_1.ipynb --output-dir materialy/lab_04
python -m nbconvert --to notebook --execute materialy/lab_04/zadanie_2.ipynb --output-dir materialy/lab_04
python -m nbconvert --to notebook --execute materialy/lab_04/zadanie_3_bonus.ipynb --output-dir materialy/lab_04
```

Zmienne środowiskowe (opcjonalne):
- `DATABASE_URL` — np. `postgresql://user:pass@host:5432/dbname` (jeśli chcesz użyć Postgres zamiast SQLite)
- `MONGO_URI` — np. `mongodb://user:pass@host:27017/` (jeśli chcesz użyć MongoDB zamiast JSON)

Uwagi:
- Dodałem notebooki i małe runnery; lokalnie przetestowałem fallbacky (SQLite/JSON/numpy) i wyniki zostały zweryfikowane.
