#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/11231

# 预期报错：
# AssertionError: -1152.7766935045422 != -1219.77524 within 0.001 delta (66.99854649545773 difference)

# 运行文件
# /root/Kratos/applications/DEMApplication/tests/test_history_dependent_CLs.py

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
/root/kratos_testcase/script/runkratos.sh 8483b2c3edc64b99a2ce5d23afc84869a784124f
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/Kratos/applications/DEMApplication/tests
python3 /root/Kratos/applications/DEMApplication/tests/test_history_dependent_CLs.py
echo "BUG测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 11231
