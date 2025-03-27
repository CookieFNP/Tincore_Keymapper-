# pip install pyvjoy==0.1.4 pywin32==306
# 主机接收端

import socket
import pyvjoy

# ======= vJoy配置 ========
DEVICE_ID = 1  # 必须与Configure vJoy中的设备号一致
AXIS_MAP = {
    'x': pyvjoy.HID_USAGE_X,
    'y': pyvjoy.HID_USAGE_Y,
    'z': pyvjoy.HID_USAGE_Z,
    'rz': pyvjoy.HID_USAGE_RZ
}

# ======= 初始化 ========
joy = pyvjoy.VJoyDevice(DEVICE_ID)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 8888))

print("等待客户端连接...")


def update_device(data: tuple):
    """更新vJoy设备状态"""
    # 数据解析：x,y,z,rz,slider0,slider1,btn1-6
    x, y, z, rz, lt, rt, a, b, x_btn, y_btn, lb, rb = map(int, data)

    # 更新轴
    joy.set_axis(AXIS_MAP['x'], x + 32768)  # vJoy轴范围为0-65535
    joy.set_axis(AXIS_MAP['y'], y + 32768)
    joy.set_axis(AXIS_MAP['z'], z + 32768)
    joy.set_axis(AXIS_MAP['rz'], rz + 32768)

    # 更新滑块（LT/RT）
    joy.set_axis(pyvjoy.HID_USAGE_SL0, lt * 257)  # 0-255 → 0-65535
    joy.set_axis(pyvjoy.HID_USAGE_SL1, rt * 257)

    # 更新按钮
    joy.set_button(1, a)
    joy.set_button(2, b)
    joy.set_button(3, x_btn)
    joy.set_button(4, y_btn)
    joy.set_button(5, lb)
    joy.set_button(6, rb)


while True:
    data, addr = sock.recvfrom(1024)
    try:
        raw = data.decode().strip('()').split(',')
        update_device(raw)
    except Exception as e:
        print(f"数据解析错误: {e}")