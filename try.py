import psycopg

conn = psycopg.connect("postgresql://postgres:sumpumm@localhost/chat_history")
cursor=conn.cursor()
cursor.execute("SELECT message FROM message_store WHERE session_id = '3684b7f33d4b984515af1ab6ca1466b8'")
messages=[]
for row in cursor.fetchall():
    # print(row,"\n \n")
    messages.append(
        {"role":row[0]["data"]["type"],"content":row[0]["data"]["content"]},
    )
conn.close()

for message in messages:
    print(message,"\n")