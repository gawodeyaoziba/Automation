
import openpyxl
from Utils.ConfigOperate import ConfigOperate
import os

# 示例使用：读取 .xlsx 文件中的测试用例数据
def read_excel_cases(file_path, start_row=2, end_row=None):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 {file_path} 不存在")

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    if end_row is None:
        end_row = sheet.max_row

    headers = [cell.value for cell in sheet[1]]
    test_cases = []
    for row_num in range(start_row, end_row + 1):
        row_data = {}
        for col_num, cell in enumerate(sheet[row_num]):
            header = headers[col_num]
            row_data[header] = ConfigOperate().apply_mapping(cell.value)
        test_cases.append(row_data)
    return test_cases


# 示例使用
if __name__ == "__main__":
    response_content = ConfigOperate().ConfigContent(key="Text_CU", section="Texe02")
    cases = read_excel_cases(response_content)
    print(response_content)
    for case in cases:
        print(case)
        # 输出解析后的内容
        # for key, value in case.items():
        #     print(f"{key}: {value}")
