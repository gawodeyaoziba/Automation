import os
import json
import re

class ConfigOperate:
    CONFIG_FILE_PATH = "../Config/path.json"

    def __init__(self):
        self.config_path = self.ConfigAddress()
        self.data = self.LoadJson()
        # 加载配置文件
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        # 提取映射表
        self.mapping_table = self.config.get('mapping_table', [{}])[0]
        # 编译正则表达式
        self.mapping_regex = re.compile("|".join(re.escape(key) for key in self.mapping_table.keys()))

    def ConfigAddress(self):
        """
        获取json配置地址
        :return: 配置地址（str）
        """
        project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.CONFIG_FILE_PATH)
        return os.path.abspath(project_path)

    def LoadJson(self):
        """
        公共函数打开读取json
        :return: json内容（dict）
        """
        with open(self.config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def SaveJson(self):
        """
        保存json内容
        """
        with open(self.config_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def ConfigContent(self, key, section):
        """
        JSON文件公共获取方式
        :param key: 要获取的键名
        :param section: JSON中的部分 ('Path', 'CU', 'BC' 等)
        :return: 键名对应的值或默认消息
        """
        # 由于每个部分是一个包含字典的列表，访问第一个字典
        section_list = self.data.get(section, [])
        if section_list and isinstance(section_list[0], dict):
            return section_list[0].get(key, "未找到对应的路径")
        return "未找到对应的路径"

    def UpdateConfig(self, section, key, value):
        """
        更新 JSON 配置文件中的内容
        :param section: JSON中的部分 ('Path', 'CU', 'BC' 等)
        :param key: 要更新的键名
        :param value: 新的值
        """
        # 确保 section 是一个列表
        if section not in self.data:
            self.data[section] = [{}]  # 初始化为空字典的列表

        if not isinstance(self.data[section], list):
            return "部分数据格式错误"

        # 更新第一个字典的值
        if self.data[section]:
            self.data[section][0][key] = value
        else:
            self.data[section].append({key: value})

        self.SaveJson()

    def GetAllConfig(self):
        """
        获取所有 JSON 配置内容
        :return: JSON 文件内容（dict）
        """
        return self.data

    def save_config(self):
        """保存配置文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def get_mapping_table(self):
        return self.mapping_table

    def update_mapping_table(self, new_mapping):
        self.mapping_table.update(new_mapping)
        # 更新正则表达式
        self.mapping_regex = re.compile("|".join(re.escape(key) for key in self.mapping_table.keys()))
        self.save_config()

    def delete_mapping(self, section, key_to_delete):
        """
        删除指定 section 中的 key
        :param section: JSON中的部分 ('Path', 'CU', 'BC' 等)
        :param key_to_delete: 要删除的键名
        :return: 是否删除成功
        """
        if section in self.data and isinstance(self.data[section], list):
            section_list = self.data[section]
            if section_list and isinstance(section_list[0], dict):
                if key_to_delete in section_list[0]:
                    del section_list[0][key_to_delete]
                    self.SaveJson()
                    return True
        return False

    def apply_mapping(self, cell_value):
        """对单元格进行映射"""
        if isinstance(cell_value, str):
            try:
                return self.mapping_regex.sub(lambda match: self.mapping_table[match.group(0)], cell_value)
            except Exception as e:
                print(f"映射过程中发生错误: {e}")
                return cell_value
        else:
            return cell_value
