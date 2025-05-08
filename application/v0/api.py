# application/v0/api.py
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, abort, render_template, redirect, url_for, session
from application.v0.service import *
from application.extensions import firestore_db as db

api = Blueprint('api', __name__)
    
@api.route('/dashboard',methods=['GET'])
def dashboard():
    course_data = session.get("lessons", [])
    sorted_courses = sorted(course_data, key=lambda x: x["has_unsubmitted"], reverse=True)
    
    return render_template("dashboard.html", courses=sorted_courses)

@api.route("/chat/<url>")
def chat(url):
    files = [
        {"name": "講義資料1.pdf", "url": "/files/lecture1.pdf"},
        {"name": "演習問題.docx", "url": "/files/exercises.docx"}
    ]
    return render_template("chat.html", course_id=url, files=files)


@api.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    data = request.form
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"success": False, "message": "Missing username or password"}), 400
    data = loginManaba(username, password)
    
    
    if data.get("status") == "error":
        return redirect(url_for("api.login"))
    else:
        session["username"] = username
        json = parse_timetable_from_manaba(data.get("html"))
        session["lessons"] = json
        print(json)
        return redirect(url_for("api.dashboard"))