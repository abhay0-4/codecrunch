import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
from db import init_db


def create_app():
    app = Flask(__name__)
    app.secret_key = "change-this-secret-key"

    # Register blueprints
    from core.auth.routes import auth_bp
    from core.main.routes import main_bp
    from core.admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Error handlers
    from flask import render_template

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app


# ── Init ──────────────────────────────────────────────────────────────────────

app = create_app()

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)