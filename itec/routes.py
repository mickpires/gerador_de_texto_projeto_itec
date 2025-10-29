from flask import render_template
from itec import app
from itec.forms import RequestPromptForm
from itec.crew import article_creater_crew

@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
    form  = RequestPromptForm()
    if form.validate_on_submit():
        inputs = {'prompt': form.prompt.data}
        results = article_creater_crew.kickoff(inputs = inputs)
        title, content = results['title'], results['content']
        return render_template('home.html', form = form, title = title, content = content)
    return render_template('home.html', form = form, title = None, content = None)
