@app.route('/hello')
def hello():
    r = requests.get('http://www.google.com')
    return r.text