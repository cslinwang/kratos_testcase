#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/11307

# 预期报错：
# 修复前有子模型，修复后没有子模型

# 运行文件
# /root/kratos_testcase/11307/11307.py

# 新版

# 环境变量

export PYTHONPATH=$PYTHONPATH:$HOME/Kratos/bin/Release
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/Kratos/bin/Release/libs

# 旧版

# 环境变量

# export PYTHONPATH=$PYTHONPATH:/root/Kratos
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/Kratos/libs

# 运行命令

# 编译
echo "开始编译Kratos..."
/root/kratos_testcase/script/runkratos.sh fa79945b8fd6c8531c7f2e4d2ab2c81796e8ad3c
echo "Kratos编译完成。"

# # 运行
# echo "开始运行测试用例..."
# cd /root/
# python3 /root/Kratos/applications/CSharpWrapperApplication/tests/run_cpp_unit_tests.py
# echo "BUG测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 11307
