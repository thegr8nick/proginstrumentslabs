import math
import random
from typing import List

class Employee:
    """Class to represent an employee."""
    def __init__(self, name: str, position: str, base_salary: float):
        self.name = name
        self.position = position
        self.base_salary = base_salary
        self.performance_score = random.uniform(0.5, 1.5)

    def calculate_bonus(self) -> float:
        """Calculate bonus based on performance."""
        return self.base_salary * 0.2 * self.performance_score

    def total_compensation(self) -> float:
        """Calculate the total compensation for the employee."""
        return self.base_salary + self.calculate_bonus()

    def __str__(self) -> str:
        return (f"Employee: {self.name}, Position: {self.position}, "
                f"Base Salary: {self.base_salary:.2f}, Total Compensation: {self.total_compensation():.2f}")

class Department:
    """Class to represent a department."""
    def __init__(self, name: str):
        self.name = name
        self.employees: List[Employee] = []

    def add_employee(self, employee: Employee) -> None:
        """Add an employee to the department."""
        self.employees.append(employee)

    def department_performance(self) -> float:
        """Calculate the average performance score of the department."""
        if not self.employees:
            return 0.0
        return sum(e.performance_score for e in self.employees) / len(self.employees)

    def total_department_salary(self) -> float:
        """Calculate the total salary of the department."""
        return sum(e.total_compensation() for e in self.employees)

    def __str__(self) -> str:
        return (f"Department: {self.name}, Number of Employees: {len(self.employees)}, "
                f"Average Performance: {self.department_performance():.2f}")

class Company:
    """Class to represent a company."""
    def __init__(self, name: str):
        self.name = name
        self.departments: List[Department] = []

    def add_department(self, department: Department) -> None:
        """Add a department to the company."""
        self.departments.append(department)

    def company_performance(self) -> float:
        """Calculate the average performance score of the company."""
        if not self.departments:
            return 0.0
        return sum(d.department_performance() for d in self.departments) / len(self.departments)

    def total_company_salary(self) -> float:
        """Calculate the total salary of the company."""
        return sum(d.total_department_salary() for d in self.departments)

    def __str__(self) -> str:
        return (f"Company: {self.name}, Number of Departments: {len(self.departments)}, "
                f"Average Performance: {self.company_performance():.2f}")