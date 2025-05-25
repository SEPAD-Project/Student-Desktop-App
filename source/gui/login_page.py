from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkCheckBox
from threading import Thread
from tkinter import messagebox
import sys
from requests import get, exceptions
from pathlib import Path
from getpass import getuser
from download_model_page import start
from alert_pages import InAppAlert
import configparser

username = getuser()
# System paths
sys.path.append(str(Path(__file__).resolve().parent))
# imports after path configuration
from backend.login_page_db import check_auth
from main_page import main_page_func_student
from add_face_page import add_face_page_func

class StudentSideAppLoginPage(CTk):
    def __init__(self):
        self.alert_system = InAppAlert(self)
        super().__init__()
        self.setup_window()
        self.init_ui()
        self.check_version()  # Add version check on startup

    def init_ui(self):
        """Initialize all UI components"""
        self.main_frame = CTkFrame(master=self, border_color='red', border_width=2)
        self.main_frame.pack(padx=20, pady=20, expand=True, fill='both')
        
        self.create_widgets()

    def setup_window(self):
        """Configure main window settings"""
        self.geometry('600x450')
        self.minsize(600, 450)
        self.title('Student Side Login Page')
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # handler for closing page

    def on_close(self):
        """Handle window close event"""
        self.destroy()
        sys.exit()

    def check_version(self):
        """Check for new version on GitHub releases"""
        try:
            # First check internet connection
            if not self.check_internet_connection():
                return

            # Get current version from local file or hardcoded
            current_version = self.get_current_version()
            
            # Get latest release info from GitHub
            latest_version = self.get_latest_github_version()
            
            if latest_version and latest_version > current_version:
                self.after(0, self.alert_system.show_alert,
                    "info",
                    "New Version Available",
                    f"Version {latest_version} is available! (You have {current_version})",
                    0,
                    "line",
                    'url',
                    'GET THE LATEST VERSION',
                    'http://185.4.28.110:2568'
                )
                

        except Exception as e:
            print(f"Version check failed: {str(e)}")

    def check_internet_connection(self):
        """Check internet connection specifically for version check"""
        try:
            get('https://google.com', timeout=5)
            return True
        except exceptions.ConnectionError:
            self.show_connection_error()
            return False

    def show_connection_error(self):
        """Show persistent connection error message"""
        self.alert_system.show_alert(
            message_type="error",
            title="Connection Error",
            message="No internet connection! Please connect to the internet and restart the application.",
            duration=0,  # Persistent until user closes it
            particle_type="off"
        )

    def get_current_version(self):
        """Get current version from config.ini file"""
        try:
            # Get path to config.ini (two levels up from current file)
            config_path = Path(__file__).parent.parent / "config.ini"
            
            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found at: {config_path}")
            
            config = configparser.ConfigParser()
            config.read(config_path)
            
            version = config.get('App', 'version', fallback='v1.0.0')
            
            # Remove 'v' prefix if exists and return clean version
            return version.lstrip('v')
            
        except Exception as e:
            print(f"Error reading version from config: {str(e)}")
            return '1.0.0'  # Fallback version

    def get_latest_github_version(self):
        """Get latest version from GitHub releases"""
        try:
            api_url = "https://api.github.com/repos/SEPAD-Project/Student-App/releases/latest"
            response = get(api_url, timeout=5)
            response.raise_for_status()
            release_info = response.json()
            tag_name = release_info.get('tag_name', '')
            
            # Clean version string (remove 'v' prefix if exists)
            return tag_name.lstrip('v') if tag_name else None
        except Exception as e:
            print(f"Failed to get latest version: {str(e)}")
            return None

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
            # self.after(0, lambda: messagebox.showerror(title, message))
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
            self.show_connection_error()
            self.toggle_login_button()
            return False

    def authenticate_user(self):
        """Authenticate user credentials"""
        try:
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

    def check_required_files(self):
        """Check if all required model files exist"""
        model_dir = Path(r"C:\sap-project\.insightface\models\buffalo_l")
        required_files = [
            "w600k_r50.onnx",
            "genderage.onnx",
            "det_10g.onnx",
            "2d106det.onnx",
            "1k3d68.onnx"
        ]
        
        # Check if all required files exist
        return all((model_dir / file).exists() for file in required_files)

    def handle_post_login(self, user_data):
        """Handle post-login operations"""
        try:
            data_path = Path(r"C:\sap-project")
            registered_image = data_path / "registered_image.jpg"
            
            if not data_path.exists():
                data_path.mkdir(parents=True, exist_ok=True)

            if self.check_required_files():
                if registered_image.exists():
                    main_page_func_student(user_data)
                else:
                    add_face_page_func(user_data)
            else:
                # User doesn't have required face recognition model files
                # Go to download page
                start(user_data)

        except (PermissionError, OSError) as e:
            self.show_error("File Error", f"File operation failed: {str(e)}")
            sys.exit(1)

    def toggle_login_button(self, state='normal'):
        """Toggle login button state"""
        self.login_btn.configure(state=state, text="Login" if state == 'normal' else "Processing...")

    def show_error(self, title, message):
        """Show error message dialog"""
        self.alert_system.show_alert(
            message_type="error",
            title=title,
            message=message,
            duration=3,
            particle_type="line"
        )

    def run(self):
        self.mainloop()

if __name__ == '__main__':
    app = StudentSideAppLoginPage()
    app.run()