from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(10000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/newpost', methods=['GET', 'POST'])
def create_newpost():

    blog_title = ''
    blog_body = ''
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
                error_body = 'wrong'

            elif len(blog_body) > 10000:
                error_body = 'long'

            else:
                blog_post = Blog(blog_title, blog_body)
                db.session.add(blog_post)
                db.session.commit()
                blog_id = blog_post.id;

                return redirect("/blog?id=" + str(blog_id) +'&title=' + blog_title + '&body=' + blog_body)

    return render_template('new-post.html', error_title=error_title, error_body=error_body)


@app.route('/', methods=['GET', 'POST'])
@app.route('/blog')
def display_posts():

    blog_post = Blog.query.all()

    blog_id = request.args.get('id')

    if not blog_id:
        return render_template('blog.html', blogs=blog_post)

    else:
        blog_title = request.args.get('title')
        blog_body = request.args.get('body')

        return render_template('blog.html', blog_id=blog_id, blog_title=blog_title, blog_body=blog_body)


    # blog_post = db.session.query(Blog.title).first()
    # blog_post = Blog.query.get(1)
    # blog_title = blog_post.title;



@app.route('/', methods=['POST', 'GET'])
def index():

    blog_posts = Blog.query.all()
    return render_template('blog.html', posts=blog_posts)


if __name__ == '__main__':
    app.run()
