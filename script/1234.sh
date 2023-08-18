#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/1234

# 预期报错：
# Kratos::Exception'what(): Error: attempting to do a GetValue for: YOUNG_MODULUS_X

# 运行文件
# /root/Kratos/applications/DEMApplication/tests/test_history_dependent_CLs.py

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
/root/kratos_testcase/script/runkratos.sh 5a170e5b03988bfd2d0b5c1009dcde3abbdc782d
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/Kratos/applications/StructuralMechanicsApplication/tests
python3 /root/Kratos/applications/StructuralMechanicsApplication/tests/test_patch_test_shells_orthotropic.py
echo "BUG测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 1234
