from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkProgressBar
from threading import Thread
from tkinter import messagebox
import sys
from pathlib import Path
import requests
import time
import os

# System paths
OPENCV_FACE_DETECTOR_PATH = r"c:\sap-project\opencv\haarcascade_frontalface_default.xml"
OPENCV_FACE_RECOGNIZER_PATH = r"c:\sap-project\opencv\face_recognition_sface_2021dec.onnx"

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "backend"))

MODELS = [
    {
        "url": "https://github.com/SAP-Program/Head-Position-Estimation/raw/main/models/face_recognition_sface_2021dec.onnx",
        "path": OPENCV_FACE_RECOGNIZER_PATH,
        "name": "Face Recognition Model"
    },
    {
        "url": "https://github.com/SAP-Program/Head-Position-Estimation/raw/main/models/haarcascade_frontalface_default.xml",
        "path": OPENCV_FACE_DETECTOR_PATH,
        "name": "Face Detector Model"
    }
]

class DownloadModelPage(CTk):
    def __init__(self):
        super().__init__()
        self.download_queue = []
        self.current_download = None
        self.running = False
        self.init_ui()
        self.setup_window()
        self.check_existing_files()

    def init_ui(self):
        """Initialize all UI components"""
        # Main frame with red border (from original code)
        self.main_frame = CTkFrame(master=self, border_color='red', border_width=2)
        self.main_frame.pack(padx=20, pady=20, expand=True, fill='both')

        # Title moved higher (pady reduced)
        self.title_label = CTkLabel(
            master=self.main_frame, 
            text="Model Download Page", 
            font=('montserrat', 26, 'bold')
        )
        self.title_label.pack(pady=(30, 20))

        # Progress bar section
        self.progress_frame = CTkFrame(self.main_frame, fg_color='transparent')
        self.progress_frame.pack(fill='x', padx=20, pady=10)
        
        self.progress_bar = CTkProgressBar(self.progress_frame, height=15)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill='x', expand=True)

        # Download details
        self.status_label = CTkLabel(
            self.progress_frame, 
            text="Ready to download", 
            text_color="gray70"
        )
        self.status_label.pack(pady=(5, 0))

        self.details_label = CTkLabel(
            self.progress_frame, 
            text="", 
            text_color="gray70"
        )
        self.details_label.pack(pady=(2, 10))

        # Download button moved lower (pady increased)
        self.download_btn = CTkButton(
            self.main_frame,
            text="Download Missing Files",
            font=('montserrat', 20, 'bold'),
            corner_radius=10,
            command=self.start_download_thread,
            state="disabled"
        )
        self.download_btn.pack(pady=(0, 30))

    def setup_window(self):
        """Configure main window settings"""
        self.geometry('600x450')
        self.minsize(600, 450)
        self.title('Model Download Page')


    def show_error(self, title, message):
        """Show error message dialog"""
        messagebox.showerror(title, message)
        self.reset_ui()

    def show_success(self):
        messagebox.showinfo("Success", "All files downloaded successfully!")
        self.reset_ui()

    def reset_ui(self):
        self.progress_bar.set(0)
        self.details_label.configure(text="")
        self.download_btn.configure(state="normal")

    def run(self):
        self.mainloop()

if __name__ == '__main__':
    app = DownloadModelPage()
    app.run()