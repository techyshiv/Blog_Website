from flask import Flask,render_template,request,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin,logout_user
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///mydb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']="thisismyname"
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    author = db.Column(db.String(50),nullable=False)
    content = db.Column(db.Text(),nullable=False)
    publish_date=db.Column(db.DateTime(),nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return '<Blog %r>' % self.title

@app.route("/")
def index():
    data = Blog.query.all()
    return render_template("index.html",data=data)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register_user",methods=['GET','POST'])
def register_user():
    if request.method == "POST":
        email=request.form.get("email")
        password=request.form.get("password")
        fname=request.form.get("firstname")
        lname=request.form.get("lastname")
        username=request.form.get("username")
        users=User.query.all()
        user_list=[users[i].username for i in range(len(users))]
        if username not in user_list: 
            user=User(username=username,email=email,fname=fname,lname=lname,password=password)
            db.session.add(user)
            db.session.commit()
            flash("User has been registered successfully",'success')
            return redirect("/login")
        else:
            return("This username already used")
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_users",methods=['GET','POST'])
def login_users():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user=User.query.filter_by(username=username).first()
        if user and password==user.password:
            login_user(user)
            return redirect("/")
        else:
            flash("Invalid Credentials","danger")
            return redirect("/login")

@app.route("/blogpost")
def blogpost():
    return render_template("blog.html")

@app.route("/user_post",methods=["GET","POST"])
def user_post():
    if request.method=="POST":
        title=request.form.get("title")
        author=request.form.get("author")
        content=request.form.get("content")
        blog=Blog(title=title,author=author,content=content)
        db.session.add(blog)
        db.session.commit()
        flash("Your Post Has been submitted successfully","success")
        return redirect("/")
    return render_template("blog.html")

@app.route("/blog_detail/<int:id>")
def blog_detail(id):
    blog = Blog.query.get(id)
    return render_template("blog_detail.html",blog=blog)

@app.route("/delete/<int:id>")
def delete(id):
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    flash("Post has been deleted","success")
    return redirect("/")

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    blog = Blog.query.get(id)
    if request.method=="POST":
        blog.title=request.form.get("title")
        blog.author=request.form.get("author")
        blog.content=request.form.get('content')
        db.session.commit()
        flash("Blog details has benn updated successfully","success")
        return redirect("/")
    return render_template("edit.html",blog=blog)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)