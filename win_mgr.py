import ctypes
from ctypes import wintypes


class WinMgr:

    @staticmethod
    def get_hwnd_by_name(name: str) -> int:
        hwnd = ctypes.windll.user32.FindWindowW(0, name)
        return hwnd

    @staticmethod
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

    def __init__(self, hwnd: int):
        self.hwnd = hwnd

    def window_to_foreground(self):
        ...

    def minimize_window(self):
        ...

    def restore_window(self):
        ...

    def get_window_rect_from_name(self) -> tuple:
        # hwnd = ctypes.windll.user32.FindWindowW(0, name)
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(self.hwnd, ctypes.pointer(rect))
        return rect.left, rect.top, rect.right, rect.bottom


def test():

    print(WinMgr.get_hwnds_by_pid(15340))


if __name__ == '__main__':
    test()
