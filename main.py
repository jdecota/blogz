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
def blog_list():
    if request.args.get('id'):
        blog_id = int(request.args.get('id'))
        single_id = blog.query.get(blog_id) 
        return render_template('Blog-single.html', blog=single_id )
    blogs = blog.query.all() 
    return render_template('blog.html',blogs=blogs)

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
            return redirect ('/blog?id='+str(new_post.id))
        if not body and not title:
            flash("Text Required In All Fields")
    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()