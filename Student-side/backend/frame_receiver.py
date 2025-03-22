import requests
import cv2
import numpy as np

# Function to send a request to the API and retrieve the image frames
def get_frames_from_api(school_code, class_name, national_code):
    # API endpoint
    url = "http://127.0.0.1:5511/get_student_image"
    
    # JSON payload
    payload = {
        "school_code": school_code,
        "class_name": class_name,
        "national_code": national_code
    }
    
    # Send POST request to the API
    response = requests.post(url, json=payload, timeout=10)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Return the raw image data (frames)
        return response.content
    else:
        # Print the error message
        print(f"Error: {response.status_code} - {response.json().get('error')}")
        return None

# Function to convert frames to an image and save it
def save_frames_as_image(frames):
    output_path = f'C://sap-project//real_image.jpg'
    if frames is None:
        print("No frames received. Cannot save image.")
        return
    
    # Convert the raw frames (bytes) to a NumPy array
    image_array = np.frombuffer(frames, dtype=np.uint8)
    
    # Decode the image array using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    
    if image is not None:
        # Save the image to the specified output path
        cv2.imwrite(output_path, image)
        print(f"Image saved successfully at: {output_path}")
    else:
        print("Failed to decode the image.")


def get_image(school_code, class_name, national_code):

    # Step 1: Get frames from the API
    frames = get_frames_from_api(school_code, class_name, national_code)
    
    # Step 2: Save frames as an image
    save_frames_as_image(frames)

# Example usage
if __name__ == "__main__":
    # Input data
    school_code = "123"
    class_name = "1052"
    national_code = "09295"
    
    get_image(school_code, class_name, national_code)