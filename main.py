from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:deco2545@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key='424323478'
class blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(200))

    def __init__ (self, title, body):
        self.title = title
        self.body = body

@app.route('/blog')
def redirect_blog():
    return redirect ('/')

@app.route('/newpost', methods=['GET','POST'])
def new_post():

    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['blog_body']
        if body and title:
            new_post = blog(title,body)
            db.session.add(new_post)
            db.session.commit()
            return redirect ('/')
        if not body and not title:
            flash("Text Required In All Fields")
    return render_template('newpost.html')

#  Else:
 #       return redirect('/')
    #   blogs = blog.query.all()   
    #   blog_title = blog.title
    #   blog_body = blog.body
    #return """ <a href="localhost:5000 """

@app.route('/', methods=['GET','POST'])
def index():

    blogs = blog.query.all() 
    return render_template('blog.html',blogs=blogs)  #variable for for loop

if __name__ == '__main__':
    app.run()