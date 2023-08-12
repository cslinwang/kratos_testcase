#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/5458

# 预期报错：
# ModuleNotFoundError: No module named 'swimming_DEM_procedures'

# 运行文件
# /root/Kratos/applications/SwimmingDEMApplication/tests/SmallTests.py

# 新版

# 环境变量

# export PYTHONPATH=$PYTHONPATH:/root/Kratos/bin/Release
# export LD_LIBRARY_PATH=/root/Kratos/build/Release/kratos:$LD_LIBRARY_PATH
# export LD_LIBRARY_PATH=/root/Kratos/bin/Release/libs:$LD_LIBRARY_PATH

# 旧版

# 环境变量

export PYTHONPATH=$PYTHONPATH:/root/Kratos
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/Kratos/libs

# 运行命令

bug_id=5458

# 编译
echo "开始编译Kratos..."
/root/kratos_testcase/script/7_kratos.sh 85619af239211663c59cbd403d7b3252df621990
echo "Kratos编译完成。"

# 运行
echo "开始运行 BUG $bug_id 测试用例..."
python3 /root/Kratos/applications/SwimmingDEMApplication/tests/SmallTests.py
echo "BUG $bug_id 测试用例运行完成。"

# 生成覆盖率报告
echo "开始生成 BUG $bug_id 覆盖率报告..."
/root/kratos_testcase/script/coverage.sh 5458
echo "BUG $bug_id 覆盖率报告生成完成。"


# 存档bug_id脚本
echo "开始存档 BUG $bug_id 脚本..."
cp "/root/kratos_testcase/script/$bug_id.sh" "/root/kratos_testcase/$bug_id/$bug_id.sh"
echo "存档 BUG $bug_id 脚本完成。"
