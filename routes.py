from flask import Flask, url_for, request, render_template
from app import app
import redis
import os

AZURE_ACCESS_KEY = os.environ.get('AZURE_ACCESS_KEY')

r = redis.StrictRedis(host='mvaflask.redis.cache.windows.net',port=6380,password=AZURE_ACCESS_KEY,ssl=True, charset='utf-8', decode_responses=True)

@app.route('/')
def hello():
  createLink = "<a href='" + url_for('create') + "'>Create a question</a>"
  return """<html>
              <title>Devin's Trivia Game</title>
                <body>
                  <h1>Hello World!!!</h1>
                  """ + createLink + """
                </body
              </html>"""

@app.route('/create', methods=['GET', 'POST'])
def create():
  if request.method == 'GET':
    return render_template('CreateQuestion.html')
  elif request.method == 'POST':
    title = request.form['title']
    question = request.form['question']
    answer = request.form['answer']

    r.set(title+':question', question)
    r.set(title+':answer', answer)
    

    return render_template('CreatedQuestion.html', question = question)
  else:
    return '<h2>Bad Request</h2>'

@app.route('/question/<title>', methods=['GET', 'POST'])
def question(title):
  if request.method == 'GET':
    # question = 'Question here...'
    question = r.get(title+':question')
    return render_template('AnswerQuestion.html', question = question)
  elif request.method == 'POST':
    submittedAnswer = request.form['submittedAnswer']
    answer = r.get(title+':answer')
    if submittedAnswer == answer:
      return render_template('Correct.html')
    else:
      return render_template('Incorrect.html', submittedAnswer = submittedAnswer)
  else:
    return '<h2>' + title + '</h2>'