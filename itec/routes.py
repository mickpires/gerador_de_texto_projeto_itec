from flask import render_template, url_for, redirect, request
from itec import app
from itec.forms import RequestPromptForm

@app.route('/')
@app.route('/home')
def home():
    form  = RequestPromptForm()
    return render_template('home.html', form = form)

@app.route('/processar')
def processar():
    texto = request.form.get('conteudo')
    return f"Você digitou: {texto}"