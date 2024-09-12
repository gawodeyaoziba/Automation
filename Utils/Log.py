import logging
import os
from datetime import datetime


class LoggerFactory:
    """日志记录器工厂"""

    @staticmethod
    def create_logger(name, log_dir):
        """创建日志记录器"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)  # 设置记录器级别为 DEBUG

        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_levels = ['info', 'debug', 'error', 'critical', 'warning']
        for lvl in log_levels:
            handler = logging.FileHandler(os.path.join(log_dir, f"{lvl}.log"), mode='a')
            handler.setLevel(getattr(logging, lvl.upper()))
            handler.setFormatter(log_format)

            # 添加过滤器，只处理特定级别的日志消息
            handler.addFilter(LevelFilter(lvl.upper()))

            logger.addHandler(handler)

        return logger


class LevelFilter(logging.Filter):
    """自定义日志过滤器，只允许指定级别的日志通过"""

    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == getattr(logging, self.level.upper())


def create_log_dir(base_dir, task_name=None):
    """创建日志目录，支持主/次日志文件夹路径生成"""
    if task_name:
        date_str = datetime.now().strftime('%Y-%m-%d')
        log_dir = os.path.join(base_dir, date_str, task_name)
    else:
        log_dir = base_dir

    os.makedirs(log_dir, exist_ok=True)
    return log_dir


class TaskLoggerManager:
    def __init__(self, base_log_dir):
        self.base_log_dir = base_log_dir
        self.loggers = {}

    def get_logger(self, task_name):
        if task_name not in self.loggers:
            log_dir = create_log_dir(self.base_log_dir, task_name)
            self.loggers[task_name] = LoggerFactory.create_logger(task_name, log_dir)
        return self.loggers[task_name]

from Utils.ConfigOperate import ConfigOperate
BASE_LOG_DIR = ConfigOperate().ConfigContent(key="log_path", section="Path")
task_logger = TaskLoggerManager(BASE_LOG_DIR)

# 创建全局的任务日志记录管理器实例
# task_logger = TaskLoggerManager(BASE_LOG_DIR)

# # 示例使用
# if __name__ == "__main__":
#     # 动态创建和使用设备日志记录器
#     devices = ["device1", "device2", "device3"]
#     print(devices)
#     for device in devices:
#         # 获取设备级别日志记录器
#         device_logger = task_logger.get_logger(device)
#
#         def x1():
#             """其他代码，这个函数也可能在其他文件"""
#             device_logger.info(f"这是设备'{device}'的一条信息日志")
#             device_logger.debug(f"这是设备'{device}'的一条调试日志")
#             device_logger.error(f"这是设备'{device}'的一条错误日志")
#
#         # 调用函数记录日志
#         x1()

