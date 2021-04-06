from decimal import Decimal

import stringcase
from pymysql import DatabaseError, OperationalError

from config import db_config
from flask import Flask, jsonify, request
from flask_cors import CORS
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
app.config.from_object(__name__)

# TODO: Restrict CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.config |= db_config
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app, autocommit=True)


def convert_value(value: object):
    if isinstance(value, Decimal):
        return str(value)
    return value


def get_cursor():
    return mysql.connect().cursor(DictCursor)


def query(sql: str, *values):
    cursor = get_cursor()
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


def get_fields(post_data, *field_names, selector=None):
    values = []
    for field_name in field_names:
        value = post_data.get(field_name)
        values.append(None if value == '' else value)
    if selector is not None:
        values.append(selector)
    return tuple(values)


@app.route('/item/<item>', methods=['PUT'])
def update_item(item):
    post_data = request.get_json()
    sql = 'UPDATE items SET parent=%s, title=%s, description=%s, acquired=%s, basis=%s, value=%s, value_as_of=%s, ' \
          'weight=%s, d1=%s, d2=%s, d3=%s, upc=%s WHERE id=%s'
    cursor = get_cursor()
    try:
        cursor.execute(sql, get_fields(post_data, 'parent', 'title', 'description', 'acquired', 'basis', 'value',
                                       'valueAsOf', 'weight', 'd1', 'd2', 'd3', 'upc', selector=item))
        add_photos(cursor, item, post_data.get('photos'))
    except DatabaseError as e:
        return jsonify({'error': e.args}), 400
    return jsonify({}), 200


def add_photos(cursor, item, photos):
    if photos is None:
        return
    cursor.execute('DELETE FROM photos WHERE item=%s', item)
    cursor.executemany('INSERT INTO photos VALUES (%s, %s, %s)', [
        (photo, item, index) for index, photo in photos
    ])


if __name__ == '__main__':
    app.run()
