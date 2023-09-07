"""
计算可疑度

1. 读取101个info文件

2. 遍历这些文件，获取101个文件共同的行，得到代码执行次数矩阵

    | 行号 | bug 执行次数 | normal1 执行次数 | normal2 执行次数 | ... | normal100 执行次数 |
    | 1   | 1           | 0               | 2               | ... | 0                  |

3. 统计以下4个度量
    a: 在失败的测试用例中执行的次数。
    b: 在成功的测试用例中执行的次数。
    c: 在失败的测试用例中未执行的次数。
    d: 在成功的测试用例中未执行的次数。

4. 应用可疑度计算公式，得到每一行的可疑度

5. 根据可疑度对代码行进行排序，得到top50的代码行

6. 保存top50的代码行到文件中

"""

from get_coverage_info import *
from tqdm import tqdm
import time
import csv
import pandas as pd
import os
import numpy as np
import subprocess

# 覆盖率文件路径
BUG_COVERAGE_FILE_PATH = "/root/kratos_testcase/bug_testcase"
NORMAL_COVERAGE_FILE_PATH = "/root/coverage_info"


def run_command(command):
    """
    运行命令
    """
    process = subprocess.Popen(command, shell=True)
    process.wait()


def prepare_data():
    """
    数据准备
    数据准备，解压覆盖率文件到指定目录
    解压数据
    tar -I pigz -xvf /root/kratos_6_coverage_info.tar.gz -C /root/coverage_info_all/kratos_6_coverage_info
    tar -I pigz -xvf /root/kratos_7.1_coverage_info.tar.gz -C /root/coverage_info_all/kratos_7.1_coverage_info
    tar -I pigz -xvf /root/kratos_8.1_coverage_info.tar.gz -C /root/coverage_info_all/kratos_8.1_coverage_info
    tar -I pigz -xvf /root/kratos_9.3.2_coverage_info.tar.gz -C /root/coverage_info_all/kratos_9.3.2_coverage_info

    :return:
    """
    # 构建目录
    run_command("mkdir -p /root/coverage_info_all/kratos_6_coverage_info")
    run_command("mkdir -p /root/coverage_info_all/kratos_7.1_coverage_info")
    run_command("mkdir -p /root/coverage_info_all/kratos_8.1_coverage_info")
    run_command("mkdir -p /root/coverage_info_all/kratos_9.3.2_coverage_info")

    # 解压数据
    run_command(
        "tar -I pigz -xvf /root/kratos_6_coverage_info.tar.gz -C /root/coverage_info_all/kratos_6_coverage_info")
    run_command(
        "tar -I pigz -xvf /root/kratos_7.1_coverage_info.tar.gz -C /root/coverage_info_all/kratos_7.1_coverage_info")
    run_command(
        "tar -I pigz -xvf /root/kratos_8.1_coverage_info.tar.gz -C /root/coverage_info_all/kratos_8.1_coverage_info")
    run_command(
        "tar -I pigz -xvf /root/kratos_9.3.2_coverage_info.tar.gz -C /root/coverage_info_all/kratos_9.3.2_coverage_info")

    pass


def get_bug_coverage_file_path():
    """
    获取bug覆盖率文件路径
    :return:
    """
    return BUG_COVERAGE_FILE_PATH


def convert_coverage_data(coverage_data_list):
    """
    转换覆盖率数据格式,转换为map
    key:文件路径
    :param coverage_data_list:
    :return: coverage_data_matrix
    """
    # 构建维空数组
    x_size = len(coverage_data_list)
    y_size = len(coverage_data_list[0])
    coverage_data_matrix = np.empty((x_size, y_size, 3), dtype=int)
    for coverage_data in coverage_data_list:
        coverage_data_matrix.append(coverage_data)
    return coverage_data_matrix


