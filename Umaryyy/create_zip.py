"""
Script to create the final ZIP file for submission.
"""

import zipfile
import os
import sys

def create_submission_zip():
    """Create the final ZIP file with proper naming format."""
    
    # Get roll number from student_info.txt (if available)
    roll_number = "ROLLNO"
    try:
        with open("student_info.txt", "r", encoding="utf-8") as f:
            content = f.read()
            # Try to extract roll number if it exists in the template
            if "Roll Number:" in content:
                lines = content.split('\n')
                for line in lines:
                    if line.startswith("Roll Number:"):
                        roll_number = line.split(":", 1)[1].strip()
                        break
    except FileNotFoundError:
        print("Warning: student_info.txt not found, using default roll number")
    
    # Create ZIP filename
    zip_filename = f"{roll_number}_Python_Final.zip"
    
    print(f"Creating ZIP file: {zip_filename}")
    
    # Files to include in ZIP
    files_to_include = [
        # SMS Project folder
        "StudentManagementSystem",
        # Individual problem files
        "palindrome_checker.py",
        "prime_generator.py",
        "list_analysis.py",
        "dict_merge.py",
        "file_handling.py",
        # Documentation and info
        "student_info.txt",
        "README.md"  # This is in the root, but we'll include it from StudentManagementSystem
    ]
    
    # Create ZIP file
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add SMS Project folder contents
            sms_folder = "StudentManagementSystem"
            if os.path.exists(sms_folder):
                for root, dirs, files in os.walk(sms_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Add file to zip with relative path
                        arcname = os.path.relpath(file_path, start=os.getcwd())
                        zipf.write(file_path, arcname)
            
            # Add individual problem files
            problem_files = [
                "palindrome_checker.py",
                "prime_generator.py",
                "list_analysis.py",
                "dict_merge.py",
                "file_handling.py",
                "student_info.txt"
            ]
            
            for file_path in problem_files:
                if os.path.exists(file_path):
                    zipf.write(file_path, file_path)
                else:
                    print(f"Warning: {file_path} not found")
            
            # Add README.md from root (if it exists)
            if os.path.exists("README.md"):
                zipf.write("README.md", "README.md")
        
        print(f"ZIP file created successfully: {zip_filename}")
        print(f"Total files in ZIP: {len([f for f in os.listdir('.') if f.endswith('.zip')])}")
        
    except Exception as e:
        print(f"Error creating ZIP file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_submission_zip()