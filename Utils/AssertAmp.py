import json
from airtest.core.api import Template, exists


def image_exists(template):
    """检查图像是否存在"""
    return exists(Template(template))


def check_or(images):
    """处理 'or' 条件"""
    return any(image_exists(img["img"]) for img in images)


def check_and(images):
    """处理 'and' 条件"""
    return all(image_exists(img["img"]) for img in images)


def check_not(images):
    """处理 'not' 条件"""
    return not any(image_exists(img["img"]) for img in images)


def check_single(image):
    """处理单个图像断言"""
    return image_exists(image["img"])


def process_condition(condition_type, images):
    """根据条件类型调用相应的检查函数"""
    condition_checks = {
        "or": check_or,
        "and": check_and,
        "not": check_not
    }
    if condition_type in condition_checks:
        return condition_checks[condition_type](images)
    else:
        raise ValueError(f"未识别的条件类型: {condition_type}")

def parse_json_string(json_str):
    """将 JSON 字符串解析为字典"""
    # 进行必要的转义处理
    json_str = json_str.replace("\\", "\\\\")
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        return {}

def execute_assertion(json_data, logger):
    """根据 JSON 数据中的断言条件检查图像"""

    # 解析 JSON 数据
    if isinstance(json_data, str):
        json_data = parse_json_string(json_data)


    if not isinstance(json_data, dict):
        logger.error("传递的 JSON 数据不是字典类型")
        return "断言失败"



    for condition in json_data.get("list", []):
        for key, value in condition.items():
            if key in ["or", "and", "not"]:
                if not process_condition(key, value):
                    logger.error(f"条件 '{key}' 未满足")
                    return "断言失败"
                logger.info(f"满足 '{key}' 条件")
            elif key == "img":
                if not check_single(value[0]):  # Assuming 'img' key contains a list
                    logger.error(f"未找到普通断言图像: {value[0]['img']}")
                    return "断言失败"
                logger.info(f"满足普通断言: {value[0]['img']}")
            else:
                logger.error(f"未识别的条件键: {key}")
                raise ValueError(f"未识别的条件键: {key}")

    return "断言成功"
"""
{
    "list": [
        {
            "or": [
                {
                    "img": "xx\\登入.png"
                }, {
                    "img": "xx\\登入.png"
                }
            ]
        }
    ]
}
{
    "list": [
        {
            "or": [
                {
                    "img": "xx\\登入.png"
                }
            ]
        }
    ]
}


{
    "list": [
        {
            "and": [
                {
                    "img": "xx\\登入.png"
                }, {
                    "img": "xx\\登入.png"
                }
            ]
        }
    ]
}

{
    "list": [
        {
            "img": [
                {
                    "img": "xx\\登入.png"
                }
            ]
        }
    ]
}

{
    "list": [
        {
            "not": [
                {
                    "img": "xx\\登入.png"
                },{
                    "img": "xx\\登入.png"
                }
            ]
        }
    ]
}
{
    "list": [
        {
            "not": [
                {
                    "img": "xx\\登入.png"
                }
            ]
        }
    ]
}

"""