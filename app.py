from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# app init
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# init marshmallow
ma = Marshmallow(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    salary = db.Column(db.Integer)

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'salary')


Employee_schema = EmployeeSchema()
Employees_schema = EmployeeSchema(many=True)

# Create
@app.route('/employee/new', methods=['POST'])
def addEmployee():
    name = request.json['name']
    salary = request.json['salary']

    new_employee = Employee(name, salary)

    db.session.add(new_employee)
    db.session.commit()

    return Employee_schema.jsonify(new_employee)


# Get ALL
@app.route('/employee', methods=['GET'])
def getAllEmployees():
    all_employee = Employee.query.all()
    result = Employees_schema.dump(all_employee)
    return jsonify(result)

# Get one
@app.route('/employee/<id>', methods=['GET'])
def getEmployee(id):
    employee = Employee.query.get(id)
    return Employee_schema.jsonify(employee)

# Update
@app.route('/employee/<id>', methods=['PUT'])
def edit_employee(id):
    updated_employee = Employee.query.get(id)
    updated_employee.name = request.json['name']
    updated_employee.salary = request.json['salary']

    db.session.add(updated_employee)
    db.session.commit()

    return Employee_schema.jsonify(updated_employee)


# Delete
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    employee_to_delete = Employee.query.get(id)
    db.session.delete(employee_to_delete)
    db.session.commit()

    return Employee_schema.jsonify(employee_to_delete)


# Run server
if __name__ == "__main__":
    app.run(debug=True)
