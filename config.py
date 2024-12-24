import psycopg

def db_connection():
    return psycopg.connect("postgresql://postgres:sumpumm@localhost/chat_history")