def read_coverage_info(filename):
    coverage_data = {}
    current_file = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()

            # Test name
            if line.startswith("TN:"):
                continue  # In this example, we ignore the test name

            # Source file
            if line.startswith("SF:"):
                current_file = line.split(":")[1]
                coverage_data[current_file] = {
                    'functions': {},
                    'lines': {},
                    'FNF': 0,
                    'FNH': 0,
                    'LF': 0,
                    'LH': 0,
                }
                continue

            # Functions
            if line.startswith("FN:"):
                line = line.replace("FN:", "")
                func_line, func_name = line.split(',')
                coverage_data[current_file]['functions'][func_name] = {
                    'line': func_line, 'count': 0}
                continue

            if line.startswith("FNDA:"):
                line = line.replace("FNDA:", "")
                count, func_name = line.split(',')
                if func_name in coverage_data[current_file]['functions']:
                    coverage_data[current_file]['functions'][func_name]['count'] = int(
                        count)
                continue

            # Summary metrics
            if line.startswith("FNF:") or line.startswith("FNH:") or line.startswith("LF:") or line.startswith("LH:"):
                key, value = line.split(":")
                coverage_data[current_file][key] = int(value)
                continue

            # Data lines
            if line.startswith("DA:"):
                line = line.replace("DA:", "")
                line_number, count = line.split(',')
                coverage_data[current_file]['lines'][int(
                    line_number)] = int(count)

    return coverage_data


def get_all_coverage_file_paths(base_path):
    """
    获取所有 coverage.json 文件的路径列表
    """
    coverage_file_paths = []

    for root, _dirs, files in os.walk(base_path):
        for file in files:
            if file == "coverage.info":
                json_path = os.path.join(root, file)
                coverage_file_paths.append(json_path)

    return coverage_file_paths


def save_coverage_to_csv(coverage_data, output_filename='function_coverage.csv'):
    """
    将代码覆盖率数据保存到 CSV 文件中。

    参数:
        coverage_data (dict): 通过 read_coverage_info 函数获取的覆盖率数据。
        output_filename (str): 输出 CSV 文件的名称。

    返回:
        None
    """

    # 打开 CSV 文件并写入数据
    with open(output_filename, 'w', newline='') as f:
        writer = csv.writer(f)

        # 写入标题
        writer.writerow(["File", "Function", "Line", "Count"])

        # 遍历覆盖率数据并写入到 CSV 文件
        for file, data in coverage_data.items():
            for func, func_data in data['functions'].items():
                writer.writerow(
                    [file, func, func_data['line'], func_data['count']])


def load_coverage_from_csv(input_filename='function_coverage.csv'):
    """
    从CSV文件中加载代码覆盖率数据。

    参数:
        input_filename (str): 输入CSV文件的名称。

    返回:
        dict: 还原的覆盖率数据。
    """

    # 初始化空字典用于存储还原的覆盖率数据
    coverage_data = {}

    # 打开CSV文件并读取数据
    with open(input_filename, 'r', newline='') as f:
        reader = csv.reader(f)

        # 跳过标题行
        next(reader)

        # 逐行读取并存储数据
        for row in reader:
            file, func, line, count = row

            # 如果文件名不在字典中，则添加一个新条目
            if file not in coverage_data:
                coverage_data[file] = {
                    'functions': {},
                    'lines': {},
                    'FNF': 0,
                    'FNH': 0,
                    'LF': 0,
                    'LH': 0,
                }

            # 存储函数覆盖率数据
            coverage_data[file]['functions'][func] = {
                'line': int(line), 'count': int(count)}

    return coverage_data


def get_function_count_matrix(function_count_matrix_map, bug_coverage_data, normal_coverage_data, bug_file_name, normal_file_name):
    """
    获取 bug 和 normal 用例之间的对应函数的执行次数矩阵。
    参数：
        function_count_matrix_map (dict): 包含每个函数的行数矩阵的字典
        bug_coverage_data (dict): bug 用例的覆盖率数据
        normal_coverage_data (dict): normal 用例的覆盖率数据
        bug_file_name (str): bug 用例的文件名
        normal_file_name (str): normal 用例的文件名
    返回：
        function_count_matrix_map (dict): 包含每个函数的行数矩阵的字典
    """
    # Iterate through each file in bug_coverage_data
    for bug_file, bug_file_data in bug_coverage_data.items():
        # Check if the same file exists in normal_coverage_data
        if bug_file in normal_coverage_data:
            normal_file_data = normal_coverage_data[bug_file]
            # Iterate through each function in the file
            for bug_function, bug_function_data in bug_file_data['functions'].items():
                if bug_function not in function_count_matrix_map:
                    file_count_map = {}
                    file_count_map[bug_file_name] = bug_function_data['count']
                else:
                    file_count_map = function_count_matrix_map[bug_function]
                # Check if the same function exists in normal_file_data
                if bug_function in normal_file_data['functions']:
                    normal_function_data = normal_file_data['functions'][bug_function]
                    file_count_map[normal_file_name] = normal_function_data['count']
                    function_count_matrix_map[bug_function] = file_count_map

    return function_count_matrix_map


