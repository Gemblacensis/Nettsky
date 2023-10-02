from flask import Flask, render_template, request, redirect, jsonify
import psycopg2
import redis
import subprocess

subprocess.run(['pip', 'install', '-r', '/requirements.txt'])

app = Flask(__name__)
redis_client = redis.Redis(
    host='cache',
    port=6379,
    decode_responses=True
)

@app.route('/')
def redirecting():
    redis_client.set('entrycounter', 0)
    return redirect('/index')


@app.route('/index', methods=['GET','POST'])
def hello_world():
    conn = psycopg2.connect(
        host='postgres',
        database='group02_db',
        user='group02',
        password='pw1234'
    )
    if request.method == 'POST':
        conn = psycopg2.connect(
        host='postgres',
        database='group02_db',
        user='group02',
        password='pw1234'
        )
        data = request.form["input_data"]
        c = conn.cursor()
        c.execute(f"INSERT INTO table2 (data) VALUES ('{data}');")
        conn.commit()
        c.execute(f'SELECT data FROM table2 ORDER BY data LIMIT 1;')
        data2 = c.fetchone()[0]
        c.close()
        conn.close()
        return jsonify({"data": data2})
    create_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO table1 (name) VALUES ('harald');")
    conn.commit()
    redis_client.incr('entrycounter')
    #select_query = f'SELECT data FROM table2 ORDER BY data DESC LIMIT 1;'   
    #select_query = f'SELECT data FROM table2 WHERE id = 1;'
    select_query = f'SELECT name FROM table1 WHERE id = 1;'
    cursor.execute(select_query)
    person_name = cursor.fetchone()[0]  
    cursor.close()
    conn.close()
    return render_template('index.html', data=person_name)

@app.route('/entrycount')
def entrycounter():
    #pagevisit_value = redis_client.incr('pagevisit')
    counter = redis_client.get('entrycounter')
    return render_template('redis.html', counter=counter)


def create_db():
    conn = psycopg2.connect(
        host='postgres',
        database='group02_db',
        user='group02',
        password='pw1234'
    )
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS table2;')
    conn.commit()
    c.execute('CREATE TABLE table2 (id serial PRIMARY KEY, data VARCHAR(50));')
    conn.commit()

    c.execute('DROP TABLE IF EXISTS table1;')
    conn.commit()
    c.execute('CREATE TABLE table1 (id serial PRIMARY KEY, name VARCHAR(50));')
    conn.commit()

    c.close()
    conn.close()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
