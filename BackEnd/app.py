from flask import Flask
app = Flask(__name__)


@app.route('/hola-mundo')
def hello_world():
    return 'La api esta funcionando!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)