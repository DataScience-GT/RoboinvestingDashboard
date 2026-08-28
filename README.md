# Roboinvesting

Student investing research project for **Data Science at Georgia Tech (DS@GT)**. This repository is the club’s working copy of a dashboard, chatbot, and related market-research experiments — not a live trading product, not a broker, and not a source of investment returns.

The public club site describes Roboinvesting as an active project around **ML-driven trading simulations and technical indicators**. What is in this repo today is earlier than that description: a Streamlit UI, a small OpenAI-backed chat API, exploratory notebooks (Polygon / sentiment), and a toy order-book demo. Treat Home-page copy that mentions PyTorch, LangChain, or MACD as **aspirational**; those libraries and signals are not implemented in the current code.

**Educational use only.** Do not use this software to make financial decisions.

---

## Current status (Fall 2026)

| | |
| --- | --- |
| **Status** | Active DS@GT project for Fall 2026 |
| **This repo** | [DataScience-GT/RoboinvestingDashboard](https://github.com/DataScience-GT/RoboinvestingDashboard) — org working copy |
| **Forked from** | [AndrewHlavacek/RoboinvestingDashboard](https://github.com/AndrewHlavacek/RoboinvestingDashboard) on 2026-08-28 by [aamoghS](https://github.com/aamoghS) |
| **Project lead** | Andrew Hlavacek — `ahlavacek6@gatech.edu` (confirmed via club email) |
| **Recruiting** | About **4–6 new members** across three tracks: Dashboard, Backtesting, Investor Personas |
| **Club** | [datasciencegt.org](https://datasciencegt.org/) · `hello@datasciencegt.org` |
| **Director of Projects** | Samantha Forero — `sforeror3@gatech.edu` |
| **President** | Aamogh Sawant |
| **Meetings / events** | After **6:30 PM ET** |

The club website has also listed **Brandon Michaels** (`bjmichaels.25@gmail.com`) as a Roboinvesting contact. Treat Andrew as the current email-confirmed lead. Brandon may be a prior or site-listed contact; do not assume a current role beyond that.

Issues are **disabled** on this GitHub repo. Use pull requests and email (below) instead of filing issues here.

---

## What is in the code (honest snapshot)

| Area | What actually exists | What does **not** exist |
| --- | --- | --- |
| **Dashboard** | Streamlit app: Home, Login, Chatbot, Learn, Assets | Production auth, persisted users, deployed site |
| **Chat** | Flask `POST /api/chat` → OpenAI `gpt-3.5-turbo` with a finance-assistant system prompt. Optional Spring Boot clone of the same endpoint | Tool-using / agentic trading, portfolio queries against real accounts |
| **Assets page** | Yahoo Finance via `yfinance`: price history, MA 5/20, RSI(14), 20-day annualized volatility; lightweight next-day sketches (kNN, EMA, linear trend, simple average) | Live orders, broker APIs, claimed backtest performance |
| **Login / Learn** | Login validates email format and password length in-session only (SHA-256 of the password is computed and discarded). Learn is a “coming soon” stub | Real accounts, Mongo-backed auth (that lives only in the deprecated Node app) |
| **Market data notebooks** | Polygon OHLCV / S&P 500 fetchers; a merge notebook that also pulls FRED-style macros | A packaged data pipeline or shared database |
| **Sentiment** | VADER and FinBERT Twitter-scrape scripts; an SVM experiment notebook and a `.pkl` model | Wired into the Streamlit UI |
| **Execution** | Hardcoded AAPL/MSFT dummy book; writes two sample fills to JSON; basic price stats | A backtester, fills against real or historical markets, strategy engine |
| **Old website** | React + Vite frontend and Express/Mongo sketches under `website (deprecated)/` | Current product surface |

There are **no** Robinhood, Alpaca, or other broker integrations in this repository.

---

## Repo layout

```
.
├── website_streamlit/          # Current UI + chat backend (start here)
│   ├── Main.py                 # Streamlit shell (tabs)
│   ├── pages/                  # Home, Login, Chatbot, Learn, Assets
│   ├── backend_server.py       # Flask chat API on :8080
│   ├── start_backend.sh        # Loads .env, then runs Flask
│   ├── start_backend.py        # Alternate Flask launcher
│   ├── test_api_key.py         # Live OpenAI quota/key check (not a unit test)
│   ├── requirements.txt
│   ├── .streamlit/config.toml
│   └── springboot_backend/     # Optional Java clone of /api/chat
├── Polygon/                    # Polygon.io notebooks (OHLCV, S&P 500)
├── polygonAPI.ipynb            # Extra Polygon notebook at repo root
├── openai.ipynb                # Early OpenAI playground notebook
├── Sentiment Model/            # VADER, FinBERT, SVM notebook + pickle
├── execution/                  # Toy order book + stats (not a backtester)
│   ├── order_book_sim.py
│   ├── analytics.py
│   ├── execution_algos.py      # Empty placeholder
│   ├── simulate_execution.ipynb
│   ├── data/fake_market_data.csv
│   └── outputs/executed_trades.json
└── website (deprecated)/       # Older React/Vite + Express/Mongo prototype
```

```text
Browser  →  Streamlit (Main.py, :8501)
                │
                ├── Assets.py  →  Yahoo Finance (yfinance), no API key in code
                └── Chatbot.py →  HTTP POST http://localhost:8080/api/chat
                                      │
                                      ▼
                                 Flask (backend_server.py)
                                      │
                                      ▼
                                 OpenAI Chat Completions (gpt-3.5-turbo)

Optional: springboot_backend exposes the same /api/chat shape (Maven / Spring Boot 2.7).
Notebooks and Sentiment Model/ are standalone; they are not imported by the Streamlit app.
```

---

## Setup, run, and test

**Language:** Python 3.10–3.12 is a reasonable target (notebooks in git were run on 3.10/3.11; `start_backend.py` prefers 3.12 if present). **Package manager:** `pip` + `website_streamlit/requirements.txt`. There is no `pyproject.toml`, Conda env file, Docker setup, or CI config.

### 1. Clone and virtualenv

```bash
git clone https://github.com/DataScience-GT/RoboinvestingDashboard.git
cd RoboinvestingDashboard
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r website_streamlit/requirements.txt
```

**Assets page extra:** `pages/Assets.py` imports `yfinance`, which is **not** listed in `requirements.txt`. Install it before using that tab:

```bash
pip install yfinance
```

Sentiment / Polygon notebooks need additional packages (`nltk`, `transformers`, `selenium`, `beautifulsoup4`, `polygon-api-client`, `ta`, `python-dotenv`, etc.) installed as you run those files. They are not in the Streamlit requirements file.

### 2. Secrets (names only)

Copy the example env file and fill in **your** keys. Never commit `.env` (it is gitignored).

```bash
cp .env.example .env
# Chatbot: also copy into the Streamlit folder if you use start_backend.sh
cp .env.example website_streamlit/.env
```

| Variable | Used by |
| --- | --- |
| `OPENAI_API_KEY` | `website_streamlit/backend_server.py`, `test_api_key.py`, `start_backend.sh`, `openai.ipynb`; Spring property `openai.api.key` |
| `POLYGON_API_KEY` | `Polygon/polygon.ipynb`, `Polygon/s&p.ipynb` (via `python-dotenv`) |

The deprecated Node app expected `MONGO_URI` if you revive it. Some older notebooks also call third-party macro APIs with keys inlined in cells — do not copy those; use env vars and rotate anything that was ever committed.

`backend_server.py` reads `OPENAI_API_KEY` from the **process environment**. It does not call `load_dotenv()` itself. Either export the variable, or start Flask with `start_backend.sh` (which sources `website_streamlit/.env`).

### 3. Run the dashboard

**Terminal A — chat backend (needed only for the Chatbot tab):**

```bash
cd website_streamlit
chmod +x start_backend.sh
./start_backend.sh
```

Or:

```bash
cd website_streamlit
export OPENAI_API_KEY=...    # if not using the shell script
python backend_server.py
```

Flask listens on **http://localhost:8080**. Routes in code:

- `POST /api/chat` — JSON `{"message": "..."}` → `{"reply": "..."}`
- `GET /health` — `{"status": "ok"}`

**Terminal B — Streamlit:**

```bash
cd website_streamlit
streamlit run Main.py
```

Default Streamlit URL is **http://localhost:8501**.

### 4. Optional Spring Boot chat backend

Same `/api/chat` contract, Java 8+ / Maven, Spring Boot **2.7.10**:

```bash
cd website_streamlit/springboot_backend
mvn spring-boot:run
```

Point the key via `openai.api.key` (environment / local properties). Do not commit keys. The Streamlit Chatbot page is hardcoded to `http://localhost:8080/api/chat`, so only one backend should bind that port.

### 5. Tests

There is **no** pytest/unittest suite and no GitHub Actions workflow.

| Check | How |
| --- | --- |
| OpenAI key / quota | `python website_streamlit/test_api_key.py` (live API call) |
| Flask up | `curl http://localhost:8080/health` |
| Order-book demo | `python execution/order_book_sim.py` (writes `execution/outputs/executed_trades.json`) |

### 6. Deploy

No Dockerfile, `Procfile`, Streamlit Cloud config, or Vercel project is in this repo. Local `localhost` is the documented run mode. Any hosting plan is future work (see Fall 2026 plan).

### Deprecated website (do not use for new work)

React 18 + Vite 6 frontend (`npm install` / `npm run dev` under `website (deprecated)/frontend`). Express backend expected Node ≥ 18 and `MONGO_URI`. The committed `server.js` in that tree is a Mongo connect helper, not a full HTTP server — treat this tree as archival.

---

## Team tracks (Fall 2026)

Andrew asked for roughly **4–6 people** split across these three tracks. Mapping below is to **this repo**, not to a separate design doc.

### 1. Dashboard

**In the repo.** Primary tree: `website_streamlit/`.

| File | Role |
| --- | --- |
| `Main.py` | Tab shell and shared dark theme |
| `pages/Home.py` | Landing copy (some claims ahead of the code) |
| `pages/Assets.py` | Charts + technicals + toy next-day models |
| `pages/Chatbot.py` | UI client for Flask `/api/chat` |
| `pages/Login.py` | Client-side validation stub |
| `pages/Learn.py` | Placeholder |
| `backend_server.py` | Chat API |
| `utils/auth.py`, `utils/styles.py` | Empty placeholders |

Natural first work: make Assets robust, wire Learn, replace fake login, keep Home copy aligned with reality, add `yfinance` to requirements.

### 2. Backtesting

**Not a backtesting library yet.** Closest existing pieces:

| Path | What it is |
| --- | --- |
| `execution/order_book_sim.py` | Dummy bids/asks; two hardcoded demo trades |
| `execution/analytics.py` | Mean/median/variance helpers on book prices |
| `execution/execution_algos.py` | Empty |
| `execution/data/fake_market_data.csv` | Two synthetic rows (AAPL, MSFT) |
| `pages/Assets.py` | Indicator + next-day sketch models (not a historical strategy backtest) |
| `Polygon/*.ipynb` | Historical OHLCV fetchers you could feed a future engine |

This track is **mostly planned work**: define a bar/event backtest API, replay Polygon (or other) history, report metrics (Sharpe, drawdown, turnover) **from code**, and never invent returns. Do not treat `executed_trades.json` as performance.

### 3. Investor Personas

**Not in the codebase.** No persona configs, risk profiles, or allocation engines. `pages/Learn.py` is an empty educational slot that might eventually explain personas.

This track is **planned work**: specify personas (horizon, risk, constraints), encode them as data the backtester and dashboard can share, and keep them educational — not personalized financial advice.

---

## Fall 2026 next-step plan

Refined from the repo. Items marked **hypothesis** are reasonable club sequencing, not commitments from a written roadmap in git.

1. **Onboarding (week 1)**  
   Join via Andrew / `hello@` (see below). Clone this org repo, run Streamlit + Flask locally, skim `Assets.py` and `backend_server.py`. Pick one track. Meetings/events are after 6:30 PM ET.

2. **First work (no GitHub Issues on this repo)**  
   Coordinate first tasks with Andrew over email or club channels, then open PRs against `main`. Suggested starters by track:  
   - **Dashboard:** add `yfinance` to requirements; tighten Assets edge cases; implement Learn; document Chatbot + backend as one command.  
   - **Backtesting:** design a small engine that reads bars (start from Polygon notebooks / CSV), plug in one naive strategy (e.g. MA crossover) with **computed** stats only.  
   - **Personas:** write a persona schema (JSON/YAML) and one page of educational copy; do not claim optimized portfolios.

3. **Data and API keys**  
   Club/lead should decide shared vs. personal `OPENAI_API_KEY` and `POLYGON_API_KEY`. Yahoo Finance on Assets does not use a key in code. Sentiment scripts scrape Twitter via Selenium — expect breakage and ToS limits; **hypothesis:** prefer a licensed news/sentiment source later.

4. **How the three tracks ship together (hypothesis)**  
   Personas → constraints and defaults. Backtesting → evaluates strategies under those constraints on historical data. Dashboard → charts, Learn, and chat explain the same objects. Share types/schemas early so the UI does not hardcode one-off metrics.

5. **Deploy (hypothesis)**  
   Nothing is deployed from this repo today. A later option is Streamlit Community Cloud or a small VM for Streamlit + Flask, with secrets in the host env — not in git.

6. **Hygiene**  
   Keep secrets out of git. Prefer env vars over `application.properties`. Do not paste backtest “returns” into the README or Home page unless a script in this repo produced them.

---

## How to join

1. **Email the lead:** Andrew Hlavacek, `ahlavacek6@gatech.edu` — say you want Roboinvesting (Dashboard / Backtesting / Investor Personas) for Fall 2026.  
2. **Club inbox:** `hello@datasciencegt.org` (general DS@GT). Project logistics: Samantha Forero, `sforeror3@gatech.edu`.  
3. **This GitHub org repo:** fork or branch, open a **pull request** to `main`. Issues are disabled here.  
4. **Upstream (optional):** [AndrewHlavacek/RoboinvestingDashboard](https://github.com/AndrewHlavacek/RoboinvestingDashboard) is the original dashboard repo this fork was copied from.

Possible prior/site contact: Brandon Michaels, `bjmichaels.25@gmail.com` — not a substitute for emailing Andrew.

Welcome to DS@GT. Read the code, run it locally, and ask Andrew where you fit before writing a large feature.
