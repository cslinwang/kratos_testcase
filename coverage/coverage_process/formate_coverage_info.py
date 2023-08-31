# get_coverage_info.py
"""
从覆盖率文件中读取覆盖率信息。

"""
import json
import os
import shutil
from tqdm import tqdm



def get_all_coverage_file_paths(base_path):
    """
    获取所有 coverage.json 文件的路径列表
    """
    coverage_file_paths = []

    for root, _dirs, files in os.walk(base_path):
        for file in files:
            if file == "coverage.json":
                json_path = os.path.join(root, file)
                coverage_file_paths.append(json_path)

    return coverage_file_paths


def read_coverage_json(file_path):
    """
    从 coverage.json 文件中读取覆盖率数据。

    Args:
        file_path (str): coverage.json 文件的路径。

    Returns:
        dict: 包含覆盖率数据的字典。
    """
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            coverage_data = json.load(json_file)
            return coverage_data
    except FileNotFoundError:
        print("找不到 coverage.json 文件。")
        return None
    except Exception as e:
        print("读取 coverage.json 文件时出现错误:", e)
        return None


def extract_coverage_data(base_path):
    """
    从给定路径下的文件中提取 coverage 数据信息。

    Args:
        base_path (str): 要搜索 coverage 文件的基础路径。

    Returns:
        list: 包含处理后 coverage 数据的列表。
    """
    coverage_file_paths = get_all_coverage_file_paths(base_path)
    # coverage_data_list = process_coverage_files(coverage_file_paths)
    return coverage_file_paths


def extract_covered_lines(data):
    """
    从嵌套的 JSON 数据中提取被执行的行号集合。

    Args:
        data (dict): 嵌套的 JSON 数据。

    Returns:
        dict: 包含被执行行号的字典。
    """

    all_lines = set()

    # Iterate through source files
    for source_file, source_data in data['sources'].items():
        # if source_file not start with /root/kratos/ , continue
        if not source_file.startswith('/root/Kratos'):
            continue
        # Get the 'lines' dictionary
        lines = source_data.get("", {}).get("lines", {})

        # Add lines with the required format to the set
        for line in lines.keys():
            formatted_line = f"{source_file}:{line}"
            all_lines.add(formatted_line)

    return all_lines


def process_coverage_files(coverage_file_paths):
    """
    处理所有的 coverage.json 文件。

    Args:
        coverage_file_paths (list): 包含所有 coverage.json 文件路径的列表。

    Returns:
        list: 包含所有覆盖率数据的列表。

    """
    coverage_data_list = []
    for coverage_file_path in tqdm(coverage_file_paths):
        coverage_data = read_coverage_json(coverage_file_path)
        coverage_data = extract_covered_lines(coverage_data)
        if coverage_data is not None:
            print("process:", coverage_file_path)
            coverage_data_list.append(coverage_data)
    return coverage_data_list


def calculate_jaccard_similarity(set1, set2):
    """
    计算两个集合的 Jaccard 相似度。

    Args:
        set1 (set): 第一个集合。
        set2 (set): 第二个集合。

    Returns:
        float: 计算得到的 Jaccard 相似度。
    """
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    jaccard_similarity = intersection / union if union != 0 else 0
    return jaccard_similarity


def calculate_average_jaccard_similarity(list1, list2):
    """Calculate average Jaccard similarities between two lists of sets."""
    jaccard_similarities = []
    for set1 in list1:
        for set2 in list2:
            jaccard_similarity = calculate_jaccard_similarity(set1, set2)
            jaccard_similarities.append(jaccard_similarity)
    return sum(jaccard_similarities) / len(jaccard_similarities) if jaccard_similarities else 0


def calculate_jaccard_matrix(bug_list, normal_list):
    """Calculate Jaccard similarities matrix between bug_list and normal_list."""
    matrix = []
    for i, normal_set in enumerate(normal_list):
        row = []
        for j, bug_set in enumerate(bug_list):
            jaccard_similarity = calculate_jaccard_similarity(
                normal_set, bug_set)
            row.append(jaccard_similarity)
        matrix.append(row)

    return matrix


def delete_coverage_directories(root_path):
    for root, dirs, files in os.walk(root_path, topdown=False):
        for dir_name in dirs:
            if dir_name == "coverage":
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"Deleted 'coverage' directory in {dir_path}")
                except Exception as e:
                    print(
                        f"Error deleting 'coverage' directory in {dir_path}: {e}")


if __name__ == "__main__":

    # 调用函数提取正常用例 coverage 数据
    normal_base_path = "/root/kratos_testcase/coverage/coverage_info"
    normal_coverage_file_paths = extract_coverage_data(
        normal_base_path)

    for file_path in tqdm(normal_coverage_file_paths):
        directory = os.path.dirname(file_path)
        print("process:", file_path)
        delete_coverage_directories(directory)

    bug_base_path = "/root/kratos_testcase/bug_testcase"
    bug_coverage_file_paths = extract_coverage_data(
        bug_base_path)

    for file_path in tqdm(bug_base_path):
        directory = os.path.dirname(file_path)
        print("process:", file_path)
        delete_coverage_directories(directory)
