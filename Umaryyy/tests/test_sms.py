import sys
import os
# ensure project root on path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root)
# also add package directory so internal module imports resolve
sys.path.insert(0, os.path.join(root, 'StudentManagementSystem'))
from StudentManagementSystem.operations import StudentOperations
import sqlite3

ops = StudentOperations()
# clear db
conn = sqlite3.connect('students.db'); c = conn.cursor(); c.execute('DELETE FROM students'); conn.commit()

ops.add_student(1, 'Alice', 20, 88.5, 95, 'alice@example.com')
print('Added', ops.get_student(1))
ops.update_student(1, 'Alice B', 21, 90, 96, 'aliceb@example.com')
print('Updated', ops.get_student(1))
print('All', ops.list_all_students())
print('Total', ops.get_total_students(), 'avg', ops.get_average_grade())
print('Highest', ops.get_highest_attendance_student())
print('Failing', ops.get_failing_students())
print('Search', ops.search_students('Alice'))
ops.export_to_csv('test_export.csv')
print('CSV created')
ops.delete_student(1)
print('Deleted, now total', ops.get_total_students())
