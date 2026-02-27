"""
Main CLI interface for the Student Management System.
Provides a menu-driven interface for all operations with login authentication.
"""

from operations import StudentOperations
from login import LoginSystem
import os

def print_menu():
    """Print the main menu options."""
    print("\n" + "="*50)
    print(" STUDENT MANAGEMENT SYSTEM ")
    print("="*50)
    print("1. Add Student")
    print("2. View Student")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. List All Students")
    print("6. Search Students")
    print("7. Reports")
    print("8. Export to CSV")
    print("9. Logout")
    print("0. Exit")
    print("-"*50)

def get_student_input() -> dict:
    """Get student information from user input with validation."""
    try:
        student_id = int(input("Enter Student ID: "))
        name = input("Enter Name: ").strip()
        age = int(input("Enter Age: "))
        grade = float(input("Enter Grade (0-100): "))
        attendance = float(input("Enter Attendance (%): "))
        
        email_input = input("Enter Email (optional, press Enter to skip): ").strip()
        email = email_input if email_input else None
        
        return {
            'student_id': student_id,
            'name': name,
            'age': age,
            'grade': grade,
            'attendance': attendance,
            'email': email
        }
    except ValueError as e:
        raise ValueError(f"Invalid input: {e}")

def login_system():
    """Handle user login authentication."""
    login_system = LoginSystem()
    
    print("\n" + "="*40)
    print(" STUDENT MANAGEMENT SYSTEM - LOGIN ")
    print("="*40)
    
    attempts = 3
    while attempts > 0:
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        if login_system.authenticate(username, password):
            print(f"\n✓ Login successful! Welcome, {username}!")
            return login_system, username
        else:
            attempts -= 1
            if attempts > 0:
                print(f"✗ Incorrect credentials. {attempts} attempt(s) remaining.")
            else:
                print("✗ Maximum login attempts exceeded. Exiting.")
                return None, None

