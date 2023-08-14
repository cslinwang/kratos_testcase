#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/2378

# 预期报错：
# ValueError: invalid literal for int() with base 10: 'cuts'

# 运行文件
# /root/Kratos/kratos/python_scripts/gid_output_process.py

# 新版

# 环境变量

# export PYTHONPATH=$PYTHONPATH:/root/Kratos/bin/Release
# export LD_LIBRARY_PATH=/root/Kratos/build/Release/kratos:$LD_LIBRARY_PATH
# export LD_LIBRARY_PATH=/root/Kratos/bin/Release/libs:$LD_LIBRARY_PATH

# 旧版

# 环境变量

export PYTHONPATH=$PYTHONPATH:/root/Kratos
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/Kratos/libs
export LD_LIBRARY_PATH=/root/Kratos/bin/Release/libs:$LD_LIBRARY_PATH

# 运行命令

# 编译
echo "开始编译Kratos..."
/root/kratos_testcase/script/7_kratos.sh 82e48cc35c34d90012005667071ba4c1933ee577
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/Kratos/kratos/python_scripts
python3 /root/Kratos/kratos/python_scripts/gid_output_process.py
echo "测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 2378
