import json,time
from datetime import datetime
from Utils.Touch import execute_step
from Utils.AssertAmp import execute_assertion
from Utils.InlayFunction import Slide_main
from Utils.ReadExecel import read_excel_cases
from Utils.ConfigOperate import ConfigOperate
from Utils.Report import Report, write_result_to_excel



def get_config_content(key, section):
    """获取配置内容"""
    try:
        return ConfigOperate().ConfigContent(key=key, section=section)
    except Exception as e:
        print(f"获取配置内容失败: {e}")
        raise

def parse_json_field(case, field_name, logger=None):
    """
    解析测试用例中的JSON字段
    :param case: 测试用例数据字典
    :param field_name: 需要解析的字段名称
    :param logger: 日志记录器对象
    :return: 解析后的列表
    """
    json_str = case.get(field_name, '')
    json_str = json_str.replace("\\", "\\\\")  # 确保反斜杠被正确转义

    try:
        return json.loads(json_str).get('list', [])
    except json.JSONDecodeError as e:
        if logger:
            logger.error(f"JSON 解析错误: {str(e)}, 错误的 JSON 字符串: {repr(json_str)}")
        return []


def execute_test_case(case, logger, template_path, response_content, file_path):
    """
    执行单个测试用例
    :param case: 测试用例数据字典
    :param logger: 日志记录器对象
    :param template_path: 模板路径
    :param file_path: Excel文件路径
    """
    case_id = case.get('ID', '未知ID')
    case_name = case.get('用例名称', '未知名称')
    is_main_process = case.get('是否是主流程')
    time_await = float(case.get('等待时间', '0') or 0)
    home_page = case.get('是否返回首页', '未知名称')

    steps = parse_json_field(case, '步骤', logger=logger)
    assertions = case.get('断言内容')

    logger.info(f'开始执行第 {case_id} 行用例')
    logger.info(f'用例名称: {case_name}')

    start_time = datetime.fromtimestamp(time.time())
    assertion = "断言失败"

    try:
        logger.info('开始执行步骤')
        for step in steps:

            execute_step(step, logger)
        logger.info('步骤执行完毕')

        logger.info(f'开始执行断言: {assertions}')
        assertion = execute_assertion(assertions, logger)
        logger.info(f'断言执行完毕: {assertion}')

        logger.info(f'等待 {time_await} 秒')
        time.sleep(time_await)

        if home_page == '是':
            logger.info('返回首页')
            Slide_main(template_path)
        elif home_page == '否':
            logger.info('不需要执行返回首页函数')
    except Exception as e:
        logger.error(f'用例执行失败: {str(e)}')
        assertion = "断言失败"
        if is_main_process == '是':
            logger.error(f'第 {case_id} 用例报错了，是主流程，停止进程')
            raise
        else:
            logger.error(f'第 {case_id} 用例报错了，但不是主流程，继续执行')
            logger.debug(f'是否是主流程: {is_main_process}')
            return False

    finally:
        total_time_ms = (time.time() - start_time.timestamp()) * 1000  # 总耗时时间（毫秒）
        logger.info(f'总耗时时间: {total_time_ms:.2f} 毫秒')

        write_result_to_excel(case_id, assertion, total_time_ms, response_content, logger)
        logger.info(f'第 {case_id} 用例执行完毕')

        Report(case_id, case_name, assertion, datetime.now(), total_time_ms, logger, file_path)

    return True

def execute_test_cases(response_content, logger):
    """
    执行所有测试用例
    :param response_content: Excel文件路径
    :param logger: 日志记录器对象
    """
    report_file = ConfigOperate().ConfigContent(key="report", section="Path")
    file_path_template = f"{report_file}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    file_path = file_path_template.format(
        thread_id=response_content,
        datetime_str=datetime.now().strftime('%Y%m%d_%H%M%S')
    )
    cases = read_excel_cases(response_content)
    template_path = get_config_content(key="home_page", section="Slide_main")
    for case in cases:
        if not execute_test_case(case, logger, template_path, response_content, file_path):
            break
