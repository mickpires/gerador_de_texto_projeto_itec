from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired

class RequestPromptForm(FlaskForm):
    token = StringField('token', validators=[DataRequired()])
    prompt = TextAreaField('prompt', validators=[DataRequired()])
    submit = SubmitField("processar")