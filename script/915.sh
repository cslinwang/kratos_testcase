#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/915

# 预期报错：
# RuntimeError: Error: bad index

# 运行文件
# /root/Kratos/applications/StructuralMechanicsApplication/tests/test_loading_conditions_line.py

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
/root/kratos_testcase/script/7_kratos.sh ef49044637ce61cd542cf846e5e0812386d28e22
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/Kratos/applications/StructuralMechanicsApplication/tests
python3 /root/Kratos/applications/StructuralMechanicsApplication/tests/test_loading_conditions.py
echo "测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 915
