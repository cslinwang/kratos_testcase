#!/bin/bash

# 示例用法
# ./run_testcase.sh DEMApplication DEM3D_chung_ooi_tests/test1_data/Chung_Ooi_test_1 /root/Kratos/applications/DEMApplication/tests/DEM3D_chung_ooi_tests/test1_data/Chung_Ooi_test_1.py
# ./run_testcase.sh CSharpWrapperApplication run_cpp_unit_tests /root/Kratos/applications/CSharpWrapperApplication/tests/run_cpp_unit_tests.py

# 设置环境变量
export PYTHONPATH=$PYTHONPATH:$HOME/Kratos/bin/Release
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/Kratos/bin/Release/libs

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

# 执行测试命令
echo "正在执行应用 ${application_name} 的测试: $python_script_path"
python3 "$python_script_path"

# 获取当前文件所在目录
# current_directory=$(cd "$(dirname "$0")"; pwd)

echo "current_directory: $current_directory"
# 执行 fastcov 命令，将输出文件保存在当前目录下
cd /root
fastcov --gcov gcov --exclude /usr/include --include /root/Kratos -o "$current_directory/coverage.json"
fastcov --lcov -o "$current_directory/coverage.info"

# 执行 genhtml 命令，将输出文件保存在当前目录下的 coverage 文件夹中
genhtml "$current_directory/coverage.info" --output-directory "$current_directory/coverage"

echo "测试完成，覆盖率报告在 $current_directory/coverage 目录中"
