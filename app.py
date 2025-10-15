from flask import Flask, render_template, request, redirect, url_for
from models import db, Todo

app = Flask(__name__)

# --- データベース設定 ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- DB初期化（テーブル作成） ---
with app.app_context():
    db.create_all()

# --- ルート設定 ---

@app.route('/')
def index():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_content = request.form['task']
    new_task = Todo(task=task_content)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

# ✅ 完了ボタンのルート
@app.route('/complete/<int:id>')
def complete(id):
    task = Todo.query.get_or_404(id)
    task.complete = not task.complete  # True/Falseを切り替え
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
