#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/7209

# 预期报错：
# 使用 OMP_NUM_THREADS>1 运行，则度量张量会被错误地写入。


# 运行文件
# /root/kratos_testcase/7209/MainKratos.py

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
/root/kratos_testcase/script/runkratos.sh df0de20a743afa102630d796265d0ac295966748
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/kratos_testcase/7209
python3 /root/kratos_testcase/7209/MainKratos.py
echo "BUG测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 7209
