import boto3
from botocore.exceptions import NoCredentialsError
from flask import Flask,jsonify,request



app=Flask(__name__)

# DynamoDB connection setup for region 'ap-south-1'
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('organization')

# Parent class: Department
class Department: # super class
    def __init__(self, dept_name):
        self._dept_name = dept_name  # Encapsulation (data hiding)

    def get_dept_name(self):
        return self._dept_name

    # Method to save department details in DynamoDB
    def save_department(self):
        try:
            table.put_item(
                Item={
                    'PK': f'DEP#{self._dept_name}',
                    'SK': f'DEPT',
                    'Name': self._dept_name,
                    'Role': 'Department'
                }
            )
            print(f"Department '{self._dept_name}' saved successfully.")
        except NoCredentialsError:
            print("Credentials not available.")

# Child class: Employee inherits Department (Inheritance)
class Employee(Department):
    def __init__(self, emp_name, emp_role, dept_name):
        super().__init__(dept_name)  # Calling the parent class constructor
        self.__emp_name = emp_name  # Encapsulation
        self.__emp_role = emp_role  # Encapsulation

    # Polymorphism: Overriding save method to save employee details
    def save_employee(self):
        try:
            table.put_item(
                Item={
                    'PK': f'EMP#{self.__emp_name}',
                    'SK': f'EMP#{self.get_dept_name()}',
                    'Name': self.__emp_name,
                    'Role': self.__emp_role,
                    'DepartmentName': self.get_dept_name()
                }
            )
            print(f"Employee '{self.__emp_name}' saved successfully in department '{self.get_dept_name()}'.")
        except NoCredentialsError:
            print("Credentials not available.")

# Example Usage


#creating an api for department
@app.route('/department',methods=['Post'])
def create_department():
    data=request.get_json()

    dept_name=data.get('dept_name')

    if not dept_name:
        return jsonify({'Status':'Fail',
                        'Message':'Department name is required',
                        'Code':400}),400
    
    dept=Department(dept_name)
    dept.save_department()

    return jsonify({'Status':'Success',
                    'Message':'Department created successfully',
                    'Code':200}),200


# creating api for employee

@app.route('/employee', methods=['POST'])
def create_employee():
    data = request.get_json()

    emp_name = data.get('emp_name')
    emp_role = data.get('emp_role')
    dept_name = data.get('dept_name')

    # Check if all required fields are provided
    if not emp_name or not emp_role or not dept_name:
        return jsonify({'Status': 'Fail',
                        'Message': 'All fields are required',
                        'Code': 400}), 400

    # Check if the employee already exists in the DynamoDB table
    try:
        response = table.get_item(
            Key={
                'PK': f'EMP#{emp_name}',
                'SK': f'EMP#{dept_name}'
            }
        )

        # If the employee exists, return an error message
        if 'Item' in response:
            return jsonify({
                'Status': 'Fail',
                'Message': f"Employee '{emp_name}' already exists",
                'Code': 400
            }), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # If the employee doesn't exist, proceed to save the new employee
    emp = Employee(emp_name, emp_role, dept_name)
    emp.save_employee()

    return jsonify({
        "Status": "Success",
        "Message": "Employee created successfully",
        "Code": 200
    }), 200

@app.route('/get_employee', methods=['POST'])
def get_employee():
    # Parse the JSON data from the request
    data = request.get_json()
    emp_name = data.get('emp_name')
    dept_name = data.get('dept_name')


    if not emp_name:
        return jsonify({'error': 'Please provide a valid employee name'}), 400

    # Retrieve the item from DynamoDB
    try:
        response = table.get_item(
            Key={
                'PK': f'EMP#{emp_name}',
                'SK': f'DEP#{dept_name}'  # Assuming employee's department is linked with DEP#
            }
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Check if the item exists
    item = response.get('Item')
    if not item:
        return jsonify({'error': 'Employee not found'}), 404

    return jsonify(item), 200

if __name__=="__main__":
    app.run('0.0.0.0',port=5001, debug=True)