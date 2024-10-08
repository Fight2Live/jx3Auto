import time
import threading
import config.global_var as gv

from utils import windows_operate, images_identify

SLEEP_TIME = 1830

class JX3Operate(threading.Thread):
    def __init__(self, hwnd, task_type):
        super().__init__()
        self.hwnd = hwnd
        self.task_type = task_type

    def run(self) -> None:
        if self.task_type == 1:
            self.start_art()

    def start_art(self):
        # windows_operate.activate_windows(hwnd)
        windows_operate.show_windows(self.hwnd, 1)
        time.sleep(0.5)
        # 设置窗口大小
        windows_operate.set_windows_position(self.hwnd, 100, 100, 1339, 782)
        left, top, right, bot = windows_operate.get_winows_position(self.hwnd)
        w, h = right - left, bot - top
        # todo 检查是否已开启艺人

        # todo 若没有则自动开启

        # 获取艺人技能的位置
        windows_operate.set_cursor_pos(500, 500)
        time.sleep(1.5)
        windows_screen_path = windows_operate.get_screenshot(self.hwnd, w, h)
        target_pos = images_identify.get_target_position(windows_screen_path)
        if target_pos[0] == 0 and target_pos[1] == 0:
            return

        windows_operate.set_cursor_pos(target_pos[0] + left, target_pos[1] + top)
        time.sleep(0.5)
        # 点击并最小化
        windows_operate.left_click()
        time.sleep(0.5)
        windows_operate.left_click()
        time.sleep(0.5)
        windows_operate.show_windows(self.hwnd, 2)

        # 休眠
        st = 0
        while gv.get_value("EXECUTING") and st < SLEEP_TIME:
            time.sleep(1)
            st += 1

        # 结束
        if not gv.get_value("EXECUTING"):
            return

        self.start_art()

if __name__ == '__main__':
    t = JX3Operate(1000, 1)
    t.start()
