# Uzdevuma rezultāts

## Projekta palaišana lokāli

### Priekšnosacījumi

Lai palaistu projektu lokāli, nepieciešams:

* **Python 3.12**
* **uv**
* **Docker / Docker Compose**
* **Node.js** un npm — frontend palaišanai

---

# 1. Backend

Visas tālāk norādītās komandas jāizpilda no `backend/` direktorijas.

### 1.1. Python vides izveide

Izveido Python virtuālo vidi un instalē visas projektam nepieciešamās bibliotēkas:

```bash
cd backend
uv sync
```

`uv sync` izmanto projektā definēto `pyproject.toml` un `uv.lock`, lai izveidotu virtuālo vidi un instalētu nepieciešamās atkarības.

---

### 1.2. PostgreSQL datu glabātuves palaišana

Datu glabāšanai tiek izmantots **PostgreSQL**, kas tiek palaists Docker konteinerī.

```bash
docker compose up -d postgres
```

> **Pamatojums:** PostgreSQL izmantošana iekš Docker kā datu glabātuvi atvieglo projekta lokālo izstrādi un testēšanu, kā arī nodrošina vidi, kas ir tuvāka tipiskai produkcijas konfigurācijai Linux serverī.

---

### 1.3. Datubāzes struktūras izveide

Pielieto projektā iekļautās datubāzes migrācijas:

```bash
uv run alembic upgrade head
```

Migrācijas izveidošanai projekta izstrādes laikā tika izmantota komanda:

```bash
uv run alembic revision --autogenerate -m "datu glabātuves struktūras izveide"
```

> Šo komandu projekta pirmreizējās palaišanas laikā **nav nepieciešams izpildīt**, jo nepieciešamā migrācija jau ir iekļauta koda repozitorijā.

---

### 1.4. XML testa datu ielāde

Tiek simulēta datu saņemšana no hipotētiska attālināta XML avota un iegūtie dati tiek saglabāti PostgreSQL datubāzē:

```bash
uv run python -m data.seed_service
```

Darbības princips:

1. ģenerē testa dokumentu datus;
2. izveido pieprasīto XML struktūru;
3. simulē XML datu saņemšanu no attālināta avota;
4. parsē XML datus;
5. validē tos ar Pydantic modeļiem;
6. saglabā dokumentus PostgreSQL datubāzē.

---

### 1.5. Backend API palaišana

Startē FastAPI serveri:

```bash
uv run uvicorn app:app --host 0.0.0.0 --port 8081
```

API dokumentācija pieejama:

**http://127.0.0.1:8081/docs**

Backend nodrošina piekļuvi saglabātajiem dokumentiem, izmantojot REST API.

---

# 2. Frontend

Frontend ir izveidots, izmantojot **Vite** un vanilla JavaScript.

Visas tālāk norādītās komandas jāizpilda no `frontend/` direktorijas:

```bash
cd frontend
npm install
npm run dev
```

Pēc `npm run dev` izpildes terminālī tiks parādīta frontend lietotnes adrese, piemēram:

```text
http://localhost:5173/
```

Frontend ielādē dokumentus no backend API un nodrošina:

* dokumentu attēlošanu tabulā;
* meklēšanu pēc nosaukuma un apraksta;
* filtrēšanu pēc kategorijas, svarīguma, faila tipa un statusa;
* šķirošanu pēc tabulas laukiem;
* datu atsvaidzināšanu (refresh).

---

# 3. Automatizētie testi

Backend automatizētajiem testiem tiek izmantots **pytest**.

Testi atrodas `backend/tests/` direktorijā.

Pašlaik testos tiek pārbaudīti:

* XML dokumentu parsēšana;
* API parametru validācija;
* nederīga `limit` vērtība;
* pārāk liela `limit` vērtība;
* negatīva `offset` vērtība.

### 3.1. Testu palaišana

Visas komandas jāizpilda no `backend/` direktorijas:

```bash
cd backend
uv run pytest
```

Veiksmīgas izpildes gadījumā terminālī tiks parādīts līdzīgs rezultāts:

```text
...
4 passed in 1.15s
```

---

# 4. Īsā palaišanas instrukcija

Ja nepieciešams ātri palaist visu projektu no jaunas vides:

### Backend

```bash
cd backend

uv sync
docker compose up -d postgres
uv run alembic upgrade head
uv run python -m data.seed_service
uv run uvicorn app:app --host 0.0.0.0 --port 8081
```

### Frontend

Atsevišķā terminālī:

```bash
cd frontend
npm install
npm run dev
```

### Automatizētie testi

Atsevišķā terminālī:

```bash
cd backend
uv run pytest
```

---

# 5. Projekta struktūra

Projekta struktūra:

```text
.
├── backend/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── seed_service.py
│   │   └── xml_generate.py
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── database.py
│   ├── migrations/
│   │   └── versions/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   └── enums.py
│   ├── modules/
│   │   └── settings.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   └── test_seed_service.py
│   ├── app.py
│   ├── alembic.ini
│   ├── docker-compose.yml
│   ├── .env
│   ├── .python-version
│   ├── .gitignore
│   ├── pyproject.toml
│   └── uv.lock
│
└── frontend/
    ├── src/
    │   ├── main.js
    │   └── style.css
    ├── .gitignore
    ├── index.html
    ├── package.json
    ├── package-lock.json
    └── vite.config.js
```
