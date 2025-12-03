import sqlite3

# Creating a new database
DB_NAME = "school.db"

# Данные для вставки
STUDENTS_DATA = [
    ("Alice Johnson", 2005),
    ("Brian Smith", 2004),
    ("Carla Reyes", 2006),
    ("Daniel Kim", 2005),
    ("Eva Thompson", 2003),
    ("Felix Nguyen", 2007),
    ("Grace Patel", 2005),
    ("Henry Lopez", 2004),
    ("Isabella Martinez", 2006),
]

GRADES_DATA = [
    (1, "Math", 88),
    (1, "English", 92),
    (1, "Science", 85),
    (2, "Math", 75),
    (2, "History", 83),
    (2, "English", 79),
    (3, "Science", 95),
    (3, "Math", 91),
    (3, "Art", 89),
    (4, "Math", 84),
    (4, "Science", 88),
    (4, "Physical Education", 93),
    (5, "English", 90),
    (5, "History", 85),
    (5, "Math", 88),
    (6, "Science", 72),
    (6, "Math", 78),
    (6, "English", 81),
    (7, "Art", 94),
    (7, "Science", 87),
    (7, "Math", 90),
    (8, "History", 77),
    (8, "Math", 83),
    (8, "Science", 80),
    (9, "English", 96),
    (9, "Math", 89),
    (9, "Art", 92),
]


def setup_database():
    """Creates databases, tables and inserts data."""
    conn = None
    try:
        # Connect to the database (will create the school.db file if it doesn't exist)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Creating tables
        # Drop tables, if they exist, for a clean start
        cursor.execute("DROP TABLE IF EXISTS grades;")
        cursor.execute("DROP TABLE IF EXISTS students;")

        # Table students
        cursor.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                birth_year INTEGER
            );
        """)

        # Grades table with foreign key
        cursor.execute("""
            CREATE TABLE grades (
                id INTEGER PRIMARY KEY,
                student_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                grade INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id)
            );
        """)

        # Adding indexes to optimize queries
        cursor.execute("CREATE INDEX idx_student_name ON students (full_name);")
        cursor.execute("CREATE INDEX idx_student_grade ON grades (student_id, grade);")
        cursor.execute("CREATE INDEX idx_subject ON grades (subject);")

        # Inserting sample data
        # Inserting students
        cursor.executemany("INSERT INTO students (full_name, birth_year) VALUES (?, ?);", STUDENTS_DATA)

        # Inserting grades
        cursor.executemany("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?);", GRADES_DATA)

        # Save changes
        conn.commit()
        print(f"Database '{DB_NAME}' successfully created and filled with data.")

    except sqlite3.Error as e:
        print(f"An error occurred SQLite: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    setup_database()