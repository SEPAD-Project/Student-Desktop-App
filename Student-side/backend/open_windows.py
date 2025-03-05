import win32gui
import time

def get_visible_windows():
    windows = []
    def enum_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
            windows.append(win32gui.GetWindowText(hwnd))
        return True
    win32gui.EnumWindows(enum_callback, None)
    return windows

try:
    while True:
        visible_windows = get_visible_windows()
        active_window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        
        print("open windows :")
        for title in visible_windows:
            print(f" - {title}")
        print(f"current active window : {active_window_title}")
        print("-------------------")
        time.sleep(5)
except KeyboardInterrupt:
    print("quiting ...")