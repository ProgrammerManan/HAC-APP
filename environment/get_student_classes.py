import requests
from main import calculate_weighted_gpa  # Import the GPA calculation function

def get(username, password):
    api_url = "https://friscoisdhacapi.vercel.app/api/currentclasses"
    payload = {'username': username, 'password': password}
    
    try:
        response = requests.get(api_url, params=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data_classes = response.json()  # Parse the JSON response

        classes_info = []

        # Extract and print course codes and numbers along with grades
        for class_info in data_classes.get('currentClasses', []):
            class_name = class_info.get('name', 'N/A')
            class_grade = class_info.get('grade', 'N/A')
            
            assignments = class_info.get('assignments', [])
            assignments_info = []

            for assignment in assignments:
                assignment_name = assignment.get('name', 'N/A')
                assignment_score = assignment.get('score', 'N/A')

                max_chars = 36  # You can adjust this value based on your preference
                truncated_assignment_name = (
                assignment_name[:max_chars] + '...' if len(assignment_name) > max_chars else assignment_name
                )
                
                # Append assignment information to the list
                assignments_info.append(
                    truncated_assignment_name + " - " + assignment_score
                )

            # Extract course code and number
            course_info = class_name.split('-')
            course_code = course_info[0].strip()
            course_number = course_info[1].split()[0].strip()

            if class_grade == "" or class_grade == " ":
                class_grade = "0.00"
            # Append information to the list

            class_name = class_name.replace(course_code, "")
            class_name = class_name.replace(course_number, "")
            class_name = class_name.replace("-", "")

            classes_info.append({
                'class_name': class_name,
                'course_code': f"{course_code} {course_number}",
                'class_grade': class_grade,
                'assignments': '<br>'.join(assignments_info)  # Exclude the first element (class name) when joining
            })


        # Calculate weighted GPA
        weighted_gpa = calculate_weighted_gpa(
            [class_info['class_name'] for class_info in classes_info],
            [class_info['class_grade'] for class_info in classes_info]
        )

        # Return the list containing information for all classes and the weighted GPA
        return classes_info, weighted_gpa

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

# Example usage
# classes_info, result_gpa = get("292291", "09262008")
# print("Classes Information:", classes_info)
# print("Weighted GPA:", result_gpa)
