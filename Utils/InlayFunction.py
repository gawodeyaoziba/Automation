from airtest.core.api import *

# 定义右滑动并点击图片的函数
def Slide_main(template_path, max_swipes=10):
    for _ in range(max_swipes):
        if exists(Template(template_path)):
            print("Image found!")
            touch(Template(template_path))  # 点击找到的图片
            return True
        else:
            # 执行右滑动
            swipe([900, 500], [100, 500], duration=0.5)
            sleep(1)  # 等待滑动动画完成

    print("Image not found after max swipes.")
    return False
