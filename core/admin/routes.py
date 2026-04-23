import json

from flask import Blueprint, render_template, request, redirect, session, abort

from db import get_db, get_problems, get_problem
from utils import admin_required, parse_test_cases

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@admin_required
def dashboard():
    conn = get_db()
    problems  = get_problems()
    users     = conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
    sub_count = conn.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]
    conn.close()
    return render_template("admin/dashboard.html",
                           problems=problems, users=users, sub_count=sub_count)


@admin_bp.route("/problem/new", methods=["GET", "POST"])
@admin_required
def new_problem():
    error = None
    if request.method == "POST":
        title      = request.form.get("title", "").strip()
        difficulty = request.form.get("difficulty", "Easy")
        desc       = request.form.get("desc", "").strip()
        raw        = request.form.get("test_cases", "").strip()
        test_cases, error = parse_test_cases(raw)

        if not title or not desc:
            error = "Title and description are required."
        elif not error:
            conn = get_db()
            conn.execute(
                "INSERT INTO problems (title, difficulty, desc, test_cases) VALUES (?, ?, ?, ?)",
                (title, difficulty, desc, json.dumps(test_cases))
            )
            conn.commit()
            conn.close()
            return redirect("/admin")

    return render_template("admin/problem_form.html", error=error,
                           problem=None, action="Add")


@admin_bp.route("/problem/<int:pid>/edit", methods=["GET", "POST"])
@admin_required
def edit_problem(pid):
    problem = get_problem(pid)
    if not problem:
        abort(404)

    error = None
    if request.method == "POST":
        title      = request.form.get("title", "").strip()
        difficulty = request.form.get("difficulty", "Easy")
        desc       = request.form.get("desc", "").strip()
        raw        = request.form.get("test_cases", "").strip()
        test_cases, error = parse_test_cases(raw)

        if not title or not desc:
            error = "Title and description are required."
        elif not error:
            conn = get_db()
            conn.execute(
                "UPDATE problems SET title=?, difficulty=?, desc=?, test_cases=? WHERE id=?",
                (title, difficulty, desc, json.dumps(test_cases), pid)
            )
            conn.commit()
            conn.close()
            return redirect("/admin")

    tc_text = "\n".join(
        f"{c['input']}|||{c['output']}" for c in problem["test_cases"]
    )
    return render_template("admin/problem_form.html", error=error,
                           problem=problem, tc_text=tc_text, action="Edit")


@admin_bp.route("/problem/<int:pid>/delete", methods=["POST"])
@admin_required
def delete_problem(pid):
    conn = get_db()
    conn.execute("DELETE FROM problems WHERE id = ?", (pid,))
    conn.commit()
    conn.close()
    return redirect("/admin")


@admin_bp.route("/user/<int:uid>/toggle-admin", methods=["POST"])
@admin_required
def toggle_admin(uid):
    if uid == session["user_id"]:
        return redirect("/admin")
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()
    if user:
        conn.execute("UPDATE users SET is_admin = ? WHERE id = ?",
                     (0 if user["is_admin"] else 1, uid))
        conn.commit()
    conn.close()
    return redirect("/admin")


@admin_bp.route("/user/<int:uid>/delete", methods=["POST"])
@admin_required
def delete_user(uid):
    if uid == session["user_id"]:
        return redirect("/admin")
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id = ?", (uid,))
    conn.execute("DELETE FROM submissions WHERE user_id = ?", (uid,))
    conn.commit()
    conn.close()
    return redirect("/admin")