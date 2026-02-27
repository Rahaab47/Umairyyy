"""
Database operations for the Student Management System.
Uses SQLite for persistent storage.
"""

import sqlite3
import os
from typing import List, Optional, Dict, Any
from student import Student

class DatabaseManager:
    """
    Manages database operations for the Student Management System.
    
    Attributes:
        db_path (str): Path to the SQLite database file
        conn (sqlite3.Connection): Database connection
    """
    
    def __init__(self, db_path: str = "students.db"):
        """
        Initialize the database manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the database and create the students table if it doesn't exist."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Create students table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    grade REAL NOT NULL,
                    attendance REAL NOT NULL,
                    email TEXT
                )
            ''')
            
            self.conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Database initialization error: {e}")
    
    def add_student(self, student: Student) -> bool:
        """
        Add a new student to the database.
        
        Args:
            student: Student object to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO students (student_id, name, age, grade, attendance, email)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student.student_id, student.name, student.age, 
                  student.grade, student.attendance, student.email))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Student with ID {student.student_id} already exists: {e}")
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error while adding student: {e}")
    
    def get_student(self, student_id: int) -> Optional[Student]:
        """
        Retrieve a student by ID.
        
        Args:
            student_id: ID of the student to retrieve
            
        Returns:
            Student object if found, None otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
            row = cursor.fetchone()
            
            if row:
                student_data = {
                    'student_id': row[0],
                    'name': row[1],
                    'age': row[2],
                    'grade': row[3],
                    'attendance': row[4],
                    'email': row[5]
                }
                return Student.from_dict(student_data)
            return None
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error while retrieving student: {e}")
    
    def update_student(self, student: Student) -> bool:
        """
        Update an existing student in the database.
        
        Args:
            student: Student object with updated data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE students 
                SET name = ?, age = ?, grade = ?, attendance = ?, email = ?
                WHERE student_id = ?
            ''', (student.name, student.age, student.grade, 
                  student.attendance, student.email, student.student_id))
            
            if cursor.rowcount == 0:
                raise ValueError(f"Student with ID {student.student_id} not found")
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error while updating student: {e}")
    
    def delete_student(self, student_id: int) -> bool:
        """
        Delete a student by ID.
        
        Args:
            student_id: ID of the student to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
            
            if cursor.rowcount == 0:
                raise ValueError(f"Student with ID {student_id} not found")
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error while deleting student: {e}")
    
    def get_all_students(self) -> List[Student]:
        """
        Retrieve all students from the database.
        
        Returns:
            List of Student objects
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM students')
            rows = cursor.fetchall()
            
            students = []
            for row in rows:
                student_data = {
                    'student_id': row[0],
                    'name': row[1],
                    'age': row[2],
                    'grade': row[3],
                    'attendance': row[4],
                    'email': row[5]
                }
                students.append(Student.from_dict(student_data))
            
            return students
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error while retrieving all students: {e}")
    
    def search_students(self, query: str) -> List[Student]:
        """
        Search students by name or ID.
        
        Args:
            query: Search term (name or ID)
            
        Returns:
            List of matching Student objects
        """
        try:
            cursor = self.conn.cursor()
            
            # Try to parse query as integer (ID search)
            try:
                student_id = int(query)
                cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
            except ValueError:
                # Search by name (case-insensitive)
                cursor.execute('SELECT * FROM students WHERE LOWER(name) LIKE ?', (f'%{query.lower()}%',))
            
            rows = cursor.fetchall()
            
            students = []
            for row in rows:
                student_data = {
                    'student_id': row[0],
                    'name': row[1],
                    'age': row[2],
                    'grade': row[3],
                    'attendance': row[4],
                    'email': row[5]
                }
                students.append(Student.from_dict(student_data))
            
            return students
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error during search: {e}")
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __enter__(self):
        """Context manager entry point."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point."""
        self.close()