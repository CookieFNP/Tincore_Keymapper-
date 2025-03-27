通过另一台电脑远程控制 Steam 主机的专业虚拟手柄方案，基于 **vJoy 驱动**实现低延迟键鼠/手柄到虚拟设备的转换，完美兼容 Steam 平台游戏。


## ✨ 核心功能
- 🕹️ **全按键支持**：映射 Xbox 标准按钮（ABXY/肩键/扳机/摇杆）
- 🌐 **跨网络传输**：局域网 UDP 通信（延迟 <50ms）
- 🔧 **即插即用**：自动识别 vJoy 虚拟设备
- 🎮 **双输入模式**：支持键盘和物理手柄作为控制源

## 🛠️ 系统要求
| 设备            | 最低配置                  |
|-----------------|--------------------------|
| Steam 主机      | Windows 10/11，Python 3.9+ |
| 客户端设备      | Windows/Linux/macOS，Python 3.9+ |
| 网络环境        | 局域网（建议千兆有线连接）|

---

## 📥 完整部署流程

### 第一阶段：Steam 主机设置（接收端）

#### 1. 安装 vJoy 驱动
1. 访问 [vJoy 官网](https://sourceforge.net/projects/vjoystick/)
2. 下载最新安装包（选择 `vJoy 2.1.9`）
3. 右键以管理员身份运行安装程序：
   - 勾选所有组件（**必须包含 Feeder**）
   - 完成安装后重启系统

#### 2. 配置虚拟手柄
1. 打开开始菜单 → 搜索 `Configure vJoy`
2. 进行设备设置：
   - 设备编号：`1`
   - 按钮数量：`10`
   - 启用轴：X/Y/Z/Rx/Ry/Rz
   - 点击 Apply 确认配置
![60866019bad7808fe2b12355377560e2](https://github.com/user-attachments/assets/2a039b15-54e3-4d29-a377-2437705c8b90)



#### 3. 验证驱动状态
1. 右键开始菜单 → 设备管理器
2. 展开 `人体学输入设备` → 确认存在 `vJoy Device`
![aac90150245e5debfd33c405eee4ccd5](https://github.com/user-attachments/assets/7ca7fc17-db87-4c0a-9947-0d11f3113cbf)


### 第二阶段：客户端设置（控制端）

#### 1. 准备 Python 环境
```bash
# Windows 用户
python -m venv gamepad-env
gamepad-env\Scripts\activate

# Linux/macOS 用户
python3 -m venv gamepad-env
source gamepad-env/bin/activate
```

#### 2. 安装依赖库
```bash
pip install pyvjoystick==1.1.2 keyboard==0.13.5
```

#### 3. 配置网络参数
1. 在客户端电脑上打开 `config.ini` 文件
2. 修改目标主机 IP：
```ini
[network]
host = 192.168.1.100  # 替换为 Steam 主机的实际 IP
port = 8888
```

---

## 🕹️ 使用指南

### 启动服务端（Steam 主机）
1. 以管理员身份打开 PowerShell/CMD
2. 进入项目目录执行：
```powershell
.\gamepad-env\Scripts\activate
python receiver.py
```

### 启动客户端（控制设备）
1. 在客户端设备打开终端
2. 进入项目目录执行：
```bash
python sender.py
```

### 默认控制方案
| 按键       | 功能        | 类型       |
|------------|-------------|------------|
| W/A/S/D    | 左摇杆移动  | 模拟输入   |
| I/J/K/L    | 右摇杆视角  | 模拟输入   |
| Q/E        | LT/RT 扳机  | 压力感应   |
| U/O        | LB/RB 肩键  | 数字按钮   |
| Space      | A 按钮      | 动作确认   |
| Shift      | B 按钮      | 取消/返回  |

---



## 🚨 常见问题解决

| 问题现象                  | 解决方案                     |
|--------------------------|----------------------------|
| Steam 检测不到虚拟设备    | 1. 重新安装 vJoy 驱动<br>2. 以管理员身份运行接收端 |
| 按键响应延迟明显          | 1. 检查网络 ping 值<br>2. 关闭防火墙/UDP 8888 放行 |
| 斜向移动速度异常          | 修改发送端 `deadzone` 参数（0.1-0.3） |
| 部分按钮无响应            | 检查 vJoy 配置的按钮数量是否足够 |

---

## 📄 协议声明
本项目采用 MIT 开源协议，允许商业使用和二次开发，但需保留原始版权声明。硬件兼容性测试数据基于 Xbox 标准手柄协议生成。

