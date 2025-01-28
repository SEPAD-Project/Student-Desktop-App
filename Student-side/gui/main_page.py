from customtkinter import CTk, CTkTextbox, CTkLabel, CTkButton, CTkFrame, CTkOptionMenu, CTkEntry, END, DISABLED, NORMAL
import cv2
from PIL import Image, ImageTk
import os
from threading import Thread
from pathlib import Path
import sys
from scapy.all import ICMP, IP, sr1
from time import time
parent_dir = Path(__file__).resolve().parent.parent.parent.parent
print(parent_dir)
sys.path.append(str(parent_dir / "Head-Position-Estimination/looking_result/"))

from func_looking_result import looking_result # type: ignore

class MainPage(CTk):
    def __init__(self, udata):
        super().__init__()
        self.udata = udata
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
        self.user_detail_textbox = CTkTextbox(master=self.elements_frame, border_color='white', border_width=2, font=('montserrat', 15, 'bold'), height=130)
        self.camera_selectbox_lbl = CTkLabel(self.elements_frame, text='Camera :' , font=('montserrat', 30, 'bold'))
        self.camera_selectbox = CTkOptionMenu(self.elements_frame, values=list(self.available_camera.keys()), font=('montserrat', 25, 'bold'), height=40, command=self.change_camera)
        self.rechech_availale_camera = CTkButton(self.elements_frame, text='Recheck', font=('montserrat', 20, 'bold'), height=40, border_color='white', border_width=2, command=self.recheck_button)
        self.connection_status_ping_lbl = CTkLabel(self.elements_frame, text='Connection Status / Ping' , font=('montserrat', 25))
        self.current_connection_status_entry = CTkEntry(self.elements_frame , font=('montserrat', 20, 'bold'), border_color='white', border_width=2)
        # self.current_ping_status_lbl = CTkLabel(self.elements_frame, text='PING :' , font=('montserrat', 30))
        self.current_ping_status_entry = CTkEntry(self.elements_frame , font=('montserrat', 20, 'bold'), border_color='white', border_width=2)
        self.start_button = CTkButton(self.elements_frame, height=50, text='START', font=('montserrat', 20, 'bold'))

        # adding user data (self.udata) to textbox
        self.user_detail_textbox.delete(1.0, END)
        self.text = f'Name : {self.udata[0]}\nFamily : {self.udata[1]}\nClass : {self.udata[3]}UID : '
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
        # self.current_ping_status_lbl.grid(  row=5, column=0,                sticky='w', pady=(15, 0))
        self.current_ping_status_entry.grid(row=4, column=2, padx=(20,0),   sticky='we',pady=(15, 0))
        self.start_button.grid(        row=6, column=0, columnspan=3,  sticky='ew', pady=(15, 0))


        Thread(target=self.start_video_stream).start()

    # starting camera with default camera index 
    def start_video_stream(self):
        default_camera_index = 0
        self.cap = cv2.VideoCapture(default_camera_index)
        self.update_video()
        self.generating_result()
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
        # print(self.available_camera)
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
        # print(self.available_camera)


    def generating_result(self):
        # print('entered')
        print(looking_result(data_path=r'C:\\sap-project\\calibration-data.txt', frame=frame))
        self.after(5000, self.generating_result)
    
    def ping(self):
        packet = IP(dst='')/ICMP() # Make a ICMP packet

        start_time = time.time()
        response = sr1(packet, timeout=2, verbose=0)
        end_time = time.time()

        if response:
            ping = (end_time - start_time) * 1000
        else:
            ping = 'faild'
        

        


    def run(self):
        self.mainloop()


def main_page_func(udata):
    app = MainPage(udata)
    app.run()


if __name__ == "__main__":
    main_page_func(('abolfazl', 'rashidian', '123456', '1052'))


