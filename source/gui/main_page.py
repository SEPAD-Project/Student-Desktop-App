from customtkinter import CTk, CTkTextbox, CTkLabel, CTkButton, CTkFrame, CTkOptionMenu, CTkEntry, END, DISABLED, NORMAL
import cv2
from PIL import Image, ImageTk
from threading import Thread
from pathlib import Path
import sys
from ping3 import ping
import time
from tkinter import messagebox
from datetime import datetime


sys.path.append(str(Path(__file__).resolve().parent.parent))
from backend.image_processing.looking_result.func_looking_result import looking_result
from backend.looking_result_sender import send_data_to_server
from backend.open_windows_sender import send_data

class MainPage(CTk):
    def __init__(self, udata):
        super().__init__()
        cv2.setLogLevel(0)
        reverse_class_code = lambda code, key="crax6ix": (str(int(code.split('#')[0], 16)), ''.join(chr(int(h, 16) ^ ord(key[i % len(key)])) for i, h in enumerate(code.split('#')[1].split('-'))))

        self.udata = udata #('Abolfazl', 'Rashidian', '123', '7b#52-42-54-4a', '09295', '123')
        print(self.udata)
        self.first_name = udata[0]
        self.family_name = udata[1]
        self.password = udata[2]
        self.unic_school_code = self.udata[3] # unic_code
        self.national_code = self.udata[4]
        self.school_code = self.udata[5]

        self.school_code, self.class_name = reverse_class_code(self.udata[3])


        self.odd_even = 1
        self.title('Main-Page')
        self.geometry('1000x650')
        self.minsize(1000, 650)
        # self.resizable(False, False)
        # getting avaiable cameras
        self.get_available_cameras()
        # main red frame
        self.main_frame = CTkFrame(master=self, border_color='red', border_width=2)
        self.main_frame.pack(padx=20, pady=20, expand=True, fill='both')
        # center frame for holding everything in center
        self.elements_frame = CTkFrame(self.main_frame, fg_color='transparent')
        self.elements_frame.place(relx=0.5, rely=0.5, anchor='center')
        # elements
        self.camera_label = CTkLabel(master=self.elements_frame, text='')
        self.user_detail_textbox = CTkTextbox(master=self.elements_frame, border_color='white', border_width=2, font=('montserrat', 14, 'bold'), height=130)
        self.camera_selectbox_lbl = CTkLabel(self.elements_frame, text='Camera :' , font=('montserrat', 30, 'bold'))
        self.camera_selectbox = CTkOptionMenu(self.elements_frame, values=list(self.available_camera.keys()), font=('montserrat', 25, 'bold'), height=40, command=self.change_camera)
        self.rechech_availale_camera = CTkButton(self.elements_frame, text='Recheck', font=('montserrat', 20, 'bold'), height=40, border_color='white', border_width=2, command=self.recheck_button)
        self.connection_status_ping_lbl = CTkLabel(self.elements_frame, text='Connection Status / Ping' , font=('montserrat', 25))
        self.current_connection_status_entry = CTkEntry(self.elements_frame , font=('montserrat', 20, 'bold'), border_color='white', border_width=2)
        self.current_ping_status_entry = CTkEntry(self.elements_frame , font=('montserrat', 20, 'bold'), border_color='white', border_width=2)
        self.start_button = CTkButton(self.elements_frame, height=50, text='START', font=('montserrat', 20, 'bold'), command=self.start_btn_func)

        # adding user data (self.udata) to textbox
        self.user_detail_textbox.delete(1.0, END) # #student_name, student_family, student_password, class_code, school_code, student_national_code
        self.text = f'Name : {self.first_name}\nFamily : {self.family_name}\nClass : {self.class_name}\nSchool Code : {self.school_code}\nNational code : {self.national_code}'
        self.user_detail_textbox.insert(1.0, text=self.text) 
        self.user_detail_textbox.configure(state=DISABLED)
        # placing elements
        self.camera_label.grid(        row=0, column=0, rowspan=4)
        self.user_detail_textbox.grid( row=0, column=1, padx=(20,0),   sticky='nswe', columnspan=2)
        self.camera_selectbox_lbl.grid(row=1, column=1, padx=(20,0),   sticky='w', pady=(5,0), columnspan=2)
        self.camera_selectbox.grid(    row=2, column=1, padx=(20,0),   sticky='we', pady=(0,5), columnspan=2)     
        self.rechech_availale_camera.grid(row=3, column=1, padx=(20, 0), sticky='we', pady=5, columnspan=2)
        self.connection_status_ping_lbl.grid(  row=4, column=0,                sticky='w', pady=(15, 0))
        self.current_connection_status_entry.grid(row=4, column=1, padx=(20,0),   sticky='we',pady=(15, 0))
        self.current_ping_status_entry.grid(row=4, column=2, padx=(20,0),   sticky='we',pady=(15, 0))
        self.start_button.grid(        row=6, column=0, columnspan=3,  sticky='ew', pady=(15, 0))
        
        self.current_connection_status_entry.insert(0, 'OFFLINE')
        self.current_connection_status_entry.configure(state=DISABLED)
        self.pinging()
        Thread(target=self.start_video_stream).start()


    # starting camera with default camera index 
    def start_video_stream(self):
        self.cap = cv2.VideoCapture(0)
        Thread(target=self.update_video).start()
        Thread(target=self.generating_result).start()
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
    # changing camera by releasing and reopening with VideoCapture
    def change_camera(self, camera_name):
        camera_index = self.available_camera.get(camera_name, -1)
        if self.cap.isOpened():
            self.cap.release()
        self.cap = cv2.VideoCapture(camera_index)
    # update video each 10ms
    def update_video(self):
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
        Thread(target=self.get_available_cameras).start()
        self.camera_selectbox.configure(values=list(self.available_camera.keys()))

    def generating_result(self):
        SCHOOL_CODE = self.school_code
        CLASS_NAME = self.class_name
        STUDENT_ID = self.udata[4]
        if self.odd_even % 2 == 0:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            reference_image = r"C:\sap-project\registered_image.jpg"
            time.sleep(2)
            self.txt = f'{looking_result(ref_image_path=reference_image, frame=frame)}|=|{current_time}'
            # sending opens windows to server
            send_data(str(SCHOOL_CODE), str(CLASS_NAME), str(STUDENT_ID))
            print(f'final message : {self.txt}')

            self.sender_func(self.txt)
        self.after(10000, self.generating_result)
    
    def pinging(self):
        response_time = ping('google.com', unit='ms')
        if response_time is not None:
            response_time = f"{response_time:.2f} ms"
        else:
            response_time = f"Failed"

        if response_time:
            self.current_ping_status_entry.configure(state=NORMAL)
            self.current_ping_status_entry.delete(0, END)
            self.current_ping_status_entry.insert(END, response_time)
        else:
            response_time == 'Failed'
            self.current_ping_status_entry.configure(state=NORMAL)
            self.current_ping_status_entry.delete(0, END)
            self.current_ping_status_entry.insert(END, response_time)
        self.current_ping_status_entry.configure(state=DISABLED)

        self.after(1000, self.pinging)

     

    def start_btn_func(self): #student_name, student_family, student_password, class_code, school_code, student_national_code, class_name
        self.odd_even+=1
        if self.odd_even % 2 == 0:
            self.current_connection_status_entry.configure(state=NORMAL)
            self.current_connection_status_entry.delete(0, END)
            self.current_connection_status_entry.insert(0, 'IN-CLASS')
            self.current_connection_status_entry.configure(state=DISABLED)
            self.start_button.configure(text="Stop", fg_color='red', hover_color='#9C1218')
            
            
        else:
            self.current_connection_status_entry.configure(state=NORMAL)
            self.current_connection_status_entry.delete(0, END)
            self.current_connection_status_entry.insert(0, 'OFFLINE')
            self.current_connection_status_entry.configure(state=DISABLED)
            self.start_button.configure(text="Start", fg_color='#1F6AA5', hover_color='#144870')

    def sender_func(self, txt):   
        data = self.udata
        try:
            print(data)
            print(f'username : {data[4]}\npassword : {data[2]}\nclass_name : {self.class_name}\nschool_code : {self.school_code}\ntext : {txt}')
            send_data_to_server(username=data[4], password=data[2], 
                                school_name=self.school_code, class_code=self.class_name, text=txt)
        except Exception as e:
            self.odd_even+=1
            messagebox.showwarning('Connection Error', 'Can not join to class at this time!\nTry again later.')
            print(e)
            self.current_connection_status_entry.configure(state=NORMAL)
            self.current_connection_status_entry.delete(0, END)
            self.current_connection_status_entry.insert(0, 'OFFLINE')
            self.current_connection_status_entry.configure(state=DISABLED)
            self.start_button.configure(text="Start", fg_color='#1F6AA5', hover_color='#144870')



    def run(self):
        self.mainloop()



def main_page_func_student(udata):
    app = MainPage(udata)
    Thread(target=app.run()).start()



if __name__ == "__main__": # student_name, student_family, student_password, class_code, school_code, student_national_code

    test_data = (
        'Abolfazl',
        'Rashidian',
        'stpass',
        '7b#52-42-54-4a',  # Example encoded class info
        '09295',
        'hn1 '
    )
    main_page_func_student(test_data)
