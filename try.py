import psycopg

conn = psycopg.connect("postgresql://postgres:sumpumm@localhost/chat_history")
print("Connection successful")
conn.close()