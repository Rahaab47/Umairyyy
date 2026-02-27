"""
Problem 5: File Handling
Create students.txt with 5 names
Read file and print names in uppercase
"""

def create_students_file():
    """
    Create students.txt with 5 student names.
    """
    students = [
        "Alice Johnson",
        "Bob Smith",
        "Carol Davis",
        "David Wilson",
        "Eva Brown"
    ]
    
    try:
        with open("students.txt", "w", encoding="utf-8") as file:
            for i, name in enumerate(students, 1):
                file.write(f"{i}. {name}\n")
        print("✓ students.txt created successfully with 5 names.")
    except IOError as e:
        print(f"✗ Error creating file: {e}")
        raise

def read_and_print_uppercase():
    """
    Read students.txt and print names in uppercase.
    """
    try:
        with open("students.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        print("\nStudents in UPPERCASE:")
        print("-" * 30)
        for line in lines:
            # Extract name (remove number and period, strip whitespace)
            if '.' in line:
                name_part = line.split('.', 1)[1].strip()
                print(name_part.upper())
            else:
                print(line.strip().upper())
                
    except FileNotFoundError:
        print("✗ students.txt not found. Please create it first.")
        raise
    except IOError as e:
        print(f"✗ Error reading file: {e}")
        raise

# Example usage
if __name__ == "__main__":
    print("File Handling Problem")
    print("=" * 30)
    
    try:
        # Create the file
        create_students_file()
        
        # Read and display in uppercase
        read_and_print_uppercase()
        
    except Exception as e:
        print(f"An error occurred: {e}")