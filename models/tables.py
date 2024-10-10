from db import db

class Teacher(db.Model):
    """
    Represents a teacher in the database.

    Attributes:
        id (int): The primary key for the teacher.
        name (str): The name of the teacher, must be unique.
        students (relationship): Relationship to the Student model.
    """
    __tablename__ = 'teachers'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    students = db.relationship('Student', backref='teacher', lazy=True)

class Student(db.Model):
    """
    Represents a student in the database.

    Attributes:
        id (int): The primary key for the student.
        name (str): The name of the student, must be unique.
        teacher_id (int): Foreign key referencing the teacher.
        enrollments (relationship): Relationship to the Enrollment model.
    """
    __tablename__ = 'students'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)  
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)

class Class(db.Model):
    """
    Represents a class in the database.

    Attributes:
        id (int): The primary key for the class.
        name (str): The name of the class, must be unique.
        enrollments (relationship): Relationship to the Enrollment model.
    """
    __tablename__ = 'classes' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    enrollments = db.relationship('Enrollment', backref='class', lazy=True)

class Enrollment(db.Model):
    """
    Represents an enrollment in the database.

    Attributes:
        id (int): The primary key for the enrollment.
        student_id (int): Foreign key referencing the student.
        class_id (int): Foreign key referencing the class.
        status (str): The status of the enrollment, default is 'In Progress'.
        exams (relationship): Relationship to the Exam model.
    """
    __tablename__ = 'enrollments'  
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)  
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False) 
    status = db.Column(db.String(20), default='In Progress')
    exams = db.relationship('Exam', backref='enrollment', lazy=True)

class Exam(db.Model):
    """
    Represents an exam in the database.

    Attributes:
        id (int): The primary key for the exam.
        enrollment_id (int): Foreign key referencing the enrollment.
        attempt_number (int): The attempt number of the exam, default is 0.
        digital_proof (bool): Indicates if digital proof is present, default is True.
        supervisor_id (int): Foreign key referencing the supervisor.
        result (int): The result of the exam, can be null.
    """
    __tablename__ = 'exams'  
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)  
    attempt_number = db.Column(db.Integer, nullable=False, default=0) 
    digital_proof = db.Column(db.Boolean, nullable=False, default=True) 
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisors.id'), nullable=False)  
    result = db.Column(db.Integer, nullable=True)  

class Supervisor(db.Model):
    """
    Represents a supervisor in the database.

    Attributes:
        id (int): The primary key for the supervisor.
        name (str): The name of the supervisor, must be unique.
    """
    __tablename__ = 'supervisors'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class Coordinator(db.Model):
    """
    Represents a coordinator in the database.

    Attributes:
        id (int): The primary key for the coordinator.
        name (str): The name of the coordinator, must be unique.
    """
    __tablename__ = 'coordinators'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
