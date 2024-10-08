import os
import win32gui
import win32api
import win32con
import win32ui

from PIL import Image

windows_title_list = set()
windows_hwnd_dict = dict()
TEMP_IMG_CACHE_PATH = "./resource/temp"

def foo(hwnd, mouse) -> ():
    """
    获取所有窗口标题
    :param hwnd:
    :param mouse:
    :return:
    """
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        windows_title_list.add(win32gui.GetWindowText(hwnd))

def get_all_hwnd(hwnd, mouse) -> {}:
    """
    获取所有窗口句柄
    :param hwnd:
    :param mouse:
    :return:
    """

    print(hwnd, win32gui.GetWindowText(hwnd))
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        windows_hwnd_dict.update({hwnd: win32gui.GetWindowText(hwnd)})


def refresh_windows_hwnd_dict():
    win32gui.EnumWindows(get_all_hwnd, 0)


def get_winows_position(jbid):
    """
    获取目标窗口size
    :param jbid:
    :return:
    """
    left, top, right, bottom = win32gui.GetWindowRect(jbid)
    return left, top, right, bottom


def set_windows_position(hwnd, x_pos, y_pos, x_size, y_size):
    """
    调整目标窗口到坐标(x_pos, y_pos),大小设置为(x_size, y_size)
    :param hwnd:
    :param x_pos:
    :param y_pos:
    :param x_size:
    :param y_size:
    :return:
    """
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x_pos, y_pos, x_size, y_size, win32con.SWP_SHOWWINDOW)

def activate_windows(hwnd):
    """
    将目标窗口放在最前
    :param hwnd:
    :return:
    """
    win32gui.SetForegroundWindow(hwnd)
    show_windows(hwnd, 1)


def show_windows(hwnd, t):
    if t == 1:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    elif t == 2:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)


def get_screenshot(hwnd, w, h):
    """
    截取目标窗口的图片
    :param hwnd:
    :return:
    """
    # Get the window's device context
    hdc_window = win32gui.GetWindowDC(hwnd)
    hdc_mem = win32ui.CreateDCFromHandle(hdc_window)

    # Create a memory device context and a bitmap object
    mem_dc = hdc_mem.CreateCompatibleDC()

    # Create a bitmap object in memory
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(hdc_mem, w, h)
    mem_dc.SelectObject(bmp)

    # Bit block transfer into our memory device context
    mem_dc.BitBlt((0, 0), (w, h), hdc_mem, (0, 0), win32con.SRCCOPY)

    # Convert the bitmap object to a PIL image
    bmp_info = bmp.GetInfo()
    bmp_str = bmp.GetBitmapBits(True)
    screenshot = Image.frombuffer(
        'RGB',
        (bmp_info['bmWidth'], bmp_info['bmHeight']),
        bmp_str, 'raw', 'BGRX', 0, 1
    )
    fn = f"{TEMP_IMG_CACHE_PATH}/jx3Screen.jpg"
    screenshot.save(fn)
    return fn

def set_cursor_pos(x, y):
    win32api.SetCursorPos([x, y])


def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


def right_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)


def test():
    win32gui.EnumWindows(foo, 0)
    lt = [t for t in windows_title_list if t]
    lt.sort()
    for t in lt:
        print(t)

    refresh_windows_hwnd_dict()
    for h, t in windows_hwnd_dict.items():
        if t != "":
            print(h, t)

    print(get_winows_position(132836))

if __name__ == '__main__':
    refresh_windows_hwnd_dict()