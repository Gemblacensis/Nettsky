from flask import Flask, render_template, request, redirect, url_for
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
    redis_client.set('pagevisitcounter', 0)
    return redirect('/index')


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/index')
def memory_page():

    conn = psycopg2.connect(
            host='postgres',
            database='group02_db',
            user='group02',
            password='pw1234'
        )

    c = conn.cursor()

    select_query = 'SELECT * FROM person'
    c.execute(select_query)

    data = c.fetchall()
    c.close()

    redis_client.incr('pagevisitcounter')

    return render_template('memory_page.html', data=data)


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        conn = psycopg2.connect(
            host='postgres',
            database='group02_db',
            user='group02',
            password='pw1234'
        )
        first_name = request.form['first_name']
        surname = request.form['surname']
        description = request.form['description']

        # Insert data into the database
        c = conn.cursor()
        
        c.execute("INSERT INTO person (first_name, surname, description) VALUES (%s,%s,%s)", (first_name,surname,description))
        conn.commit()
        c.close()

        return redirect('/index')


@app.route('/pagevisitcount')
def pagevisitcounter():
    #pagevisit_value = redis_client.incr('pagevisit')
    counter = redis_client.get('pagevisitcounter')
    return render_template('redis.html', counter=counter)


def create_db():
    conn = psycopg2.connect(
        host='postgres',
        database='group02_db',
        user='group02',
        password='pw1234'
    )
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS person (id serial PRIMARY KEY, first_name VARCHAR(50), surname VARCHAR(70), description VARCHAR(300));')
    conn.commit()
    c.close()
    conn.close()

if __name__ == '__main__':
    create_db()
    app.run(host='0.0.0.0', port=80)
