import requests
import os
import logging
import configparser

config_path = os.path.join(os.path.dirname(__file__), '../config.ini')
config = configparser.ConfigParser()
config.read(config_path)

ip_address = config['Server']['IP']
port = config['Server']['Looking_result_sender_port']

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Server configuration
SERVER_URL = f"http://{ip_address}:{port}/upload_text"
TIMEOUT = 10  # seconds
MAX_RETRIES = 3
REQUIRED_HEADER = {'X-Application': 'SchoolApp'}

def send_data_to_server(
    text: str,
    username: str,
    password: str ,
    school_name: str,
    class_code: str
) -> bool:
    """
    Send data to the server with enhanced error handling and security
    
    Args:
        text: Text content to send
        username: Authentication username
        password: Authentication password
        school_name: School identifier
        class_code: Class identifier
    
    Returns:
        bool: True if successful, False otherwise
    """
    payload = {
        'username': username,
        'password': password,
        'school_name': school_name,
        'class_code': class_code,
        'text': text
    }

    headers = {
        'User-Agent': 'SchoolApp',
        **REQUIRED_HEADER
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                SERVER_URL,
                data=payload,
                headers=headers,
                timeout=TIMEOUT
            )
            
            # Parse JSON response
            response_data = response.json()
            
            # Check for 2xx status codes
            if response.ok:
                logger.info(f"Success: {response_data.get('message', '')}")
                return True
                
            # Handle specific error codes
            error_msg = response_data.get('error', 'Unknown error')
            logger.error(f"Server Response: {error_msg} (Code: {response.status_code})")
            
            # Non-retryable errors
            if response.status_code in (400, 401, 403, 404):
                return False
                
            # Retryable errors
            logger.info(f"Retrying... ({attempt + 1}/{MAX_RETRIES})")

        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP Error: {err}")
            return False
            
        except requests.exceptions.ConnectionError:
            logger.error("Connection failed - check network")
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {TIMEOUT} seconds")
            
        except requests.exceptions.RequestException as err:
            logger.error(f"Request failed: {err}")
            
        except ValueError as err:
            logger.error(f"Invalid server response: {err}")
            return False

    return False

# Example usage
if __name__ == "__main__":
    text_to_send = "sended txt by user"
    success = send_data_to_server(  text_to_send,
                                    '09295',
                                    '123',
                                    '1',
                                    '2')
    
    if success:
        print("Status sent successfully")
    else:
        print("Failed to send status")
