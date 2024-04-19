from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')

def index():
    data = {
    "title": "Proyecto MPI4py",
    "datos": [1,2,3,4,5]
}
    return render_template('index.html', data=data)

@app.route('/web')

def web():
    data = {
    "title": "Web Scrapping",
    "datos": [1,2,3,4,5]
}
    return render_template('web.html', data=data)

#---------------------------------------------------------------------

@app.route('/binary')

def binary():
    data = {
    "title": "Binary Search",
    "datos": [1,2,3,4,5]
}
    return render_template('binary.html', data=data)

@app.route('/binaryres', methods=["POST"])

def binaryres():
    array = request.form['datos']
    data = {
    "title": "Binary Search",
    "datos": array
}
    return render_template('binaryres.html', data=data)

#---------------------------------------------------------------------

@app.route('/quick')

def quick():
    data = {
    "title": "Quick Sort",
    "datos": [1,2,3,4,5]
}
    return render_template('quick.html', data=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True)