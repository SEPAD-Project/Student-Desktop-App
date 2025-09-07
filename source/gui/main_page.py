from customtkinter import CTk, CTkTextbox, CTkLabel, CTkButton, CTkFrame, CTkOptionMenu, CTkEntry, END, DISABLED, NORMAL
import cv2
from PIL import Image, ImageTk
from threading import Thread, Lock
from pathlib import Path
import sys
from ping3 import ping
import time
from tkinter import messagebox
from datetime import datetime
import keyboard
import mediapipe as mp
from insightface.app import FaceAnalysis
from plyer import notification

sys.path.append(str(Path(__file__).resolve().parent.parent))
from backend.image_processing.looking_result.func_looking_result import looking_result #type:ignore
from backend.looking_result_sender import send_data_to_server
from backend.open_windows_sender import send_data
from backend.path_manager import INSIGHTFACE_DIR
from alert_pages import InAppAlert

class MainPage(CTk):
    def __init__(self, udata):
        super().__init__()
        cv2.setLogLevel(0)

        # Load the FaceAnalysis model only once, outside the loop
        self.app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"],  # Can change to "CUDAExecutionProvider" for GPU
            root=INSIGHTFACE_DIR
        )
        self.app.prepare(ctx_id=0)  # Prepare the model (once)

        self.pose_face_mesh_obj = mp.solutions.face_mesh.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1
        )
        
        self.eye_face_mesh_obj = mp.solutions.face_mesh.FaceMesh(
            refine_landmarks=True,
            max_num_faces=1
        )

        self.udata = udata
        # print(self.udata)
        self.first_name = udata[0]
        self.family_name = udata[1]
        self.password = udata[2]
        self.national_code = udata[4]
        self.class_id = udata[3]
        self.school_id = udata[5]

        self.odd_even = 1
        self.attendance_check_active = False
        self.attendance_confirmed = True
        self.present = True
        self.attendance_lock = Lock()
        self.title('Main-Page')
        self.geometry('1000x650')
        self.minsize(1000, 650)
        
        # Initialize components
        self.get_available_cameras()
        self.setup_ui()
        
        # Initialize alert system
        self.alert_system = InAppAlert(self)
        
        # Start background threads
        Thread(target=self.ping_handler, daemon=True).start()
        Thread(target=self.start_video_stream, daemon=True).start()
        Thread(target=self.monitor_attendance_status, daemon=True).start()
        
        # Setup keyboard listener
        keyboard.on_press_key("k", lambda _: self.key_pressed())

    def monitor_attendance_status(self):
        """Continuously monitor attendance status and show/hide alert"""
        while True:
            if not self.present and self.odd_even % 2 == 0:
                self.after(0, self.alert_system.show_alert, 
            "error",
            "ATTENDANCE REQUIRED",
            "You have been marked as absent for the current session.\n\nPress K to confirm your attendance",
            0,
            "line"
)
            elif self.present and self.alert_system.alert_active:
                self.after(0, self.alert_system._cleanup)
            time.sleep(1)

    def setup_ui(self):
        """Initialize all UI components"""
        self.main_frame = CTkFrame(master=self, border_color='red', border_width=2)
        self.main_frame.pack(padx=20, pady=20, expand=True, fill='both')
        
        self.elements_frame = CTkFrame(self.main_frame, fg_color='transparent')
        self.elements_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Create UI elements
        self.camera_label = CTkLabel(master=self.elements_frame, text='')
        self.user_detail_textbox = CTkTextbox(master=self.elements_frame, 
                                            border_color='white', 
                                            border_width=2, 
                                            font=('montserrat', 14, 'bold'), 
                                            height=130)
        self.camera_selectbox_lbl = CTkLabel(self.elements_frame, 
                                            text='Camera:', 
                                            font=('montserrat', 30, 'bold'))
        self.camera_selectbox = CTkOptionMenu(self.elements_frame, 
                                             values=list(self.available_camera.keys()), 
                                             font=('montserrat', 25, 'bold'), 
                                             height=40, 
                                             command=self.change_camera)
        self.rechech_availale_camera = CTkButton(self.elements_frame, 
                                               text='Recheck', 
                                               font=('montserrat', 20, 'bold'), 
                                               height=40, 
                                               border_color='white', 
                                               border_width=2, 
                                               command=self.recheck_button)
        self.connection_status_ping_lbl = CTkLabel(self.elements_frame, 
                                                 text='Connection Status / Ping', 
                                                 font=('montserrat', 25))
        self.current_connection_status_entry = CTkEntry(self.elements_frame, 
                                                       font=('montserrat', 20, 'bold'), 
                                                       border_color='white', 
                                                       border_width=2)
        self.current_ping_status_entry = CTkEntry(self.elements_frame, 
                                                font=('montserrat', 20, 'bold'), 
                                                border_color='white', 
                                                border_width=2)
        self.start_button = CTkButton(self.elements_frame, 
                                    height=50, 
                                    text='START', 
                                    font=('montserrat', 20, 'bold'), 
                                    command=self.start_btn_func)

        # Add user data to textbox
        self.user_detail_textbox.delete(1.0, END)
        self.text = f'Name: {self.first_name}\nFamily: {self.family_name}\nSCHOOL: {self.school_id}\nCLASS: {self.class_id}'
        self.user_detail_textbox.insert(1.0, text=self.text) 
        self.user_detail_textbox.configure(state=DISABLED)
        
        # Place UI elements
        self.camera_label.grid(row=0, column=0, rowspan=4)
        self.user_detail_textbox.grid(row=0, column=1, padx=(20,0), sticky='nswe', columnspan=2)
        self.camera_selectbox_lbl.grid(row=1, column=1, padx=(20,0), sticky='w', pady=(5,0), columnspan=2)
        self.camera_selectbox.grid(row=2, column=1, padx=(20,0), sticky='we', pady=(0,5), columnspan=2)     
        self.rechech_availale_camera.grid(row=3, column=1, padx=(20, 0), sticky='we', pady=5, columnspan=2)
        self.connection_status_ping_lbl.grid(row=4, column=0, sticky='w', pady=(15, 0))
        self.current_connection_status_entry.grid(row=4, column=1, padx=(20,0), sticky='we', pady=(15, 0))
        self.current_ping_status_entry.grid(row=4, column=2, padx=(20,0), sticky='we', pady=(15, 0))
        self.start_button.grid(row=6, column=0, columnspan=3, sticky='ew', pady=(15, 0))
        
        # Set initial connection status
        self.current_connection_status_entry.insert(0, 'OFFLINE')
        self.current_connection_status_entry.configure(state=DISABLED)

    def start_video_stream(self):
        """Initialize and start video stream"""
        self.cap = cv2.VideoCapture(0)
        Thread(target=self.update_video, daemon=True).start()
        Thread(target=self.start_handler, daemon=True).start()
    
    def get_available_cameras(self):
        """Detect available cameras"""
        cameras = {}
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                name = f"CAM-{i}"
                cameras[name] = i
                cap.release()
        self.available_camera = cameras if cameras else {'No Camera found': -1}
    
    def change_camera(self, camera_name):
        """Change the active camera"""
        camera_index = self.available_camera.get(camera_name, -1)
        if self.cap.isOpened():
            self.cap.release()
        self.cap = cv2.VideoCapture(camera_index)
    
    def update_video(self):
        """Update video feed"""
        global frame
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (480, 360))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
        
        self.after(10, self.update_video)
    
    def recheck_button(self):
        """Recheck available cameras"""
        Thread(target=self.get_available_cameras, daemon=True).start()
        self.camera_selectbox.configure(values=list(self.available_camera.keys()))

    def generating_result(self):
        """Generate and send attendance results"""
        
        SCHOOL_CODE = self.school_id
        CLASS_NAME = self.class_id
        STUDENT_ID = self.udata[4]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reference_image = r"C:\sap-project\registered_image.jpg"

        if not self.present:
            send_data(str(SCHOOL_CODE), str(CLASS_NAME), str(STUDENT_ID))
            self.sender_func(f'absent|=|{current_time}')
            return 
    
        time.sleep(1)
        self.txt = f'{looking_result(ref_image_path=reference_image, frame=frame, pose_face_mesh_obj=self.pose_face_mesh_obj, eye_face_mesh_obj=self.eye_face_mesh_obj, app=self.app)}|=|{current_time}'
        
        # Send data to server
        send_data(str(SCHOOL_CODE), str(CLASS_NAME), str(STUDENT_ID))
        print(f'Final message: {self.txt}')

        self.sender_func(self.txt)
    
    def start_handler(self):
        """Main handler for attendance checks"""
        while True:
            if self.odd_even % 2 == 0:
                Thread(target=self.generating_result, daemon=True).start()
            time.sleep(10)

    def random_attendance_check(self):
        """Manage random attendance checks"""
        with self.attendance_lock:
            if self.attendance_check_active:
                return
                
            self.attendance_check_active = True
        
        try:
            # Wait random time between 1-10 minutes
            wait_time = 60 #random.randint(1, 2) * 60
            print(f"Next attendance check in {wait_time//60} minutes")
            time.sleep(wait_time)
            
            if self.odd_even % 2 == 0:  # Only if still in class
                self.attendance_confirmed = False
                
                # Show notification
                notification.notify(
                    title='Attendance Check',
                    message='Press K to confirm your attendance',
                    app_name='Class Attendance',
                    timeout=60
                )
                
                # print("Press K to confirm your attendance")
                
                # Wait for 2 minutes for user response
                start_time = time.time()
                while time.time() - start_time < 60:
                    if self.attendance_confirmed:
                        break
                    time.sleep(1)
                
                if not self.attendance_confirmed:
                    self.present = False # if not press k, mark as absent
                    notification.notify(
                        title='Attendance Warning',
                        message='You have been marked as absent! Press K to confirm attendance',
                        app_name='Class Attendance',
                        timeout=60
                    )
                    # print("User marked as absent. Press K to confirm attendance")
        finally:
            with self.attendance_lock:
                self.attendance_check_active = False

    def key_pressed(self):
        """Handle K key press for attendance confirmation"""
        if not self.attendance_confirmed:
            self.attendance_confirmed = True
            self.present = True # if press k, mark as present
            notification.notify(
                title='Attendance Confirmed',
                message='Your attendance has been confirmed!',
                app_name='Class Attendance'
            )
            # print("User attendance confirmed")
            
            # Schedule next check
            if self.odd_even % 2 == 0:
                Thread(target=self.random_attendance_check, daemon=True).start()

    def pinging(self):
        """Check network ping"""
        response_time = ping('google.com', unit='ms')
        if response_time is not None:
            response_time = f"{response_time:.2f} ms"
        else:
            response_time = "Failed"

        self.current_ping_status_entry.configure(state=NORMAL)
        self.current_ping_status_entry.delete(0, END)
        self.current_ping_status_entry.insert(END, response_time)
        self.current_ping_status_entry.configure(state=DISABLED)

    def ping_handler(self):
        """Continuous ping monitoring"""
        while True:
            self.pinging()
            time.sleep(1)
    
    def start_btn_func(self):
        """Handle start/stop button"""
        self.odd_even += 1
        if self.odd_even % 2 == 0:
            self.current_connection_status_entry.configure(state=NORMAL)
            self.current_connection_status_entry.delete(0, END)
            self.current_connection_status_entry.insert(0, 'IN-CLASS')
            self.current_connection_status_entry.configure(state=DISABLED)
            self.start_button.configure(text="Stop", fg_color='red', hover_color='#9C1218')
            
            # Start the first attendance check
            Thread(target=self.random_attendance_check, daemon=True).start()
        else:
            self.current_connection_status_entry.configure(state=NORMAL)
            self.current_connection_status_entry.delete(0, END)
            self.current_connection_status_entry.insert(0, 'OFFLINE')
            self.current_connection_status_entry.configure(state=DISABLED)
            self.start_button.configure(text="Start", fg_color='#1F6AA5', hover_color='#144870')
        
        self.attendance_confirmed = True

    def sender_func(self, txt):   
        """Send data to server"""
        data = self.udata
        try:
            print(f'Username: {data[4]}\nPassword: {data[2]}\nClass: {self.class_id}\nSchool: {self.school_id}\nText: {txt}')
            send_data_to_server(username=data[4], password=data[2], 
                              school_name=self.school_id, class_code=self.class_id, text=txt)
        except Exception as e:
            self.odd_even += 1
            messagebox.showwarning('Connection Error', 'Cannot join to class at this time!\nTry again later.')
            print(e)
            self.current_connection_status_entry.configure(state=NORMAL)
            self.current_connection_status_entry.delete(0, END)
            self.current_connection_status_entry.insert(0, 'OFFLINE')
            self.current_connection_status_entry.configure(state=DISABLED)
            self.start_button.configure(text="Start", fg_color='#1F6AA5', hover_color='#144870')

    def run(self):
        """Start the application"""
        self.mainloop()

def main_page_func_student(udata):
    """Entry point for student main page"""
    app = MainPage(udata)
    app.run()

if __name__ == "__main__":
    test_data = (
        'Abolfazl',
        'Rashidian',
        'stpass',
        '7b#52-42-54-4a',
        '09295',
        'hn1'
    )
    main_page_func_student(test_data)