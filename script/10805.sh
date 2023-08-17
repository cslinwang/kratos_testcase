#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/10805/

# 预期报错：
# self.find_neighbour_elements_of_conditions_process.Execute()
# RuntimeError: Error: Some conditions found without any corresponding element

# 运行文件
# /root/kratos_testcase/10805/MainKratos.py

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
/root/kratos_testcase/script/runkratos.sh b0b8655633dbaf674f99ddd2c0fc6e2d717f2819
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/kratos_testcase/10805
python3 /root/kratos_testcase/10805/MainKratos.py
echo "BUG测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 10805
