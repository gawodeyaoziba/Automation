from airtest.core.api import touch, text, sleep
from airtest.core.cv import Template

def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        logger = kwargs['logger']
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'{func.__name__} 操作失败: {e}')
    return wrapper

def validate_params(img=None, time_ms=None, frequency=None):
    if img is None:
        raise ValueError('图片路径为空')
    if time_ms is not None and time_ms <= 0:
        raise ValueError('时间必须大于0毫秒')
    if frequency is not None and frequency <= 0:
        raise ValueError('频率必须大于0')

@handle_exceptions
def click(img, logger):
    validate_params(img=img)
    template = Template(img)
    logger.info(f'执行点击操作，图片：{img}')
    touch(template)

@handle_exceptions
def input_text(text_input, logger):
    if not text_input:
        raise ValueError('文本为空')
    logger.info(f'执行输入操作，文本：{text_input}')
    text(text_input)

@handle_exceptions
def long_press(img, time_ms, logger):
    validate_params(img=img, time_ms=time_ms)
    template = Template(img)
    logger.info(f'执行长按操作，图片：{img}，时长：{time_ms}毫秒')
    touch(template, times=1, duration=time_ms / 1000)

@handle_exceptions
def continuous_click(img, frequency, time_ms, logger):
    validate_params(img=img, time_ms=time_ms, frequency=frequency)
    template = Template(img)
    logger.info(f'执行连续点击操作，图片：{img}，频率：{frequency}，间隔时长：{time_ms}毫秒')
    for _ in range(frequency):
        touch(template)
        sleep(time_ms / 1000)

def execute_step(step, logger):
    """
    执行单个步骤
    :param step: 步骤数据字典
    :param logger: 日志记录器
    """
    operate = step.get('operate')
    if not operate:
        logger.error('操作类型为空')
        return

    operations = {
        '点击': lambda: click(step.get('img'), logger=logger),
        '输入': lambda: input_text(step.get('text'), logger=logger),
        '长按': lambda: long_press(step.get('img'), step.get('time', 1000), logger=logger),  # 默认1000毫秒
        '连续点击': lambda: continuous_click(step.get('img'), step.get('frequency', 1), step.get('time', 1000), logger=logger)  # 默认1次点击和1000毫秒
    }

    operation = operations.get(operate)
    if operation:
        operation()
    else:
        logger.error(f'未知的操作类型：{operate}')

"""
step = {
    "operate": "点击",
    "img": "path/to/image.png"
}



step = {
    "operate": "输入",
    "text": "Hello, World!"
}



step = {
    "operate": "长按",
    "img": "path/to/image.png",
    "time": 2000  # 长按2秒
}
step = {
    "operate": "连续点击",
    "img": "path/to/image.png",
    "frequency": 5,  # 点击5次
    "time": 500  # 每次点击间隔500毫秒
}


step = {
    "operate": "未知操作",
    "img": "path/to/image.png"
}
"""