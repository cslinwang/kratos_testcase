#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/4896

# 预期报错：
# AssertionError: False is not true

# 运行文件
# /root/kratos_testcase/4896/4896.py

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

# 编译
echo "开始编译Kratos..."
/root/kratos_testcase/script/7_kratos.sh 67e9f81119d3acd3c25c370ea2f20faf7bb29bc9
echo "Kratos编译完成。"

# 运行
echo "开始运行 BUG $bug_id 测试用例..."
cd /root/kratos_testcase/4896
python3 /root/kratos_testcase/4896/4896.py
echo "BUG $bug_id 测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 4896
