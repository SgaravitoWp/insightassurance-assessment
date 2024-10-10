from flask_smorest import Blueprint
from flask.views import MethodView
from schemas.schemas import *
from models.tables import *
from flask import jsonify
from db import db

blp = Blueprint("Supervisor", __name__, description="Operation on Supervisor")

@blp.route("/evaluateExam")
class Evaluate(MethodView):
    """
    Endpoint for supervisors to evaluate an exam.

    Methods:
        post(data): Evaluates an exam and updates the result and status.
    """
   
    @blp.arguments(EvaluateExamSchema)
    def post(self, data):
        """
        POST method for evaluating an exam.

        Args:
            data (dict): JSON payload containing supervisor_id, enrollment_id, and result.

        Returns:
            Response: JSON response with a message indicating the result of the operation.
        """
        supervisor_id = data.get("supervisor_id")
        enrollment_id = data.get("enrollment_id")
        result = data.get("result")
        
        supervisor = Exam.query.filter_by(enrollment_id=enrollment_id, id=supervisor_id).first()
        enrollment = Enrollment.query.filter_by(id=enrollment_id).first()

        if not enrollment:
            return jsonify({"message": "Enter a valid enrollment id."}), 400
        
        if not supervisor:
            return jsonify({"message": "The supervisor has no permissions over this exam."}), 400

        if 0 <= result < 2:
            status  =  "Disapproved"
        elif 2 <= result < 3.5:
            status  = "Conditional"
        elif result >= 3.5:
            status  = "Approved"

        supervisor.result = result
        enrollment.status = status 

        try:
            db.session.commit()
            return jsonify({ 
                    "message": "The evaluation has been done."
                    }), 201

        except Exception:
            db.session.rollback()
            return jsonify({ 
                    "message": "Internal server error."
                    }), 500
