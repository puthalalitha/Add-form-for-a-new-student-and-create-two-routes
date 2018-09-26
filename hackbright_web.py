"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route("/project-search")
def search_project():
    """Show form for search of project"""

    return render_template("search-project.html")

@app.route("/project")
def project_info():
    """Display info about project"""

    title = request.args.get('title')

    info = hackbright.get_project_by_title(title)

    return render_template("project_info.html",
                           title = info[0],
                           description = info[1],
                           max_grade = info[2])

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    if github in [None,'']:
        return redirect("/student-search")

    first, last, github = hackbright.get_student_by_github(github)
    projects_list = hackbright.get_grades_by_github(github)

    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           projects = projects_list)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/new-student")
def new_student_form():
    """Show form for a new student"""
    return render_template("student-add.html")

@app.route("/student-add", methods=['POST'])
def student_add():
     """Add a student."""


     first_name  = request.form.get("fname")
     last_name = request.form.get("lname")
     github = request.form.get("github")

     hackbright.make_new_student(first_name, last_name, github)

     return render_template("added_student.html", github = github)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

