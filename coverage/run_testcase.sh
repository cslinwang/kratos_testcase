#!/bin/bash

# 示例用法
# ./run_testcase.sh DEMApplication DEM3D_chung_ooi_tests/test1_data/Chung_Ooi_test_1 /root/Kratos/applications/DEMApplication/tests/DEM3D_chung_ooi_tests/test1_data/Chung_Ooi_test_1.py
# ./run_testcase.sh CSharpWrapperApplication run_cpp_unit_tests /root/Kratos/applications/CSharpWrapperApplication/tests/run_cpp_unit_tests.py

# 设置环境变量
# v6
export PYTHONPATH=$PYTHONPATH:/root/Kratos
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/Kratos/libs
export LD_LIBRARY_PATH=/root/Kratos/bin/Release/libs:$LD_LIBRARY_PATH

# 检查是否提供了三个输入参数

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo "请提供应用名称、测试用例名称和要执行的Python脚本的路径。"
  exit 1
fi

# 提取输入参数
application_name="$1"
test_case_name="$2"
python_script_path="$3"

# 删除之前的覆盖率信息
echo "删除之前的覆盖率信息"
lcov --directory /root/Kratos/ --zerocounters

current_directory="/root"
# 创建覆盖率信息保存的目录结构
coverage_dir="$current_directory/coverage_info/$application_name/$test_case_name"
mkdir -p "$coverage_dir"
# 获取当前文件所在目录
current_directory="$coverage_dir"

echo "current_directory: $current_directory"

# 如果存在覆盖率信息，则跳过
if [ -f "$current_directory/coverage.info" ]; then
  echo "覆盖率信息已存在，跳过测试"
  exit 0
fi

# 执行测试命令
echo "正在执行应用 ${application_name} 的测试: $python_script_path"
cd /root/Kratos/applications/"$application_name"/tests
# python3 "$python_script_path"
# 生成python覆盖率，如果不存在，创建
PYTHON_COVERAGE_PATH="$current_directory/python"
if [ ! -d "$PYTHON_COVERAGE_PATH" ]; then
  mkdir -p "$PYTHON_COVERAGE_PATH"
fi
# 清除覆盖率数据
coverage erase

coverage run --source=/root/Kratos/ "$python_script_path"

# 生成文本覆盖率报告
coverage report -m

# 创建HTML覆盖率报告
coverage html -d ${PYTHON_COVERAGE_PATH}

# 创建JSON覆盖率报告
coverage json -o ${PYTHON_COVERAGE_PATH}/coverage.json

# 创建XML覆盖率报告
coverage xml -o ${PYTHON_COVERAGE_PATH}/coverage.xml

# 执行 fastcov 命令，将输出文件保存在当前目录下
cd /root
fastcov --gcov gcov --exclude /usr/include --include /root/Kratos -o "$current_directory/coverage.json"
fastcov --lcov -o "$current_directory/coverage.info"

# 执行 genhtml 命令，将输出文件保存在当前目录下的 coverage 文件夹中
# genhtml "$current_directory/coverage.info" --output-directory "$current_directory/coverage"

echo "测试完成，覆盖率报告在 $current_directory 目录中"
