from decimal import Decimal

import stringcase

from config import db_config
from flask import Flask, jsonify, request
from flask_cors import CORS
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
app.config.from_object(__name__)

# TODO: Restrict CORS
CORS(app, resources={r'/*': {'origins': '*'}})

mysql = MySQL(autocommit=True, cursorclass=DictCursor)
app.config |= db_config
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


def convert_value(value: object):
    if isinstance(value, Decimal):
        return str(value)
    return value


def query(sql: str, *values):
    cursor.execute(sql, values)
    return [dict((stringcase.camelcase(key), convert_value(value)) for key, value in rows.items()) for rows in
            cursor.fetchall()]


@app.route('/items/<parent>', methods=['GET'])
def get_children(parent):
    sql = 'SELECT * FROM items_with_sums WHERE parent=%s'
    return jsonify({'items': query(sql, parent)})


@app.route('/items', methods=['GET'])
def all_items():
    sql = 'SELECT id, title FROM items WHERE id > 1'
    return jsonify({'items': query(sql)})


@app.route('/details/<item>', methods=['GET'])
def get_details(item):
    sql = 'SELECT * FROM items WHERE id=%s'
    return jsonify({'item': query(sql, item)[0]})


@app.route('/item/<item>', methods=['PUT'])
def update_item(item):
    post_data = request.get_json()
    sql = 'UPDATE items SET parent=%s, title=%s, description=%s, acquired=%s, basis=%s, value=%s, value_as_of=%s, ' \
          'weight=%s, d1=%s, d2=%s, d3=%s, upc=%s WHERE id=%s'
    cursor.execute(sql, (post_data.get('parent'), post_data.get('title'), post_data.get('description'),
                         post_data.get('acquired'), post_data.get('basis'), post_data.get('value'),
                         post_data.get('valueAsOf'), post_data.get('weight'), post_data.get('d1'),
                         post_data.get('d2'), post_data.get('d3'), post_data.get('upc'), item))
    return "Did it?"


if __name__ == '__main__':
    app.run()
