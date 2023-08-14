#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/727

# 预期报错：
# strain_YY：
# Element 24:
# 0.0004323619941715151
# 0.0001158510422101244
# 0.0001158510422101244
# 0.0004323619941715151
# Element 25:
# 0.0004323619941715151
# 0.0001158510422101244
# 0.0001158510422101244
# 0.0004323619941715151

# 运行文件
# /root/kratos_testcase/727/Incorrect gauss output example/clamped_cylinder1_test.gid/MainKratos.py

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
/root/kratos_testcase/script/7_kratos.sh 84df6f82eb1098c611d52193c010bc577bd2bf63
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/kratos_testcase/727/Incorrect gauss output example/clamped_cylinder1_test.gid
python3 /root/kratos_testcase/727/Incorrect gauss output example/clamped_cylinder1_test.gid/MainKratos.py
echo "测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 727