def get_coverage_data(base_path, res_save_path, coverage_subfolder="coverage_res"):
    """
    获取覆盖率数据
    参数：
        base_path (str): 覆盖率文件的基础路径
        res_save_path (str): 保存结果的路径
        coverage_subfolder (str): 保存覆盖率数据的子文件夹名，默认为 "coverage_res"
    返回：
        coverage_data_map (dict): 包含所有覆盖率数据的字典
    """
    if not os.path.exists(res_save_path):
        os.mkdir(res_save_path)

    # Initialize an empty dictionary to store the coverage data
    coverage_data_map = {}

    # Get all coverage file paths
    coverage_file_paths = get_all_coverage_file_paths(base_path)

    counter = 0

    for coverage_file_path in tqdm(coverage_file_paths):
        # 方便测试，早期只取前5个
        # counter += 1
        # if counter > 5:
        #     break
        # 如果是bug_testcase文件夹，那么将文件名作为key
        if coverage_file_path.split("/")[-2].isdigit():
            coverage_file_name = coverage_file_path.split("/")[-2]
        else:
            coverage_file_name = coverage_file_path.split("/")
            coverage_file_name = coverage_file_name[-3] + \
                "_"+coverage_file_name[-2]

        # Construct the save path
        coverage_data_save_path = os.path.join(
            res_save_path, coverage_subfolder)

        # Create the directory if it does not exist
        if not os.path.exists(coverage_data_save_path):
            os.mkdir(coverage_data_save_path)

        # Create the save file name
        coverage_data_save_name = coverage_file_name + "_coverage.csv"
        coverage_data_save_path = os.path.join(
            coverage_data_save_path, coverage_data_save_name)

        # If the file already exists, load the data
        if os.path.exists(coverage_data_save_path):
            coverage_data = load_coverage_from_csv(coverage_data_save_path)
        else:
            # Otherwise, read the original file and save the data
            coverage_data = read_coverage_info(coverage_file_path)
            save_coverage_to_csv(coverage_data, coverage_data_save_path)

        # Add the coverage data to the map
        coverage_data_map[coverage_file_name] = coverage_data

    return coverage_data_map


def get_jaccard_matrix(bug_base_path, normal_base_path, bug_file_name):

    # 调用函数提取 bug coverage 数据
    bug_coverage_file_paths, bug_coverage_data_list = extract_coverage_data(
        bug_base_path)

    # 仅保留当前bug的覆盖率数据
    for bug_index, bug_coverage_file_path in enumerate(bug_coverage_file_paths):
        if bug_coverage_file_path.split("/")[-2] == bug_file_name:
            bug_coverage_file_paths = bug_coverage_file_paths[bug_index]
            bug_coverage_data_list = bug_coverage_data_list[bug_index]
            break

    # 调用函数提取正常用例 coverage 数据
    normal_coverage_file_paths, normal_coverage_data_list = extract_coverage_data(
        normal_base_path)

    # 计算 Jaccard 相似度矩阵
    jaccard_matrix = calculate_jaccard_matrix(
        bug_coverage_data_list, normal_coverage_data_list)

    return jaccard_matrix


def pre():
    if not os.path.exists(RES_SAVE_PATH):
        os.mkdir(RES_SAVE_PATH)
    if not os.path.exists(FUNCTION_RES_SAVE_PATH):
        os.mkdir(FUNCTION_RES_SAVE_PATH)


