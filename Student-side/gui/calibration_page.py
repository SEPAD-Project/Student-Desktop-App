from customtkinter import CTkFrame, CTk, CTkButton, CTkLabel, CTkOptionMenu
import cv2
from PIL import Image, ImageTk
from threading import Thread
from time import sleep
from webbrowser import open
import os
from tkinter import messagebox



class CalibrationPage(CTk):
    def __init__(self):
        super().__init__()


        self.title('Calibration-Page')
        self.geometry('900x630')
        self.minsize(900, 630)
        # self.resizable(False, False)

        self.get_available_cameras()
        # main red frame
        self.main_frame = CTkFrame(master=self, border_color='red', border_width=2)
        self.main_frame.pack(padx=20, pady=20, expand=True, fill='both')
        # center frame for holding everything in center
        self.element_frame = CTkFrame(master=self.main_frame, fg_color='transparent')
        self.element_frame.place(relx=0.5, rely=0.5, anchor='center')
        # main elements
        self.video_label = CTkLabel(master=self.element_frame, text='', height=297, width=405)
        self.capture_button_1 = CTkButton(master=self.element_frame, text='TOP LEFT\nCAPTURE', border_color='white', border_width=2, font=('montserrat', 15, 'bold'), height=70, command=lambda: self.capture_image(1))
        self.capture_button_2 = CTkButton(master=self.element_frame, text='BOTTOM RIGHT\nCAPTURE', border_color='white', border_width=2, font=('montserrat', 15, 'bold'), height=70, command=lambda: self.capture_image(2))
        self.guide_button = CTkButton(master=self.element_frame, text='Guide', border_color='white', border_width=2, font=('montserrat', 25, 'bold'), command=lambda: open('hnsch1.ir'))
        # self.camera_selectbotx_lbl = CTkLabel(master=self.element_frame, text='Camera :', font=('montserrat', 30, 'bold'))
        self.camera_selectbox = CTkOptionMenu(self.element_frame, values=list(self.available_camera.keys()), font=('montserrat', 15, 'bold'), height=60, command=self.change_camera)
        self.recheck_button = CTkButton(self.element_frame, text='Recheck', font=('montserrat', 20, 'bold'), height=40, border_color='white', border_width=2, command=self.recheck_button_func) 
        self.next_page_button = CTkButton(master=self.element_frame, text='Next Page', font=('montserrat', 20, 'bold'), border_color='white', border_width=2, height=70, command=self.next_page_func)
        self.close_button = CTkButton(master=self.element_frame, text='Close', font=('montserrat', 20, 'bold'), border_color='white', border_width=2, command=lambda: self.destroy(), fg_color='red', hover_color='#6B0011')

        # placing elements in elements_frame
        self.video_label.grid(      row=0, column=0, rowspan=3, columnspan=2, sticky='ew')
        self.capture_button_1.grid( row=3, column=0, pady=20, sticky='ew')
        self.capture_button_2.grid( row=3, column=1, padx=(20,0), sticky='ew')
        self.guide_button.grid(     row=0, column=2, padx=(20,0), sticky='ensw')
        # self.camera_selectbotx_lbl.grid(row=1, column=2, padx=20, sticky='nws')
        self.camera_selectbox.grid( row=1, column=2, padx=(20,0), sticky='ew')
        self.recheck_button.grid(   row=2, column=2, padx=(20,0), sticky='ensw')
        self.next_page_button.grid (row=3, column=2, padx=(20,0), sticky='ew')
        self.close_button.grid(row=4, column=0, columnspan=3,sticky='ew')

        Thread(target=self.start_video_stream).start()

    # starting camera with default camera index 
    def start_video_stream(self):
        default_camera_index = 0
        self.cap = cv2.VideoCapture(default_camera_index)
        self.update_video()

    # update video each 10ms
    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (540, 405))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.after(10, self.update_video)

    # changing camera by releasing and reopening with VideoCapture
    def change_camera(self, camera_name):
        camera_index = self.available_camera.get(camera_name, -1)
        if self.cap.isOpened():
            self.cap.release()
        self.cap = cv2.VideoCapture(camera_index)

    # getting connected camera to system by testing their index in VideoCapture
    def get_available_cameras(self):
        cameras = {}
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                name = f"CAM-{i}"
                cameras[name] = i
                cap.release()
        self.available_camera = cameras if cameras else {'No Camera found' : -1}
        print(self.available_camera)

    def recheck_button_func(self):
        Thread(target=self.get_available_cameras).start()
        def waiter():
            self.camera_selectbox.set(list(self.available_camera.keys())[0] if self.available_camera else 'No Camera found')
            self.camera_selectbox.configure(values=list(self.available_camera.keys()))
            sleep(3)
        Thread(target=waiter).start()

    def capture_image(self, button_number):
        ret, frame = self.cap.read()
        if ret:
            filename = f'captured_image_{button_number}.jpg'
            cv2.imwrite(filename, frame)
            print(f'Image {button_number} saved as {filename}')
        
    def next_page_func(self):
        if os.path.exists('captured_image_1.jpg') and os.path.exists('captured_image_2.jpg') :
            self.destroy()
        else:
            messagebox.showerror('Calibration Error', 'You have not taken picture 1 or 2 !')

    def run(self):
        self.mainloop()


    
def calibration_page_func():
    calib_app = CalibrationPage()
    calib_app.run()

if __name__ == '__main__' : 
    calibration_page_func()