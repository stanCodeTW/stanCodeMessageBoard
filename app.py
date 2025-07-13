from flask import Flask, request, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import os

app = Flask(__name__)

# Debug DATABASE_URL and connection
database_url = os.environ.get('DATABASE_URL')
print(f"DATABASE_URL: {database_url}")
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Test database connection
try:
    engine = create_engine(database_url)
    with engine.connect() as conn:
        print("Database connection successful!")
except OperationalError as e:
    print(f"Database connection failed: {e}")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    msg = db.Column(db.Text, nullable=False)
    time = db.Column(db.String(100), nullable=False)

HTML = """
<!doctype html>
<html>
<head>
    <title>stanCode 簡易留言板</title>
</head>
<body>
    <h1>stanCode 簡易留言板</h1>
    <form method='post'>
        <p>
            <label>暱稱：<input name='name' required></label>
        </p>
        <p>
            <label>留言：<br><textarea name='msg' required></textarea></label>
        </p>
        <p>
            <button type='submit'>送出</button>
        </p>
    </form>
    
    <h2>留言列表：</h2>
    <hr>
    {% for ele in messages %}
    <p>
    <strong>{{ ele.name }}</strong> 說：
    </p>
    <blockquote>{{ ele.msg }}</blockquote>
    <p style="font-size: 0.9em; color: gray;">
    {{ ele.time }}
    </p>
    {% endfor %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    with app.app_context():
        # Debug table existence
        print("Checking if 'message' table exists...")
        table_exists = db.engine.dialect.has_table(db.engine, 'message')
        print(f"Table exists: {table_exists}")
        if not table_exists:
            print("Creating 'message' table...")
            try:
                db.create_all()
                print("Table creation successful!")
            except Exception as e:
                print(f"Table creation failed: {e}")
        if request.method == 'POST':
            name = request.form.get('name', "").strip()
            msg = request.form.get('msg', '').strip()
            if name and msg:
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_msg = Message(name=name, msg=msg, time=time)
                db.session.add(new_msg)
                db.session.commit()
            return redirect('/')
        elif request.method == 'HEAD':
            return '', 200
        all_messages = Message.query.order_by(Message.id.desc()).all()
        return render_template_string(HTML, messages=all_messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
