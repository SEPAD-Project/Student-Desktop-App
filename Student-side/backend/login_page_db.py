import sys
from pathlib import Path
from typing import Tuple, Union

# Add database-code directory to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent / "database-code"))
from searching import get_values_by_username  # type: ignore


def check_auth(
    username: str, 
    password: str, 
    person_type: str
) -> Tuple[bool, Union[tuple, str]]:
    """
    Authenticate user credentials against database records
    
    Parameters:
        username: User identifier (case-sensitive)
        password: User's secret credential
        person_type: Account type (student/teacher)
    
    Returns:
        Tuple containing:
            - Authentication status (True/False)
            - User data tuple or error message string
    
    Raises:
        Indirect exceptions from database operations
    """
    try:
        # Validate input format first
        if not all([username.strip(), password.strip()]):
            return (False, "Username and password cannot be empty")
            
        if len(username) > 50 or any(c in username for c in "!@#$%^&*()"):
            return (False, "Invalid username format - special characters not allowed")

        # Fetch user data from database
        user_data = get_values_by_username(
            value=username,
            person=person_type
        )

        # Handle user not found case
        if user_data == "not found":
            return (False, "Credentials not found in database")

        # Extract stored password (assuming index 2 contains password)
        stored_password = user_data[2]

        # Verify password match
        if stored_password != password:
            return (False, "Invalid credentials - password mismatch")

        return (True, user_data)

    except ConnectionError as e:
        # Handle database connection issues
        return (False, f"Database connection failed: {str(e)}")
    except TimeoutError as e:
        # Handle query timeout scenarios
        return (False, "Database operation timed out")
    except Exception as e:
        # Catch-all for unexpected errors
        return (False, f"Authentication process failed: {str(e)}")


if __name__ == "__main__":
    # Test cases for different authentication scenarios
    test_cases = [
        # Valid credentials
        ("09295", "stpass", "student"),
        # Empty username
        ("", "pass", "student"),
        # Invalid username format
        ("invalid#user", "pass", "teacher"),
        # Non-existent user
        ("nonexistent", "pass", "teacher")
    ]

    # Execute test cases
    for uname, pwd, ptype in test_cases:
        result = check_auth(uname, pwd, ptype)
        print(f"Input: ({uname}, {pwd}, {ptype}) => Result: {result}")

# udata  student_name, student_family, student_password, class_code, school_code, student_national_code