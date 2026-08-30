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
            "#EAF3FF",
            "#1976D2"
        )

    # ========================================================
    # LEGACY FILES
    # ========================================================

    def show_legacy(self):

        self.clear_page()

        self.page_header(
            "Legacy File-Based System",
            "The old system stores information in separate independent files. "
            "Search and update one selected file to demonstrate the maintenance difficulty."
        )

        self.info_card(
            "Why is the Legacy System Difficult?",
            "Student, marks and attendance information are stored in separate files. "
            "The files are independent, so changing one file does NOT automatically "
            "change another file. The user has to know which file contains the "
            "required information and update it separately.",
            ORANGE_LIGHT,
            ORANGE
        )

        # --------------------------------------------------------
        # INDEPENDENT LEGACY FILE DATA
        # --------------------------------------------------------
        # Each file has its own independent copy of the required data.
        # Updating one file will NOT update the other files.
        self.legacy_demo_students = [
            ["101", "Bhargavi", "C01"],
            ["102", "Aarav", "C01"],
            ["103", "Diya", "C02"]
        ]

        self.legacy_demo_marks = [
            ["101", "S01", "85"],
            ["101", "S02", "91"],
            ["102", "S01", "74"],
            ["102", "S02", "82"],
            ["103", "S01", "90"],
            ["103", "S02", "88"]
        ]

        self.legacy_demo_attendance = [
            ["101", "S01", "92%"],
            ["101", "S02", "89%"],
            ["102", "S01", "84%"],
            ["102", "S02", "88%"],
            ["103", "S01", "95%"],
            ["103", "S02", "93%"]
        ]

        # --------------------------------------------------------
        # SEARCH ONE SELECTED FILE
        # --------------------------------------------------------

        self.section_title("1. Search a Selected Legacy File")

        search_card = tk.Frame(
            self.content,
            bg=BLUE_LIGHT,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        search_card.pack(fill="x", padx=35, pady=6)

        tk.Label(
            search_card,
            text="Select File:",
            font=("Segoe UI", 10, "bold"),
            fg=DARK,
            bg=WHITE
        ).grid(row=0, column=0, padx=(20, 8), pady=15)

        search_file = ttk.Combobox(
            search_card,
            values=[
                "Students.txt",
                "Marks.txt",
                "Attendance.txt"
            ],
            state="readonly",
            width=18
        )
        search_file.set("Students.txt")
        search_file.grid(row=0, column=1, padx=5)

        tk.Label(
            search_card,
            text="Search ID:",
            font=("Segoe UI", 10, "bold"),
            fg=DARK,
            bg=WHITE
        ).grid(row=0, column=2, padx=(20, 8))

        search_id = tk.Entry(
            search_card,
            font=("Segoe UI", 10),
            width=12
        )
        search_id.insert(0, "101")
        search_id.grid(row=0, column=3, padx=5)

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
            row=1, column=0, columnspan=5,
            sticky="w", padx=20, pady=(0, 15)
        )

        def search_selected_file():

            filename = search_file.get()
            sid = search_id.get().strip()

            if filename == "Students.txt":
                rows = [
                    r for r in self.legacy_demo_students
                    if r[0] == sid
                ]
                result = "\n".join(
                    f"Student ID: {r[0]} | Name: {r[1]} | Course: {r[2]}"
                    for r in rows
                )

            elif filename == "Marks.txt":
                rows = [
                    r for r in self.legacy_demo_marks
                    if r[0] == sid
                ]
                result = "\n".join(
                    f"Student ID: {r[0]} | Subject ID: {r[1]} | Marks: {r[2]}"
                    for r in rows
                )

            else:
                rows = [
                    r for r in self.legacy_demo_attendance
                    if r[0] == sid
                ]
                result = "\n".join(
                    f"Student ID: {r[0]} | Subject ID: {r[1]} | Attendance: {r[2]}"
                    for r in rows
                )

            if not result:
                result = f"No matching record found in {filename}."
                search_result.config(text=result, fg=RED)
            else:
                search_result.config(
                    text=f"✓ Searched ONLY {filename}\n{result}",
                    fg=BLUE
                )

        tk.Button(
            search_card,
            text="SEARCH FILE",
            command=search_selected_file,
            font=("Segoe UI", 9, "bold"),
            bg=BLUE,
            fg=WHITE,
            activebackground=BLUE,
            activeforeground=WHITE,
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2"
        ).grid(row=0, column=4, padx=20)

        # --------------------------------------------------------
        # UPDATE ONE SELECTED FILE
        # --------------------------------------------------------

        self.section_title("2. Update ONLY the Selected Legacy File")

        update_card = tk.Frame(
            self.content,
            bg=GREEN_LIGHT,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        update_card.pack(fill="x", padx=35, pady=6)

        tk.Label(
            update_card,
            text="Select File:",
            font=("Segoe UI", 10, "bold"),
            fg=DARK,
            bg=WHITE
        ).grid(row=0, column=0, padx=(20, 8), pady=15)

        update_file = ttk.Combobox(
            update_card,
            values=[
                "Students.txt",
                "Marks.txt",
                "Attendance.txt"
            ],
            state="readonly",
            width=18
        )
        update_file.set("Students.txt")
        update_file.grid(row=0, column=1, padx=5)

        tk.Label(
            update_card,
            text="Student ID:",
            font=("Segoe UI", 10, "bold"),
            fg=DARK,
            bg=WHITE
        ).grid(row=0, column=2, padx=(20, 8))

        update_id = tk.Entry(
            update_card,
            font=("Segoe UI", 10),
            width=12
        )
        update_id.insert(0, "101")
        update_id.grid(row=0, column=3, padx=5)

        tk.Label(
            update_card,
            text="Update Value:",
            font=("Segoe UI", 10, "bold"),
            fg=DARK,
            bg=WHITE
        ).grid(row=1, column=0, padx=(20, 8), pady=12)

        update_value = tk.Entry(
            update_card,
            font=("Segoe UI", 10),
            width=25
        )
        # Update Value means NEW STUDENT ID only.
        # The student's name and other fields must remain unchanged.
        update_value.insert(0, "201")
        update_value.grid(row=1, column=1, columnspan=2, padx=5, sticky="w")

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
            row=2, column=0, columnspan=5,
            sticky="w", padx=20, pady=(0, 15)
        )

        def update_selected_file():

            filename = update_file.get()
            old_id = update_id.get().strip()
            new_id = update_value.get().strip()

            if not old_id or not new_id:
                update_result.config(
                    text="Enter the existing Student ID and the new Student ID.",
                    fg=RED
                )
                return

            if not old_id.isdigit() or not new_id.isdigit():
                update_result.config(
                    text="Student IDs must contain numbers only.",
                    fg=RED
                )
                return

            if old_id == new_id:
                update_result.config(
                    text="New Student ID must be different from the existing ID.",
                    fg=RED
                )
                return

            if filename == "Students.txt":
                rows = self.legacy_demo_students
            elif filename == "Marks.txt":
                rows = self.legacy_demo_marks
            else:
                rows = self.legacy_demo_attendance

            # Only the Student ID column (column 0) is changed.
            # Names, subjects, marks and attendance values stay untouched.
            matching_rows = [row for row in rows if row[0] == old_id]

            if not matching_rows:
                update_result.config(
                    text=f"Student ID {old_id} was not found in {filename}.",
                    fg=RED
                )
                return

            # Prevent duplicate IDs inside the selected independent file.
            if any(row[0] == new_id for row in rows):
                update_result.config(
                    text=f"Student ID {new_id} already exists in {filename}.",
                    fg=RED
                )
                return

            for row in matching_rows:
                row[0] = new_id

            update_result.config(
                text=(
                    f"✓ ONLY {filename} was updated.\n"
                    f"Student ID: {old_id} → {new_id}\n"
                    f"Updated records: {len(matching_rows)}\n\n"
                    "Other legacy files were NOT changed.\n"
                    "Name and all other values remain unchanged."
                ),
                fg=GREEN
            )

            self.refresh_legacy_demo_files()

        tk.Button(
            update_card,
            text="UPDATE SELECTED FILE",
            command=update_selected_file,
            font=("Segoe UI", 9, "bold"),
            bg=ORANGE,
            fg=WHITE,
            activebackground=ORANGE,
            activeforeground=WHITE,
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2"
        ).grid(row=1, column=4, padx=20)

        # --------------------------------------------------------
        # FILE CONTENTS
        # --------------------------------------------------------

        self.section_title("3. Independent Legacy Files")

        self.legacy_file_area = tk.Frame(
            self.content,
            bg=BG
        )
        self.legacy_file_area.pack(
            fill="x",
            padx=35
        )

        self.refresh_legacy_demo_files()

        self.info_card(
            "What this demonstrates",
            "Select Students.txt, Marks.txt or Attendance.txt before updating. "
            "Only the selected file changes. The other files remain unchanged. "
            "This demonstrates that legacy files are independent and do not "
            "automatically maintain relationships between each other.",
            ORANGE_LIGHT,
            ORANGE
        )

    def refresh_legacy_demo_files(self):

        # Safety initialization: the independent legacy file cards
        # must always contain visible demo records.
        if not hasattr(self, "legacy_demo_students"):
            self.legacy_demo_students = [
                ["101", "Bhargavi", "CSE-AI&DS"],
                ["102", "Aarav", "CSE-AI&DS"],
                ["103", "Diya", "CSE-AI&DS"]
            ]

        if not hasattr(self, "legacy_demo_marks"):
            self.legacy_demo_marks = [
                ["101", "1", "85"], ["101", "2", "91"], ["101", "3", "78"],
                ["102", "1", "74"], ["102", "2", "82"], ["102", "3", "80"],
                ["103", "1", "90"], ["103", "2", "88"], ["103", "3", "84"]
            ]

        if not hasattr(self, "legacy_demo_attendance"):
            self.legacy_demo_attendance = [
                ["101", "1", "92%"], ["101", "2", "89%"], ["101", "3", "86%"],
                ["102", "1", "84%"], ["102", "2", "88%"], ["102", "3", "91%"],
                ["103", "1", "95%"], ["103", "2", "93%"], ["103", "3", "90%"]
            ]


        if not hasattr(self, "legacy_file_area"):
            return

        for widget in self.legacy_file_area.winfo_children():
            widget.destroy()

        files_data = [
            (
                "Students.txt",
                "Student ID | Name | Course",
                self.legacy_demo_students
            ),
            (
                "Marks.txt",
                "Student ID | Subject ID | Marks",
                self.legacy_demo_marks
            ),
            (
                "Attendance.txt",
                "Student ID | Subject ID | Attendance",
                self.legacy_demo_attendance
            )
        ]

        for filename, heading, rows in files_data:

            card = tk.Frame(
                self.legacy_file_area,
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


    def show_view_level(self):

        self.clear_page()

        self.page_header(
            "View / External Level",
            "Different users can see different views of the same logical database."
        )

        self.info_card(
            "External / View Level",
            "The View Level contains user-specific views. These are not new database "
            "tables; they are selected presentations of data from the logical tables. "
            "All views use the same underlying DBMS data.",
            "#F0EEFF",
            "#6C63FF"
        )

        # -------------------- View 1 --------------------
        self.section_title("View 1 – Student Information View")
        rows = self.application.get_all_tables().get("STUDENT", [])
        if not rows:
            rows = [
                (101, "Bhargavi", 1, "bhargavi@example.com"),
                (102, "Aarav", 1, "aarav@example.com"),
                (103, "Diya", 1, "diya@example.com")
            ]
        self.create_view_table(
            "Student View",
            "Administrator view – basic student information only.",
            ["Student ID", "Student Name", "Course ID", "Email"],
            rows
        )

        # -------------------- View 2 --------------------
        self.section_title("View 2 – Academic Performance View")
        student_names = {str(r[0]): str(r[1]) for r in rows if len(r) >= 2}
        marks = self.application.get_all_tables().get("MARKS", [])
        academic_rows = []
        for r in marks:
            if len(r) >= 3:
                sid = str(r[0])
                academic_rows.append((sid, student_names.get(sid, "Unknown"), r[1], r[2]))
        if not academic_rows:
            academic_rows = [
                (101, "Bhargavi", 1, 85),
                (101, "Bhargavi", 2, 91),
                (102, "Aarav", 1, 74),
                (103, "Diya", 1, 90)
            ]
        self.create_view_table(
            "Academic View",
            "Faculty view – student performance without exposing unrelated data.",
            ["Student ID", "Student Name", "Subject ID", "Marks"],
            academic_rows
        )

        # -------------------- View 3 --------------------
        self.section_title("View 3 – Attendance View")
        attendance = self.application.get_all_tables().get("ATTENDANCE", [])
        attendance_rows = []
        for r in attendance:
            if len(r) >= 3:
                sid = str(r[0])
                attendance_rows.append((sid, student_names.get(sid, "Unknown"), r[1], r[2]))
        if not attendance_rows:
            attendance_rows = [
                (101, "Bhargavi", 1, "92%"),
                (101, "Bhargavi", 2, "89%"),
                (102, "Aarav", 1, "84%"),
                (103, "Diya", 1, "95%")
            ]
        self.create_view_table(
            "Attendance View",
            "Faculty/admin view – attendance information only.",
            ["Student ID", "Student Name", "Subject ID", "Attendance"],
            attendance_rows
        )

        self.info_card(
            "View Level and Data Independence",
            "These views are different presentations of the same logical database. "
            "Changing the presentation of a view does not require changing the "
            "Logical Level tables or the Physical Level storage.",
            "#E9F8F0",
            "#16A05D"
        )

    def create_view_table(self, title, description, headings, rows):

        card = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(fill="x", padx=35, pady=6)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 11, "bold"),
            fg=DARK,
            bg=WHITE,
            anchor="w"
        ).pack(fill="x", padx=15, pady=(10, 2))

        tk.Label(
            card,
            text=description,
            font=("Segoe UI", 9),
            fg=GRAY,
            bg=WHITE,
            anchor="w"
        ).pack(fill="x", padx=15, pady=(0, 5))

        columns=[f"c{i}" for i in range(len(headings))]
        tree=ttk.Treeview(card, columns=columns, show="headings", height=max(3,min(7,len(rows))))
        for c,h in zip(columns,headings):
            tree.heading(c,text=h)
            tree.column(c,width=180,anchor="center")
        for row in rows:
            tree.insert("","end",values=tuple(row))
        tree.pack(fill="x",padx=15,pady=(3,14))


    def show_logical_level(self):

        self.clear_page()

        self.page_header(
            "Logical / Conceptual Level",
            "The logical level defines the tables, attributes, keys and relationships."
        )

        self.info_card(
            "Logical Level",
            "This level describes what data exists and how the data is related. "
            "It does not describe the physical storage method.",
            "#FFF6DF",
            "#F59E0B"
        )

        self.section_title("Relational Tables")

        tables = [
            ("COURSE", "course_id (PK)\ncourse_name", "Stores course information."),
            ("STUDENT", "student_id (PK)\nname\ncourse_id (FK)\nemail", "Stores student information."),
            ("SUBJECT", "subject_id (PK)\nsubject_name\ncourse_id (FK)", "Stores subjects linked to courses."),
            ("MARKS", "student_id (PK/FK)\nsubject_id (PK/FK)\nmarks", "Connects students and subjects with marks."),
            ("ATTENDANCE", "student_id (PK/FK)\nsubject_id (PK/FK)\nattendance_percentage", "Connects students and subjects with attendance.")
        ]

        for table_name, fields, purpose in tables:
            box=tk.Frame(self.content,bg=BLUE_LIGHT,highlightbackground=BLUE,highlightthickness=1,cursor="hand2")
            box.pack(fill="x",padx=35,pady=5)
            title=tk.Label(box,text=table_name,font=("Segoe UI",12,"bold"),fg=BLUE,bg=BLUE_LIGHT,cursor="hand2")
            title.pack(anchor="w",padx=16,pady=(12,2))
            detail=tk.Label(box,text="Click to view table structure and purpose",font=("Segoe UI",9),fg=BLUE,bg=BLUE_LIGHT,anchor="w",cursor="hand2")
            detail.pack(anchor="w",padx=16,pady=(0,10))
            def show_detail(event=None, d=detail, f=fields, p=purpose):
                d.config(text=f"{p}\n\n{f}")
            for w in (box,title,detail):
                w.bind("<Button-1>",show_detail)

        self.section_title("Relationships")
        self.info_card(
            "Entity Relationships",
            "COURSE 1 ─────────< STUDENT\n"
            "COURSE 1 ─────────< SUBJECT\n"
            "STUDENT 1 ────────< MARKS >──────── 1 SUBJECT\n"
            "STUDENT 1 ────────< ATTENDANCE >──── 1 SUBJECT",
            "#EAF3FF",
            "#1976D2"
        )

        self.info_card(
            "Logical Data Independence",
            "A change in the logical schema should be managed without forcing "
            "every external user view to change. The purpose of this level is "
            "to describe the complete logical structure independently of storage.",
            "#F0EEFF",
            "#6C63FF"
        )


    def show_physical_level(self):

        self.clear_page()

        self.page_header(
            "Physical / Internal Level",
            "The physical level describes internal storage and access structures used by the DBMS."
        )

        self.info_card(
            "Physical / Internal Level",
            "This is where the DBMS manages how records are stored and accessed internally. "
            "Users do not need to know these implementation details.",
            "#E9F8F0",
            "#16A05D"
        )

        self.section_title("Internal Storage / Access Structures")

        physical_items = [
            ("Student Data File", "student data records", "Stores student records internally."),
            ("Course Data File", "course data records", "Stores course records internally."),
            ("Subject Data File", "subject data records", "Stores subject records internally."),
            ("Marks Data File", "marks records", "Stores marks records internally."),
            ("Attendance Data File", "attendance records", "Stores attendance records internally."),
        ]

        for name, structure, purpose in physical_items:
            card=tk.Frame(self.content,bg=PURPLE_LIGHT,highlightbackground=PURPLE,highlightthickness=1,cursor="hand2")
            card.pack(fill="x",padx=35,pady=5)
            title=tk.Label(card,text=name,font=("Segoe UI",11,"bold"),fg=PURPLE,bg=PURPLE_LIGHT,cursor="hand2")
            title.pack(anchor="w",padx=16,pady=(12,2))
            detail=tk.Label(card,text=f"{structure}  •  Click to view physical details",font=("Segoe UI",9),fg=PURPLE,bg=PURPLE_LIGHT,anchor="w",cursor="hand2")
            detail.pack(anchor="w",padx=16,pady=(0,10))
            def show_detail(event=None, d=detail, s=structure, p=purpose):
                d.config(text=f"{p}\nStorage representation: {s}\nThe logical table can remain unchanged even when internal access/storage is changed.")
            for w in (card,title,detail):
                w.bind("<Button-1>",show_detail)

        self.section_title("Physical Access Structures")
        structures=self.application.get_physical_structures()
        for index_name, table_name, sql in structures:
            row=tk.Frame(self.content,bg=GREEN_LIGHT,highlightbackground=GREEN,highlightthickness=1)
            row.pack(fill="x",padx=35,pady=4)
            tk.Label(row,text=index_name,font=("Consolas",10,"bold"),fg=GREEN,bg=GREEN_LIGHT,width=30,anchor="w").pack(side="left",padx=15,pady=12)
            tk.Label(row,text=table_name,font=("Consolas",10),fg=GREEN,bg=GREEN_LIGHT,width=22,anchor="w").pack(side="left")
            tk.Label(row,text="Index / access structure",font=FONT,fg=GREEN,bg=GREEN_LIGHT).pack(side="left",padx=10)

        self.info_card(
            "Physical Data Independence",
            "Changing internal storage or access structures should not require "
            "changes to the logical tables or the user-facing views.",
            "#FFF6DF",
            "#F59E0B"
        )


    def show_three_tier(self):

        self.clear_page()

        self.page_header(
            "Three-Tier Architecture",
            "How the application is organised into Presentation, Application / Logic and Database tiers."
        )

        self.info_card(
            "Why is 3-Tier Architecture used?",
            "It separates the user interface, application processing and database storage. "
            "This makes the application easier to understand, maintain and modify because each tier has a separate responsibility.",
            "#EAF3FF",
            "#1976D2"
        )

        self.section_title("Application Architecture")

        # Same neutral appearance for all three tiers. No tier-specific
        # colour coding is used because the tiers are separate by function,
        # not by colour.
        self.create_clickable_tier(
            "1",
            "PRESENTATION TIER",
            "User Interface / GUI",
            "RESPONSIBILITY:\n"
            "This is the part visible to the user.\n\n"
            "In our project:\n"
            "• Dashboard and screens\n"
            "• Search and Update controls\n"
            "• Legacy Files display\n"
            "• DBMS table display\n\n"
            "The Presentation Tier sends the user's request to the Application Tier."
        )

        tk.Label(
            self.content,
            text="↓",
            font=("Segoe UI", 18, "bold"),
            fg=DARK,
            bg=BG
        ).pack(pady=2)

        self.create_clickable_tier(
            "2",
            "APPLICATION / LOGIC TIER",
            "Python Application Logic",
            "RESPONSIBILITY:\n"
            "Processes requests received from the user interface.\n\n"
            "In our project:\n"
            "• Processes Search requests\n"
            "• Processes Update requests\n"
            "• Validates input\n"
            "• Connects the GUI with the database\n"
            "• Performs application operations\n\n"
            "The Logic Tier acts as the middle layer between the UI and database."
        )

        tk.Label(
            self.content,
            text="↓",
            font=("Segoe UI", 18, "bold"),
            fg=DARK,
            bg=BG
        ).pack(pady=2)

        self.create_clickable_tier(
            "3",
            "DATABASE TIER",
            "DBMS / SQLite Database",
            "RESPONSIBILITY:\n"
            "Stores and manages the application's data.\n\n"
            "In our project:\n"
            "• Student table\n"
            "• Course table\n"
            "• Subject table\n"
            "• Marks table\n"
            "• Attendance table\n"
            "• Keys and relationships\n\n"
            "The Database Tier returns the required data to the Application Tier."
        )

        self.section_title("How a Request Travels Through the 3 Tiers")

        self.info_card(
            "Example: Search for a Student",
            "USER\n"
            "↓\n"
            "PRESENTATION TIER – user clicks Search\n"
            "↓\n"
            "APPLICATION / LOGIC TIER – processes the request\n"
            "↓\n"
            "DATABASE TIER – searches the required table\n"
            "↓\n"
            "APPLICATION / LOGIC TIER – receives the result\n"
            "↓\n"
            "PRESENTATION TIER – displays the result",
            "#F0EEFF",
            "#6C63FF"
        )

        self.info_card(
            "Important Difference",
            "3-Tier Architecture is about the APPLICATION:\n"
            "Presentation → Application / Logic → Database.\n\n"
            "DBMS Three-Level Architecture is about DATABASE ABSTRACTION:\n"
            "View / External → Logical / Conceptual → Physical / Internal.\n\n"
            "So this screen explains why our application is divided into three tiers. "
            "The View, Logical, Physical and Data Independence sections elsewhere in the project are not changed by this screen.",
            "#E9F8F0",
            "#16A05D"
        )

    def create_clickable_tier(self, number, title, technology, details):
        card = tk.Frame(
            self.content,
            bg=BLUE_LIGHT,
            highlightbackground=BLUE,
            highlightthickness=1,
            cursor="hand2"
        )
        card.pack(fill="x", padx=35, pady=5)

        top = tk.Frame(card, bg=BLUE_LIGHT)
        top.pack(fill="x", padx=18, pady=(13, 5))

        tk.Label(
            top,
            text=number,
            font=("Segoe UI", 22, "bold"),
            fg=BLUE,
            bg=BLUE_LIGHT,
            width=3
        ).pack(side="left")

        title_frame = tk.Frame(top, bg=BLUE_LIGHT)
        title_frame.pack(side="left", fill="x", expand=True)

        tk.Label(
            title_frame,
            text=title,
            font=("Segoe UI", 14, "bold"),
            fg=BLUE,
            bg=BLUE_LIGHT,
            anchor="w"
        ).pack(fill="x")

        tk.Label(
            title_frame,
            text=technology,
            font=("Segoe UI", 10, "bold"),
            fg=BLUE,
            bg=BLUE_LIGHT,
            anchor="w"
        ).pack(fill="x", pady=(2, 0))

        detail = tk.Label(
            card,
            text="Click this tier to view its responsibility →",
            font=("Segoe UI", 9),
            fg=BLUE,
            bg=BLUE_LIGHT,
            justify="left",
            anchor="w"
        )
        detail.pack(fill="x", padx=18, pady=(3, 13))

        def show_details(event=None):
            detail.config(text=details)

        for widget in (card, top, title_frame, detail):
            widget.bind("<Button-1>", show_details)

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

    def _independence_status_panel(self, parent, changed_level):
        """Show level isolation using one common UI style for all levels."""
        panel = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        panel.pack(fill="x", padx=35, pady=10)

        tk.Label(
            panel,
            text="DATA INDEPENDENCE / ISOLATION",
            font=("Segoe UI", 12, "bold"),
            fg=DARK,
            bg=WHITE
        ).pack(anchor="w", padx=18, pady=(14, 8))

        levels = [
            ("View Level", "View Level"),
            ("Logical Level", "Logical Level"),
            ("Physical Level", "Physical Level")
        ]

        for label, key in levels:
            state = "CHANGED ✓" if key == changed_level else "UNCHANGED ✓"

            row = tk.Frame(panel, bg=WHITE)
            row.pack(fill="x", padx=18, pady=3)

            tk.Label(
                row,
                text=label,
                font=("Segoe UI", 10, "bold"),
                fg=DARK,
                bg=WHITE,
                width=18,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                row,
                text=state,
                font=("Segoe UI", 10),
                fg=DARK,
                bg=WHITE,
                anchor="w"
            ).pack(side="left")

        tk.Label(
            panel,
            text="UI theme / colours → UNCHANGED ✓    Database data → UNCHANGED ✓",
            font=("Segoe UI", 10),
            fg=DARK,
            bg=WHITE
        ).pack(anchor="w", padx=18, pady=(8, 14))


    def show_data_independence(self):

        self.clear_page()

        self.page_header(
            "Data Independence & Isolation",
            "Each level can be changed independently. A change in one level "
            "does not require changes to the other levels."
        )

        self.info_card(
            "Data Independence",
            "The three levels are isolated. Changing the VIEW changes only "
            "the presentation; changing the LOGICAL level changes only the "
            "conceptual schema; changing the PHYSICAL level changes only "
            "internal storage/access. The other levels remain unchanged.",
            BLUE_LIGHT,
            BLUE
        )

        self.section_title("Interactive Demonstration")

        panel = tk.Frame(
            self.content,
            bg=BLUE_LIGHT,
            highlightbackground=BLUE,
            highlightthickness=1
        )
        panel.pack(fill="x", padx=35, pady=8)

        # IMPORTANT: all three rows use the SAME neutral colour.
        # The colour is only a UI style; changing a level never changes
        # the colour/state of another level or any other project page.
        neutral = DARK

        self.create_independence_row(
            panel, 0,
            "VIEW / EXTERNAL LEVEL",
            "Student Dashboard → Result Cards",
            neutral,
            self.change_view
        )

        self.create_independence_row(
            panel, 1,
            "LOGICAL / CONCEPTUAL LEVEL",
            "Relational Schema",
            neutral,
            self.change_logical
        )

        self.create_independence_row(
            panel, 2,
            "PHYSICAL / INTERNAL LEVEL",
            "Index Structures",
            neutral,
            self.change_physical
        )

        self.section_title("Live Result")

        self.independence_result = tk.Label(
            self.content,
            text=(
                "No change made yet.\n\n"
                "Click any button above. Only that level will show a change; "
                "the other levels will remain UNCHANGED."
            ),
            font=("Segoe UI", 11),
            fg=BLUE,
            bg=BLUE_LIGHT,
            justify="left",
            anchor="w",
            padx=25,
            pady=20
        )
        self.independence_result.pack(fill="x", padx=35, pady=8)

        self.section_title("Isolation Check")

        self.isolation_tree = ttk.Treeview(
            self.content,
            columns=("level", "status", "other1", "other2"),
            show="headings",
            height=3
        )

        for key, heading, width in [
            ("level", "Selected Level", 260),
            ("status", "Its Status", 220),
            ("other1", "Other Level 1", 280),
            ("other2", "Other Level 2", 280)
        ]:
            self.isolation_tree.heading(key, text=heading)
            self.isolation_tree.column(key, width=width, anchor="center")

        self.isolation_tree.insert(
            "", "end",
            iid="view",
            values=("View / External", "UNCHANGED", "Logical: UNCHANGED", "Physical: UNCHANGED")
        )
        self.isolation_tree.insert(
            "", "end",
            iid="logical",
            values=("Logical / Conceptual", "UNCHANGED", "View: UNCHANGED", "Physical: UNCHANGED")
        )
        self.isolation_tree.insert(
            "", "end",
            iid="physical",
            values=("Physical / Internal", "UNCHANGED", "View: UNCHANGED", "Logical: UNCHANGED")
        )
        self.isolation_tree.pack(fill="x", padx=35, pady=8)

    def create_independence_row(self, parent, row, level, current, color, command):

        tk.Label(
            parent,
            text=level,
            font=("Segoe UI", 11, "bold"),
            fg=BLUE,
            bg=BLUE_LIGHT,
            anchor="w",
            width=30
        ).grid(row=row, column=0, padx=18, pady=15, sticky="w")

        value = tk.Label(
            parent,
            text=current,
            font=("Segoe UI", 10, "bold"),
            fg=BLUE,
            bg=BLUE_LIGHT,
            anchor="w",
            width=30
        )
        value.grid(row=row, column=1, padx=10, sticky="w")

        button = tk.Button(
            parent,
            text="CHANGE THIS LEVEL",
            command=lambda: command(value),
            font=("Segoe UI", 9, "bold"),
            bg=BLUE,
            fg=WHITE,
            activebackground=BLUE,
            activeforeground=WHITE,
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2"
        )
        button.grid(row=row, column=2, padx=15)
        parent.grid_columnconfigure(1, weight=1)

    def update_isolation_status(self, selected):

        states = {
            "view": ["View / External", "UNCHANGED", "Logical: UNCHANGED", "Physical: UNCHANGED"],
            "logical": ["Logical / Conceptual", "UNCHANGED", "View: UNCHANGED", "Physical: UNCHANGED"],
            "physical": ["Physical / Internal", "UNCHANGED", "View: UNCHANGED", "Logical: UNCHANGED"]
        }

        selected_row = {
            "view": ["View / External", "CHANGED ✓", "Logical: UNCHANGED ✓", "Physical: UNCHANGED ✓"],
            "logical": ["Logical / Conceptual", "CHANGED ✓", "View: UNCHANGED ✓", "Physical: UNCHANGED ✓"],
            "physical": ["Physical / Internal", "CHANGED ✓", "View: UNCHANGED ✓", "Logical: UNCHANGED ✓"]
        }

        for iid, values in states.items():
            self.isolation_tree.item(iid, values=values)
        self.isolation_tree.item(selected, values=selected_row[selected])

    def change_view(self, label):

        # Presentation-only change. No database data, logical schema,
        # physical structures, or other UI colours are changed.
        label.config(text="Student Dashboard → Result Cards")
        self.independence_result.config(
            text=(
                "VIEW LEVEL CHANGED ✓\n\n"
                "Example: Table View → Card View\n\n"
                "Database data: UNCHANGED ✓\n"
                "Logical level: UNCHANGED ✓\n"
                "Physical level: UNCHANGED ✓\n"
                "Other project UI / colours: UNCHANGED ✓\n\n"
                "Only the user-facing presentation changed."
            ),
            fg=DARK
        )
        self.update_isolation_status("view")

    def change_logical(self, label):

        # Conceptual-schema-only change. Other levels remain isolated.
        label.config(text="STUDENT Table + Email Attribute")
        self.independence_result.config(
            text=(
                "LOGICAL LEVEL CHANGED ✓\n\n"
                "Example: EMAIL attribute added to the STUDENT schema.\n\n"
                "View level: UNCHANGED ✓\n"
                "Physical level: UNCHANGED ✓\n"
                "Existing Student/Course IDs: UNCHANGED ✓\n"
                "Other project UI / colours: UNCHANGED ✓\n\n"
                "Only the conceptual schema changed."
            ),
            fg=DARK
        )
        self.update_isolation_status("logical")

    def change_physical(self, label):

        # Internal-storage/access-only change. Other levels remain isolated.
        label.config(text="Index Added / Access Method Changed")
        self.independence_result.config(
            text=(
                "PHYSICAL LEVEL CHANGED ✓\n\n"
                "Example: an INDEX/access method is changed for faster retrieval.\n\n"
                "View level: UNCHANGED ✓\n"
                "Logical level: UNCHANGED ✓\n"
                "Actual student/marks information: UNCHANGED ✓\n"
                "Other project UI / colours: UNCHANGED ✓\n\n"
                "Only the internal implementation changed."
            ),
            fg=DARK
        )
        self.update_isolation_status("physical")

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

        # ========================================================
        # SEARCH
        # ========================================================

        self.section_title("1. Search Student in DBMS")

        search_card = tk.Frame(
            self.content,
            bg=BLUE_LIGHT,
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
            bg=GREEN_LIGHT,
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