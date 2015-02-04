import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row
#     """\
# Student: %s %s
# Github account: %s"""%(row[0], row[1], row[2])

def get_project_by_title(title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query,(title,))
    row = DB.fetchone()
    print """\
Title: %s
Description: %s
Max_Grade: %i"""%(row[0], row[1], row[2])

def student_grade_by_project(title, first_name, last_name): 
    query = """SELECT grade FROM Students AS s JOIN Grades AS g ON (g.student_github = s.github) WHERE (title = ?) AND (first_name = ?) AND (last_name = ?)"""
    DB.execute(query,(title, first_name, last_name))
    row = DB.fetchone()
    print "Grade: %r"%(row[0])

def show_grades_for_student(first_name, last_name):
    query = """SELECT title, grade FROM Students AS s JOIN Grades AS g ON (g.student_github = s.github) WHERE first_name = ? AND last_name = ?"""
    DB.execute(query,(first_name, last_name))
    row = DB.fetchall()
    print "Here are all the grades for %s %s:" % (first_name, last_name)
    for title, grade in row:
        print "%s %s" % (title, grade)


def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?,?,?)"""
    DB.execute(query,(first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) VALUES (?,?,?)"""
    DB.execute(query,(title, description,max_grade))
    CONN.commit()
    print "Successfully added project: %s %s %s" % (title, description, max_grade)

def give_student_grade(first_name, last_name, title, grade):
    query = """INSERT INTO Grades VALUES((SELECT github FROM Students WHERE first_name = ? AND last_name = ?), ?, ?)"""
    DB.execute(query,(first_name, last_name, title, grade))
    CONN.commit()
    print "Successfully gave %s %s the grade %s on %s project" % (first_name, last_name, grade, title)

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(",")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "get_grade":
            student_grade_by_project(*args)
        elif command == "give_grade":
            give_student_grade(*args)
        elif command == "print_grades":
            show_grades_for_student(*args)
    CONN.close()

if __name__ == "__main__":
    main()
