#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/7762

# 预期报错：
# AssertionError: False is not true : Results do not coincide with the JSON reference

# 运行文件
# /root/Kratos/applications/StructuralMechanicsApplication/tests/structural_mechanics_test_factory.py

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
/root/kratos_testcase/script/runkratos.sh d193db3987aaf2ba1b05a8a01e64d664a75e059c
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/Kratos/applications/StructuralMechanicsApplication/tests
python3 /root/Kratos/applications/StructuralMechanicsApplication/tests/structural_mechanics_test_factory.py
echo "BUG测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 7762
