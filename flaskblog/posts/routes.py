from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.models import Post
from flaskblog.posts.forms import NewPost
from flaskblog import db
from flask_login import current_user, login_required


from flask import Blueprint
posts = Blueprint('posts', __name__)

# posts = [
#     {
#         'author': 'Corey Schafer',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'April 20, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'April 21, 2018'
#     }
# ]

@posts.route("/post/new", methods = ["GET", "POST"])
@login_required
def newpost():
    form = NewPost()
    if form.validate_on_submit():
        post = Post(title = form.title.data, 
                    content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("main.home"))
    return render_template("newpost.html",
                            title= 'new_post', form = form,
                              legend = 'New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    # if post_id is found then post object is returned
    #  or else 404 page not found error
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title= post.title, post = post)

@posts.route("/post/<int:post_id>/update", methods = ["GET", "POST"])
def updatepost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.username != current_user.username:
        # if it is not authorized then 403 unauthorized error
        abort(403)
    form = NewPost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.date_posted = datetime.now()
        db.session.commit()
        flash("Post is successfully updated!",'success')
        return redirect(url_for("posts.post", post_id=post.id))
    if request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("newpost.html",
                            title= post.title, form = form, 
                            legend = "Update Post")


@posts.route("/post/<int:post_id>/delete", methods = ["POST"])
def deletePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.username != current_user.username:
        # if it is not authorized then 403 unauthorized error
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for("main.home"))
    



