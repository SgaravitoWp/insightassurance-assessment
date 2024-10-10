from marshmallow import Schema, fields

class AssignStudentSchema(Schema):
    """
    Schema for assigning a student to a teacher.

    Attributes:
        teacher_id (int): The ID of the teacher.
        student_name (str): The name of the student.
    """
    teacher_id = fields.Int(required=True)
    student_name = fields.Str(required=True)

class EnrollClassesSchema(Schema):
    """
    Schema for enrolling a student in classes.

    Attributes:
        teacher_id (int): The ID of the teacher.
        student_id (int): The ID of the student.
        classes (list of int): List of class IDs.
    """
    teacher_id = fields.Int(required=True)
    student_id = fields.Int(required=True)
    classes = fields.List(fields.Int(), required=True)

class ExamSchema(Schema):
    """
    Schema for submitting an exam.

    Attributes:
        enrollment_id (int): The ID of the enrollment.
    """
    enrollment_id = fields.Int(required=True)

class ResultsSchema(Schema):
    """
    Schema for retrieving top students based on exam results.

    Attributes:
        top (int): The number of top students to retrieve.
    """
    top = fields.Int(required=True)

class EvaluateExamSchema(Schema):
    """
    Schema for evaluating an exam.

    Attributes:
        supervisor_id (int): The ID of the supervisor.
        enrollment_id (int): The ID of the enrollment.
        result (float): The result of the exam, must be between 0 and 5.
    """
    supervisor_id = fields.Int(required=True)
    enrollment_id = fields.Int(required=True)
    result = fields.Float(required=True, validate=lambda x: 0 <= x <= 5)

class EvaluateStudentSchema(Schema):
    """
    Schema for evaluating a student's enrollment status.

    Attributes:
        student_id (int): The ID of the student.
    """
    student_id = fields.Int(required=True)
