import psycopg

hostname='localhost'
database='chat_PDF'
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
    
def create_user_table():
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id SERIAL PRIMARY KEY,
                 username TEXT NOT NULL UNIQUE,
                 email TEXT NOT NULL UNIQUE CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
                 full_name TEXT NOT NULL,
                 password TEXT NOT NULL
                 )
                 
                 ''')
    conn.commit()
    cursor.close()
    conn.close()
    
def get_user(identifier: str):
    conn=db_connection()
    cursor=conn.cursor()
    user={}
    cursor.execute("SELECT * FROM users WHERE username = %s OR email=%s ", (identifier,identifier,))
    for row in cursor.fetchall():
        user={"username" :row[1],"email":row[2],"full_name":row[3],"password" :row[4]}
    cursor.close()
    conn.close()
    return user 

def create_user(username: str,email: str,full_name: str, password: str):
    conn=db_connection()
    cursor=conn.cursor()
    cursor.execute('INSERT INTO users (username,email,full_name,password) VALUES (%s,%s,%s,%s)',(username,email,full_name,password))
    conn.commit()
    cursor.close()
    conn.close()

