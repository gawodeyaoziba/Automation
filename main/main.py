# app.py
from multiprocessing import Process, Queue
from airtest.core.api import connect_device
from Utils.Device import get_connected_devices
from Utils.Log import TaskLoggerManager
from Utils.ConfigOperate import ConfigOperate
from Utils.Steps import execute_test_cases

BASE_LOG_DIR = ConfigOperate().ConfigContent(key="log_path", section="Path")
task_logger = TaskLoggerManager(BASE_LOG_DIR)

def execute_test_steps(device_info, key, queue, section):
    """
    在给定设备上执行测试步骤
    :param device_info: 设备信息字典，包含设备ID和名称
    :param key: 测试步骤的关键字
    :param queue: 多进程队列
    :param section: 配置文件中的章节
    """
    device_id = device_info["Serial"]
    device_name = device_info["Model"]

    # 在子进程中获取设备日志记录器
    logger = task_logger.get_logger(device_id)
    try:
        logger.info(f"尝试连接设备 {device_name} ({device_id})")
        connect_device("Android:///" + device_id)
        logger.info(f"设备 {device_name} ({device_id}) 连接成功，开始执行用例 {key}")

        # 获取对应的文件路径
        file_path = ConfigOperate().ConfigContent(key=key, section=section)  # 确保 section 是字符串
        # 这里调用具体的测试步骤执行函数
        execute_test_cases(response_content=file_path, logger=logger)  # 确保文件路径传递正确

        queue.put((device_name, "成功"))
    except Exception as e:
        logger.error(f"设备 {device_name} ({device_id}) 执行用例 {key} 失败: {str(e)}")
        queue.put((device_name, f"失败: {str(e)}"))

def main(keys, names, sections):
    """
    主函数，负责分配任务并在多个设备上执行测试步骤
    :param keys: 测试步骤的关键字列表
    :param names: 设备名称列表
    :param sections: 配置文件中的章节列表
    """
    devices = get_connected_devices()  # 获取已连接的设备列表

    processes = []
    queue = Queue()
    device_key_pairs = []

    # 为每个设备创建一个 (设备信息, key) 对
    for name, key in zip(names, keys):
        for device in devices:
            if device['Model'] == name:
                device_key_pairs.append((device, key))
                break

    # 为每个设备创建一个进程
    for (device_info, key), section in zip(device_key_pairs, sections):
        process = Process(target=execute_test_steps, args=(device_info, key, queue, section))
        processes.append(process)
        process.start()

    # 等待所有进程执行完毕
    for process in processes:
        process.join()

    results = []
    while not queue.empty():
        device, result = queue.get()
        results.append({'device': device, 'result': result})

    return results

if __name__ == '__main__':
    results1 = main(keys=['Text_CU', 'Text_BC'], names=["V2246", 'V2166A'], sections=["Texe02", 'Texe01'])
    print(results1)
