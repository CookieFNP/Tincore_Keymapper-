# pip install pyvjoystick==1.1.2 keyboard==0.13.5
# 客户发送端

import socket
import keyboard
import math
from pyvjoystick import vjoy

# ======= 配置区 ========
STEAM_PC_IP = "192.168.1.100"  # Steam主机IP
UDP_PORT = 8888
DEADZONE = 0.15  # 摇杆死区过滤

# 键位映射（可自定义）
KEYMAP = {
    # 左摇杆（移动）
    'w': ('axis', 'y', -1.0),
    's': ('axis', 'y', +1.0),
    'a': ('axis', 'x', -1.0),
    'd': ('axis', 'x', +1.0),

    # 右摇杆（视角）
    'i': ('axis', 'rz', -1.0),
    'k': ('axis', 'rz', +1.0),
    'j': ('axis', 'z', -1.0),
    'l': ('axis', 'z', +1.0),

    # 按钮
    'space': 1,  # A
    'shift': 2,  # B
    'ctrl': 3,  # X
    'enter': 4,  # Y

    # 肩键 & 扳机
    'q': ('slider', 0, 255),  # LT
    'e': ('slider', 1, 255),  # RT
    'u': 5,  # LB
    'o': 6  # RB
}


# ======= 核心逻辑 ========
class JoystickState:
    def __init__(self):
        self.axes = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'rz': 0.0}
        self.buttons = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.sliders = {0: 0, 1: 0}

    def _normalize_axis(self, vec_x, vec_y):
        # 向量归一化 + 死区过滤
        length = math.hypot(vec_x, vec_y)
        if length < DEADZONE:
            return 0.0, 0.0
        scale = (length - DEADZONE) / (1.0 - DEADZONE)
        return (vec_x / length) * scale, (vec_y / length) * scale

    def update(self):
        # 处理摇杆输入
        for stick_type in ['left', 'right']:
            vec_x, vec_y = 0.0, 0.0
            axes_map = {'left': ('x', 'y'), 'right': ('z', 'rz')}[stick_type]

            for key in KEYMAP:
                if KEYMAP[key][0] == 'axis' and KEYMAP[key][1] in axes_map:
                    axis_type, axis_name, factor = KEYMAP[key]
                    if keyboard.is_pressed(key):
                        if axis_name == axes_map[0]:
                            vec_x += factor
                        else:
                            vec_y += factor

            # 计算归一化值
            norm_x, norm_y = self._normalize_axis(vec_x, vec_y)
            self.axes[axes_map[0]] = int(norm_x * 32767)
            self.axes[axes_map[1]] = int(norm_y * 32767)

        # 处理按钮/滑块
        for key in KEYMAP:
            if isinstance(KEYMAP[key], int):  # 按钮
                self.buttons[KEYMAP[key]] = 1 if keyboard.is_pressed(key) else 0
            elif KEYMAP[key][0] == 'slider':  # 扳机
                slider_id, value = KEYMAP[key][1], KEYMAP[key][2]
                self.sliders[slider_id] = value if keyboard.is_pressed(key) else 0


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    state = JoystickState()

    print("发送端已启动，使用 WASD 控制移动，IJKL 控制视角...")

    try:
        while True:
            state.update()
            # 数据格式：x,y,z,rz,slider0,slider1,btn1-6
            data = (
                state.axes['x'], state.axes['y'],
                state.axes['z'], state.axes['rz'],
                state.sliders[0], state.sliders[1],
                state.buttons[1], state.buttons[2],
                state.buttons[3], state.buttons[4],
                state.buttons[5], state.buttons[6]
            )
            sock.sendto(str(data).encode(), (STEAM_PC_IP, UDP_PORT))
            keyboard.wait(0.01)
    except KeyboardInterrupt:
        print("\n已终止发送端")


if __name__ == "__main__":
    main()