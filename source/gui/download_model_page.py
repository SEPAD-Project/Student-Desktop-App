from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkCheckBox
from threading import Thread
from tkinter import messagebox
import sys
from requests import get, exceptions
from pathlib import Path

# System paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "backend"))


class DownloadModelPage(CTk):
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
        self.title('Model Download Page')

    def create_widgets(self):
        """Create and arrange GUI elements"""
        self.element_frame = CTkFrame(master=self.main_frame, fg_color='transparent')
        self.element_frame.place(relx=0.5, rely=0.5, anchor='center')

        # List of GUI elements
        elements = [
            CTkLabel(master=self.element_frame, text="Model Download Page", font=('montserrat', 26, 'bold')),
            CTkButton(master=self.element_frame, text="Download", font=('montserrat', 20, 'bold'),
                     corner_radius=10)
        ]

        # Positioning settings
        grid_config = [
            (0, 0, {'columnspan': 2}),
            (1, 0, {'columnspan': 2, 'sticky': 'ew'})
        ]

        # Placing elements in the grid
        for element, (row, col, kwargs) in zip(elements, grid_config):
            element.grid(row=row, column=col, **kwargs)

        # Assignment to class variables
        (self.download_text,
         self.download_btn) = elements


    def check_internet(self):
        """Check internet connection"""
        try:
            get('https://google.com', timeout=5)
            return True
        except exceptions.ConnectionError:
            self.show_error("Connection Error", "No internet connection!")
            self.toggle_button()
            return False

    def toggle__button(self, state='normal'):
        """Toggle button state"""
        self.download_btn.configure(state=state, text="Download" if state == 'normal' else "Downloading ...")

    def show_error(self, title, message):
        """Show error message dialog"""
        self.after(0, lambda: messagebox.showerror(title, message))

    def run(self):
        self.mainloop()

if __name__ == '__main__':
    app = DownloadModelPage()
    app.run()