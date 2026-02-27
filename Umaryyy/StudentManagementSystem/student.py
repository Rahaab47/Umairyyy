"""
Student class for the Student Management System.
Implements object-oriented programming principles with proper validation.
"""

import re
from typing import Optional

class Student:
    """
    Represents a student with various attributes and validation methods.
    
    Attributes:
        student_id (int): Unique identifier for the student
        name (str): Student's full name
        age (int): Student's age
        grade (float): Student's grade (0-100)
        attendance (float): Student's attendance percentage (0-100)
        email (Optional[str]): Student's email address (optional)
    """
    
    def __init__(self, student_id: int, name: str, age: int, grade: float, 
                 attendance: float, email: Optional[str] = None):
        """
        Initialize a Student object with validation.
        
        Args:
            student_id: Unique identifier for the student
            name: Student's full name
            age: Student's age
            grade: Student's grade (0-100)
            attendance: Student's attendance percentage (0-100)
            email: Student's email address (optional)
            
        Raises:
            ValueError: If any validation fails
        """
        self.student_id = self._validate_student_id(student_id)
        self.name = self._validate_name(name)
        self.age = self._validate_age(age)
        self.grade = self._validate_grade(grade)
        self.attendance = self._validate_attendance(attendance)
        self.email = self._validate_email(email) if email else None
    
    def _validate_student_id(self, student_id: int) -> int:
        """Validate student ID is a positive integer."""
        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Student ID must be a positive integer")
        return student_id
    
    def _validate_name(self, name: str) -> str:
        """Validate name is a non-empty string."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        return name.strip()
    
    def _validate_age(self, age: int) -> int:
        """Validate age is between 5 and 100."""
        if not isinstance(age, int) or age < 5 or age > 100:
            raise ValueError("Age must be an integer between 5 and 100")
        return age
    
    def _validate_grade(self, grade: float) -> float:
        """Validate grade is between 0 and 100."""
        if not isinstance(grade, (int, float)) or grade < 0 or grade > 100:
            raise ValueError("Grade must be a number between 0 and 100")
        return float(grade)
    
    def _validate_attendance(self, attendance: float) -> float:
        """Validate attendance is between 0 and 100."""
        if not isinstance(attendance, (int, float)) or attendance < 0 or attendance > 100:
            raise ValueError("Attendance must be a number between 0 and 100")
        return float(attendance)
    
    def _validate_email(self, email: str) -> str:
        """Validate email format using regex."""
        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        
        # Simple email validation pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
        return email
    
    def to_dict(self) -> dict:
        """Convert student object to dictionary for database storage."""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'grade': self.grade,
            'attendance': self.attendance,
            'email': self.email
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create a Student object from a dictionary."""
        return cls(
            student_id=data['student_id'],
            name=data['name'],
            age=data['age'],
            grade=data['grade'],
            attendance=data['attendance'],
            email=data.get('email')
        )
    
    def __str__(self) -> str:
        """String representation of the student."""
        email_str = f", Email: {self.email}" if self.email else ""
        return f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, " \
               f"Grade: {self.grade:.1f}, Attendance: {self.attendance:.1f}%{email_str}"
    
    def __repr__(self) -> str:
        """Detailed representation of the student."""
        return f"Student({self.student_id}, '{self.name}', {self.age}, " \
               f"{self.grade}, {self.attendance}, '{self.email}')"