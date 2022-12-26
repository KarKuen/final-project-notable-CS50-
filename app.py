import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required
# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_COOKIE_NAME"]
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///notes.db")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":

        filename = request.form.get("filename")
        if (not(not filename) and len(filename) != 0) and db.execute("SELECT filename from notes WHERE filename = ? AND user_id = ?", filename, session["user_id"]) == []:
            db.execute("INSERT INTO notes (user_id, filename, notes, todo, scribbles) VALUES (?, ?, ?, ?, ?)", session["user_id"], request.form.get("filename"), "notable", "<input class='checkbox' type='checkbox'> todo", "<u>scribbles</u>&nbsp;")
            session["filename"] = request.form.get("filename")
        elif (request.form.get("notes_id")):
            session["filename"] = db.execute("SELECT filename FROM notes WHERE notes_id = ?", request.form.get("notes_id"))[0]["filename"]
        elif (request.form.get("newfilename")):
            db.execute("UPDATE notes SET filename = ? WHERE notes_id = ?", request.form.get("newfilename"), request.form.get("filenameref"))
            session["filename"] = request.form.get("newfilename")
        elif (request.form.get("deletefile")):
            db.execute("DELETE FROM notes WHERE notes_id = ?", request.form.get("deletefile"))
        else:
            notable = request.form.get("content")
            db.execute("UPDATE notes SET notes = ? WHERE user_id = ? AND filename = ?", notable, session["user_id"], session["filename"])

            notable1 = request.form.get("content1")
            db.execute("UPDATE notes SET scribbles = ? WHERE user_id = ? AND filename = ?", notable1, session["user_id"], session["filename"])

            notable2 = request.form.get("content2")
            db.execute("UPDATE notes SET todo = ? WHERE user_id = ? AND filename = ?", notable2, session["user_id"], session["filename"])
    try:
        notes = db.execute("SELECT notes FROM notes WHERE user_id = ? AND filename = ?", session["user_id"], session["filename"])[0]["notes"]
        files = db.execute("SELECT filename, notes_id FROM notes WHERE user_id = ?", session["user_id"])
        todo = db.execute("SELECT todo FROM notes WHERE user_id = ? AND filename = ?", session["user_id"], session["filename"])[0]["todo"]
        scribbles = db.execute("SELECT scribbles FROM notes WHERE user_id = ? AND filename = ?", session["user_id"], session["filename"])[0]["scribbles"]
        return render_template("index.html", notes=notes, files=files, todo=todo, scribbles=scribbles)
    except IndexError:
        return render_template("index.html")
    except KeyError:
        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method =="POST":
        try:
            check = db.execute("SELECT password FROM users WHERE name = ?", request.form.get("username"))[0]["password"]

            if (len(check) != 0 and check_password_hash(db.execute("SELECT * FROM users WHERE name = ?", request.form.get("username"))[0]["password"], request.form.get("password"))):
                session["user_id"] = db.execute("SELECT user_id FROM users WHERE name = ?", request.form.get("username"))[0]["user_id"]
                try:
                    session["filename"] = db.execute("SELECT filename FROM notes WHERE user_id = ? LIMIT 1", session["user_id"])[0]["filename"]
                    return redirect("/")
                except IndexError:
                    return redirect("/")
            else:
                flash("username or password incorrect")

        except IndexError:
            flash("username or password incorrect")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method=="POST":
        if not request.form.get("username"):
            flash("missing username")
        if not request.form.get("password"):
            flash("missing password")
        try:
            if len(db.execute("SELECT name FROM users WHERE name = ?", request.form.get("username"))[0]["name"]) != 0:
                flash("username taken")
        except IndexError:
            db.execute("INSERT INTO users (name, password) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
            session["user_id"] = db.execute("SELECT user_id FROM users WHERE name = ?", request.form.get("username"))[0]["user_id"]
            db.execute("INSERT INTO notes (user_id, notes, filename, todo, scribbles) VALUES (?, ?, ?, ?, ?)", session["user_id"], "notable", "notebook 1", "<input class='checkbox' type='checkbox'> todo", "<u>scribbles</u>&nbsp;")
            return redirect("/login")

    return render_template("register.html")

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")