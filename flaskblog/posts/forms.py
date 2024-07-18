from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class NewPost(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=50)])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")