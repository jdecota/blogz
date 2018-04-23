from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:deco2545@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key='424323gfdgf'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__ (self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__ (self, username, password):
        self.username = username
        self.password = password

@app.before_request               
def require_login():
    allowed_routes = ['login','signup','blog']
    if request.endpoint not in allowed_routes and "username" not in session:    #if email KEY is not in session dictionary
        return redirect('/login')

@app.route('/')
def index():
        users = User.query.all()
        return render_template('index.html', users=users)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['username'] = username
            flash('Logged in')
            return redirect('/newpost')
        
        else:
            flash('INCORRECT USERNAME OR PASSWORD')

    return render_template('login.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  
        verify = request.form['verify']   

        existing_user = User.query.filter_by(username=username).first()

        if (username.strip() == '' 
            or password.strip() == ''
            or verify.strip() == ''):
            flash('ONE OR MORE FIELDS ARE INVALID')

        if password != verify:
            flash('PASSWORDS DO NOT MATCH')

        if len(username) < 3:
            flash('INVALID USERNAME')

        if len(password) < 3:
            flash('INVALID PASSWORD')
    
        if existing_user:
            flash("USERNAME ALREADY EXISTS")

        if not existing_user:   
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/signup')

    return render_template('signup.html')

@app.route('/blog')
def blog():
    if request.args.get('id'):
        blog_id = int(request.args.get('id'))
        single_id = Blog.query.get(blog_id)
        return render_template('Blog-single.html', blog=single_id)

    blogs = Blog.query.all()
    return render_template('blog.html',blogs=blogs)

@app.route('/singleuser')
def singleuser():
    if request.method == 'GET':
        user_id = int(request.args.get('id'))
        user = User.query.filter_by(id=user_id).first()
        blogs = Blog.query.filter_by(owner_id=user_id)

        return render_template('singleUser.html', blogs=blogs, user=user)

@app.route('/newpost', methods=['GET','POST'])
def newpost():

    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['blog_body']
        owner = User.query.filter_by(username=session['username']).first()

        if body and title:
            new_post = Blog(title,body,owner)
            db.session.add(new_post)
            db.session.commit()
            return redirect ('/blog?id='+str(new_post.id))

        if not body or not title:
            flash("Text Required In All Fields")
    return render_template('newpost.html')

@app.route('/logout')
def logout():
    del session['username']
    flash('Successfully Logged Out')
    return redirect ('/login')

if __name__ == '__main__':
    app.run()