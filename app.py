from flask import Flask, request, redirect, render_template_string
from datetime import datetime

app = Flask(__name__)

messages = []
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

@app.route('/', methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        name = request.form.get('name', "").strip()
        msg = request.form.get('msg', '').strip()
        if name and msg:
           time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
           messages.append({'name': name, 'msg': msg, 'time': time})
        return redirect('/')
    return render_template_string(HTML, messages=messages)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
