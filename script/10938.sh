#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/10938

# 预期报错：
# the cond_id=10 should be in rank 0.

# 运行文件
# /root/kratos_testcase/10938/test_code.py

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
/root/kratos_testcase/script/runkratos.sh e9690c5ee5dab2cd4701f2ab74a10290376fa90f
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/kratos_testcase/10938
mpirun --allow-run-as-root -np 3 python3 /root/kratos_testcase/10938/test_code.py
echo "BUG测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 10938
