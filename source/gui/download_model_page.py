from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkCheckBox
from threading import Thread



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
        self.title('Student Side Login Page')

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
        (self.login_text, self.username_lbl, self.password_lbl, 
         self.username_entry, self.password_entry, self.checkbox, 
         self.login_btn) = elements


    def run(self):
        self.mainloop()

if __name__ == '__main__':
    app = DownloadModelPage()
    app.run()