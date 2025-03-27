通过另一台电脑远程控制Steam游戏主机的虚拟手柄方案。使用Python + vJoy实现跨网络手柄输入穿透。

## 📌 功能特性

- ✅ 将任意设备（手柄/键盘）输入转发到Steam主机
- ✅ 低延迟网络传输（局域网约10-50ms）
- ✅ 支持最多8轴+128按钮配置
- ✅ 即插即用无需物理数据线

## 🛠️ 先决条件

| 设备          | 要求                                  |
|---------------|--------------------------------------|
| Steam主机     | Windows 10/11, Python 3.9+, vJoy驱动 |
| 客户端电脑    | Windows/Linux, Python 3.9+           |
| 网络          | 建议千兆有线连接                     |

## 📥 安装步骤

### Steam主机（接收端）

1. **安装vJoy驱动**
   ```powershell
   # 下载vJoy 2.1.9
   https://sourceforge.net/projects/vjoystick/files/latest/download

   # 以管理员身份安装，配置：
   # - 按钮数: 8
   # - 启用轴: X/Y/Z Rotation
   ```

2. **设置Python环境**
   ```cmd
   git clone https://github.com/yourusername/remote-controller.git
   cd remote-controller/receiver

   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

### 客户端电脑（发送端）

```bash
git clone https://github.com/yourusername/remote-controller.git
cd remote-controller/sender

# 物理手柄用户
pip install inputs==0.1.0

# 或键盘模拟用户
pip install keyboard==0.13.5
```

## 🚀 使用方法

### 接收端（Steam主机）
```powershell
# 管理员模式运行
.\venv\Scripts\activate
python receiver.py --ip 0.0.0.0 --port 8888
```

### 发送端（客户端）
```python
# 编辑config.ini
[network]
host = 192.168.1.100
port = 8888

# 启动发送程序
python sender.py --config config.ini
```

## 🔧 配置调优

### 调整vJoy参数
![vJoy配置示例](docs/vjoy-config.png)
1. 打开 `Configure vJoy`
2. 根据游戏需求调整轴范围和按钮数量
3. 保存配置后重启接收端程序

### 网络优化
```ini
# config.ini
[performance]
packet_interval = 0.01  # 发送间隔（秒）
buffer_size = 1024      # UDP数据包大小
```

## 🧪 验证配置

1. **vJoy输入测试**
   - 运行 `vJoyMonitor.exe` 查看实时输入信号

2. **Steam控制器检测**
   ```
   Steam > 设置 > 控制器 > 检测到的控制器
   ```

