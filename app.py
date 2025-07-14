from flask import Flask, render_template,request,redirect,url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb+srv://sdreddy786:uprGBHOQTElk6lEK@cluster0.ohqybxv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["crudOperations"]
collection = db["crudOperationsCollection"]

students = db["students"]
courses = db["courses"]

# @app.before_request
# def seed_courses():
#     if courses.count_documents({}) == 0:
#         courses.insert_many([
#             {"name":"Python"},
#             {"name":"Flask"},
#             {"name":"MongoDB"}
#         ])

@app.route("/")
def index():
    users = list(collection.find())
    return render_template("index.html", users = users)

@app.route("/add", methods =["GET","POST"])
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        collection.insert_one({"name":name,"email":email})
        return redirect(url_for("index"))
    return render_template("add_user.html")

@app.route("/edit/<id>",methods=["GET","POST"])
def edit_user(id):
    print(id)
    print(collection)
    user = collection.find_one({"_id":ObjectId(id)})
    print("user:",user)
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        collection.update_one({"_id":ObjectId(id)},{"$set":{"name":name,"email":email}})
        return redirect(url_for("index"))
    return render_template("edit_user.html",user = user)

@app.route("/delete/<id>")
def delete_user(id):
    collection.delete_one({"_id":ObjectId(id)})
    return redirect(url_for("index"))


@app.route("/addStudent",methods=["GET","POST"])
def add_student():
    all_courses = list(courses.find())
    if request.method == "POST":
        name = request.form["name"]
        select_ids = request.form.getlist("courses")
        course_ids = [ObjectId(cid) for cid in select_ids]
        students.insert_one({"name":name,"course_ids":course_ids})
        return redirect("/studentOutput")
    return render_template("add_student.html", courses = all_courses)


@app.route("/studentOutput", methods =["GET"])
def print_student():
    student_list = list(students.find())
    for student in student_list:
        enrolled = []
        for cid in student.get("course_ids",[]):
            course = courses.find_one({"_id" :cid})
            if course:
                enrolled.append(course["name"])
    
        student['course_ids'] = enrolled

    return render_template("display_students.html",students = student_list)

if __name__ == "__main__":
    app.run(debug=True)