import psycopg

hostname='localhost'
database='chat_history'
username='postgres'
pwd='sumpumm'
port_id=5432

def db_connection():
    return psycopg.connect(
                            host=hostname,
                            dbname=database,
                            user=username,
                            password=pwd,
                            port=port_id
                           )

def create_logs():
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS application_logs 
                 (id SERIAL PRIMARY KEY,
                 session_id TEXT,
                 user_query TEXT,
                 response TEXT,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                     
                 )
                 
                 ''')
    conn.commit()
    cursor.close()
    conn.close()

def insert_log(session_id,user_query,response):
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('INSERT INTO application_logs (session_id,user_query,response) VALUES (%s,%s,%s)',(session_id,user_query,response))
    conn.commit()
    cursor.close()
    conn.close()

def get_chat_history(session_id):
    conn = db_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT user_query,response FROM application_logs WHERE session_id = %s ORDER BY created_at", (session_id,)) 
    messages=[]
    for row in cursor.fetchall():
        messages.extend([
            {"role":"human","content":row[0]},
            {"role":"ai","content":row[1]},
            ])
    cursor.close()
    conn.close()
    return messages
    
    
# print(get_chat_history("15ae3f98f29f99cb8a0bb569a0fda399"))