from config import db_config
from flask import Flask, jsonify
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


@app.route('/items/<parent>', methods=['GET'])
def get_children(parent):
    parent = int(parent)
    sql = 'SELECT id, title, child_count AS childCount, value, weight, volume, total_value AS totalValue, ' \
          'total_weight AS totalWeight, total_volume AS totalVolume FROM items_with_sums WHERE id=%d'
    cursor.execute(sql, (parent,))
    result = cursor.fetchall()
    return jsonify({'items': result})


if __name__ == '__main__':
    app.run()
