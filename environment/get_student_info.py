import requests
from flask import Flask, jsonify

def get(username, password):
    api_url_info = "https://friscoisdhacapi.vercel.app/api/info"
    payload = {'username': username, 'password': password}

    try:
        response = requests.get(api_url_info, params=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data_info = response.json()  # Parse the JSON response
        return data_info

    except requests.exceptions.HTTPError as errh:
        return jsonify({'error': f"HTTP Error: {errh}"})
    except requests.exceptions.ConnectionError as errc:
        return jsonify({'error': f"Error Connecting: {errc}"})
    except requests.exceptions.Timeout as errt:
        return jsonify({'error': f"Timeout Error: {errt}"})
    except requests.exceptions.RequestException as err:
        return jsonify({'error': f"An unexpected error occurred: {err}"})
    