import pytest
from unittest.mock import Mock
from lab_5.initcode import Employee, Department, Company

def test_employee_initialization():
    """Test if an Employee is correctly initialized."""
    employee = Employee("Nikita", "Manager", 60000)
    assert employee.name == "Nikita"
    assert employee.position == "Manager"
    assert employee.base_salary == 60000
    assert 0.5 <= employee.performance_score <= 1.5

def test_employee_calculate_bonus():
    """Test if the bonus is calculated correctly for an Employee."""
    employee = Employee("Nikita", "Manager", 60000)
    bonus = employee.calculate_bonus()
    expected_bonus = employee.base_salary * 0.2 * employee.performance_score
    assert pytest.approx(bonus, 0.01) == expected_bonus

def test_employee_total_compensation():
    """Test if the total compensation is calculated correctly for an Employee."""
    employee = Employee("Nikita", "Manager", 60000)
    total_comp = employee.total_compensation()
    expected_total_comp = employee.base_salary + (employee.base_salary * 0.2 * employee.performance_score)
    assert pytest.approx(total_comp, 0.01) == expected_total_comp

def test_department_initialization():
    """Test if a Department is correctly initialized."""
    department = Department("HR")
    assert department.name == "HR"
    assert len(department.employees) == 0

def test_department_add_employee():
    """Test adding an employee to a Department."""
    department = Department("HR")
    employee = Employee("Nikita", "Manager", 60000)
    department.add_employee(employee)
    assert len(department.employees) == 1
    assert department.employees[0] == employee

def test_department_performance():
    """Test if the average performance score for a Department is calculated correctly."""
    department = Department("HR")
    employee1 = Employee("Nikita", "Manager", 60000)
    employee2 = Employee("Sanya", "Developer", 80000)
    department.add_employee(employee1)
    department.add_employee(employee2)
    avg_perf = department.department_performance()
    expected_avg_perf = (employee1.performance_score + employee2.performance_score) / 2
    assert pytest.approx(avg_perf, 0.01) == expected_avg_perf

def test_total_department_salary():
    """Test if the total salary for a Department is calculated correctly."""
    department = Department("HR")
    employee1 = Employee("Nikita", "Manager", 60000)
    employee2 = Employee("Sanya", "Developer", 80000)
    department.add_employee(employee1)
    department.add_employee(employee2)
    total_salary = department.total_department_salary()
    expected_total_salary = employee1.total_compensation() + employee2.total_compensation()
    assert pytest.approx(total_salary, 0.01) == expected_total_salary

def test_company_initialization():
    """Test if a Company is correctly initialized."""
    company = Company("TestCorp")
    assert company.name == "TestCorp"
    assert len(company.departments) == 0

def test_company_add_department():
    """Test adding a Department to a Company."""
    company = Company("TestCorp")
    department = Department("HR")
    company.add_department(department)
    assert len(company.departments) == 1
    assert company.departments[0] == department

def test_company_performance():
    """Test if the average performance score for the Company is calculated correctly."""
    company = Company("TestCorp")
    department1 = Department("HR")
    department2 = Department("Engineering")
    employee1 = Employee("Nikita", "Manager", 60000)
    employee2 = Employee("Sanya", "Developer", 80000)
    employee3 = Employee("Gripa", "Analyst", 55000)
    department1.add_employee(employee1)
    department1.add_employee(employee2)
    department2.add_employee(employee3)
    company.add_department(department1)
    company.add_department(department2)
    avg_perf = company.company_performance()
    total_performance = department1.department_performance() + department2.department_performance()
    expected_avg_perf = total_performance / 2
    assert pytest.approx(avg_perf, 0.01) == expected_avg_perf

def test_total_company_salary():
    """Test if the total salary for the Company is calculated correctly."""
    company = Company("TestCorp")
    department1 = Department("HR")
    department2 = Department("Engineering")
    employee1 = Employee("Nikita", "Manager", 60000)
    employee2 = Employee("Sanya", "Developer", 80000)
    employee3 = Employee("Gripa", "Analyst", 55000)
    department1.add_employee(employee1)
    department1.add_employee(employee2)
    department2.add_employee(employee3)
    company.add_department(department1)
    company.add_department(department2)
    total_salary = company.total_company_salary()
    total_department_salary = department1.total_department_salary() + department2.total_department_salary()
    assert pytest.approx(total_salary, 0.01) == total_department_salary