import requests
import cv2
import numpy as np

# Function to send a request to the API and retrieve the image frames
def get_frames_from_api(school_code, class_name, national_code):
    # API endpoint
    url = "http://127.0.0.1:5000/get_student_image"
    
    # JSON payload
    payload = {
        "school_code": school_code,
        "class_name": class_name,
        "national_code": national_code
    }
    
    # Send POST request to the API
    response = requests.post(url, json=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Return the raw image data (frames)
        return response.content
    else:
        # Print the error message
        print(f"Error: {response.status_code} - {response.json().get('error')}")
        return None

