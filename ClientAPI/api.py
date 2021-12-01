"""
The example is based on https://www.flaskapi.org/ with modification
"""

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flaskext.mysql import MySQL
mysql = MySQL()
app = FlaskAPI(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'data_staff'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config["DEBUG"] = True
mysql.init_app(app)

clients = {}


def client_get_all():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('SELECT * FROM client')
    rows = cur.fetchall()
    for row in rows:
        index = row[0]  # assign to key
        name = row[1]  # assign to client name
        clients[index] = name
    con.commit()
    cur.close()
    con.close()
    return clients
    print("clients: " + str(len(clients)))


def client_display(key):
    return {
        'all': request.host_url.rstrip('/api/resources/clients'),  # link to all clients
        'link': request.host_url.rstrip('/api/resources/clients') + url_for('clients_detail', key=key),
        'client': clients[key]
    }


@app.route("/", methods=['GET', 'POST'])
def clients_list():
    """
    List or create clients.
    """
    if request.method == 'POST':
        con = mysql.connect()
        cur = con.cursor()
        client = str(request.data.get('client', ''))
        index = len(clients.keys()) + 1
        clients[index] = client
        cur.execute('INSERT INTO client (id, name)VALUES( %s, %s)', (index, client))
        con.commit()
        print("add a new client to the table")
        return client_display(index), status.HTTP_201_CREATED
        cur.close()
        con.close()
    elif request.method == 'GET':
        client_get_all()
        return [client_display(index) for index in sorted(clients.keys())]


@app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def clients_detail(key):
    """
    Retrieve, update or delete clients instances.
    """
    con = mysql.connect()
    cur = con.cursor()
    request.host_url.rstrip('/')
    if request.method == 'PUT':
        name = str(request.data.get('client', ''))
        clients[key] = name
        cur.execute('UPDATE client SET name=%s WHERE id=%s', (name, key))
        con.commit()
        print("update the client table")
        return client_display(key)

    elif request.method == 'DELETE':
        clients.pop(key, None)
        cur.execute('DELETE FROM client WHERE id=%s', key)
        con.commit()
        print("delete the client from the table")
        if len(clients) ==0:
            return request.host_url.rstrip('/api/resources/clients')
        else:
            return [client_display(index) for index in sorted(clients.keys())], status.HTTP_204_NO_CONTENT

    elif request.method == 'GET':
        if key not in clients:
            raise exceptions.NotFound()
            client_get_all()
        else:
            return client_display(key)

    cur.close()
    con.close()


if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
