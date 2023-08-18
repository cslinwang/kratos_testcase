#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/7481

# 预期报错：
# NameError: name 'context_string' is not defined


# 运行文件
# /root/Kratos/applications/DamApplication/python_scripts/gid_dam_output_process.py

# 新版

# 环境变量

export PYTHONPATH=$PYTHONPATH:/root/Kratos/bin/Release
export LD_LIBRARY_PATH=/root/Kratos/build/Release/kratos:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/root/Kratos/bin/Release/libs:$LD_LIBRARY_PATH

# v9
# export PYTHONPATH=$PYTHONPATH:$HOME/Kratos/bin/Release
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/Kratos/bin/Release/libs

# 旧版

# 环境变量

# export PYTHONPATH=$PYTHONPATH:/root/Kratos
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/Kratos/libs

# 运行命令

# 编译
echo "开始编译Kratos..."
/root/kratos_testcase/script/runkratos.sh da4c63388bc6c45d9ca7ecbd0c4f6b8da55c7052
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/Kratos/applications/DamApplication/python_scripts
python3 /root/Kratos/applications/DamApplication/python_scripts/gid_dam_output_process.py
echo "BUG测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 7481
