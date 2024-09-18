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
            class_assignments_all_empty = True

            for assignment in assignments:
                if assignment.get('category') == "Assessment of Learning":
                    assignment_name = assignment.get('name', 'N/A')
                    assignment_score = assignment.get('score', 'N/A')
                    assignment_category = assignment.get('category', 'N/A')
                    assignment_dateAssigned = assignment.get('dateAssigned', 'N/A')
                    if assignment_dateAssigned == "":
                        assignment_dateAssigned = "None"
                    assignment_dateDue = assignment.get('dateDue', 'N/A')
                    if assignment_dateDue == "":
                        assignment_dateDue = "None"
                    max_chars = 20  # You can adjust this value based on your preference
                    truncated_assignment_name = (
                    assignment_name[:max_chars] + '...' if len(assignment_name) > max_chars else assignment_name
                    )
                    truncated_assignment_name = truncated_assignment_name.strip()
                    if any(assignment['name'] == truncated_assignment_name for assignment in assignments_info):
                        truncated_assignment_name = truncated_assignment_name.replace("...","(D)...")

                    # Append assignment information to the list
                    assignments_info.append({
                    'name': truncated_assignment_name,
                    'full_name': assignment_name,
                    'score': assignment_score,
                    'category': assignment_category,
                    'dateAssigned': assignment_dateAssigned,
                    'dateDue': assignment_dateDue
                    })

                    if assignment_score not in ("", " "):
                        assessment_assignments_all_empty = False

            # Extract course code and number
            course_info = class_name.split('-')
            course_code = course_info[0].strip()
            course_number = course_info[1].split()[0].strip()

            if class_grade in ("", " ") or assessment_assignments_all_empty:
                class_grade = "1010"
            # Append information to the list

            class_name = class_name.replace(course_code, "")
            class_name = class_name.replace(course_number, "", 1)
            class_name = class_name.replace("-", "")
            class_name = class_name.strip()

            # max_chars = 20
            # truncated_classname = (
            #     class_name[:max_chars] + '...' if len(
            #         class_name) > max_chars else class_name
            # )

            classes_info.append({
                "class_name": class_name,
                "course_code": f"{course_code} {course_number}",
                "class_grade": class_grade,
                "assignments": assignments_info  # Exclude the first element (class name) when joining
            })

        # print(classes_info)
        # Filter classes based on the condition that they have at least one assignment with:
        # category == "Assessment of learning" and score != ""
        filtered_classes_info = [
            class_info for class_info in classes_info
            if any(
                assignment['category'] == "Assessment of Learning" and assignment['score'] != ""
                for assignment in class_info['assignments']
            )
        ]

        # Calculate weighted GPA only for the filtered classes
        weighted_gpa = calculate_weighted_gpa(
            [class_info["class_name"] for class_info in filtered_classes_info],
            [class_info["class_grade"] for class_info in filtered_classes_info]
        )

        # Return the list containing information for all classes and the weighted GPA
        if classes_info == []:
            return "incorrect credentials"
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
# classes_info, result_gpa = get("000000", "000000")
# print("Classes Information:", classes_info)
# print("Weighted GPA:", result_gpa)