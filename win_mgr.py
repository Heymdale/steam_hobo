import ctypes
from ctypes import wintypes


def get_hwnd_by_name(name: str) -> int:
    hwnd = ctypes.windll.user32.FindWindowW(0, name)
    return hwnd


def get_hwnds_by_pid(pid: int) -> list[int]:
    hwnds = []

    def activate_window(hwnd):
        target_pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(target_pid))
        if pid == target_pid.value:
            return True
        return False

    def each_window(hwnd, _):
        if activate_window(hwnd):
            hwnds.append(hwnd)
        return 1

    proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_ulong, ctypes.c_ulong)(each_window)
    ctypes.windll.user32.EnumWindows(proc, 0)

    return hwnds

def get_window_rect_from_name(hwnd: int) -> tuple:
    # hwnd = ctypes.windll.user32.FindWindowW(0, name)
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
    return rect.left, rect.top, rect.right, rect.bottom



def test():
    print(get_hwnds_by_pid(15340))



if __name__ == '__main__':
    test()
