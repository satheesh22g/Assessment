import json

class Employee:
    def __init__(self, name, employee_id, title, department):
        # Initialize employee attributes
        self.name = name
        self.employee_id = employee_id
        self.title = title
        self.department = department

    def display_details(self):
        # Display detailed information about the employee
        print(f"Employee Details: Name: {self.name}, ID: {self.employee_id}, Title: {self.title}, Department: {self.department}")

    def __str__(self):
        # Return a string representation of the employee
        return f"{self.name} - ID: {self.employee_id}"

class Department:
    def __init__(self, name):
        # Initialize department attributes
        self.name = name
        self.employees = []  # List to store employees in the department

    def add_employee(self, employee):
        # Add an employee to the department
        self.employees.append(employee)

    def remove_employee(self, employee_id):
        # Remove an employee from the department based on employee ID
        self.employees = [emp for emp in self.employees if emp.employee_id != employee_id]

    def list_employees(self):
        # Display a list of employees in the department
        for employee in self.employees:
            print(employee)

class Company:
    def __init__(self):
        # Initialize the company with an empty dictionary of departments
        self.departments = {}

    def add_department(self, department):
        # Add a department to the company
        self.departments[department.name] = department

    def remove_department(self, department_name):
        # Remove a department from the company based on department name
        del self.departments[department_name]

    def display_all_departments(self):
        # Display information about all departments and their employees
        for department_name, department in self.departments.items():
            print(f"Department: {department_name}")
            department.list_employees()
            print()

    def save_data(self, filename):
        # Save company data to a file in JSON format
        data = {'departments': {}}
        for department_name, department in self.departments.items():
            data['departments'][department_name] = [str(employee) for employee in department.employees]

        with open(filename, 'w') as file:
            json.dump(data, file)

    def load_data(self, filename):
        # Load company data from a JSON file
        with open(filename, 'r') as file:
            data = json.load(file)

        for department_name, employees in data['departments'].items():
            department = Department(department_name)
            for emp_str in employees:
                emp_data = emp_str.split(' - ID: ')
                employee = Employee(emp_data[0], emp_data[1], "", department_name)
                department.add_employee(employee)

            self.departments[department_name] = department

def print_menu():
    # Display the main menu options for the user
    print("Employee Management System Menu:")
    print("1. Add Employee")
    print("2. Remove Employee")
    print("3. Display Department")
    print("4. Add Department")
    print("5. Remove Department")
    print("6. Display All Departments")
    print("7. Save Data")
    print("8. Load Data")
    print("9. Exit")

def main():
    # Main function to run the Employee Management System
    company = Company()  # Create an instance of the Company class

    while True:
        print_menu()  # Display the main menu
        choice = input("Enter your choice (1-9): ")  # Get user input for menu choice

        if choice == '1':
            # Add Employee
            name = input("Enter employee name: ")
            employee_id = input("Enter employee ID: ")
            title = input("Enter employee title: ")
            department = input("Enter department name: ")

            employee = Employee(name, employee_id, title, department)
            if department in company.departments:
                company.departments[department].add_employee(employee)
            else:
                print(f"Error: Department '{department}' does not exist.")
            
        elif choice == '2':
            # Remove Employee
            employee_id = input("Enter employee ID to remove: ")
            for department in company.departments.values():
                department.remove_employee(employee_id)

        elif choice == '3':
            # Display Department
            department_name = input("Enter department name to display: ")
            if department_name in company.departments:
                company.departments[department_name].list_employees()
            else:
                print(f"Error: Department '{department_name}' does not exist.")

        elif choice == '4':
            # Add Department
            department_name = input("Enter department name to add: ")
            department = Department(department_name)
            company.add_department(department)

        elif choice == '5':
            # Remove Department
            department_name = input("Enter department name to remove: ")
            if department_name in company.departments:
                company.remove_department(department_name)
            else:
                print(f"Error: Department '{department_name}' does not exist.")

        elif choice == '6':
            # Display All Departments
            company.display_all_departments()

        elif choice == '7':
            # Save Data
            filename = input("Enter filename to save data: ")
            company.save_data(filename)

        elif choice == '8':
            # Load Data
            filename = input("Enter filename to load data: ")
            company.load_data(filename)

        elif choice == '9':
            # Exit the program
            print("Exiting Employee Management System. Goodbye!")
            break

        else:
            # Handle invalid choice
            print("Invalid choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()
