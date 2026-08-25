import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ============================================================
# DBMS UNIT 1 MINI PROJECT
# LEGACY FILE SYSTEM -> RELATIONAL DBMS
#
# Demonstrates:
#   1. Legacy File-Based System
#   2. View / External Level
#   3. Logical / Conceptual Level
#   4. Physical / Internal Level
#   5. Three-Tier Architecture
#   6. Logical Data Independence
#   7. Physical Data Independence
#   8. Relational DBMS Tables
#
# No external Python packages are required.
# ============================================================

# -------------------- COLORS --------------------

BG = "#F4F7FB"
WHITE = "#FFFFFF"
DARK = "#172033"
BLUE = "#1976D2"
BLUE_LIGHT = "#EAF3FF"
PURPLE = "#6C63FF"
PURPLE_LIGHT = "#F0EEFF"
GREEN = "#16A05D"
GREEN_LIGHT = "#E9F8F0"
ORANGE = "#F59E0B"
ORANGE_LIGHT = "#FFF6DF"
RED = "#D64545"
GRAY = "#667085"
BORDER = "#DDE3EC"

FONT = ("Segoe UI", 10)
TITLE = ("Segoe UI", 23, "bold")
SECTION = ("Segoe UI", 16, "bold")


# ============================================================
# DATABASE TIER
# ============================================================

