"""Tkinter-based GUI for Student Management System.

This replaces the HTML/web interface by providing a Python-only GUI.
The backend logic uses the existing StudentOperations class; all
validation, storage, and reporting remain unchanged.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from operations import StudentOperations
from login import LoginSystem


class SMSApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Management System")
        self.ops = StudentOperations()
        self.login_system = LoginSystem()
        self.current_user = None
        self._show_login_screen()

    def _show_login_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.master, padx=20, pady=20)
        frame.pack()
        
        tk.Label(frame, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(frame)
        self.username_entry.grid(row=0, column=1)
        
        tk.Label(frame, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1)
        
        tk.Button(frame, text="Login", command=self._attempt_login).grid(row=2, columnspan=2, pady=10)

    def _attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if self.login_system.authenticate(username, password):
            self.current_user = username
            self._show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def _show_main_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
        menu_frame = tk.Frame(self.master, padx=20, pady=20)
        menu_frame.pack(fill="both", expand=True)
        
        tk.Label(menu_frame, text=f"Welcome, {self.current_user}", font=(None, 14)).pack(pady=10)
        actions = [
            ("Add Student", self._add_student),
            ("View Student", self._view_student),
            ("Update Student", self._update_student),
            ("Delete Student", self._delete_student),
            ("List All Students", self._list_students),
            ("Search Students", self._search_students),
            ("Reports", self._reports),
            ("Export to CSV", self._export_csv),
            ("Logout", self._logout),
            ("Exit", self.master.quit)
        ]
        
        for (text, cmd) in actions:
            tk.Button(menu_frame, text=text, width=25, command=cmd).pack(pady=2)

    def _get_student_data(self, prefill=None):
        data = {}
        try:
            data['student_id'] = int(simpledialog.askstring("Student ID", "Enter Student ID:", initialvalue=prefill and prefill.get('student_id')))
            data['name'] = simpledialog.askstring("Name", "Enter Name:", initialvalue=prefill and prefill.get('name')).strip()
            data['age'] = int(simpledialog.askstring("Age", "Enter Age:", initialvalue=prefill and prefill.get('age')))
            data['grade'] = float(simpledialog.askstring("Grade", "Enter Grade (0-100):", initialvalue=prefill and prefill.get('grade')))
            data['attendance'] = float(simpledialog.askstring("Attendance", "Enter Attendance (%):", initialvalue=prefill and prefill.get('attendance')))
            email = simpledialog.askstring("Email", "Enter Email (optional):", initialvalue=prefill and prefill.get('email') or '')
            data['email'] = email.strip() if email else None
        except (TypeError, ValueError):
            messagebox.showerror("Invalid Input", "Please enter valid student details.")
            return None
        return data

    def _add_student(self):
        data = self._get_student_data()
        if not data:
            return
        try:
            self.ops.add_student(**data)
            messagebox.showinfo("Success", "Student added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _view_student(self):
        sid = simpledialog.askinteger("View Student", "Enter Student ID:")
        if sid is None:
            return
        student = self.ops.get_student(sid)
        if student:
            messagebox.showinfo("Student Details", str(student))
        else:
            messagebox.showinfo("Not Found", f"No student with ID {sid}.")

    def _update_student(self):
        sid = simpledialog.askinteger("Update Student", "Enter Student ID:")
        if sid is None:
            return
        student = self.ops.get_student(sid)
        if not student:
            messagebox.showinfo("Not Found", f"No student with ID {sid}.")
            return
        pre = student.to_dict()
        data = self._get_student_data(prefill=pre)
        if not data:
            return
        try:
            self.ops.update_student(sid, data['name'], data['age'], data['grade'], data['attendance'], data['email'])
            messagebox.showinfo("Success", "Student updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _delete_student(self):
        sid = simpledialog.askinteger("Delete Student", "Enter Student ID to delete:")
        if sid is None:
            return
        if messagebox.askyesno("Confirm", f"Delete student {sid}?" ):
            try:
                self.ops.delete_student(sid)
                messagebox.showinfo("Deleted", "Student deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _list_students(self):
        students = self.ops.list_all_students()
        if not students:
            messagebox.showinfo("List Students", "No students in database.")
            return
        output = "\n".join(str(s) for s in students)
        self._show_scrollable_text("All Students", output)

    def _search_students(self):
        query = simpledialog.askstring("Search", "Enter ID or name to search:")
        if not query:
            return
        results = self.ops.search_students(query)
        if results:
            output = "\n".join(str(s) for s in results)
            self._show_scrollable_text("Search Results", output)
        else:
            messagebox.showinfo("No Results", "No matching students found.")

    def _reports(self):
        total = self.ops.get_total_students()
        avg = self.ops.get_average_grade()
        highest = self.ops.get_highest_attendance_student()
        failing = self.ops.get_failing_students()
        report = f"Total Students: {total}\nAverage Grade: {avg:.2f}\n"
        if highest:
            report += f"Highest Attendance: {highest.name} ({highest.attendance:.1f}%)\n"
        report += f"Failing Students: {len(failing)}\n"
        for s in failing:
            report += f" - {s.name} (Grade: {s.grade})\n"
        self._show_scrollable_text("Reports", report)

    def _export_csv(self):
        filename = simpledialog.askstring("Export CSV", "Enter filename (default students_export.csv):")
        if not filename:
            filename = "students_export.csv"
        try:
            self.ops.export_to_csv(filename)
            messagebox.showinfo("Exported", f"Data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _logout(self):
        self.current_user = None
        self._show_login_screen()

    def _show_scrollable_text(self, title, text):
        win = tk.Toplevel(self.master)
        win.title(title)
        txt = tk.Text(win, wrap="word", width=80, height=20)
        txt.insert("1.0", text)
        txt.pack(side="left", fill="both", expand=True)
        scroll = tk.Scrollbar(win, command=txt.yview)
        scroll.pack(side="right", fill="y")
        txt.config(yscrollcommand=scroll.set)


if __name__ == "__main__":
    root = tk.Tk()
    app = SMSApp(root)
    root.mainloop()