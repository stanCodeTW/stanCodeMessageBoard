from flask import Flask, request, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///messages.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
    <form>
    
    <h2>留言列表：</h2>
    <hr>
    {% for ele in messages %}
    <p>
    <strong>{{ele.name}}</strong> 說：
    </p>

    <blockquote>{{ele['msg']}}</blockquote>

    <p style="font-size: 0.9em; color: gray;">
    {{ele.time}}
    </p>

    {% endfor %}
</body>
</html>
"""

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        name = request.form.get('name', "").strip()
        msg = request.form.get('msg', '').strip()
        if name and msg:
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_msg = Message(name=name, msg=msg, time=time)
            db.session.add(new_msg)
            db.session.commit()
        return redirect('/')
    all_messages = Message.query.order_by(Message.id.desc()).all()
    return render_template_string(HTML, messages=all_messages)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
