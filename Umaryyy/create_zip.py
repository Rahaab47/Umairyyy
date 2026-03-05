"""
Submission ZIP Creator for Python Final Exam Project

This script creates a ZIP file containing all required files for submission.
Naming format: RollNo_Python_Final.zip
Usage: python create_zip.py
"""

import os
import zipfile
from datetime import datetime

def create_submission_zip(roll_number="00000"):
    """
    Create a ZIP file with all required submission files.
    
    Args:
        roll_number: Student's roll number (default: "00000")
    """
    
    # Define ZIP filename based on roll number
    zip_filename = f"{roll_number}_Python_Final.zip"
    
    # Files and folders to include in ZIP
    files_to_include = [
        "StudentManagementSystem",           # Entire SMS folder
        "palindrome_checker.py",
        "prime_generator.py",
        "list_analysis.py",
        "dict_merge.py",
        "file_handling.py",
        "students.txt",
        "student_info.txt",
        "README.md"
    ]
    
    try:
        # Create ZIP file
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            
            # Add files and folders
            for item in files_to_include:
                item_path = os.path.join(os.getcwd(), item)
                
                if os.path.isfile(item_path):
                    # Add individual file
                    arcname = os.path.basename(item_path)
                    zipf.write(item_path, arcname=arcname)
                    print(f"✓ Added file: {arcname}")
                
                elif os.path.isdir(item_path):
                    # Add entire directory
                    for foldername, subfolders, filenames in os.walk(item_path):
                        for filename in filenames:
                            file_path = os.path.join(foldername, filename)
                            # Create relative path for ZIP
                            arcname = os.path.relpath(file_path, os.getcwd())
                            zipf.write(file_path, arcname=arcname)
                    print(f"✓ Added folder: {item}")
        
        # Print summary
        zip_size = os.path.getsize(zip_filename)
        print(f"\n{'='*50}")
        print(f"✓ Submission ZIP created successfully!")
        print(f"{'='*50}")
        print(f"ZIP Filename: {zip_filename}")
        print(f"ZIP Size: {zip_size:,} bytes ({zip_size / 1024 / 1024:.2f} MB)")
        print(f"Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}")
        print(f"\nNext Steps:")
        print(f"1. Download the file: {zip_filename}")
        print(f"2. Upload to Hunarmand LMS")
        print(f"3. Verify all files are included")
        print(f"{'='*50}\n")
        
        return True
        
    except FileNotFoundError as e:
        print(f"✗ Error: File not found - {e}")
        print(f"  Make sure all required files are in the current directory")
        return False
    except IOError as e:
        print(f"✗ Error creating ZIP file: {e}")
        return False

def verify_files():
    """
    Verify that all required files exist before creating ZIP.
    """
    required_files = [
        "StudentManagementSystem",
        "palindrome_checker.py",
        "prime_generator.py",
        "list_analysis.py",
        "dict_merge.py",
        "file_handling.py",
        "students.txt",
        "student_info.txt",
        "README.md"
    ]
    
    print("Verifying required files...")
    print("-" * 50)
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ Found: {file}")
        else:
            print(f"✗ Missing: {file}")
            missing_files.append(file)
    
    print("-" * 50)
    
    if missing_files:
        print(f"\n✗ Error: {len(missing_files)} file(s) missing:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("✓ All required files found!")
        return True

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  PYTHON FINAL EXAM - SUBMISSION ZIP CREATOR")
    print("="*50 + "\n")
    
    # Verify files first
    if verify_files():
        # Create ZIP file
        rollno = input("\nEnter your roll number (default: 00000): ").strip() or "00000"
        create_submission_zip(rollno)
    else:
        print("\n✗ Cannot create submission. Please ensure all files are present.")
        print("  Required files:")
        print("    - StudentManagementSystem/ folder")
        print("    - palindrome_checker.py")
        print("    - prime_generator.py")
        print("    - list_analysis.py")
        print("    - dict_merge.py")
        print("    - file_handling.py")
        print("    - students.txt")
        print("    - student_info.txt")
        print("    - README.md")