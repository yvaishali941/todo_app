from flask import Flask,render_template,request,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config['SECRET_KEY'] = 'secret@123'
db = SQLAlchemy(app)


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80),nullable=False)
    desc=db.Column(db.String(80),nullable=False)
    date=db.Column(db.DateTime(80),nullable=False , default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.title


@app.route("/",methods=['GET','POST'])
def todo():
    if request.method=="POST":
        title=request.form.get('title')
        desc=request.form.get('desc')
        todo=User(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    allTodo=User.query.all()
    return render_template("home.html",allTodo=allTodo)

@app.route("/todo_update/<int:id>",methods=['GET','POST'])
def update(id):
    todo=User.query.get(id)
    if request.method=="POST":
        todo.title=request.form.get('title')
        todo.desc=request.form.get('desc')
        db.session.commit()
        flash('Post has been updated successfully', 'success')
        return redirect('/')

    return render_template('update.html',todo=todo)


@app.route("/todo_delete/<int:id>")
def delete(id):
    todo = User.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    flash('Post has been deleted successfully', 'danger')
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True,port=7000)