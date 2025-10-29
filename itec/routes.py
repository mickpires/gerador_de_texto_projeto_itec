from flask import render_template, url_for, redirect, request
from itec import app
from itec.forms import RequestPromptForm

def simulacao(prompt):
    if prompt == '5G':
        title = 'A Revolução do 5G'
        content = '''
        A tecnologia 5G promete velocidades de internet sem precedentes. Isso permitirá avanços em áreas como realidade aumentada e medicina remota.

    Além da velocidade, a baixa latência do 5G possibilitará novas aplicações. Estamos à beira de uma transformação digital ainda maior.
        '''
    elif prompt == 'fisica':
        title = 'buraco negro'
        content = 'relatividade e é os guri'
    return title, content


@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
    form  = RequestPromptForm()
    if form.validate_on_submit():
        title, content = simulacao(form.prompt.data)
        return render_template('home.html', form = form, title = title, content = content)
    return render_template('home.html', form = form, title = None, content = None)
