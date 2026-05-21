from fastapi import FastAPI

app = FastAPI()

students = []

#create
@app.post("/students")
def create_student(student: dict):
    students.append(student)
    return {"message": "Student created successfully"}

#read
@app.get("/students")
def read_students():
    return students

#update
@app.put("/students/{student_id}")  
def update_student(student_id: int, updated_student: dict):
    if student_id < len(students):
        students[student_id] = updated_student
        return {"message": "Student updated successfully"}
    return {"error": "Student not found"}

#delete
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id < len(students):
        students.pop(student_id)
        return {"message": "Student deleted successfully"}
    return {"error": "Student not found"}