def main():
    """Main function to run the Student Management System."""
    # Initialize operations
    ops = StudentOperations()
    current_user = None
    
    try:
        # Login first
        login_manager, current_user = login_system()
        if not login_manager:
            return
        
        while True:
            print_menu()
            
            try:
                choice = input("Enter your choice (0-9): ").strip()
                
                if choice == '1':
                    # Add Student
                    print("\n--- Add New Student ---")
                    try:
                        data = get_student_input()
                        success = ops.add_student(
                            data['student_id'], data['name'], data['age'],
                            data['grade'], data['attendance'], data['email']
                        )
                        if success:
                            print(f"✓ Student '{data['name']}' added successfully!")
                        else:
                            print("✗ Failed to add student.")
                    except ValueError as e:
                        print(f"✗ Error: {e}")
                    except Exception as e:
                        print(f"✗ Unexpected error: {e}")
                
                elif choice == '2':
                    # View Student
                    print("\n--- View Student ---")
                    try:
                        student_id = int(input("Enter Student ID to view: "))
                        student = ops.get_student(student_id)
                        if student:
                            print(f"\nStudent Details:")
                            print(student)
                        else:
                            print(f"✗ Student with ID {student_id} not found.")
                    except ValueError:
                        print("✗ Please enter a valid student ID.")
                    except Exception as e:
                        print(f"✗ Error: {e}")
                
                elif choice == '3':
                    # Update Student
                    print("\n--- Update Student ---")
                    try:
                        student_id = int(input("Enter Student ID to update: "))
                        student = ops.get_student(student_id)
                        if not student:
                            print(f"✗ Student with ID {student_id} not found.")
                            continue
                        
                        print(f"Current details: {student}")
                        
                        # Get updated fields
                        name = input(f"Enter new name [{student.name}]: ").strip() or None
                        age_input = input(f"Enter new age [{student.age}]: ").strip()
                        age = int(age_input) if age_input else None
                        grade_input = input(f"Enter new grade [{student.grade}]: ").strip()
                        grade = float(grade_input) if grade_input else None
                        attendance_input = input(f"Enter new attendance [{student.attendance}%]: ").strip()
                        attendance = float(attendance_input) if attendance_input else None
                        email_input = input(f"Enter new email [{student.email or ''}]: ").strip()
                        email = email_input if email_input else None
                        
                        success = ops.update_student(
                            student_id, name, age, grade, attendance, email
                        )
                        if success:
                            print(f"✓ Student '{student.name}' updated successfully!")
                        else:
                            print("✗ Failed to update student.")
                    except ValueError as e:
                        print(f"✗ Error: {e}")
                    except Exception as e:
                        print(f"✗ Unexpected error: {e}")
                
                elif choice == '4':
                    # Delete Student
                    print("\n--- Delete Student ---")
                    try:
                        student_id = int(input("Enter Student ID to delete: "))
                        confirm = input(f"Are you sure you want to delete student {student_id}? (y/n): ").lower()
                        if confirm == 'y':
                            success = ops.delete_student(student_id)
                            if success:
                                print(f"✓ Student with ID {student_id} deleted successfully!")
                            else:
                                print("✗ Failed to delete student.")
                        else:
                            print("Operation cancelled.")
                    except ValueError:
                        print("✗ Please enter a valid student ID.")
                    except Exception as e:
                        print(f"✗ Error: {e}")
                
                elif choice == '5':
                    # List All Students
                    print("\n--- All Students ---")
                    try:
                        students = ops.list_all_students()
                        if students:
                            print(f"\nTotal Students: {len(students)}")
                            print("-" * 60)
                            for i, student in enumerate(students, 1):
                                print(f"{i:2d}. {student}")
                        else:
                            print("No students found.")
                    except Exception as e:
                        print(f"✗ Error: {e}")
                
                elif choice == '6':
                    # Search Students
                    print("\n--- Search Students ---")
                    try:
                        query = input("Enter student ID or name to search: ").strip()
                        if not query:
                            print("✗ Please enter a search term.")
                            continue
                        
                        students = ops.search_students(query)
                        if students:
                            print(f"\nFound {len(students)} student(s):")
                            print("-" * 60)
                            for i, student in enumerate(students, 1):
                                print(f"{i:2d}. {student}")
                        else:
                            print("No students found matching the search criteria.")
                    except Exception as e:
                        print(f"✗ Error: {e}")
                
                elif choice == '7':
                    # Reports
                    print("\n--- Reports ---")
                    try:
                        print(f"Total Students: {ops.get_total_students()}")
                        print(f"Average Grade: {ops.get_average_grade():.2f}")
                        
                        highest_attendance = ops.get_highest_attendance_student()
                        if highest_attendance:
                            print(f"Student with Highest Attendance: {highest_attendance.name} ({highest_attendance.attendance:.1f}%)")
                        else:
                            print("No students to calculate highest attendance.")
                        
                        failing_students = ops.get_failing_students()
                        if failing_students:
                            print(f"Failing Students (Grade < 50): {len(failing_students)}")
                            for student in failing_students:
                                print(f"  - {student.name} (Grade: {student.grade:.1f})")
                        else:
                            print("No failing students found.")
                        
                        # Sort options
                        print("\nSort Options:")
                        print("1. Sort by Grade (Descending)")
                        print("2. Sort by Grade (Ascending)")
                        print("3. Sort by Attendance (Descending)")
                        print("4. Sort by Attendance (Ascending)")
                        sort_choice = input("Choose sort option (1-4) or press Enter to skip: ").strip()
                        
                        if sort_choice == '1':
                            sorted_students = ops.sort_students_by_grade(reverse=True)
                            print("\nStudents sorted by Grade (Highest to Lowest):")
                            for i, student in enumerate(sorted_students, 1):
                                print(f"{i:2d}. {student}")
                        elif sort_choice == '2':
                            sorted_students = ops.sort_students_by_grade(reverse=False)
                            print("\nStudents sorted by Grade (Lowest to Highest):")
                            for i, student in enumerate(sorted_students, 1):
                                print(f"{i:2d}. {student}")
                        elif sort_choice == '3':
                            sorted_students = ops.sort_students_by_attendance(reverse=True)
                            print("\nStudents sorted by Attendance (Highest to Lowest):")
                            for i, student in enumerate(sorted_students, 1):
                                print(f"{i:2d}. {student}")
                        elif sort_choice == '4':
                            sorted_students = ops.sort_students_by_attendance(reverse=False)
                            print("\nStudents sorted by Attendance (Lowest to Highest):")
                            for i, student in enumerate(sorted_students, 1):
                                print(f"{i:2d}. {student}")
                    except Exception as e:
                        print(f"✗ Error generating reports: {e}")
                
                elif choice == '8':
                    # Export to CSV
                    print("\n--- Export to CSV ---")
                    try:
                        filename = input("Enter filename for export (default: students_export.csv): ").strip()
                        if not filename:
                            filename = "students_export.csv"
                        
                        success = ops.export_to_csv(filename)
                        if success:
                            print(f"✓ Data exported successfully to '{filename}'!")
                        else:
                            print("✗ Failed to export data.")
                    except Exception as e:
                        print(f"✗ Error: {e}")
                
                elif choice == '9':
                    # Logout
                    print(f"\n✓ Logged out successfully. Goodbye, {current_user}!")
                    login_manager, current_user = login_system()
                    if not login_manager:
                        break
                
                elif choice == '0':
                    # Exit
                    print("\nThank you for using Student Management System!")
                    break
                
                else:
                    print("✗ Invalid choice. Please enter a number between 0 and 9.")
            
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user. Exiting...")
                break
            except Exception as e:
                print(f"✗ An unexpected error occurred: {e}")
                print("Please try again.")
    
    finally:
        # Clean up resources
        ops.close()
        print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()