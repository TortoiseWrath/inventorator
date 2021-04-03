from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/ping', methods=['GET'])
def pong():
    return jsonify('PONG')


if __name__ == '__main__':
    app.run()
