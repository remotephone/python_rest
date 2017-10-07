from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

class Employees(Resource):
    def get(self):
        conn = db_connect.connect() # connect to the database
        # This line performs the query and returns json result
        query = conn.execute("select * from employees")
        return {'employees': [i[0] for i in query.cursor.fetchall()]}


class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d " %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class IT_Staff(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from employees WHERE LIKE('%IT%',title)=1;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Employees, '/employees')
api.add_resource(Tracks, '/tracks')
api.add_resource(Employees_Name, '/employees/<employee_id>')
api.add_resource(IT_Staff, '/itstaff')

if __name__ == '__main__':
    app.run(port='5002', host='0.0.0.0')
