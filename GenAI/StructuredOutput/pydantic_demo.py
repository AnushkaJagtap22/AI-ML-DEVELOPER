from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int = 21
    grade: str

new_student = Student(name="Alice",  grade="A")


print(new_student)