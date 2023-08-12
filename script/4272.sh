#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/4272

# 预期报错：
# 收敛问题，没有具体报错提示

# 运行文件
# /root/kratos_testcase/4272/MainKratos.py

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
/root/kratos_testcase/script/7_kratos.sh ecba702e6d595ae5a39e8d003cdb61add5617051
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
python3 /root/kratos_testcase/4272/MainKratos.py
echo "测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 4272
