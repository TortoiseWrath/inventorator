from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

# TODO: Restrict CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/items/<parent>', methods=['GET'])
def get_children(parent):
    parent = int(parent)
    return jsonify({'items': [
        {
            'title': 'Item Title',
            'childCount': 0 if parent > 5 else 1,
            'value': 300.53,
            'weight': 388.9,
            'volume': 19398,
            'id': parent + 1,
        },
    ]})


if __name__ == '__main__':
    app.run()
