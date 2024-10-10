from flask_smorest import Blueprint
from flask.views import MethodView
from schemas.schemas import *
from sqlalchemy import func
from models.tables import *
from flask import jsonify
from db import db

blp = Blueprint("Coordinator", __name__, description="Operation on Coordinators")

@blp.route("/evaluateStudent/<int:student_id>")
class Evaluate(MethodView):
    """
    Endpoint to evaluate a student's enrollment status.

    Methods:
        get(args): Retrieves the status and count of status enrollments for a given student.
    """
    
    @blp.arguments(EvaluateStudentSchema, location='query')
    def get(self, args):
        """
        GET method to evaluate a student's enrollment status.

        Args:
            args (dict): Query parameters containing the student_id.

        Returns:
            Response: JSON response with the student's ID, status, and count of status enrollments.
        """
        student_id = args.get("student_id")
        results = db.session.query(
            Enrollment.status, func.count(Enrollment.id)
        ).filter_by(student_id=student_id) \
        .group_by(Enrollment.status).all()

        status, count = max(results, key=lambda x: x)

        return jsonify({"student_id": student_id,
                        "status": status,
                        "count": count}), 200