def run():
    '''
    主函数
    '''
    pre()
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
    # 获取所有的bug覆盖率
    bug_coverage_data_map = get_coverage_data(
        BUG_BASE_PATH, RES_SAVE_PATH, "bug_coverage_res")
    # 获取所有的normal覆盖率
    normal_coverage_data_map_v6 = get_coverage_data(
        NORMAL_BASE_PATH_V6, RES_SAVE_PATH, "normal_coverage_res_v6")
    normal_coverage_data_map_v7 = get_coverage_data(
        NORMAL_BASE_PATH_V7, RES_SAVE_PATH, "normal_coverage_res_v7")
    normal_coverage_data_map_v8 = get_coverage_data(
        NORMAL_BASE_PATH_V8, RES_SAVE_PATH, "normal_coverage_res_v8")
    normal_coverage_data_map_v9 = get_coverage_data(
        NORMAL_BASE_PATH_V9, RES_SAVE_PATH, "normal_coverage_res_v9")

    # 读取相似度矩阵
    jaccard_matrix = pd.read_excel(os.path.join(
        CURRENT_PATH, "Kratos_jaccard_similarity_top100.xlsx"), index_col=1)
    # 获取相似度矩阵的行，获取第11307行的数据list

    for bug_file, bug_data in bug_coverage_data_map.items():
        # 处理每一个bug测试用例
        bug_version = BUG_VERSION[int(bug_file)]
        normal_coverage_data_map = eval(
            "normal_coverage_data_map_v"+bug_version[0:1])

        # 获取前100个相似度最高的用例
        if not os.path.exists(os.path.join(CURRENT_PATH, bug_file+"_top100.xlsx")):
            continue
        normal_testcase_names = pd.read_excel(os.path.join(
            CURRENT_PATH, bug_file+"_top100.xlsx"), index_col=0)
        # 可以在这儿设置top多少
        normal_testcase_names = normal_testcase_names.index.tolist()[0:100]

        # 开始构建可疑度矩阵
        function_count_matrix_map = {}
        count = 0
        for normal_file, normal_data in normal_coverage_data_map.items():
            if normal_file in normal_testcase_names:
                count += 1
                function_count_matrix_map = get_function_count_matrix(function_count_matrix_map,
                                                                      bug_data, normal_data, bug_file, normal_file)
        # 如果不是100个用例，那么就报错退出
        if count != 100:
            print("normal_testcase_names的长度不为100，程序退出")
            # exit(1)
        # 保存可疑度矩阵
        function_count_matrix_map = pd.DataFrame.from_dict(
            function_count_matrix_map, orient='index')
        function_count_matrix_map.to_excel(os.path.join(
            FUNCTION_RES_SAVE_PATH, bug_file+"_function_count_matrix_map.xlsx"))


# V9.3.2：11307、11231、10805、10649、10553、9818
# V8.1：9079
# V7.1：5458、4896
# V6：4623、3442
BUG_VERSION = {11307: "9.3.2", 11231: "9.3.2", 10805: "9.3.2", 10649: "9.3.2", 10553: "9.3.2", 9818: "9.3.2",
               9079: "8.1", 5458: "7.1", 4896: "7.1", 4623: "6", 3442: "6"}
NORMAL_BASE_PATH_V6 = "/root/coverage_info_all/kratos_6_coverage_info"
NORMAL_BASE_PATH_V7 = "/root/coverage_info_all/kratos_7.1_coverage_info"
NORMAL_BASE_PATH_V8 = "/root/coverage_info_all/kratos_8.1_coverage_info"
NORMAL_BASE_PATH_V9 = "/root/coverage_info_all/kratos_9.3.2_coverage_info"
BUG_BASE_PATH = "/root/kratos_testcase/bug_testcase"
RES_SAVE_PATH = "/root/kratos_testcase/coverage/coverage_process/coverage_res"
FUNCTION_RES_SAVE_PATH = "/root/kratos_testcase/coverage/coverage_process/function_res"


if __name__ == "__main__":
    # 数据准备，解压数据，仅运行一次
    # prepare_data()
    start_time = time.time()
    run()
    end = time.time()
    print("读取bug覆盖率数据耗时：", end - start_time)
