from customtkinter import CTkFrame, CTk, CTkButton, CTkLabel, CTkOptionMenu, CTkImage
import cv2
from PIL import Image, ImageTk
import threading
from time import sleep
from webbrowser import open
import os
from tkinter import messagebox
from main_page import main_page_func_student
from pathlib import Path
import sys
import queue
from threading import Thread

sys.path.append(str(Path(__file__).resolve().parent))
from backend.frame_receiver import get_image
from backend.image_processing.face_recognition.compare import compare


class AddFacePage(CTk):
    def __init__(self, udata):
        super().__init__()
        self.udata = udata
        cv2.setLogLevel(0)
        self.title('Add Face-Page')
        self.geometry('750x580')
        self.minsize(750, 580)
        # self.resizable(False, False)


        

        self.get_available_cameras()
        # main red frame
        self.main_frame = CTkFrame(master=self, border_color='red', border_width=2)
        self.main_frame.pack(padx=20, pady=20, expand=True, fill='both')
        # center frame for holding everything in center
        self.element_frame = CTkFrame(master=self.main_frame, fg_color='transparent')
        self.element_frame.place(relx=0.5, rely=0.5, anchor='center')
        # main elements
        self.video_label = CTkLabel(master=self.element_frame, text='', height=220, width=320)
        self.capture_button = CTkButton(master=self.element_frame, text='CAPTURE', border_color='white', border_width=2, font=('montserrat', 20, 'bold'), height=60, command=self.capture_image)
        self.guide_button = CTkButton(master=self.element_frame, text='Guide', border_color='white', border_width=2, font=('montserrat', 25, 'bold'), command=lambda: open('hnsch1.ir'))
        # self.camera_selectbotx_lbl = CTkLabel(master=self.element_frame, text='Camera :', font=('montserrat', 30, 'bold'))
        self.camera_selectbox = CTkOptionMenu(self.element_frame, values=list(self.available_camera.keys()), font=('montserrat', 15, 'bold'), height=60, command=self.change_camera)
        self.recheck_button = CTkButton(self.element_frame, text='Recheck', font=('montserrat', 20, 'bold'), height=40, border_color='white', border_width=2, command=self.recheck_button_func) 
        self.add_face_button = CTkButton(master=self.element_frame, text='Add Face', font=('montserrat', 20, 'bold'), border_color='white', border_width=2, height=60, command=self.adding_face_func, width=200)
        self.close_button = CTkButton(master=self.element_frame, text='Close', font=('montserrat', 20, 'bold'), border_color='white', border_width=2, height=60, command=lambda: self.destroy(), fg_color='red', hover_color='#6B0011')

        # placing elements in elements_frame
        self.video_label.grid(      row=0, column=0, rowspan=3, sticky='ew')
        self.capture_button.grid( row=3, column=0, pady=20, sticky='ew')
        self.guide_button.grid(     row=0, column=1, padx=(20,0), sticky='ensw')
        # self.camera_selectbotx_lbl.grid(row=1, column=2, padx=20, sticky='nws')
        self.camera_selectbox.grid( row=1, column=1, padx=(20,0), sticky='ew')
        self.recheck_button.grid(   row=2, column=1, padx=(20,0), sticky='ensw')
        self.add_face_button.grid (row=3, column=1, padx=(20,0), sticky='ew')
        self.close_button.grid(row=4, column=0, columnspan=3,sticky='ew')
        self.face_frame = None
        self.taken_image = None
        self.stat = True
        Thread(target=self.start_video_stream).start()

    # starting camera with default camera index 
    def start_video_stream(self):
        default_camera_index = 0
        self.cap = cv2.VideoCapture(default_camera_index)
        self.update_video()

    # update video each 10ms
    def update_video(self):
        if self.stat:
            try:
                ret, frame = self.cap.read()
                if ret:
                    frame = cv2.resize(frame, (432, 324))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame)
                    imagectk = CTkImage(light_image=img, size=(324, 243))
                    try:
                        self.video_label.configure(image=imagectk)
                    except Exception as er:
                        print('SUP ER')
                        print(er)
                self.after(30, self.update_video)
            except Exception as e:
                print('E')
                print(e)
        else:
            self.cap.release()
    # changing camera by releasing and reopening with VideoCapture
    def change_camera(self, camera_name):
        camera_index = self.available_camera.get(camera_name, -1)
        print(camera_index)
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


    # checking available cameras
    def recheck_button_func(self):
        Thread(target=self.get_available_cameras, daemon=True).start()
        def waiter():
            self.camera_selectbox.set(list(self.available_camera.keys())[0] if self.available_camera else 'No Camera found')
            self.camera_selectbox.configure(values=list(self.available_camera.keys()))
            sleep(3)
        Thread(target=waiter).start()

    # capturing image 
    def capture_image(self):
        ret, self.face_frame = self.cap.read()
        if ret:
            self.taken_image = Image.fromarray(self.face_frame)
    # adding face after comparing two frames 
    def adding_face_func(self):
        unic_class_code = self.udata[3]
        reverse_class_code = lambda code, key="crax6ix": (str(int(code.split('#')[0], 16)), ''.join(chr(int(h, 16) ^ ord(key[i % len(key)])) for i, h in enumerate(code.split('#')[1].split('-'))))
        original_school_code, original_class_name = reverse_class_code(unic_class_code)
        self.real_image = "C:\\sap-project\\real_image.jpg"
        self.registered_image = "C:\\sap-project\\registered_image.jpg"
        
        def add_face():
            # disabling button
            self.add_face_button.configure(state='disabled', text='Adding Face')
            
            # creating queue
            result_queue = queue.Queue()
            error_queue = queue.Queue()
            
            def download_and_compare():
                try:
                    if self.face_frame is None:
                        error_queue.put("No image taken!")
                        return
                    
                    # getting image from server in other thread
                    download_thread = threading.Thread(target=get_image, args=(original_school_code, original_class_name, self.udata[4]))
                    download_thread.start()
                    download_thread.join()  # waiting for download complete
                    
                    if not os.path.exists(self.real_image):
                        error_queue.put("Couldn't connect to server!")
                        return
                    
                    # comparing pictures
                    print(type(self.face_frame))
                    compare_result = compare(ref_image_path=self.real_image,
                                            new_frame=self.face_frame)
                    result_queue.put(compare_result)
                    
                    if compare_result:
                        # saving if it was same
                        cv2.imwrite(self.registered_image, self.face_frame)
                        print(f'Image saved as {self.registered_image}')
                        sleep(1)
                        result_queue.put("success")
                    else:
                        error_queue.put("Image does not match system records!")
                
                except Exception as e:
                    error_queue.put(f"Error: {str(e)}")
            
            def check_results():
                try:
                    # checking errors
                    if not error_queue.empty():
                        error_msg = error_queue.get()
                        messagebox.showwarning('Error', error_msg)
                        self.add_face_button.configure(state='normal', text='Add Face')
                        return
                    
                    # checking results
                    if not result_queue.empty():
                        result = result_queue.get()
                        if result == "success":
                            try:
                                self.destroy()
                            except Exception as e:
                                print(f'Destroy error: {e}')
                            main_page_func_student(self.udata)
                        else:
                            self.add_face_button.configure(state='normal', text='Add Face')
                
                finally:
                    # enable button at the end 
                    self.after(100, lambda: self.add_face_button.configure(state='normal', text='Add Face'))
            
                self.after(100, check_results)
        
            processing_thread = threading.Thread(target=download_and_compare)
            processing_thread.start()
            check_results()

        # calling function
        add_face()


    def run(self):
        self.mainloop()


    
def add_face_page_func(udata):
    add_face_app = AddFacePage(udata)
    add_face_app.run()

if __name__ == '__main__' : 
    test_data = [
        'Abolfazl',
        'Rashidian',
        'stpass',
        '7b#52-42-54-4a',  # Example encoded class info
        '09295',
        'hn1 '
    ]
    add_face_page_func(udata=test_data)