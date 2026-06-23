import tkinter as tk
from tkinter import ttk, messagebox
import attendance_logic as logic
class AttendanceApp:
    """
    Main application class. Creates the window and all four tabs:
    1. Add Student
    2. Mark Attendance
    3. View / Search Records
    4. Reports
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Tracking System")
        self.root.geometry("750x500")
        self.root.resizable(False, False)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        self.add_student_tab = ttk.Frame(self.notebook)
        self.mark_attendance_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.report_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_student_tab, text="Add Student")
        self.notebook.add(self.mark_attendance_tab, text="Mark Attendance")
        self.notebook.add(self.view_tab, text="View / Search")
        self.notebook.add(self.report_tab, text="Reports")

        # Build the contents of each tab
        self.build_add_student_tab()
        self.build_mark_attendance_tab()
        self.build_view_tab()
        self.build_report_tab()
    def build_add_student_tab(self):
        frame = self.add_student_tab
        tk.Label(frame, text="Add New Student", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=15
        )
        tk.Label(frame, text="Roll Number:").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.roll_entry = tk.Entry(frame, width=30)
        self.roll_entry.grid(row=1, column=1, pady=8)
        tk.Label(frame, text="Full Name:").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.name_entry = tk.Entry(frame, width=30)
        self.name_entry.grid(row=2, column=1, pady=8)
        tk.Label(frame, text="Branch:").grid(row=3, column=0, sticky="e", padx=10, pady=8)
        self.branch_entry = tk.Entry(frame, width=30)
        self.branch_entry.grid(row=3, column=1, pady=8)
        self.branch_entry.insert(0, "AI & DS") 
        tk.Label(frame, text="Year:").grid(row=4, column=0, sticky="e", padx=10, pady=8)
        self.year_entry = tk.Entry(frame, width=30)
        self.year_entry.grid(row=4, column=1, pady=8)
        self.year_entry.insert(0, "2")
        tk.Button(
            frame, text="Add Student", bg="#4CAF50", fg="white",
            command=self.handle_add_student
        ).grid(row=5, column=0, columnspan=2, pady=20)
    def handle_add_student(self):
        roll_no = self.roll_entry.get().strip()
        name = self.name_entry.get().strip()
        branch = self.branch_entry.get().strip()
        year = self.year_entry.get().strip()
        if not roll_no or not name:
            messagebox.showwarning("Missing Data", "Roll number and name are required.")
            return
        success, message = logic.add_student(roll_no, name, branch, year)
        if success:
            messagebox.showinfo("Success", message)
            self.roll_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.refresh_student_dropdown()
        else:
            messagebox.showerror("Error", message)
    def build_mark_attendance_tab(self):
        frame = self.mark_attendance_tab

        tk.Label(frame, text="Mark Attendance", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=15
        )
        tk.Label(frame, text="Select Student:").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.student_dropdown = ttk.Combobox(frame, width=35, state="readonly")
        self.student_dropdown.grid(row=1, column=1, pady=8)
        tk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.date_entry = tk.Entry(frame, width=37)
        self.date_entry.grid(row=2, column=1, pady=8)
        import datetime
        self.date_entry.insert(0, datetime.date.today().isoformat())  # default = today
        tk.Label(frame, text="Status:").grid(row=3, column=0, sticky="e", padx=10, pady=8)
        self.status_var = tk.StringVar(value="Present")
        status_frame = tk.Frame(frame)
        status_frame.grid(row=3, column=1, sticky="w")
        tk.Radiobutton(status_frame, text="Present", variable=self.status_var, value="Present").pack(side="left")
        tk.Radiobutton(status_frame, text="Absent", variable=self.status_var, value="Absent").pack(side="left")
        tk.Button(
            frame, text="Mark Attendance", bg="#2196F3", fg="white",
            command=self.handle_mark_attendance
        ).grid(row=4, column=0, columnspan=2, pady=20)
    def refresh_student_dropdown(self):
        """Reloads the student list shown in the 'Mark Attendance' dropdown."""
        students = logic.get_all_students()
        self.student_map = {f"{roll_no} - {name}": student_id for student_id, roll_no, name, branch, year in students}
        self.student_dropdown["values"] = list(self.student_map.keys())
    def handle_mark_attendance(self):
        selected = self.student_dropdown.get()
        attendance_date = self.date_entry.get().strip()
        status = self.status_var.get()
        if not selected:
            messagebox.showwarning("Missing Data", "Please select a student.")
            return
        student_id = self.student_map.get(selected)
        success, message = logic.mark_attendance(student_id, status, attendance_date)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
    def build_view_tab(self):
        frame = self.view_tab
        top_frame = tk.Frame(frame)
        top_frame.pack(fill="x", pady=10, padx=10)
        tk.Label(top_frame, text="Search by Roll No / Name:").pack(side="left")
        self.search_entry = tk.Entry(top_frame, width=25)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(top_frame, text="Search", command=self.handle_search).pack(side="left", padx=5)
        tk.Button(top_frame, text="Show All", command=self.load_all_records).pack(side="left", padx=5)
        columns = ("Name", "Roll No", "Date", "Status")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_all_records()
    def load_all_records(self):
        """Clears the table and reloads ALL attendance records from the database."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        records = logic.get_all_attendance()
        for name, roll_no, att_date, status in records:
            self.tree.insert("", "end", values=(name, roll_no, att_date, status))
    def handle_search(self):
        """Searches attendance records by roll number or student name."""
        search_text = self.search_entry.get().strip()
        if not search_text:
            self.load_all_records()
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        records = logic.get_attendance_for_student(search_text)
        if not records:
            messagebox.showinfo("No Results", "No attendance records found for that search.")
            return

        for name, roll_no, att_date, status in records:
            self.tree.insert("", "end", values=(name, roll_no, att_date, status))
    def build_report_tab(self):
        frame = self.report_tab
        tk.Label(frame, text="Attendance Report (All Students)", font=("Arial", 14, "bold")).pack(pady=10)
        columns = ("Roll No", "Name", "Total Days", "Present", "Absent", "Percentage")
        self.report_tree = ttk.Treeview(frame, columns=columns, show="headings", height=14)
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=110, anchor="center")
        self.report_tree.pack(fill="both", expand=True, padx=10, pady=5)
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        tk.Button(
            button_frame, text="Generate Report", bg="#FF9800", fg="white",
            command=self.handle_generate_report
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame, text="Save Report to File", bg="#9C27B0", fg="white",
            command=self.handle_save_report
        ).pack(side="left", padx=5)
    def handle_generate_report(self):
        for row in self.report_tree.get_children():
            self.report_tree.delete(row)
        self.current_report = logic.generate_report()
        if not self.current_report:
            messagebox.showinfo("No Data", "No students/attendance found yet.")
            return
        for roll_no, name, total, present, absent, pct in self.current_report:
            self.report_tree.insert("", "end", values=(roll_no, name, total, present, f"{absent}", f"{pct}%"))
    def handle_save_report(self):
        if not hasattr(self, "current_report") or not self.current_report:
            messagebox.showwarning("No Report", "Please click 'Generate Report' first.")
            return
        filename = logic.save_report_to_file(self.current_report)
        messagebox.showinfo("Saved", f"Report saved as '{filename}' in the project folder.")
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
