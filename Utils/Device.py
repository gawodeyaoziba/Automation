import subprocess
from Utils.ConfigOperate import ConfigOperate

def run_adb_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return ""

def get_device_info(adb_path: str, device_serial: str) -> dict:
    """
    获取单个设备的详细信息

    Args:
        adb_path (str): adb路径
        device_serial (str): 设备序列号

    Returns:
        dict: 设备信息，包括型号、品牌名称、Android 版本和序列号
    """
    brand = run_adb_command([adb_path, "-s", device_serial, "shell", "getprop", "ro.product.brand"])
    model = run_adb_command([adb_path, "-s", device_serial, "shell", "getprop", "ro.product.model"])
    android_version = run_adb_command([adb_path, "-s", device_serial, "shell", "getprop", "ro.build.version.release"])

    return {
        "Serial": device_serial,
        "Brand": brand,
        "Model": model,
        "Android": android_version
    }

def get_connected_devices() -> list:
    """
    获取连接的设备详细信息列表

    Returns:
        list: 连接的设备详细信息列表
    """
    try:
        adb_path = ConfigOperate().ConfigContent("adb_path", 'Path')
        if not adb_path:
            print("ADB路径未配置或无效")
            return []

        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True, check=True)
        device_lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
        devices = [line.split('\t')[0] for line in device_lines if 'device' in line]

        device_info_list = []
        for device_serial in devices:
            device_info = get_device_info(adb_path, device_serial)
            device_info_list.append(device_info)

        return device_info_list
    except subprocess.CalledProcessError as e:
        print(f"获取设备列表失败: {e}")
        return []

if __name__ == '__main__':
    try:
        devices_info = get_connected_devices()
        print(devices_info)
    except Exception as e:
        print(f"读取配置或获取设备时发生错误: {e}")
