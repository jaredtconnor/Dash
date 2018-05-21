import sqlite3 as sql
import pandas as pd

conn = sql.connect("twitter_sentiment.db")

df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE '%trump%' ORDER BY unix DESC LIMIT 1000", con = conn)

df.head()
