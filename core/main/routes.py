import subprocess

from flask import Blueprint, render_template, request, redirect, session, abort

from db import get_db, get_problems, get_problem
from utils import LANGUAGES, STARTERS, logged_in, login_required, run_code

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    problems = get_problems()
    solved = set()
    if logged_in():
        conn = get_db()
        rows = conn.execute(
            "SELECT DISTINCT problem_id FROM submissions WHERE user_id = ? AND verdict = 'Accepted'",
            (session["user_id"],)
        ).fetchall()
        conn.close()
        solved = {row["problem_id"] for row in rows}
    return render_template("home.html", problems=problems, solved=solved)


@main_bp.route("/problem/<int:pid>", methods=["GET", "POST"])
@login_required
def show_problem(pid):
    problem = get_problem(pid)
    if not problem:
        abort(404)

    if request.method == "POST":
        user_code = request.form.get("code", "").strip()
        language  = request.form.get("language", "python")

        if language not in LANGUAGES:
            language = "python"

        if not user_code:
            return render_template("problem.html", problem=problem,
                                   languages=LANGUAGES, starters=STARTERS,
                                   error="Code cannot be empty.",
                                   selected_lang=language)

        results = []
        final_verdict = "Accepted"

        for case in problem["test_cases"]:
            try:
                stdout, stderr, returncode = run_code(language, user_code, case["input"])

                user_output     = stdout.strip()
                expected_output = case["output"].strip()

                if returncode != 0:
                    final_verdict = "Runtime Error" if "Compilation Error" not in stderr else "Compilation Error"
                    results.append({
                        "input":    case["input"],
                        "expected": expected_output,
                        "got":      stderr.strip(),
                        "status":   final_verdict
                    })
                    break

                if user_output != expected_output:
                    final_verdict = "Wrong Answer"

                results.append({
                    "input":    case["input"],
                    "expected": expected_output,
                    "got":      user_output,
                    "status":   "Passed" if user_output == expected_output else "Failed"
                })

            except subprocess.TimeoutExpired:
                final_verdict = "Time Limit Exceeded"
                results.append({
                    "input":    case["input"],
                    "expected": case["output"],
                    "got":      "Execution Timed Out",
                    "status":   "TLE"
                })
                break

        conn = get_db()
        conn.execute(
            "INSERT INTO submissions (user_id, problem_id, code, language, verdict) VALUES (?, ?, ?, ?, ?)",
            (session["user_id"], pid, user_code, language, final_verdict)
        )
        conn.commit()
        conn.close()

        return render_template("result.html", problem=problem,
                               verdict=final_verdict, results=results,
                               language=LANGUAGES[language]["label"])

    # GET — use last submitted language for this problem if available
    selected_lang = "python"
    if logged_in():
        conn = get_db()
        last = conn.execute(
            "SELECT language FROM submissions WHERE user_id=? AND problem_id=? ORDER BY submitted_at DESC LIMIT 1",
            (session["user_id"], pid)
        ).fetchone()
        conn.close()
        if last and last["language"] in LANGUAGES:
            selected_lang = last["language"]

    return render_template("problem.html", problem=problem,
                           languages=LANGUAGES, starters=STARTERS,
                           selected_lang=selected_lang)


@main_bp.route("/profile")
@login_required
def profile():
    conn = get_db()
    submissions = conn.execute(
        "SELECT * FROM submissions WHERE user_id = ? ORDER BY submitted_at DESC",
        (session["user_id"],)
    ).fetchall()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (session["user_id"],)
    ).fetchone()
    conn.close()

    total    = len(submissions)
    accepted = sum(1 for s in submissions if s["verdict"] == "Accepted")
    solved   = len({s["problem_id"] for s in submissions if s["verdict"] == "Accepted"})
    problems = {p["id"]: p for p in get_problems()}

    return render_template("profile.html", submissions=submissions,
                           total=total, accepted=accepted, solved=solved,
                           user=user, problems=problems, languages=LANGUAGES)


@main_bp.route("/leaderboard")
def leaderboard():
    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    board = []
    for user in users:
        solved = conn.execute(
            "SELECT COUNT(DISTINCT problem_id) FROM submissions WHERE user_id = ? AND verdict = 'Accepted'",
            (user["id"],)
        ).fetchone()[0]
        total = conn.execute(
            "SELECT COUNT(*) FROM submissions WHERE user_id = ?",
            (user["id"],)
        ).fetchone()[0]
        board.append({"username": user["username"], "solved": solved, "total": total})
    conn.close()
    board.sort(key=lambda x: x["solved"], reverse=True)
    return render_template("leaderboard.html", board=board)