from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///university.db')  
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))

    def __str__(self):
        return self.name

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subjects = relationship("Subject", back_populates="teacher")

    def __str__(self):
        return self.name

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", back_populates="subjects")

    def __str__(self):
        return self.name

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer,ForeignKey('students.id'))
    subject_id = Column(Integer,ForeignKey('subjects.id')) 
    grade = Column(Integer)
    date = Column(Date)

    def __str__(self):
        return f"{self.grade}"



Base.metadata.create_all(engine)
