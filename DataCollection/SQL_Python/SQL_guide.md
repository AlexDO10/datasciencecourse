# SQL in Python — How It Works & Tips

## Overview

Python doesn't have a single "SQL library" — it uses a layered system:

| Layer                 | Purpose                                            | Example Libraries                |
| --------------------- | -------------------------------------------------- | -------------------------------- |
| **DBAPI2 drivers**    | Low-level connection to a specific database engine | `pymysql`, `psycopg2`, `sqlite3` |
| **Abstraction / ORM** | Unified interface across databases                 | `SQLAlchemy`, `pandas`           |



## Common Libraries

### `sqlite3` (built-in)

No installation needed. Great for local, file-based databases.

```python
import sqlite3

conn = sqlite3.connect("mydb.db")   # creates file if not exists
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
conn.commit()
conn.close()
```

---

### `pymysql`

Connects to **MySQL / MariaDB** databases.

```python
import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="secret",
    database="mydb"
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
conn.close()
```

---

### `pandas` + SQL

`pd.read_sql()` lets you run a query and get results directly as a **DataFrame**.

```python
import pandas as pd
import pymysql

conn = pymysql.connect(host="localhost", user="root", database="mydb")
df = pd.read_sql("SELECT * FROM users WHERE age > 25", conn)
conn.close()
print(df.head())
```

---

### `SQLAlchemy` (recommended for production)

A powerful ORM and connection manager that works with **any database**.

```python
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("mysql+pymysql://user:password@localhost/mydb")

with engine.connect() as conn:
    df = pd.read_sql("SELECT * FROM users", conn)

print(df.head())
```

> ✅ **Tip:** Pandas officially recommends using SQLAlchemy connections over raw DBAPI2 objects to avoid `UserWarning`.

---

## General Workflow

```
1. Connect      →   establish a connection to the database
2. Query        →   send SQL via cursor.execute() or pd.read_sql()
3. Fetch        →   retrieve results (fetchone, fetchall, or DataFrame)
4. Commit       →   save changes for INSERT/UPDATE/DELETE
5. Close        →   always close the connection when done
```

---

## Tips

### ✅ Always close your connection

Use a `try/finally` block or a context manager to ensure the connection is closed even if an error occurs:

```python
try:
    conn = pymysql.connect(...)
    df = pd.read_sql("SELECT 1", conn)
finally:
    conn.close()
```

Or with SQLAlchemy:

```python
with engine.connect() as conn:
    df = pd.read_sql("SELECT 1", conn)
# connection is automatically closed here
```

---

### ✅ Use parameterized queries (avoid SQL injection)

Never format user input directly into SQL strings.

```python
# ❌ Dangerous
cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")

# ✅ Safe
cursor.execute("SELECT * FROM users WHERE name = %s", (user_input,))
```

---

### ✅ Use `fetchall()` vs `fetchone()` wisely

- `fetchone()` — retrieves a single row (memory efficient for large results)
- `fetchall()` — retrieves all rows at once (convenient for small results)
- `pd.read_sql()` — best when you want to work with data in a DataFrame

---

### ✅ Connecting to remote databases (e.g., UCSC Genome)

Some public databases allow read-only access without a password:

```python
import pymysql
import pandas as pd

conn = pymysql.connect(
    host="genome-mysql.cse.ucsc.edu",
    user="genome",
    database="hg19"
)

df = pd.read_sql("SELECT * FROM affyU133Plus2 WHERE misMatches BETWEEN 1 AND 3", conn)
conn.close()

print(df["misMatches"].quantile([0, 0.25, 0.5, 0.75, 1.0]))
```

---

### ✅ Common SQL commands to know

```sql
SHOW DATABASES;                          -- list all databases
SHOW TABLES;                             -- list all tables in current DB
DESCRIBE tableName;                      -- show columns/types of a table
SELECT * FROM table LIMIT 10;            -- preview first 10 rows
SELECT col FROM table WHERE col = val;   -- filter rows
SELECT * FROM table WHERE x BETWEEN a AND b;  -- range filter
```

---

## Quick Reference

| Task                  | Code                                                |
| --------------------- | --------------------------------------------------- |
| Connect (MySQL)       | `pymysql.connect(host=..., user=..., database=...)` |
| Run query → DataFrame | `pd.read_sql("SELECT ...", conn)`                   |
| Run query → raw rows  | `cursor.execute(...); cursor.fetchall()`            |
| Close connection      | `conn.close()`                                      |
| Get quantiles         | `df["col"].quantile([0, 0.25, 0.5, 0.75, 1.0])`     |
