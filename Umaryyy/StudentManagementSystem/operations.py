"""
Operations module for the Student Management System.
Contains CRUD operations and reporting functions.
"""

from database import DatabaseManager
from student import Student
from typing import List, Optional, Dict, Any
import csv
import os

class StudentOperations:
    """
    Provides operations for managing students including CRUD and reporting.
    
    Attributes:
        db_manager (DatabaseManager): Database manager instance
    """
    
    def __init__(self, db_path: str = "students.db"):
        """
        Initialize the student operations manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_manager = DatabaseManager(db_path)
    
    def add_student(self, student_id: int, name: str, age: int, grade: float, 
                    attendance: float, email: Optional[str] = None) -> bool:
        """
        Add a new student with validation.
        
        Args:
            student_id: Unique identifier for the student
            name: Student's full name
            age: Student's age
            grade: Student's grade (0-100)
            attendance: Student's attendance percentage (0-100)
            email: Student's email address (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            student = Student(student_id, name, age, grade, attendance, email)
            return self.db_manager.add_student(student)
        except Exception as e:
            raise ValueError(f"Failed to add student: {e}")
    
    def get_student(self, student_id: int) -> Optional[Student]:
        """
        Retrieve a student by ID.
        
        Args:
            student_id: ID of the student to retrieve
            
        Returns:
            Student object if found, None otherwise
        """
        try:
            return self.db_manager.get_student(student_id)
        except Exception as e:
            raise ValueError(f"Failed to retrieve student: {e}")
    
    def update_student(self, student_id: int, name: Optional[str] = None, 
                       age: Optional[int] = None, grade: Optional[float] = None, 
                       attendance: Optional[float] = None, email: Optional[str] = None) -> bool:
        """
        Update an existing student with validation.
        
        Args:
            student_id: ID of the student to update
            name: New name (optional)
            age: New age (optional)
            grade: New grade (optional)
            attendance: New attendance (optional)
            email: New email (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get current student data
            student = self.db_manager.get_student(student_id)
            if not student:
                raise ValueError(f"Student with ID {student_id} not found")
            
            # Update fields if provided
            if name is not None:
                student.name = name
            if age is not None:
                student.age = age
            if grade is not None:
                student.grade = grade
            if attendance is not None:
                student.attendance = attendance
            if email is not None:
                student.email = email
            
            return self.db_manager.update_student(student)
        except Exception as e:
            raise ValueError(f"Failed to update student: {e}")
    
    def delete_student(self, student_id: int) -> bool:
        """
        Delete a student by ID.
        
        Args:
            student_id: ID of the student to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            return self.db_manager.delete_student(student_id)
        except Exception as e:
            raise ValueError(f"Failed to delete student: {e}")
    
    def list_all_students(self) -> List[Student]:
        """
        Retrieve all students from the database.
        
        Returns:
            List of Student objects
        """
        try:
            return self.db_manager.get_all_students()
        except Exception as e:
            raise ValueError(f"Failed to list all students: {e}")
    
    def search_students(self, query: str) -> List[Student]:
        """
        Search students by name or ID.
        
        Args:
            query: Search term (name or ID)
            
        Returns:
            List of matching Student objects
        """
        try:
            return self.db_manager.search_students(query)
        except Exception as e:
            raise ValueError(f"Failed to search students: {e}")
    
    def get_total_students(self) -> int:
        """
        Get the total number of students.
        
        Returns:
            Total count of students
        """
        try:
            students = self.list_all_students()
            return len(students)
        except Exception as e:
            raise ValueError(f"Failed to get total students: {e}")
    
    def get_average_grade(self) -> float:
        """
        Calculate the average grade of all students.
        
        Returns:
            Average grade as a float
        """
        try:
            students = self.list_all_students()
            if not students:
                return 0.0
            
            total_grade = sum(student.grade for student in students)
            return total_grade / len(students)
        except Exception as e:
            raise ValueError(f"Failed to calculate average grade: {e}")
    
    def get_highest_attendance_student(self) -> Optional[Student]:
        """
        Find the student with the highest attendance.
        
        Returns:
            Student object with highest attendance, or None if no students
        """
        try:
            students = self.list_all_students()
            if not students:
                return None
            
            return max(students, key=lambda s: s.attendance)
        except Exception as e:
            raise ValueError(f"Failed to find highest attendance student: {e}")
    
    def get_failing_students(self) -> List[Student]:
        """
        Get list of students with grade < 50 (failing).
        
        Returns:
            List of failing Student objects
        """
        try:
            students = self.list_all_students()
            return [student for student in students if student.grade < 50]
        except Exception as e:
            raise ValueError(f"Failed to get failing students: {e}")
    
    def export_to_csv(self, filename: str = "students_export.csv") -> bool:
        """
        Export all student data to CSV file.
        
        Args:
            filename: Name of the CSV file to create
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            students = self.list_all_students()
            if not students:
                raise ValueError("No students to export")
            
            # Define CSV headers
            headers = ['student_id', 'name', 'age', 'grade', 'attendance', 'email']
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                
                for student in students:
                    writer.writerow({
                        'student_id': student.student_id,
                        'name': student.name,
                        'age': student.age,
                        'grade': student.grade,
                        'attendance': student.attendance,
                        'email': student.email if student.email else ''
                    })
            
            return True
        except Exception as e:
            raise ValueError(f"Failed to export to CSV: {e}")
    
    def sort_students_by_grade(self, reverse: bool = True) -> List[Student]:
        """
        Sort students by grade.
        
        Args:
            reverse: If True, sort descending (highest first), else ascending
            
        Returns:
            Sorted list of Student objects
        """
        try:
            students = self.list_all_students()
            return sorted(students, key=lambda s: s.grade, reverse=reverse)
        except Exception as e:
            raise ValueError(f"Failed to sort students by grade: {e}")
    
    def sort_students_by_attendance(self, reverse: bool = True) -> List[Student]:
        """
        Sort students by attendance.
        
        Args:
            reverse: If True, sort descending (highest first), else ascending
            
        Returns:
            Sorted list of Student objects
        """
        try:
            students = self.list_all_students()
            return sorted(students, key=lambda s: s.attendance, reverse=reverse)
        except Exception as e:
            raise ValueError(f"Failed to sort students by attendance: {e}")
    
    def close(self):
        """Close the database connection."""
        self.db_manager.close()