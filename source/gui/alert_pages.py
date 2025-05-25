import customtkinter as ctk
from threading import Thread
import time

class InAppAlert:
    def __init__(self, root):
        self.root = root
        self.alert_active = False
        
    def show_alert(self, message, duration=0, alert_type="warning"):
        if self.alert_active:
            return
            
        self.alert_active = True
        
        # Color schemes based on alert type
        color_palette = {
            "warning": {"bg": "#1F1F1F", "border": "#FF9500", "text": "#FF9500", "icon": "⚠"},
            "error": {"bg": "#1F1F1F", "border": "#FF4444", "text": "#FF4444", "icon": "❌"},
            "success": {"bg": "#1F1F1F", "border": "#4CAF50", "text": "#4CAF50", "icon": "✓"},
            "info": {"bg": "#1F1F1F", "border": "#2196F3", "text": "#2196F3", "icon": "ℹ"}
        }
        
        colors = color_palette.get(alert_type, color_palette["warning"])
        
        # Create overlay frame
        self.overlay = ctk.CTkFrame(self.root,
                                   fg_color="gray20",
                                   corner_radius=0)
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Main alert frame
        self.alert_frame = ctk.CTkFrame(self.overlay,
                                      fg_color=colors["bg"],
                                      border_color=colors["border"],
                                      border_width=2,
                                      corner_radius=12,
                                      width=500,
                                      height=250)
        self.alert_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Header section
        header_frame = ctk.CTkFrame(self.alert_frame, fg_color="transparent")
        header_frame.pack(pady=(20, 10), fill="x")
        
        ctk.CTkLabel(header_frame,
                    text=f"{colors['icon']} {alert_type.upper()} {colors['icon']}",
                    font=("Arial", 22, "bold"),
                    text_color=colors["text"]).pack()
        
        # Message content
        message_frame = ctk.CTkFrame(self.alert_frame, fg_color="transparent")
        message_frame.pack(pady=10, padx=30, fill="both", expand=True)
        
        self.message_label = ctk.CTkLabel(message_frame,
                                        text=message,
                                        font=("Arial", 16),
                                        text_color="white",
                                        wraplength=450,
                                        justify="center")
        self.message_label.pack()
        
        # Button section
        button_frame = ctk.CTkFrame(self.alert_frame, fg_color="transparent")
        button_frame.pack(pady=(10, 20))
        
        close_btn = ctk.CTkButton(button_frame,
                                text="OK",
                                fg_color=colors["border"],
                                hover_color=colors["text"],
                                text_color="white",
                                width=120,
                                height=35,
                                corner_radius=8,
                                command=self._cleanup)
        close_btn.pack()
        
        # Auto-close if duration is specified
        if duration > 0:
            Thread(target=self._auto_close, args=(duration,), daemon=True).start()

    def _auto_close(self, duration):
        time.sleep(duration)
        self.root.after(0, self._cleanup)

    def _cleanup(self):
        if hasattr(self, 'overlay'):
            self.overlay.destroy()
        self.alert_active = False


# Example usage:
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")
    
    alert = InAppAlert(root)
    
    def show_test_alert():
        alert.show_alert("This is a sample warning message to demonstrate the alert system. The text should now be properly visible.", 0, "warning")
    
    test_btn = ctk.CTkButton(root, text="Show Alert", command=show_test_alert)
    test_btn.pack(pady=50)
    
    root.mainloop()