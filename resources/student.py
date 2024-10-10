from sqlalchemy.exc import IntegrityError
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify, request
from schemas.schemas import *
from sqlalchemy import func
from models.tables import *
from db import db

blp = Blueprint("Student", __name__, description="Operation on Students")

@blp.route("/assignStudent")
class Assignment(MethodView):
    """
    Endpoint to assign a student to a teacher.

    Methods:
        post(data): Assigns a student to a teacher.
    """
   
    @blp.arguments(AssignStudentSchema)
    def post(self, data):
        """
        POST method to assign a student to a teacher.

        Args:
            data (dict): JSON payload containing teacher_id and student_name.

        Returns:
            Response: JSON response with a message indicating the result of the operation.
        """
        teacher_id = data.get("teacher_id")
        student_name = data.get("student_name")
        new_student = Student(teacher_id=teacher_id, name=student_name)

        try:
            db.session.add(new_student)
            db.session.commit()
            return jsonify({ 
                    "message": "The student has been assigned "
                    }), 201
        
        except IntegrityError:
            db.session.rollback()
            return jsonify({ 
                    "message": "Student already assigned."
                    }), 400
           
        except Exception:
            db.session.rollback()
            return jsonify({ 
                    "message": "Internal server error."
                    }), 500
            
@blp.route("/submitExam")
class Submit(MethodView):
    """
    Endpoint to submit an exam for a student.

    Methods:
        post(data): Submits an exam for a student.
    """
   
    @blp.arguments(ExamSchema)
    def post(self, data):
        """
        POST method to submit an exam for a student.

        Args:
            data (dict): JSON payload containing enrollment_id.

        Returns:
            Response: JSON response with a message indicating the result of the operation.
        """
        enrollment_id = data.get("enrollment_id")

        if 'file' not in request.files:
            return jsonify({"message": "No exam attached."}), 400

        exam = Exam.query.filter_by(enrollment_id=enrollment_id).first()

        if exam:
            if exam.status == "Conditional":
                if exam.attempt_number == 3:
                    return jsonify({"message": "The maximum number of attempts for this exam has been reached."}), 200
                exam.attempt_number = exam.attempt_number + 1
            else:
                return jsonify({"message": "Exam already evaluated.",
                                "status": exam.status}), 200

        else:
            supervisor_id = Supervisor.query.order_by(func.random()).first()
            new_exam = Exam(enrollment_id=enrollment_id, 
                            supervisor_id=supervisor_id)
            db.session.add(new_exam)

        try:
            db.session.commit()
            return jsonify({ 
                    "message": "The exam was sent"
                    }), 201
        
        except Exception:
            db.session.rollback()
            return jsonify({ 
                    "message": "Internal server error."
                    }), 500

@blp.route("/results")
class Results(MethodView):
    """
    Endpoint to get the top students based on exam results.

    Methods:
        get(args): Retrieves the top students based on their average exam results.
    """
    
    @blp.arguments(ResultsSchema, location='query')
    def get(self, args):
        """
        GET method to retrieve the top students based on their average exam results.

        Args:
            args (dict): Query parameters containing the number of top students to retrieve.

        Returns:
            Response: JSON response with the top students and their average results.
        """
        top = args.get("top")
        subquery = (
        db.session.query(
            Exam.enrollment_id,
            func.avg(Exam.result).label('average_result')
        )
        .join(Enrollment)
        .join(Student)
        .group_by(Enrollment.student_id)
        .subquery()
        )

        top_students = (
            db.session.query(Student.id, Student.name, subquery.c.average_result)
            .join(subquery, Student.id == Enrollment.student_id)
            .order_by(subquery.c.average_result.desc())
            .limit(top)
            .all()
        )

        results = [{"id": student.id,
                     "name": student.name, 
                     "average_result": avg.average_result}
                for student, avg in top_students]

        return jsonify(results), 200
