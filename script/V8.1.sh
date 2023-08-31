#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/11307

# 预期报错：
# 修复前有子模型，修复后没有子模型

# 运行文件
# /root/kratos_testcase/11307/11307.py

# 新版

# 环境变量

export PYTHONPATH=$PYTHONPATH:/root/Kratos/bin/Release
export LD_LIBRARY_PATH=/root/Kratos/build/Release/kratos:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/root/Kratos/bin/Release/libs:$LD_LIBRARY_PATH

# 旧版

# 环境变量

# export PYTHONPATH=$PYTHONPATH:/root/Kratos
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/Kratos/libs

# 运行命令

# 编译
echo "开始编译Kratos..."
/root/kratos_testcase/script/runkratos.sh 5db879349aa2ba28cf6b99d32abd2fcaa98ad557
echo "Kratos编译完成。"

# # 运行
# echo "开始运行测试用例..."
# cd /root/kratos_testcase/11307
# python3 /root/kratos_testcase/11307/11307.py
# echo "BUG测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 11307
