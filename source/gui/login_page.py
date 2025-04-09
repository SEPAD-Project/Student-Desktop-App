from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkCheckBox
from threading import Thread
from tkinter import messagebox
import sys
from requests import get, exceptions
from pathlib import Path
from download_model_page import start

# System paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "backend"))
print(BASE_DIR)
# imports after path configuration
from login_page_db import check_auth
from main_page import main_page_func_student
from add_face_page import add_face_page_func

class StudentSideAppLoginPage(CTk):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_window()

    def init_ui(self):
        """Initialize all UI components"""
        self.main_frame = CTkFrame(master=self, border_color='red', border_width=2)
        self.main_frame.pack(padx=20, pady=20, expand=True, fill='both')
        
        # Creating GUI elements in a separate thread
        Thread(target=self.create_widgets, daemon=True).start()

    def setup_window(self):
        """Configure main window settings"""
        self.geometry('600x450')
        self.minsize(600, 450)
        self.title('Student Side Login Page')

    def create_widgets(self):
        """Create and arrange GUI elements"""
        self.element_frame = CTkFrame(master=self.main_frame, fg_color='transparent')
        self.element_frame.place(relx=0.5, rely=0.5, anchor='center')

        # List of GUI elements
        elements = [
            CTkLabel(master=self.element_frame, text="Login Page", font=('montserrat', 26, 'bold')),
            CTkLabel(master=self.element_frame, text='USERNAME', font=('montserrat', 20)),
            CTkLabel(master=self.element_frame, text='PASSWORD', font=('montserrat', 20)),
            CTkEntry(master=self.element_frame, placeholder_text='username', width=180, height=38, 
                    font=('montserrat', 15, 'bold'), corner_radius=10),
            CTkEntry(master=self.element_frame, placeholder_text='password', show="*", width=180, height=38,
                    font=('montserrat', 15, 'bold'), corner_radius=10),
            CTkCheckBox(master=self.element_frame, text='I agree to Terms and Conditions',
                       font=('montserrat', 15), corner_radius=20, onvalue='on', offvalue='off'),
            CTkButton(master=self.element_frame, text="Login", font=('montserrat', 20, 'bold'),
                     corner_radius=10, command=self.handle_login)
        ]

        # Positioning settings
        grid_config = [
            (0, 0, {'columnspan': 2}),
            (1, 0, {'padx': (0,40), 'pady': (40,15)}),
            (2, 0, {'padx': (0,40), 'pady': (0,15)}),
            (1, 1, {'padx': (40,0), 'pady': (40,15)}),
            (2, 1, {'padx': (40,0), 'pady': (0,15)}),
            (3, 0, {'pady': (0,15), 'columnspan': 2}),
            (4, 0, {'columnspan': 2, 'sticky': 'ew'})
        ]

        # Placing elements in the grid
        for element, (row, col, kwargs) in zip(elements, grid_config):
            element.grid(row=row, column=col, **kwargs)

        # Assignment to class variables
        (self.login_text, self.username_lbl, self.password_lbl, 
         self.username_entry, self.password_entry, self.checkbox, 
         self.login_btn) = elements

    def handle_login(self):
        """Manage login process with threading"""
        self.toggle_login_button(state='disabled')
        
        try:
            Thread(target=self.login_workflow, daemon=True).start()
        except Exception as e:
            self.show_error("Thread Error", f"Error starting thread: {str(e)}")
            self.toggle_login_button()

    def login_workflow(self):
        """Main login process flow"""
        try:
            # Checking the internet connection
            if not self.check_internet():
                return

            # Initial validation
            if not self.validate_inputs():
                return

            # Authentication
            auth_result = self.authenticate_user()
            self.after(0, self.process_auth_result, auth_result)

        except Exception as e:
            self.show_error("Login Error", str(e))
            self.toggle_login_button()

    def validate_inputs(self):
        """Validate user inputs"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not all([username, password]):
            self.show_error("Input Error", "Username and password cannot be empty!")
            self.toggle_login_button()
            return False
        
        if self.checkbox.get() != 'on':
            self.show_error("Agreement Error", "You must agree to the terms and conditions!")
            self.toggle_login_button()
            return False
        
        return True

    def check_internet(self):
        """Check internet connection"""
        try:
            get('https://google.com', timeout=5)
            return True
        except exceptions.ConnectionError:
            self.show_error("Connection Error", "No internet connection!")
            self.toggle_login_button()
            return False

    def authenticate_user(self):
        """Authenticate user credentials"""
        try:
            print(self.username_entry.get().strip())
            print(self.password_entry.get().strip())
            return check_auth(
                self.username_entry.get().strip(),
                self.password_entry.get().strip(),
                'student'
            )
        except Exception as e:
            self.show_error("Authentication Error", str(e))
            return (False, None)

    def process_auth_result(self, result):
        """Process authentication result"""
        success, user_data = result
        
        if success:
            self.destroy()
            self.handle_post_login(user_data)
        else:
            self.show_error("Login Failed", "Invalid username or password!")
            self.toggle_login_button()

    def handle_post_login(self, user_data):
        """Handle post-login operations"""
        try:
            data_path = Path(r"C:\\sap-project")
            registered_image = data_path / "registered_image.jpg"

            if not data_path.exists():
                data_path.mkdir(parents=True, exist_ok=True)
            if registered_image.exists():
                main_page_func_student(user_data)
            else:
                OPENCV_FACE_DETECTOR_PATH = Path(r"c:\\sap-project\\opencv\\haarcascade_frontalface_default.xml")
                OPENCV_FACE_RECOGNIZER_PATH = Path(r"c:\\sap-project\\opencv\\face_recognition_sface_2021dec.onnx")
                if OPENCV_FACE_DETECTOR_PATH.exists() and OPENCV_FACE_RECOGNIZER_PATH.exists():
                    add_face_page_func(user_data)
                else:
                    # user doesnt have face recognizer or face detector model
                    # go to download page
                    start()

        except (PermissionError, OSError) as e:
            self.show_error("File Error", f"File operation failed: {str(e)}")
            sys.exit(1)

    def toggle_login_button(self, state='normal'):
        """Toggle login button state"""
        self.login_btn.configure(state=state, text="Login" if state == 'normal' else "Processing...")

    def show_error(self, title, message):
        """Show error message dialog"""
        self.after(0, lambda: messagebox.showerror(title, message))

    def run(self):
        self.mainloop()

if __name__ == '__main__':
    app = StudentSideAppLoginPage()
    app.run()