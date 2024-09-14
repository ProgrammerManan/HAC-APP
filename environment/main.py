import json
import os

from flask import Flask, abort, render_template, request, session, redirect, url_for, jsonify
import requests
import get_student_info #Importing the student info file to get the info from the api
import get_student_classes #Importing the student classes file to get the classes and grades from the api

app = Flask(__name__, static_folder='static')
app.secret_key = "your_secret_key"  # Change this to a secure secret key

#Function to calculate GPA
def calculate_weighted_gpa(class_names, class_grades):
    try:
        total_weighted_grade = 0
        max_weighted_grade = 0
        classes_num = len(class_names)

        for i in range(classes_num):
            grade = float(class_grades[i])  # Convert grade to float
            grade = round(grade, 0)
            grade = int(grade)
            class_name = class_names[i]

            if "AP" in class_name or "IB" in class_name or "Computer Sci 3 Adv" in class_name:
                if grade<70 or grade==0.00:
                    total_weighted_grade += 0
                else:
                    total_weighted_grade += 6.0 - ((100 - grade)/10)
                    print(6.0 - ((100 - grade)/10))
                max_weighted_grade += 6.0
            elif "Adv" in class_name:
                if grade < 70 or grade == 0.00:
                    total_weighted_grade += 0
                else:
                    total_weighted_grade += 5.5 - ((100 - grade) / 10)
                    print(5.5 - ((100 - grade) / 10))
                max_weighted_grade += 5.5
            else:
                if grade < 70 or grade == 0.00:
                    total_weighted_grade += 0
                else:
                    total_weighted_grade += 5.0 - ((100 - grade) / 10)
                    print(5.0 - ((100 - grade) / 10))
                max_weighted_grade += 5.0

        if session['hac_username'] == str(os.environ["ojas_ID"]):
            classes_num = classes_num - 1
            max_weighted_grade = max_weighted_grade - 6

        weighted_gpa = total_weighted_grade / classes_num
        max_weighted_gpa = max_weighted_grade / classes_num

        weighted_gpa = round(weighted_gpa, 4)
        max_weighted_gpa = round(max_weighted_gpa, 4)
    except Exception as e:
        print(f"An exception occurred: {e}")
        weighted_gpa = 0.000
        max_weighted_gpa = 0.000
    gpa = [weighted_gpa, max_weighted_gpa]
    return gpa

#Home Index page (default page)
# @app.route('/')
# def index_page():
#     return render_template('index.html')e
#HAC Login page (for entering hac username and password)
@app.route('/', methods=['GET','POST'])
def hac_login():
    if request.method == 'POST':
        # Get the username and password from the request form
        username = request.form['username']
        password = request.form['password']

        session['hac_username'] = username
        session['hac_password'] = password

        # Redirect to the '/app' route with the username and password as query parameters
        return redirect(url_for('app_page'))

    return render_template('login.html')

#Fetching classes and student info from hac api and sending to app.html to display info to user
#Hac API
def convert_to_integer(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0  # Handle the case where conversion is not possible

@app.route('/app', methods=['GET'])
def app_page():
    username = session.get('hac_username')
    password = session.get('hac_password')

    if not (username and password):
        return redirect('/')

    if "result" not in session or "data_info" not in session:
        result = get_student_classes.get(username, password)
        data_info = get_student_info.get(username, password)
        session["result"] = result
        session["data_info"] = data_info
    else:
        result = session["result"]
        data_info = session["data_info"]

    data_classes, weighted_gpa = result


    # for class_info in data_classes:
    #     class_info['class_grade'] = convert_to_integer(class_info['class_grade'])

    return render_template('app.html', data_info=data_info,
                           data_classes=data_classes,
                           weighted_gpa=weighted_gpa[0], maxGPA=weighted_gpa[1])

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('hac_login'))

@app.route('/beta')
def beta_page():
    is_logged_in = ('hac_username' in session) and ('hac_password' in session)
    return render_template('beta.html', is_logged_in=is_logged_in)

@app.route('/refresh-data', methods=['GET'])
def refresh_data():
    username = session.get('hac_username')
    password = session.get('hac_password')

    if not (username and password):
        return jsonify({'error': 'Not logged in'}), 401

    # Make the API call to get fresh data
    result = get_student_classes.get(username, password)
    data_info = get_student_info.get(username, password)

    # Update session with new data
    session["result"] = result
    session["data_info"] = data_info

    # Respond with new data (or a success message)
    return jsonify({'success': 'Data refreshed successfully'}), 200

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=9999)

if __name__ == '__main__':
   app.run(debug=False, host='0.0.0.0')