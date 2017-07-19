from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__, static_url_path='/static')

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(20000))
    date = db.Column(db.DateTime)

    def __init__(self, title, body, date=None):
        self.title = title
        self.body = body
        if date is None:
            date = datetime.utcnow()
        self.date = date

@app.route('/newpost', methods=['GET', 'POST'])
def create_newpost():

    error_title = ''
    error_body = ''

    if request.method == 'POST':

        blog_title = request.form['blog-title']
        if not blog_title:
            error_title = "Please fill in the title"
        elif len(blog_title) > 120:
            error_title = "Please take a shorter title"
        else:
            blog_body = request.form['blog-body']
            if not blog_body:
                error_body = 'Please fill in the body'

            elif len(blog_body) > 20000:
                error_body = 'Your blog post exceeds the limit'

            else:
                blog_post = Blog(blog_title, blog_body)
                db.session.add(blog_post)
                db.session.commit()
                blog_id = blog_post.id;
                return redirect("/blog?id=" + str(blog_id))

    return render_template('new-post.html', error_title=error_title, error_body=error_body)

@app.route('/blog', methods=['GET', 'POST'])
def display_posts():

    blog_id = request.args.get('id')
    if  blog_id:

        blog_post = Blog.query.filter_by(id=blog_id).first()
        return render_template('blog.html', blog=blog_post, blog_id=blog_id)

    else:
        blog_posts = Blog.query.all()
        return render_template('blog.html', blogs=blog_posts)

@app.route('/')
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()
