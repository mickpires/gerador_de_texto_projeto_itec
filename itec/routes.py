from flask import render_template
from itec import app
from itec.forms import RequestPromptForm
from itec.crew import gerar_texto

@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
    form  = RequestPromptForm()
    if form.validate_on_submit():
        title, content = gerar_texto(form.prompt.data, form.token.data)
        return render_template('home.html', form = form, title = title, content = content)
    return render_template('home.html', form = form, title = None, content = None)
