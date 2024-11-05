# problem statement 

#1 create emplo class with first name , lastname, fullname, emploid.
#2 emplo id should be unique 
#3  create salary with methods pay salary , get salary result
#4 10000 and 20000 
#5 check employe id in the list we need to pay the salary to the empolye 
#6 pass result to get salary method e
# print all empolyee conditional statement


class Employee:

    # Class Level Variables
    employee_id = set()

    # End Class Level Variables 

    def __init__(self, first_name, last_name, id, tax_percentage):
        if id in Employee.employee_id:
            raise ValueError("ID must be unique")
        
        self.first_name = first_name
        self.last_name = last_name
        self.emp_id = id
        self.tax_percentage  = tax_percentage
        Employee.employee_id.add(id)

    # def temp():
    #     return 0
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID:{self.emp_id} )"

class Salary:
    def __init__(self):
        self.salary = {}
    def pay_salary(self, emp, amount):
        if not isinstance(emp, Employee):
            raise ValueError("Invalid employee object")
        if (amount <= 10000 or amount >= 150000):
            raise ValueError("Salary must be between 10,000 or 1,00,000")
        
        paid_amount = (emp.tax_percentage/100)*amount
        self.salary[emp.emp_id] = amount-paid_amount

    def get_salary_result(self, emp):
        if emp.emp_id in self.salary:
            if (80000 <= self.salary[emp.emp_id] <= 150000):
                return f"the salary of {emp} is {self.salary[emp.emp_id]} with {emp.tax_percentage}%tax is an Extraordinary Employee "
            elif (60000 <= self.salary[emp.emp_id] < 80000):
                return f"the salary of {emp} is {self.salary[emp.emp_id]} with {emp.tax_percentage}%tax  is an Good employee"
            elif (30000 <= self.salary[emp.emp_id] < 60000):
                return f"the salary of {emp} is {self.salary[emp.emp_id]} with {emp.tax_percentage}%tax  is an Average employee"
            else:
                return f"Please improve your performance to get more salary"
        else:
            return f" No salary available for the {emp} ID"

def main():
    employee = Employee("Gowri", "Ganesh", 1,20)

    salary = Salary()
    salary.pay_salary(employee, 100000)
    print(salary.get_salary_result(employee))
    
    employee = Employee("pavan", "Kumar", 2, 10)
    salary.pay_salary(employee, 80000)
    print(salary.get_salary_result(employee))

    #Employee.temp()

if __name__ == "__main__":
    main()