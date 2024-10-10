from sqlalchemy.exc import IntegrityError
from flask_smorest import Blueprint
from flask.views import MethodView
from schemas.schemas import *
from models.tables import *
from flask import jsonify
from db import db

blp = Blueprint("Teacher", __name__, description="Operation on Teachers")

@blp.route("/enrollClasses")
class Enrollments(MethodView):
    """
    Endpoint for teachers to enroll students in classes.

    Methods:
        post(data): Enrolls a student in multiple classes.
    """
   
    @blp.arguments(EnrollClassesSchema)
    def post(self, data):
        """
        POST method for enrolling a student in classes.

        Args:
            data (dict): JSON payload containing teacher_id, student_id, and a list of class_ids.

        Returns:
            Response: JSON response with a message indicating the result of the operation.
        """
        teacher_id = data.get("teacher_id")
        student_id = data.get("student_id")
        class_ids = data.get("classes") 
        
        student = Student.query.filter_by(teacher_id=teacher_id, id=student_id).first()

        if not student:
            return jsonify({"message": "The teacher has no permissions over this student."}), 400

        if len(class_ids) < 5:
            return jsonify({"message": "Minimum 5 classes for enrollment"}), 400
    
        enrollments = []

        for class_id in class_ids:
            enrollment = Enrollment(
                student_id=student_id,
                class_id=class_id,
            )
            enrollments.append(enrollment)

        try:
            db.session.add_all(enrollments)
            db.session.commit()
            return jsonify({ 
                    "message": "The enrollment has been done."
                    }), 201
        
        except IntegrityError:
            db.session.rollback()
            return jsonify({ 
                    "message": "The enrollment has been done before."
                    }), 400

        except Exception:
            db.session.rollback()
            return jsonify({ 
                    "message": "Internal server error."
                    }), 500
