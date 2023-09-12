#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/3442

# 预期报错：
# 查看info文件，属于计算错误

# 运行文件
# /root/kratos_testcase/3442/MainKratos.py

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
/root/kratos_testcase/script/7_kratos.sh d386b0f7d873c3db99c71f03cd0e125d72313ddf
# a741949882c360ae3f738839a793b6c1a449f5a7
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/kratos_testcase/3442
PYTHON_COVERAGE_PATH=/root/kratos_testcase/3442/python
if [ ! -d "$PYTHON_COVERAGE_PATH" ]; then
  mkdir -p "$PYTHON_COVERAGE_PATH"
fi
# 清除覆盖率数据
coverage erase

coverage run --source=/root/Kratos/ /root/kratos_testcase/3442/MainKratos.py
coverage report -m

# 创建HTML覆盖率报告
coverage html -d ${PYTHON_COVERAGE_PATH}

# 创建JSON覆盖率报告
coverage json -o ${PYTHON_COVERAGE_PATH}/coverage.json

# 创建XML覆盖率报告
coverage xml -o ${PYTHON_COVERAGE_PATH}/coverage.xml

echo "测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 3442
