"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchone()

    print("Student: {} {}\nGitHub account: {}".format(row[0], row[1], row[2]))


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    USER_QUERY = """
        INSERT INTO students (first_name, last_name, github) 
        VALUES (:first_name, :last_name, :github) 
        """

    db.session.execute(USER_QUERY, {'first_name': first_name,
        'last_name': last_name, 'github': github})
    # user_row = user_cursor.fetchone()

    db.session.commit()

    print(f"Successfully added student: {first_name} {last_name}")


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    TITLE_QUERY = """ 
            SELECT title, description, max_grade
            FROM projects
            WHERE title = :title
            """
    projects_cursor = db.session.execute(TITLE_QUERY, {'title': title})

    title_row = projects_cursor.fetchone()

    print("Title: {}\nDescription: {}\n Max_grade: {}".format(title_row[0], title_row[1], title_row[2]))


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    GET_GRADE_QUERY = """
        SELECT grade
        FROM grades
        WHERE student_github = :github AND project_title = :title
        """
    grade_cursor = db.session.execute(GET_GRADE_QUERY, {'github': github, 'title': title})
    grade = grade_cursor.fetchone()
      # grade_cursor = db.session.execute(GET_GRADE_QUERY, {'grade': grade})

    print(f"Student grade is {grade}")


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    pass


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        else:
            if command != "quit":
                print("Invalid Entry. Try again.")


if __name__ == "__main__":
    connect_to_db(app)

    # handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
