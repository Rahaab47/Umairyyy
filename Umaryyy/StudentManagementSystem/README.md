# Student Management System

A comprehensive Python project demonstrating Object-Oriented Programming, CRUD operations, database handling, and reporting capabilities.

## Features

- **Object-Oriented Design**: Student class with proper validation
- **CRUD Operations**: Add, View, Update, Delete, List students
- **Persistent Storage**: SQLite database for data persistence
- **Input Validation**: Comprehensive validation for all fields
- **Reporting**: Statistics, filtering, and sorting capabilities
- **Export**: CSV export functionality
- **Command-Line Interface**: User-friendly menu system

## Requirements

- Python 3.6 or higher
- SQLite (built-in with Python)

## Installation

1. Clone or download the repository
2. Navigate to the project directory
3. No additional dependencies required (uses only standard library modules)

## Usage

### Running the Application

```bash
python main.py
```

This will launch the command-line interface with the following menu options:
1. Add Student
2. View Student
3. Update Student
4. Delete Student
5. List All Students
6. Search Students
7. Reports
8. Export to CSV
9. Exit

### Database File

The application automatically creates a SQLite database file named `students.db` in the project directory.

## Project Structure

```
StudentManagementSystem/
│
├── main.py             → CLI interface
├── student.py          → Student class implementation
├── database.py         → SQLite database operations
├── operations.py       → CRUD and reporting functions
├── students.db         → SQLite database file (auto-created)
└── README.md           → This documentation
```

## Student Fields

Each student record contains:
- `student_id`: Unique integer identifier
- `name`: Student's full name (string)
- `age`: Student's age (integer, 5-100)
- `grade`: Academic grade (float, 0-100)
- `attendance`: Attendance percentage (float, 0-100)
- `email`: Optional email address (validated format)

## Error Handling

The system includes comprehensive error handling for:
- Invalid input types
- Out-of-range values
- Database errors
- Missing records
- Email format validation

## Reporting Capabilities

- Total number of students
- Average grade calculation
- Student with highest attendance
- List of failing students (grade < 50)
- Sorting by grade or attendance
- CSV export functionality

## License

This project is for educational purposes only.