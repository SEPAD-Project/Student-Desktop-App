import customtkinter as ctk
from threading import Thread
import time
import random
import math

class ParticleLine:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.reset_position()
        self.length = random.randint(8, 15)
        self.speed = random.uniform(0.3, 1.2)
        self.angle = random.uniform(0, math.pi*2)
        self.color = self._select_color()
        self.line = self.canvas.create_line(
            self.x, self.y,
            self.x + math.cos(self.angle) * self.length,
            self.y + math.sin(self.angle) * self.length,
            fill=self.color, width=1
        )
    
    def reset_position(self):
        """Reset particle to random position within canvas"""
        self.x = random.randint(0, self.width)
        self.y = random.randint(0, self.height)
    
    def _select_color(self):
        colors = ["#FF4444", "#AAAAAA", "#888888", "#FF3333"]
        return random.choice(colors)
    
    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Wrap around edges
        if self.x < 0: self.x = self.width
        if self.x > self.width: self.x = 0
        if self.y < 0: self.y = self.height
        if self.y > self.height: self.y = 0
            
        self.canvas.coords(
            self.line,
            self.x, self.y,
            self.x + math.cos(self.angle) * self.length,
            self.y + math.sin(self.angle) * self.length
        )

class InAppAlert:
    def __init__(self, root):
        self.root = root
        self.alert_active = False
        self.particles = []
        
    def _create_particle_background(self, overlay):
        # Create canvas for particles
        self.particle_canvas = ctk.CTkCanvas(
            overlay, 
            bg="#111111",
            highlightthickness=0
        )
        self.particle_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Get actual canvas dimensions
        self.particle_canvas.update()
        width = self.particle_canvas.winfo_width()
        height = self.particle_canvas.winfo_height()
        
        # Create minimalist particle lines
        self.particles = [
            ParticleLine(self.particle_canvas, width, height) 
            for _ in range(40)
        ]
        self._animate_particles()
    
    def _animate_particles(self):
        if not self.alert_active or not hasattr(self, 'particle_canvas'):
            return
            
        for particle in self.particles:
            particle.move()
        self.root.after(30, self._animate_particles)
        
    def show_alert(self, message_type="warning", title="", message="", duration=0, enable_particles=True):
        """
        Display a customizable alert
        
        Parameters:
        - message_type: "warning", "error", "success", or "info"
        - title: The header text for the alert
        - message: The main content of the alert
        - duration: Auto-close after seconds (0 = manual close)
        - enable_particles: Boolean to toggle particle effects
        """
        if self.alert_active:
            return
            
        self.alert_active = True
        
        # Color schemes for different message types
        color_palette = {
            "warning": {
                "bg": "#1A1A1A",
                "border": "#FF9500",
                "text": "#FF9500",
                "icon": "⚠",
                "secondary": "#AAAAAA"
            },
            "error": {
                "bg": "#1A1A1A",
                "border": "#FF4444",
                "text": "#FF4444",
                "icon": "❌",
                "secondary": "#AAAAAA"
            },
            "success": {
                "bg": "#1A1A1A",
                "border": "#4CAF50",
                "text": "#4CAF50",
                "icon": "✓",
                "secondary": "#AAAAAA"
            },
            "info": {
                "bg": "#1A1A1A",
                "border": "#2196F3",
                "text": "#2196F3",
                "icon": "ℹ",
                "secondary": "#AAAAAA"
            }
        }
        
        # Default to warning if invalid type provided
        colors = color_palette.get(message_type.lower(), color_palette["warning"])
        
        # Create overlay frame
        self.overlay = ctk.CTkFrame(
            self.root,
            fg_color="#111111" if enable_particles else colors["bg"],
            corner_radius=0
        )
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Create particle background if enabled
        if enable_particles:
            self._create_particle_background(self.overlay)
        
        # Alert frame
        self.alert_frame = ctk.CTkFrame(
            self.overlay,
            fg_color=colors["bg"],
            border_color=colors["border"],
            border_width=1,
            corner_radius=8,
            width=500,
            height=300
        )
        self.alert_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.alert_frame.lift()
        
        # Header
        header_frame = ctk.CTkFrame(self.alert_frame, fg_color="transparent")
        header_frame.pack(pady=(25, 15), fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text=message_type.upper(),
            font=("Arial", 18, "bold"),
            text_color=colors["secondary"]
        ).pack()
        
        ctk.CTkLabel(
            header_frame,
            text=title,
            font=("Arial", 22, "bold"),
            text_color=colors["text"]
        ).pack(pady=(5, 0))
        
        # Divider line
        ctk.CTkFrame(
            self.alert_frame,
            fg_color=colors["border"],
            height=1
        ).pack(fill="x", padx=30, pady=10)
        
        # Message content
        ctk.CTkLabel(
            self.alert_frame,
            text=message,
            font=("Arial", 15),
            text_color="white",
            wraplength=450,
            justify="center"
        ).pack(pady=10, padx=30)
        
        # Button
        button_frame = ctk.CTkFrame(self.alert_frame, fg_color="transparent")
        button_frame.pack(pady=(10, 20))
        
        ctk.CTkButton(
            button_frame,
            text="ACKNOWLEDGE",
            fg_color="transparent",
            border_color=colors["border"],
            border_width=1,
            hover_color="#2A2A2A",
            text_color=colors["text"],
            width=140,
            height=32,
            corner_radius=4,
            command=self._cleanup
        ).pack()
        
        # Auto-close if duration specified
        if duration > 0:
            Thread(target=self._auto_close, args=(duration,), daemon=True).start()

    def _auto_close(self, duration):
        time.sleep(duration)
        self.root.after(0, self._cleanup)

    def _cleanup(self):
        if hasattr(self, 'overlay'):
            self.overlay.destroy()
        self.alert_active = False
        self.particles = []


# Example usage with particle toggle
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")
    
    alert = InAppAlert(root)
    
    # Example with particles enabled
    def show_with_particles():
        alert.show_alert(
            message_type="error",
            title="SECURITY ALERT",
            message="Unauthorized access attempt detected",
            duration=0

        )
    
    # Example with particles disabled
    def show_without_particles():
        alert.show_alert(
            message_type="info",
            title="SYSTEM NOTIFICATION",
            message="New update available for installation",
            duration=3
        )
    
    # Create test buttons
    ctk.CTkButton(root, 
                 text="Show Alert With Particles", 
                 command=show_with_particles).pack(pady=10)
    
    ctk.CTkButton(root, 
                 text="Show Alert Without Particles", 
                 command=show_without_particles).pack(pady=10)
    
    root.mainloop()