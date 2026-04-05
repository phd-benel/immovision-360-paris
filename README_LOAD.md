# README_LOAD — Data Warehouse Load (PostgreSQL)

## Scope

- **Input (Silver CSV)**: `data/processed/transformed_elysee.csv`
- **Target Data Warehouse**: PostgreSQL
- **Script**: `0.6_load.py`
- **Loaded table**: `elysee_listings_silver` (or your chosen name — keep it consistent)

## 1) Why a Data Warehouse (and not a CSV)

Explain why the data must be loaded into a relational database for:

- SQL queries at scale,
- BI tools (Tableau / Power BI),
- reproducibility and governance (typed schema, centralized truth).

## 2) Environment variables and secrets (.env)

Never commit secrets. Document the required variables and how they are provided:

```text
DB_USER=postgres
DB_PASSWORD=your_secret_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=immovision_db
```

- `.env` must be in `.gitignore`
- Provide a `.env.example` in the repo (no real passwords)

## 3) Connection method (SQLAlchemy)

Describe how `0.6_load.py` connects to PostgreSQL (SQLAlchemy engine) and which driver is used.

## 4) Idempotence strategy

Explain what happens if the script is executed multiple times:

- `if_exists="replace"` (simple and safe for this module), or
- `append` / `UPSERT` (advanced, optional).

## 5) What was loaded (schema overview)

- Table name
- Key columns
- The main enriched AI features loaded (e.g. `Standardization_Score`, `Neighborhood_Impact`, etc.)
- Any type conversions performed (price to numeric, booleans, dates).

## 6) Evidence (screenshot)

Add a screenshot in the GitHub repository showing:

- the database exists (`immovision_db`),
- the table exists (`elysee_listings_silver`),
- row count / preview of columns.

Recommended path:

- `docs/screenshots/postgres_load.png`

And reference in Markdown:

```md
![PostgreSQL Data Warehouse — elysee_listings_silver](docs/screenshots/postgres_load.png)
```

