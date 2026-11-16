"""Run every query in sql/queries.sql against data/exeter_ai.db and cache results for make_query_library.py."""
import pathlib, re, sqlite3
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
sql = (ROOT / "sql" / "queries.sql").read_text()
blocks = {re.match(r"-- @name: (\w+)", b).group(1): b
          for b in re.split(r"(?=^-- @name: )", sql, flags=re.M) if b.startswith("-- @name")}
con = sqlite3.connect(ROOT / "data" / "exeter_ai.db")
results = {name: pd.read_sql_query(q, con) for name, q in blocks.items()}
pd.to_pickle(results, ROOT / "sql" / "results.pkl")
for name, df in results.items():
    print(f"{name}: {len(df)} rows")
