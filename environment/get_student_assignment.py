import requests

def get_assignments(username, password):
    api_url = "https://friscoisdhacapi.vercel.app/api/currentclasses"
    payload = {'username': username, 'password': password}

    try:
        response = requests.get(api_url, params=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data_classes = response.json()  # Parse the JSON response

        if data_classes is None:
            return "Login Invalid"

        for class_info in data_classes.get('currentClasses', []):
            # print(f"\n{class_name} - {class_grade}\n{'-' * 40}")

            assignments = class_info.get('assignments', [])

            for assignment in assignments:
                assignment_name = assignment.get('name', 'N/A')
                assignment_score = assignment.get('score', 'N/A')
                assignment_type = assignment.get('category', 'N/A')

                if assignment_type == "Assessment of Learning":
                    print(f"{assignment_name} ({assignment_type}) - {assignment_score}")

    except Exception as e:
        # Print or log the error
        #print(f"Error in get_assignments: {e}")

        # Return None or an empty list to indicate failure
        return None


# Example usage
# get_assignments("000000", "000000")
