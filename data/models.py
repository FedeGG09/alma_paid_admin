# data/models.py

from dataclasses import dataclass

@dataclass
class Student:
    id: int
    name: str
    email: str
    dni: str
    status: str  # PENDING / PAID

@dataclass
class Course:
    id: int
    title: str
    description: str = ""   # ahora opcional, por defecto vacío

@dataclass
class Enrollment:
    id: int
    student_id: int
    course_id: int
    status: str

@dataclass
class Invoice:
    id: int
    enrollment_id: int
    dni: str
    base_fee: float
    surcharge: float
    total: float
    status: str
