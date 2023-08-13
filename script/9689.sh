#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/9689

# 预期报错：
# RuntimeError: Error: Parsing error in function: (0.0)*(50*(exp(t)-1))

# 运行文件
# /root/Kratos/applications/RomApplication/tests/test_structural_rom.py

# 新版

# 环境变量

export PYTHONPATH=$PYTHONPATH:/root/Kratos/bin/Release
export LD_LIBRARY_PATH=/root/Kratos/build/Release/kratos:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/root/Kratos/bin/Release/libs:$LD_LIBRARY_PATH

# v9
export PYTHONPATH=$PYTHONPATH:$HOME/Kratos/bin/Release
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/Kratos/bin/Release/libs

# 旧版

# 环境变量

# export PYTHONPATH=$PYTHONPATH:/root/Kratos
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/Kratos/libs

# 运行命令

# 编译
echo "开始编译Kratos..."
/root/kratos_testcase/script/runkratos.sh 0bc6047de5ca282309df5e8bb80172f19b7f270f
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/Kratos/applications/RomApplication/tests
python3 /root/Kratos/applications/RomApplication/tests/test_structural_rom.py
echo "BUG测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 9689