class DatabaseTier:

    def __init__(self):
        self.connection = sqlite3.connect(":memory:")
        self.create_database()
        self.insert_sample_data()

    # -------------------- Logical Schema --------------------

    def create_database(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE course (
                course_id INTEGER PRIMARY KEY,
                course_name TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE student (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                course_id INTEGER NOT NULL,
                email TEXT,
                FOREIGN KEY(course_id) REFERENCES course(course_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE subject (
                subject_id INTEGER PRIMARY KEY,
                subject_name TEXT NOT NULL,
                course_id INTEGER NOT NULL,
                FOREIGN KEY(course_id) REFERENCES course(course_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE marks (
                student_id INTEGER,
                subject_id INTEGER,
                marks INTEGER,
                PRIMARY KEY(student_id, subject_id),
                FOREIGN KEY(student_id) REFERENCES student(student_id),
                FOREIGN KEY(subject_id) REFERENCES subject(subject_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE attendance (
                student_id INTEGER,
                subject_id INTEGER,
                attendance_percentage REAL,
                PRIMARY KEY(student_id, subject_id),
                FOREIGN KEY(student_id) REFERENCES student(student_id),
                FOREIGN KEY(subject_id) REFERENCES subject(subject_id)
            )
        """)

        # ---------------- Physical / Internal Structures ----------------

        cursor.execute(
            "CREATE INDEX idx_student_course ON student(course_id)"
        )

        cursor.execute(
            "CREATE INDEX idx_subject_course ON subject(course_id)"
        )

        cursor.execute(
            "CREATE INDEX idx_marks_student ON marks(student_id)"
        )

        cursor.execute(
            "CREATE INDEX idx_marks_subject ON marks(subject_id)"
        )

        cursor.execute(
            "CREATE INDEX idx_attendance_student ON attendance(student_id)"
        )

        self.connection.commit()

    # -------------------- Sample Data --------------------

    def insert_sample_data(self):

        cursor = self.connection.cursor()

        cursor.executemany(
            "INSERT INTO course VALUES (?, ?)",
            [
                (1, "B.Tech CSE - AI & Data Science"),
                (2, "B.Tech CSE")
            ]
        )

        cursor.executemany(
            "INSERT INTO student VALUES (?, ?, ?, ?)",
            [
                (101, "Bhargavi", 1, "bhargavi@example.com"),
                (102, "Aarav", 1, "aarav@example.com"),
                (103, "Diya", 1, "diya@example.com")
            ]
        )

        cursor.executemany(
            "INSERT INTO subject VALUES (?, ?, ?)",
            [
                (1, "DBMS", 1),
                (2, "Python", 1),
                (3, "Digital Electronics", 1)
            ]
        )

        cursor.executemany(
            "INSERT INTO marks VALUES (?, ?, ?)",
            [
                (101, 1, 85),
                (101, 2, 91),
                (101, 3, 78),
                (102, 1, 74),
                (102, 2, 82),
                (102, 3, 80),
                (103, 1, 90),
                (103, 2, 88),
                (103, 3, 84)
            ]
        )

        cursor.executemany(
            "INSERT INTO attendance VALUES (?, ?, ?)",
            [
                (101, 1, 92),
                (101, 2, 89),
                (101, 3, 86),
                (102, 1, 84),
                (102, 2, 88),
                (102, 3, 91),
                (103, 1, 95),
                (103, 2, 93),
                (103, 3, 90)
            ]
        )

        self.connection.commit()

    # -------------------- Queries --------------------

    def get_courses(self):
        return self.connection.execute("""
            SELECT course_id, course_name
            FROM course
            ORDER BY course_id
        """).fetchall()

    def get_students(self):
        return self.connection.execute("""
            SELECT student_id, name, course_id, email
            FROM student
            ORDER BY student_id
        """).fetchall()

    def get_subjects(self):
        return self.connection.execute("""
            SELECT subject_id, subject_name, course_id
            FROM subject
            ORDER BY subject_id
        """).fetchall()

    def get_marks(self):
        return self.connection.execute("""
            SELECT student_id, subject_id, marks
            FROM marks
            ORDER BY student_id, subject_id
        """).fetchall()

    def get_attendance(self):
        return self.connection.execute("""
            SELECT student_id, subject_id, attendance_percentage
            FROM attendance
            ORDER BY student_id, subject_id
        """).fetchall()

    def get_student_dashboard(self, student_id=101):

        return self.connection.execute("""
            SELECT
                s.student_id,
                s.name,
                c.course_id,
                c.course_name,
                sub.subject_id,
                sub.subject_name,
                m.marks,
                a.attendance_percentage
            FROM student s
            JOIN course c
                ON s.course_id = c.course_id
            JOIN marks m
                ON s.student_id = m.student_id
            JOIN subject sub
                ON m.subject_id = sub.subject_id
            LEFT JOIN attendance a
                ON m.student_id = a.student_id
                AND m.subject_id = a.subject_id
            WHERE s.student_id = ?
            ORDER BY sub.subject_id
        """, (student_id,)).fetchall()

    def search_student(self, student_id):

        return self.connection.execute("""
            SELECT
                s.student_id, s.name, c.course_id, c.course_name,
                sub.subject_id, sub.subject_name, m.marks,
                a.attendance_percentage
            FROM student s
            JOIN course c ON s.course_id = c.course_id
            JOIN marks m ON s.student_id = m.student_id
            JOIN subject sub ON m.subject_id = sub.subject_id
            LEFT JOIN attendance a
              ON m.student_id = a.student_id
             AND m.subject_id = a.subject_id
            WHERE s.student_id = ?
            ORDER BY sub.subject_id
        """, (student_id,)).fetchall()

    def update_student_id(self, old_id, new_id):

        cur = self.connection.cursor()

        cur.execute("SELECT name FROM student WHERE student_id = ?", (old_id,))
        student = cur.fetchone()

        if student is None:
            return False, "Student ID not found in STUDENT table."

        cur.execute("SELECT 1 FROM student WHERE student_id = ?", (new_id,))
        if cur.fetchone() is not None:
            return False, "New Student ID already exists."

        try:
            # Update related rows first, then the primary Student record.
            # This visibly demonstrates how related DBMS tables stay connected.
            marks_count = cur.execute(
                "SELECT COUNT(*) FROM marks WHERE student_id = ?", (old_id,)
            ).fetchone()[0]

            attendance_count = cur.execute(
                "SELECT COUNT(*) FROM attendance WHERE student_id = ?", (old_id,)
            ).fetchone()[0]

            cur.execute(
                "UPDATE marks SET student_id = ? WHERE student_id = ?",
                (new_id, old_id)
            )
            cur.execute(
                "UPDATE attendance SET student_id = ? WHERE student_id = ?",
                (new_id, old_id)
            )
            cur.execute(
                "UPDATE student SET student_id = ? WHERE student_id = ?",
                (new_id, old_id)
            )

            self.connection.commit()

            return True, (
                f"✓ STUDENT table → 1 record updated\n"
                f"✓ MARKS table → {marks_count} related record(s) updated\n"
                f"✓ ATTENDANCE table → {attendance_count} related record(s) updated\n\n"
                "DBMS: one logical student update can be handled across "
                "related tables using keys and relationships."
            )

        except sqlite3.IntegrityError as error:
            self.connection.rollback()
            return False, f"Update failed: {error}"

    def get_indexes(self):

        return self.connection.execute("""
            SELECT name, tbl_name, sql
            FROM sqlite_master
            WHERE type = 'index'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """).fetchall()


# ============================================================
# APPLICATION TIER
# ============================================================

class ApplicationTier:

    def __init__(self, database):
        self.database = database

    def student_dashboard(self):
        return self.database.get_student_dashboard()

    def get_all_tables(self):
        return {
            "COURSE": self.database.get_courses(),
            "STUDENT": self.database.get_students(),
            "SUBJECT": self.database.get_subjects(),
            "MARKS": self.database.get_marks(),
            "ATTENDANCE": self.database.get_attendance()
        }

    def search_student(self, student_id):
        return self.database.search_student(student_id)

    def update_student_id(self, old_id, new_id):
        return self.database.update_student_id(old_id, new_id)

    def get_physical_structures(self):
        return self.database.get_indexes()


# ============================================================
# PRESENTATION TIER / UI
# ============================================================

class DBMSProjectApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "DBMS Unit 1 Mini Project - Legacy Files to DBMS"
        )

        self.root.geometry("1400x850")
        self.root.minsize(1100, 700)
        self.root.configure(bg=BG)

        self.database = DatabaseTier()
        self.application = ApplicationTier(self.database)

        # Data Independence state
        # Demonstration state for data independence.
        # These are descriptions of changes, NOT data/version counters.
        self.view_demo_active = False
        self.logical_demo_active = False
        self.physical_demo_active = False

        self.build_layout()
        self.show_dashboard()

    # ========================================================
    # MAIN LAYOUT
    # ========================================================

    def build_layout(self):

        # ---------------- Sidebar ----------------

        self.sidebar = tk.Frame(
            self.root,
            bg=DARK,
            width=255
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # ---------------- Main area ----------------

        main = tk.Frame(
            self.root,
            bg=BG
        )

        main.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Canvas + scrollbar
        self.canvas = tk.Canvas(
            main,
            bg=BG,
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            main,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.content = tk.Frame(
            self.canvas,
            bg=BG
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw"
        )

        self.content.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_content
        )

        # Mouse wheel only when pointer is over main area
        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_scroll
        )

        self.build_sidebar()

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def resize_content(self, event):

        self.canvas.itemconfigure(
            self.canvas_window,
            width=event.width
        )

    def mouse_scroll(self, event):

        try:
            if event.delta:
                self.canvas.yview_scroll(
                    int(-event.delta / 120),
                    "units"
                )
        except Exception:
            pass

    # ========================================================
    # SIDEBAR
    # ========================================================

    def build_sidebar(self):

        tk.Label(
            self.sidebar,
            text="DBMS",
            font=("Segoe UI", 26, "bold"),
            fg=WHITE,
            bg=DARK
        ).pack(pady=(28, 0))

        tk.Label(
            self.sidebar,
            text="UNIT 1 MINI PROJECT",
            font=("Segoe UI", 9, "bold"),
            fg="#AEB9CC",
            bg=DARK
        ).pack(pady=(0, 25))

        self.create_sidebar_button(
            "Dashboard",
            self.show_dashboard
        )

        self.create_sidebar_button(
            "Legacy Files",
            self.show_legacy
        )

        self.create_sidebar_button(
            "View / External Level",
            self.show_view_level
        )

        self.create_sidebar_button(
            "Logical / Conceptual Level",
            self.show_logical_level
        )

        self.create_sidebar_button(
            "Physical / Internal Level",
            self.show_physical_level
        )

        self.create_sidebar_button(
            "Three-Tier Architecture",
            self.show_three_tier
        )

        self.create_sidebar_button(
            "Data Independence",
            self.show_data_independence
        )

        self.create_sidebar_button(
            "DBMS Tables",
            self.show_dbms_tables
        )

        tk.Label(
            self.sidebar,
            text=(
                "PROJECT FLOW\n\n"
                "Legacy Files\n"
                "↓\n"
                "Relational DBMS\n"
                "↓\n"
                "3 Schema Levels\n"
                "↓\n"
                "3 Tier Architecture\n"
                "↓\n"
                "Data Independence"
            ),
            font=("Segoe UI", 9),
            fg=WHITE,
            bg=DARK,
            justify="center"
        ).pack(pady=25)

    def create_sidebar_button(self, text, command):

        button = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            fg=WHITE,
            bg=DARK,
            activebackground=BLUE,
            activeforeground=WHITE,
            bd=0,
            relief="flat",
            anchor="w",
            padx=18,
            pady=12,
            cursor="hand2"
        )

        button.pack(
            fill="x"
        )

        # Make hover obvious
        button.bind(
            "<Enter>",
            lambda e: button.configure(bg="#24314A")
        )

        button.bind(
            "<Leave>",
            lambda e: button.configure(bg=DARK)
        )

    # ========================================================
    # PAGE HELPERS
    # ========================================================

    def clear_page(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        self.canvas.yview_moveto(0)

    def page_header(self, title, subtitle):

        tk.Label(
            self.content,
            text=title,
            font=TITLE,
            fg=DARK,
            bg=BG,
            anchor="w"
        ).pack(
            fill="x",
            padx=35,
            pady=(30, 5)
        )

        tk.Label(
            self.content,
            text=subtitle,
            font=FONT,
            fg=GRAY,
            bg=BG,
            anchor="w",
            justify="left",
            wraplength=1050
        ).pack(
            fill="x",
            padx=35,
            pady=(0, 18)
        )

    def section_title(self, text):

        tk.Label(
            self.content,
            text=text,
            font=SECTION,
            fg=DARK,
            bg=BG,
            anchor="w"
        ).pack(
            fill="x",
            padx=35,
            pady=(18, 7)
        )

    def info_card(
        self,
        title,
        text,
        background=WHITE,
        title_color=DARK
    ):

        card = tk.Frame(
            self.content,
            bg=background,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=35,
            pady=7
        )

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 14, "bold"),
            fg=title_color,
            bg=background,
            anchor="w"
        ).pack(
            fill="x",
            padx=20,
            pady=(14, 4)
        )

        tk.Label(
            card,
            text=text,
            font=FONT,
            fg=GRAY,
            bg=background,
            anchor="w",
            justify="left",
            wraplength=1050
        ).pack(
            fill="x",
            padx=20,
            pady=(0, 14)
        )

    # ========================================================
    # CLICKABLE DASHBOARD CARDS
    # ========================================================

    def dashboard_card(
        self,
        parent,
        number,
        title,
        description,
        command,
        background,
        foreground
    ):

        card = tk.Frame(
            parent,
            bg=background,
            highlightbackground=BORDER,
            highlightthickness=1,
            cursor="hand2"
        )

        card.pack(
            fill="x",
            pady=6
        )

        number_label = tk.Label(
            card,
            text=number,
            font=("Segoe UI", 21, "bold"),
            fg=foreground,
            bg=background,
            width=3
        )

        number_label.pack(
            side="left",
            padx=(15, 5),
            pady=15
        )

        text_frame = tk.Frame(
            card,
            bg=background
        )

        text_frame.pack(
            side="left",
            fill="x",
            expand=True,
            pady=13
        )

        title_label = tk.Label(
            text_frame,
            text=title,
            font=("Segoe UI", 13, "bold"),
            fg=DARK,
            bg=background,
            anchor="w"
        )

        title_label.pack(
            fill="x"
        )

        description_label = tk.Label(
            text_frame,
            text=description,
            font=("Segoe UI", 9),
            fg=GRAY,
            bg=background,
            anchor="w",
            justify="left"
        )

        description_label.pack(
            fill="x",
            pady=(3, 0)
        )

        arrow = tk.Label(
            card,
            text="→",
            font=("Segoe UI", 20, "bold"),
            fg=foreground,
            bg=background
        )

        arrow.pack(
            side="right",
            padx=20
        )

        widgets = [
            card,
            number_label,
            text_frame,
            title_label,
            description_label,
            arrow
        ]

        for widget in widgets:
            widget.bind(
                "<Button-1>",
                lambda e, c=command: c()
            )

            widget.bind(
                "<Enter>",
                lambda e, f=card, bg=background:
                    f.configure(bg=WHITE)
            )

            widget.bind(
                "<Leave>",
                lambda e, f=card, bg=background:
                    f.configure(bg=bg)
            )

    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.clear_page()

        self.page_header(
            "DBMS Unit 1 Mini Project",
            "Legacy File-Based Student System → Relational DBMS → "
            "Three-Schema Architecture → Three-Tier Architecture → "
            "Data Independence"
        )

        self.info_card(
            "Project Objective",
            "We start with a simple legacy system where student data "
            "is stored in separate text files. We analyse its problems, "
            "convert it into relational tables and then demonstrate "
            "the three database levels, three-tier architecture and "
            "data independence.",
            BLUE_LIGHT,
            BLUE
        )

        self.section_title("Open Project Sections")

        grid = tk.Frame(
            self.content,
            bg=BG
        )

        grid.pack(
            fill="x",
            padx=35
        )

        left = tk.Frame(grid, bg=BG)
        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )

        right = tk.Frame(grid, bg=BG)
        right.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(7, 0)
        )

        self.dashboard_card(
            left,
            "1",
            "Legacy Files",
            "See the old Students.txt, Subjects.txt, "
            "Marks.txt and Attendance.txt system.",
            self.show_legacy,
            ORANGE_LIGHT,
            ORANGE
        )

        self.dashboard_card(
            left,
            "2",
            "View / External Level",
            "See what the user actually sees in the application.",
            self.show_view_level,
            BLUE_LIGHT,
            BLUE
        )

        self.dashboard_card(
            left,
            "3",
            "Logical / Conceptual Level",
            "See relational tables, primary keys, foreign keys "
            "and relationships.",
            self.show_logical_level,
            PURPLE_LIGHT,
            PURPLE
        )

        self.dashboard_card(
            right,
            "4",
            "Physical / Internal Level",
            "See internal access structures such as indexes.",
            self.show_physical_level,
            GREEN_LIGHT,
            GREEN
        )

        self.dashboard_card(
            right,
            "5",
            "Three-Tier Architecture",
            "See Presentation → Application → Database tiers.",
            self.show_three_tier,
            BLUE_LIGHT,
            BLUE
        )

        self.dashboard_card(
            right,
            "6",
            "Data Independence",
            "Interactively demonstrate View, Logical and "
            "Physical changes and what remains unaffected.",
            self.show_data_independence,
            GREEN_LIGHT,
            GREEN
        )

        self.dashboard_card(
            right,
            "7",
            "DBMS Tables",
            "See the complete relational tables with Course ID, "
            "Student ID, Subject ID, Marks and Attendance.",
            self.show_dbms_tables,
            PURPLE_LIGHT,
            PURPLE
        )

        self.info_card(
            "Important",
            "The three-schema architecture and three-tier architecture "
            "are related but different concepts. The project shows both "
            "so that the architecture and data-independence requirements "
            "are clearly visible.",
            WHITE,
            DARK
        )

    # ========================================================
    # LEGACY FILES
    # ========================================================

    def show_legacy(self):

        self.clear_page()

        self.page_header(
            "Legacy File-Based System",
            "The old system stores related information in separate files. "
            "Use SEARCH and UPDATE below to see the manual effort."
        )

        self.info_card(
            "Why is the legacy system difficult?",
            "Student details, marks and attendance are stored separately. "
            "To find one student's complete information, we must search "
            "different files. If a Student ID changes, the same ID must be "
            "found and updated manually in every related file.",
            ORANGE_LIGHT,
            ORANGE
        )

        self.info_card(
            "CONCEPT EXPLANATION – LEGACY FILE SYSTEM",
            "LEGACY FILE SYSTEM is the old file-based approach. Different parts of student information are stored in separate files such as Students.txt, Marks.txt and Attendance.txt. Related information is not centrally managed, so searching, combining and updating related records is harder. This is the starting point of our project; we then migrate the information into a relational DBMS.",
            ORANGE_LIGHT, ORANGE
        )

        # Separate legacy-file data. These are intentionally NOT DBMS tables.
        students = [
            ["101", "Bhargavi", "CSE-AI&DS"],
            ["102", "Aarav", "CSE-AI&DS"],
            ["103", "Diya", "CSE-AI&DS"]
        ]

        subjects = [
            ["1", "DBMS"],
            ["2", "Python"],
            ["3", "Digital Electronics"]
        ]

        marks = [
            ["101", "1", "85"], ["101", "2", "91"], ["101", "3", "78"],
            ["102", "1", "74"], ["102", "2", "82"], ["102", "3", "80"],
            ["103", "1", "90"], ["103", "2", "88"], ["103", "3", "84"]
        ]

        attendance = [
            ["101", "1", "92%"], ["101", "2", "89%"], ["101", "3", "86%"],
            ["102", "1", "84%"], ["102", "2", "88%"], ["102", "3", "91%"],
            ["103", "1", "95%"], ["103", "2", "93%"], ["103", "3", "90%"]
        ]

        # --------------------------------------------------------
        # SEARCH
        # --------------------------------------------------------

        self.section_title("1. Search Across Legacy Files")

        search_card = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        search_card.pack(fill="x", padx=35, pady=6)

        tk.Label(
            search_card,
            text="Student ID:",
            font=("Segoe UI", 10, "bold"),
            fg=DARK,
            bg=WHITE
        ).grid(row=0, column=0, padx=(20, 8), pady=15)

        search_entry = tk.Entry(
            search_card,
            font=("Segoe UI", 10),
            width=15
        )
        search_entry.insert(0, "101")
        search_entry.grid(row=0, column=1, padx=5, pady=15)

        search_button = tk.Button(
            search_card,
            text="SEARCH FILES",
            font=("Segoe UI", 9, "bold"),
            bg=BLUE,
            fg=WHITE,
            activebackground=BLUE,
            activeforeground=WHITE,
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2"
        )
        search_button.grid(row=0, column=2, padx=20)

        search_result = tk.Label(
            search_card,
            text="",
            font=("Segoe UI", 10),
            fg=GRAY,
            bg=WHITE,
            justify="left",
            anchor="w"
        )
        search_result.grid(
            row=1, column=0, columnspan=3,
            sticky="w", padx=20, pady=(0, 15)
        )

        def search_legacy():
            sid = search_entry.get().strip()

            if not sid:
                search_result.config(
                    text="Please enter a Student ID.",
                    fg=RED
                )
                return

            student = next((r for r in students if r[0] == sid), None)
            mark_rows = [r for r in marks if r[0] == sid]
            attendance_rows = [r for r in attendance if r[0] == sid]

            if student is None:
                search_result.config(
                    text="Student not found in Students.txt.",
                    fg=RED
                )
                return

            search_result.config(
                text=(
                    f"Students.txt  → ID: {student[0]}, Name: {student[1]}, "
                    f"Course: {student[2]}\n"
                    f"Marks.txt      → {len(mark_rows)} related record(s) found\n"
                    f"Attendance.txt → {len(attendance_rows)} related record(s) found\n\n"
                    "⚠ One student's complete information required searching "
                    "multiple separate files."
                ),
                fg=BLUE
            )

        search_button.config(command=search_legacy)

        # --------------------------------------------------------
        # UPDATE
        # --------------------------------------------------------

        self.section_title("2. Update a Student ID in the Legacy System")

        update_card = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        update_card.pack(fill="x", padx=35, pady=6)

        tk.Label(
            update_card,
            text="Old ID:",
            font=("Segoe UI", 10, "bold"),
            fg=DARK,
            bg=WHITE
        ).grid(row=0, column=0, padx=(20, 8), pady=15)

        old_id_entry = tk.Entry(
            update_card,
            font=("Segoe UI", 10),
            width=12
        )
        old_id_entry.insert(0, "101")
        old_id_entry.grid(row=0, column=1, padx=5)

        tk.Label(
            update_card,
            text="New ID:",
            font=("Segoe UI", 10, "bold"),
            fg=DARK,
            bg=WHITE
        ).grid(row=0, column=2, padx=(20, 8))

        new_id_entry = tk.Entry(
            update_card,
            font=("Segoe UI", 10),
            width=12
        )
        new_id_entry.insert(0, "201")
        new_id_entry.grid(row=0, column=3, padx=5)

        update_result = tk.Label(
            update_card,
            text="",
            font=("Segoe UI", 10),
            fg=GRAY,
            bg=WHITE,
            justify="left",
            anchor="w"
        )
        update_result.grid(
            row=1, column=0, columnspan=5,
            sticky="w", padx=20, pady=(0, 15)
        )

        def update_legacy():
            old_id = old_id_entry.get().strip()
            new_id = new_id_entry.get().strip()

            if not old_id or not new_id:
                update_result.config(
                    text="Enter both Old ID and New ID.",
                    fg=RED
                )
                return

            if old_id == new_id:
                update_result.config(
                    text="Old ID and New ID must be different.",
                    fg=RED
                )
                return

            if any(r[0] == new_id for r in students):
                update_result.config(
                    text="New ID already exists in Students.txt.",
                    fg=RED
                )
                return

            found = any(r[0] == old_id for r in students)

            if not found:
                update_result.config(
                    text="Old ID not found in Students.txt.",
                    fg=RED
                )
                return

            # Manually update the ID in every related legacy file.
            student_count = 0
            mark_count = 0
            attendance_count = 0

            for row in students:
                if row[0] == old_id:
                    row[0] = new_id
                    student_count += 1

            for row in marks:
                if row[0] == old_id:
                    row[0] = new_id
                    mark_count += 1

            for row in attendance:
                if row[0] == old_id:
                    row[0] = new_id
                    attendance_count += 1

            update_result.config(
                text=(
                    "✓ MANUAL UPDATE COMPLETED\n\n"
                    f"Students.txt  → {student_count} record updated\n"
                    f"Marks.txt     → {mark_count} records updated\n"
                    f"Attendance.txt→ {attendance_count} records updated\n\n"
                    "⚠ Notice: We had to know which files contain the ID "
                    "and update each file separately. In a real large legacy "
                    "system, missing even one related file can create "
                    "inconsistent data."
                ),
                fg=ORANGE
            )

            refresh_files()

        tk.Button(
            update_card,
            text="UPDATE ALL FILES",
            command=update_legacy,
            font=("Segoe UI", 9, "bold"),
            bg=ORANGE,
            fg=WHITE,
            activebackground=ORANGE,
            activeforeground=WHITE,
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2"
        ).grid(row=0, column=4, padx=20)

        # --------------------------------------------------------
        # FILES
        # --------------------------------------------------------

        self.section_title("3. Separate Legacy Files")

        file_area = tk.Frame(self.content, bg=BG)
        file_area.pack(fill="x", padx=35)

        def refresh_files():
            for widget in file_area.winfo_children():
                widget.destroy()

            file_data = [
                ("Students.txt", "Student ID | Name | Course", students),
                ("Subjects.txt", "Subject ID | Subject Name", subjects),
                ("Marks.txt", "Student ID | Subject ID | Marks", marks),
                ("Attendance.txt", "Student ID | Subject ID | Attendance", attendance)
            ]

            for filename, heading, rows in file_data:
                card = tk.Frame(
                    file_area,
                    bg=WHITE,
                    highlightbackground=BORDER,
                    highlightthickness=1
                )
                card.pack(fill="x", pady=5)

                tk.Label(
                    card,
                    text="📄  " + filename,
                    font=("Segoe UI", 12, "bold"),
                    fg=DARK,
                    bg=WHITE,
                    anchor="w"
                ).pack(fill="x", padx=15, pady=(10, 4))

                tk.Label(
                    card,
                    text=heading,
                    font=("Consolas", 9, "bold"),
                    fg=BLUE,
                    bg=WHITE,
                    anchor="w"
                ).pack(fill="x", padx=15)

                text = tk.Text(
                    card,
                    height=min(6, max(3, len(rows))),
                    font=("Consolas", 9),
                    bg="#F8FAFC",
                    fg=DARK,
                    bd=0
                )
                text.pack(fill="x", padx=15, pady=(5, 12))

                for row in rows:
                    text.insert("end", " | ".join(row) + "\n")

                text.config(state="disabled")

        refresh_files()

        self.info_card(
            "What this demonstration proves",
            "SEARCH → one student's information is spread across files.\n\n"
            "UPDATE → changing one key value requires manually finding and "
            "updating that value in multiple files.\n\n"
            "DBMS advantage → related data is organized into tables and "
            "connected using Primary Keys and Foreign Keys, making retrieval "
            "and maintenance much easier.",
            BLUE_LIGHT,
            BLUE
        )



    # ========================================================
    # VIEW / EXTERNAL LEVEL
    # ========================================================

    def show_view_level(self):

        self.clear_page()

        self.page_header(
            "View / External Level",
            "This is the user-facing view of the DBMS. "
            "The displayed student information is retrieved from the "
            "relational database."
        )

        self.info_card(
            "CONCEPT — What is the View / External Level?",
            "The View Level is the user-facing level of the DBMS three-schema architecture. "
            "It shows only the information a particular user needs instead of exposing the "
            "complete database structure. Different user views can be created from the same "
            "logical data. In this project, examples include Student Information View, "
            "Academic / Marks View and Attendance View. Changing how a view is displayed does "
            "not change the underlying logical tables or physical storage.",
            WHITE,
            DARK
        )

        self.info_card(
            "View Level",
            "The user does not need to see the internal database structures. "
            "This view shows only the information required by the user.",
            BLUE_LIGHT,
            BLUE
        )

        self.section_title("Student View")

        # Get real data from the DBMS so the view table is never blank.
        try:
            rows = self.application.get_all_tables().get("STUDENT", [])
        except Exception:
            try:
                rows = self.logic.all_tables().get("STUDENT", [])
            except Exception:
                rows = []

        # If the table is still empty, show the same project demo records
        # already used by the DBMS instead of an empty view.
        if not rows:
            rows = [
                (101, "Bhargavi", 1, "bhargavi@example.com"),
                (102, "Aarav", 1, "aarav@example.com"),
                (103, "Diya", 1, "diya@example.com")
            ]

        table_frame = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        table_frame.pack(
            fill="x",
            padx=35,
            pady=8
        )

        columns = [
            ("student_id", "Student ID"),
            ("name", "Student Name"),
            ("course_id", "Course ID"),
            ("email", "Email")
        ]

        tree = ttk.Treeview(
            table_frame,
            columns=[c[0] for c in columns],
            show="headings",
            height=max(4, min(8, len(rows)))
        )

        for key, heading in columns:
            tree.heading(key, text=heading)
            tree.column(
                key,
                width=220,
                anchor="center"
            )

        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack(
            fill="x",
            padx=15,
            pady=15
        )

        self.info_card(
            "What this demonstrates",
            "View Level → shows only user-required student information.\n"
            "Logical Level → contains the complete relational table structure.\n"
            "Physical Level → handles internal storage and access structures.\n\n"
            "Changing the way this view is displayed does not require changing "
            "the underlying logical tables or physical storage.",
            GREEN_LIGHT,
            GREEN
        )

        self.info_card(
            'Concept Explanation',
            'VIEW / EXTERNAL LEVEL is the user-facing level. It shows only the information needed for a particular user or task. Examples include a Student View, Academic/Marks View and Attendance View. These are user views, not separate copies of the database. Changing how a view is presented should not require changing the logical tables or physical storage.',
            WHITE, DARK
        )

    def show_logical_level(self):

        self.clear_page()

        self.page_header(
            "Logical / Conceptual Level",
            "Level 2 of the three-schema architecture. It describes "
            "what data is stored and how the data items are related."
        )

        self.info_card(
            "CONCEPT — What is the Logical / Conceptual Level?",
            "The Logical Level describes WHAT data is stored in the database and HOW the data "
            "is related. It contains the complete logical structure such as tables, attributes, "
            "Primary Keys, Foreign Keys and relationships. In this project, STUDENT, COURSE, "
            "SUBJECT, MARKS and ATTENDANCE are logically related. Users do not need to know "
            "how these records are physically stored.",
            WHITE,
            DARK
        )

        self.info_card(
            "Legacy Files → Relational DBMS",
            "Students.txt → STUDENT\n"
            "Subjects.txt → SUBJECT\n"
            "Marks.txt → MARKS\n"
            "Attendance.txt → ATTENDANCE\n"
            "Course information → COURSE",
            BLUE_LIGHT,
            BLUE
        )

        self.section_title("Relational Schema")

        tables = [
            (
                "COURSE",
                "course_id (PK)\n"
                "course_name"
            ),
            (
                "STUDENT",
                "student_id (PK)\n"
                "name\n"
                "course_id (FK)\n"
                "email"
            ),
            (
                "SUBJECT",
                "subject_id (PK)\n"
                "subject_name\n"
                "course_id (FK)"
            ),
            (
                "MARKS",
                "student_id (PK/FK)\n"
                "subject_id (PK/FK)\n"
                "marks"
            ),
            (
                "ATTENDANCE",
                "student_id (PK/FK)\n"
                "subject_id (PK/FK)\n"
                "attendance_percentage"
            )
        ]

        container = tk.Frame(
            self.content,
            bg=BG
        )

        container.pack(
            fill="x",
            padx=35
        )

        for table_name, fields in tables:

            box = tk.Frame(
                container,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            box.pack(
                side="left",
                fill="both",
                expand=True,
                padx=4
            )

            tk.Label(
                box,
                text=table_name,
                font=("Segoe UI", 12, "bold"),
                fg=BLUE,
                bg=WHITE
            ).pack(
                pady=(13, 8)
            )

            tk.Label(
                box,
                text=fields,
                font=("Consolas", 9),
                fg=GRAY,
                bg=WHITE,
                justify="left"
            ).pack(
                padx=8,
                pady=(0, 13)
            )

        self.section_title("Relationships")

        self.info_card(
            "Entity Relationships",
            "COURSE 1 ─────────< STUDENT\n"
            "COURSE 1 ─────────< SUBJECT\n"
            "STUDENT 1 ────────< MARKS >──────── 1 SUBJECT\n"
            "STUDENT 1 ────────< ATTENDANCE >──── 1 SUBJECT",
            WHITE,
            PURPLE
        )

        self.info_card(
            "Why relationships are useful",
            "The DBMS can identify which course a student belongs to, "
            "which subjects belong to that course, and which marks "
            "and attendance records belong to a particular student "
            "and subject.",
            GREEN_LIGHT,
            GREEN
        )

        self.info_card(
            'Concept Explanation',
            'LOGICAL / CONCEPTUAL LEVEL describes what data the database contains and how it is organized and related. Our logical schema contains COURSE, STUDENT, SUBJECT, MARKS and ATTENDANCE tables. Primary Keys identify records and Foreign Keys connect related tables. This level describes the database structure, not the physical location of the stored bytes.',
            WHITE, DARK
        )

    # ========================================================
    # PHYSICAL / INTERNAL LEVEL
    # ========================================================

    def show_physical_level(self):

        self.clear_page()

        self.page_header(
            "Physical / Internal Level",
            "Level 3 of the three-schema architecture. It describes "
            "how the DBMS internally manages and accesses the logical data."
        )

        self.info_card(
            "CONCEPT — What is the Physical / Internal Level?",
            "The Physical Level describes HOW the DBMS actually stores and accesses data internally. "
            "It deals with storage structures, records, files and indexes used to locate data. "
            "Users and application views normally do not need to know these internal details. "
            "For example, an index can be changed or added to improve access without changing "
            "the logical tables or the user's view.",
            WHITE,
            DARK
        )

        self.info_card(
            "What happens internally?",
            "The user does not need to know exactly where every record "
            "is stored. The DBMS manages storage and access structures. "
            "Indexes can be used to locate records efficiently.",
            ORANGE_LIGHT,
            ORANGE
        )

        self.section_title("Physical Access Structures")

        structures = self.application.get_physical_structures()

        for index_name, table_name, sql in structures:

            row = tk.Frame(
                self.content,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            row.pack(
                fill="x",
                padx=35,
                pady=4
            )

            tk.Label(
                row,
                text=index_name,
                font=("Consolas", 10, "bold"),
                fg=BLUE,
                bg=WHITE,
                width=30,
                anchor="w"
            ).pack(
                side="left",
                padx=15,
                pady=12
            )

            tk.Label(
                row,
                text=table_name,
                font=("Consolas", 10),
                fg=DARK,
                bg=WHITE,
                width=22,
                anchor="w"
            ).pack(
                side="left"
            )

            tk.Label(
                row,
                text="Index / access structure",
                font=FONT,
                fg=GRAY,
                bg=WHITE
            ).pack(
                side="left",
                padx=10
            )

        self.section_title("Internal Representation")

        self.info_card(
            "Example",
            "Logical table:\n"
            "MARKS(student_id, subject_id, marks)\n\n"
            "Physical access structures:\n"
            "idx_marks_student → student_id\n"
            "idx_marks_subject → subject_id\n\n"
            "The logical table can remain the same even if the "
            "internal access method changes.",
            BLUE_LIGHT,
            BLUE
        )

        self.info_card(
            "Physical Data Independence",
            "Changing internal storage or access structures should "
            "not require changes to the logical tables or the "
            "user-facing view.",
            GREEN_LIGHT,
            GREEN
        )

        self.info_card(
            'Concept Explanation',
            'PHYSICAL / INTERNAL LEVEL describes how the DBMS stores and accesses data internally. In this project, physical concepts are represented using data files, records and access structures such as indexes. An internal access-method change, for example adding or changing an index for faster retrieval, should not require redesigning the logical tables or user views. This demonstrates Physical Data Independence.',
            WHITE, DARK
        )

    # ========================================================
    # THREE-TIER ARCHITECTURE
    # ========================================================

    def show_three_tier(self):

        self.clear_page()

        self.page_header(
            "Three-Tier Architecture",
            "This architecture describes how the application is "
            "organized into Presentation, Application and Database tiers."
        )

        self.info_card(
            "CONCEPT — Why is Three-Tier Architecture used?",
            "Three-Tier Architecture organizes the APPLICATION into three separate tiers: "
            "Presentation, Application / Logic and Database. The Presentation Tier handles the "
            "GUI, the Application Tier processes requests and business logic, and the Database "
            "Tier stores and manages data. This separation makes the application easier to "
            "understand, maintain and modify. It is different from the DBMS three-schema levels "
            "(View, Logical and Physical), which describe database abstraction and data independence.",
            WHITE,
            DARK
        )

        self.create_tier(
            "1",
            "Presentation Tier",
            "Tkinter User Interface",
            "Displays screens, buttons, tables and dashboards. "
            "The user interacts only with this tier.",
            BLUE_LIGHT,
            BLUE
        )

        self.create_tier(
            "2",
            "Application Tier",
            "Python Application Logic",
            "Receives requests from the UI, processes them and "
            "asks the database tier for the required data.",
            PURPLE_LIGHT,
            PURPLE
        )

        self.create_tier(
            "3",
            "Database Tier",
            "DBMS / SQLite",
            "Stores and manages relational tables, keys, "
            "relationships and physical access structures.",
            GREEN_LIGHT,
            GREEN
        )

        self.section_title("Request Flow")

        self.info_card(
            "Example: User asks for Bhargavi's DBMS marks",
            "USER\n"
            "↓\n"
            "PRESENTATION TIER – button / screen\n"
            "↓\n"
            "APPLICATION TIER – processes request\n"
            "↓\n"
            "DATABASE TIER – searches relational tables\n"
            "↓\n"
            "APPLICATION TIER – receives result\n"
            "↓\n"
            "PRESENTATION TIER – displays result to user",
            WHITE,
            BLUE
        )

        self.info_card(
            "Important: Three-Schema vs Three-Tier",
            "Three-Schema Architecture:\n"
            "View / External → Logical / Conceptual → Physical / Internal\n\n"
            "Three-Tier Architecture:\n"
            "Presentation → Application → Database\n\n"
            "They are different concepts, but this project demonstrates "
            "both because the project requirement mentions both.",
            ORANGE_LIGHT,
            ORANGE
        )

        self.info_card(
            'Concept Explanation',
            'THREE-TIER ARCHITECTURE describes how the APPLICATION is organized, not the three database abstraction levels. Presentation Tier handles the GUI and user interaction. Application/Logic Tier processes requests, validates input and connects the interface to the database. Database Tier stores and manages relational data. Example: Search Student → Presentation receives the click → Logic processes the request → Database retrieves the record → Logic returns the result → Presentation displays it.',
            WHITE, DARK
        )

    def create_tier(
        self,
        number,
        title,
        technology,
        description,
        background,
        foreground
    ):

        card = tk.Frame(
            self.content,
            bg=background,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=35,
            pady=8
        )

        tk.Label(
            card,
            text=number,
            font=("Segoe UI", 28, "bold"),
            fg=foreground,
            bg=background,
            width=3
        ).pack(
            side="left",
            padx=15,
            pady=18
        )

        text = tk.Frame(
            card,
            bg=background
        )

        text.pack(
            side="left",
            fill="x",
            expand=True,
            pady=15
        )

        tk.Label(
            text,
            text=title,
            font=("Segoe UI", 16, "bold"),
            fg=DARK,
            bg=background,
            anchor="w"
        ).pack(
            fill="x"
        )

        tk.Label(
            text,
            text=technology,
            font=("Segoe UI", 11, "bold"),
            fg=foreground,
            bg=background,
            anchor="w"
        ).pack(
            fill="x",
            pady=2
        )

        tk.Label(
            text,
            text=description,
            font=FONT,
            fg=GRAY,
            bg=background,
            anchor="w",
            wraplength=950,
            justify="left"
        ).pack(
            fill="x"
        )

    # ========================================================
    # DATA INDEPENDENCE
    # ========================================================

    def show_data_independence(self):

        self.clear_page()

        self.page_header(
            "Data Independence & Isolation",
            "This page demonstrates the main idea of the three-schema "
            "architecture: changes at one level should be isolated from "
            "other levels as much as possible."
        )

        self.info_card(
            "CONCEPT — What is Data Independence?",
            "Data Independence means that changes made at one schema level should not require "
            "unnecessary changes at the other levels. There are TWO main types: Physical Data "
            "Independence (physical/internal changes do not affect the logical schema) and "
            "Logical Data Independence (logical/conceptual changes do not unnecessarily affect "
            "external views). The three levels involved are View / External, Logical / Conceptual "
            "and Physical / Internal.",
            WHITE,
            DARK
        )

        self.info_card(
            "Logical Data Independence",
            "A change in the conceptual/logical schema should not "
            "force every external view to change. Example: adding "
            "a new STUDENT attribute such as email does not require "
            "a result screen that does not use email to display it.",
            GREEN_LIGHT,
            GREEN
        )

        self.info_card(
            "Physical Data Independence",
            "A change in the internal/physical storage or access method "
            "should not require changes to the logical tables or "
            "the user view. Example: adding or changing indexes.",
            BLUE_LIGHT,
            BLUE
        )

        self.info_card(
            "View-Level Independence",
            "Changing the presentation of information means changing "
            "HOW the same data is displayed, not changing the actual "
            "database data. Example: a result table can be redesigned "
            "as cards while the underlying tables remain unchanged.",
            ORANGE_LIGHT,
            ORANGE
        )

        self.section_title("Interactive Demonstration")

        panel = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        panel.pack(
            fill="x",
            padx=35,
            pady=8
        )

        # ---------------- View ----------------

        self.create_independence_row(
            panel,
            0,
            "VIEW / EXTERNAL LEVEL",
            "Student Dashboard → Result Cards",
            BLUE,
            self.change_view
        )

        # ---------------- Logical ----------------

        self.create_independence_row(
            panel,
            1,
            "LOGICAL / CONCEPTUAL LEVEL",
            "Relational Schema",
            GREEN,
            self.change_logical
        )

        # ---------------- Physical ----------------

        self.create_independence_row(
            panel,
            2,
            "PHYSICAL / INTERNAL LEVEL",
            "Index Structures",
            PURPLE,
            self.change_physical
        )

        self.section_title("Live Result")

        self.independence_result = tk.Label(
            self.content,
            text=(
                "No change made yet.\n\n"
                "Click any button above to demonstrate "
                "isolation between the levels."
            ),
            font=("Segoe UI", 11),
            fg=GRAY,
            bg=WHITE,
            justify="left",
            anchor="w",
            padx=25,
            pady=20
        )

        self.independence_result.pack(
            fill="x",
            padx=35,
            pady=8
        )

        self.section_title("What remains unchanged?")

        self.unchanged_tree = ttk.Treeview(
            self.content,
            columns=("level", "change", "affected", "unchanged"),
            show="headings",
            height=5
        )

        headings = [
            ("level", "Changed Level", 220),
            ("change", "Example Change", 300),
            ("affected", "Directly Affected", 260),
            ("unchanged", "Should Remain Unchanged", 420)
        ]

        for key, heading, width in headings:
            self.unchanged_tree.heading(key, text=heading)
            self.unchanged_tree.column(key, width=width)

        self.unchanged_tree.insert(
            "",
            "end",
            values=(
                "View / External",
                "Redesign dashboard",
                "Presentation / View",
                "Logical tables + Physical structures"
            )
        )

        self.unchanged_tree.insert(
            "",
            "end",
            values=(
                "Logical / Conceptual",
                "Add STUDENT.email",
                "Logical schema",
                "Unrelated existing views + Physical implementation"
            )
        )

        self.unchanged_tree.insert(
            "",
            "end",
            values=(
                "Physical / Internal",
                "Add/change index",
                "Internal access method",
                "Logical tables + User view"
            )
        )

        self.unchanged_tree.pack(
            fill="x",
            padx=35,
            pady=8
        )

        self.info_card(
            'Concept Explanation',
            'DATA INDEPENDENCE means changes at one database level should not unnecessarily force changes at another level. There are TWO types: Logical Data Independence — changes to the logical schema should have minimal/no impact on external views; and Physical Data Independence — changes to internal storage or access methods should have minimal/no impact on the logical schema. The architecture still has THREE levels: View, Logical and Physical.',
            WHITE, DARK
        )

    def create_independence_row(
        self,
        parent,
        row,
        level,
        current,
        color,
        command
    ):

        tk.Label(
            parent,
            text=level,
            font=("Segoe UI", 11, "bold"),
            fg=color,
            bg=WHITE,
            anchor="w",
            width=30
        ).grid(
            row=row,
            column=0,
            padx=18,
            pady=15,
            sticky="w"
        )

        value = tk.Label(
            parent,
            text=current,
            font=("Segoe UI", 10, "bold"),
            fg=DARK,
            bg=WHITE,
            anchor="w",
            width=28
        )

        value.grid(
            row=row,
            column=1,
            padx=10,
            sticky="w"
        )

        button = tk.Button(
            parent,
            text="CHANGE THIS LEVEL",
            command=lambda: command(value),
            font=("Segoe UI", 9, "bold"),
            bg=color,
            fg=WHITE,
            activebackground=color,
            activeforeground=WHITE,
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2"
        )

        button.grid(
            row=row,
            column=2,
            padx=15
        )

        parent.grid_columnconfigure(
            1,
            weight=1
        )

    def change_view(self, label):

        # IMPORTANT:
        # View-level change means changing HOW data is displayed.
        # It does NOT mean changing the actual student/marks data.

        self.view_demo_active = True

        label.config(
            text="Student Dashboard → Result Cards"
        )

        self.independence_result.config(
            text=(
                "VIEW LEVEL CHANGED ✓\n\n"
                "Example change:\n"
                "The old student result TABLE VIEW is redesigned "
                "as a CARD VIEW.\n\n"
                "Actual database data: NOT changed ✓\n"
                "Logical tables: NOT changed ✓\n"
                "Course ID / Student ID / Subject ID: NOT changed ✓\n"
                "Physical indexes: NOT changed ✓\n\n"
                "ONLY THE PRESENTATION / VIEW CHANGED.\n\n"
                "This demonstrates VIEW-LEVEL ISOLATION "
                "(external-level data independence)."
            ),
            fg=BLUE
        )

    def change_logical(self, label):

        # Logical-level change means changing the conceptual schema.
        # Existing data can remain; the schema is extended.

        self.logical_demo_active = True

        label.config(
            text="STUDENT Table + Email Attribute"
        )

        self.independence_result.config(
            text=(
                "LOGICAL LEVEL CHANGED ✓\n\n"
                "Example change:\n"
                "The STUDENT logical schema is extended by adding "
                "an EMAIL attribute.\n\n"
                "View that does not use EMAIL: NOT required to change ✓\n"
                "Physical storage method: NOT required to change ✓\n"
                "Existing Student IDs / Course IDs: remain unchanged ✓\n\n"
                "This demonstrates LOGICAL DATA INDEPENDENCE."
            ),
            fg=GREEN
        )

    def change_physical(self, label):

        # Physical-level change means changing internal access/storage
        # structures, not the logical data model.

        self.physical_demo_active = True

        label.config(
            text="Index Added / Access Method Changed"
        )

        self.independence_result.config(
            text=(
                "PHYSICAL LEVEL CHANGED ✓\n\n"
                "Example change:\n"
                "The DBMS adds or changes an INDEX to improve "
                "record retrieval.\n\n"
                "Logical relational tables: NOT changed ✓\n"
                "Primary / Foreign keys: NOT changed ✓\n"
                "User-facing dashboard: NOT changed ✓\n"
                "Actual student/marks information: NOT changed ✓\n\n"
                "This demonstrates PHYSICAL DATA INDEPENDENCE."
            ),
            fg=PURPLE
        )

    # ========================================================
    # DBMS TABLES
    # ========================================================

    def show_dbms_tables(self):

        self.clear_page()

        self.page_header(
            "Relational DBMS Tables",
            "Search and update the same student data here so the DBMS can be "
            "directly compared with the Legacy File-Based System."
        )

        self.info_card(
            "DBMS Search & Update",
            "Use SEARCH and UPDATE below. The DBMS stores data in related "
            "tables using primary keys and foreign keys, so related data "
            "can be retrieved together and maintained in an organized way.",
            BLUE_LIGHT,
            BLUE
        )

        self.info_card(
            "CONCEPT EXPLANATION – RELATIONAL DBMS",
            "RELATIONAL DBMS is the organized system that replaces the old scattered file approach. Student, course, subject, marks and attendance information is stored in related tables. Keys and relationships connect the records, making search, update and retrieval more systematic. This screen is interactive so the DBMS can be compared directly with the legacy files.",
            BLUE_LIGHT, BLUE
        )

        # ========================================================
        # SEARCH
        # ========================================================

        self.section_title("1. Search Student in DBMS")

        search_card = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        search_card.pack(fill="x", padx=35, pady=6)

        tk.Label(
            search_card,
            text="Student ID:",
            font=("Segoe UI", 10, "bold"),
            fg=DARK,
            bg=WHITE
        ).grid(row=0, column=0, padx=(20, 8), pady=15)

        search_entry = tk.Entry(
            search_card,
            font=("Segoe UI", 10),
            width=15
        )
        search_entry.insert(0, "101")
        search_entry.grid(row=0, column=1, padx=5)

        search_result = tk.Label(
            search_card,
            text="",
            font=("Segoe UI", 10),
            fg=GRAY,
            bg=WHITE,
            justify="left",
            anchor="w"
        )
        search_result.grid(
            row=1,
            column=0,
            columnspan=4,
            sticky="w",
            padx=20,
            pady=(0, 15)
        )

        def search_dbms():

            try:
                student_id = int(search_entry.get().strip())
            except ValueError:
                search_result.config(
                    text="Please enter a valid numeric Student ID.",
                    fg=RED
                )
                return

            rows = self.application.search_student(student_id)

            if not rows:
                search_result.config(
                    text="Student not found in DBMS.",
                    fg=RED
                )
                return

            first = rows[0]

            subjects = "\n".join(
                f"   • {row[5]} → Marks: {row[6]}, "
                f"Attendance: {row[7]}%"
                for row in rows
            )

            search_result.config(
                text=(
                    "✓ DBMS SEARCH RESULT\n"
                    f"Student ID: {first[0]}   Name: {first[1]}\n"
                    f"Course: {first[3]}\n"
                    f"Related records retrieved through table relationships:\n"
                    f"{subjects}\n\n"
                    "DBMS advantage: one search can retrieve related data "
                    "from multiple tables using JOINs."
                ),
                fg=GREEN
            )

        tk.Button(
            search_card,
            text="SEARCH DBMS",
            command=search_dbms,
            font=("Segoe UI", 9, "bold"),
            bg=BLUE,
            fg=WHITE,
            activebackground=BLUE,
            activeforeground=WHITE,
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2"
        ).grid(row=0, column=3, padx=20)

        # ========================================================
        # UPDATE
        # ========================================================

        self.section_title("2. Update Student ID in DBMS")

        update_card = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        update_card.pack(fill="x", padx=35, pady=6)

        tk.Label(
            update_card,
            text="Old Student ID:",
            font=("Segoe UI", 10, "bold"),
            fg=DARK,
            bg=WHITE
        ).grid(row=0, column=0, padx=(20, 8), pady=15)

        old_entry = tk.Entry(
            update_card,
            font=("Segoe UI", 10),
            width=12
        )
        old_entry.insert(0, "101")
        old_entry.grid(row=0, column=1, padx=5)

        tk.Label(
            update_card,
            text="New Student ID:",
            font=("Segoe UI", 10, "bold"),
            fg=DARK,
            bg=WHITE
        ).grid(row=0, column=2, padx=(20, 8))

        new_entry = tk.Entry(
            update_card,
            font=("Segoe UI", 10),
            width=12
        )
        new_entry.insert(0, "201")
        new_entry.grid(row=0, column=3, padx=5)

        update_result = tk.Label(
            update_card,
            text="",
            font=("Segoe UI", 10),
            fg=GRAY,
            bg=WHITE,
            justify="left",
            anchor="w"
        )
        update_result.grid(
            row=1,
            column=0,
            columnspan=5,
            sticky="w",
            padx=20,
            pady=(0, 15)
        )

        def update_dbms():

            try:
                old_id = int(old_entry.get().strip())
                new_id = int(new_entry.get().strip())
            except ValueError:
                update_result.config(
                    text="Please enter valid numeric Student IDs.",
                    fg=RED
                )
                return

            if old_id == new_id:
                update_result.config(
                    text="Old and New Student IDs must be different.",
                    fg=RED
                )
                return

            success, message = self.application.update_student_id(
                old_id,
                new_id
            )

            update_result.config(
                text=message,
                fg=GREEN if success else RED
            )

            if success:
                self.after(800, self.show_dbms_tables)

        tk.Button(
            update_card,
            text="UPDATE DBMS",
            command=update_dbms,
            font=("Segoe UI", 9, "bold"),
            bg=GREEN,
            fg=WHITE,
            activebackground=GREEN,
            activeforeground=WHITE,
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2"
        ).grid(row=0, column=4, padx=20)

        # ========================================================
        # TABLES
        # ========================================================

        self.section_title("3. DBMS Tables")

        all_tables = self.application.get_all_tables()

        for table_name, rows in all_tables.items():

            self.section_title(table_name)

            if table_name == "COURSE":
                columns = [
                    ("course_id", "Course ID"),
                    ("course_name", "Course Name")
                ]
            elif table_name == "STUDENT":
                columns = [
                    ("student_id", "Student ID"),
                    ("name", "Name"),
                    ("course_id", "Course ID"),
                    ("email", "Email")
                ]
            elif table_name == "SUBJECT":
                columns = [
                    ("subject_id", "Subject ID"),
                    ("subject_name", "Subject Name"),
                    ("course_id", "Course ID")
                ]
            elif table_name == "MARKS":
                columns = [
                    ("student_id", "Student ID"),
                    ("subject_id", "Subject ID"),
                    ("marks", "Marks")
                ]
            else:
                columns = [
                    ("student_id", "Student ID"),
                    ("subject_id", "Subject ID"),
                    ("attendance_percentage", "Attendance %")
                ]

            tree = ttk.Treeview(
                self.content,
                columns=[x[0] for x in columns],
                show="headings",
                height=max(3, min(7, len(rows)))
            )

            for key, heading in columns:
                tree.heading(key, text=heading)
                tree.column(key, width=240, anchor="center")

            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(
                fill="x",
                padx=35,
                pady=(0, 8)
            )

        self.info_card(
            "Now Compare Both Systems",
            "LEGACY FILES → SEARCH requires checking separate files; "
            "UPDATE may require manually maintaining related records.\n\n"
            "DBMS → SEARCH retrieves related information through table "
            "relationships/JOINs; UPDATE is handled through keys and the "
            "related tables.\n\n"
            "This gives you a live demonstration of why the relational "
            "DBMS is easier to manage than the old file-based system.",
            GREEN_LIGHT,
            GREEN
        )

        self.info_card(
            "Keys and Relationships",
            "COURSE.course_id → Primary Key\n"
            "STUDENT.student_id → Primary Key\n"
            "STUDENT.course_id → Foreign Key → COURSE\n"
            "SUBJECT.subject_id → Primary Key\n"
            "SUBJECT.course_id → Foreign Key → COURSE\n"
            "MARKS(student_id, subject_id) → Composite Primary Key + Foreign Keys\n"
            "ATTENDANCE(student_id, subject_id) → Composite Primary Key + Foreign Keys",
            BLUE_LIGHT,
            BLUE
        )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "Treeview",
        rowheight=31,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold")
    )

    app = DBMSProjectApp(root)

    root.mainloop()
