#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/10553

# 预期报错：
# AssertionError: False != True

# 运行文件
# /root/Kratos/kratos/tests/test_particles_utilities.py

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
/root/kratos_testcase/script/runkratos.sh 303f30678a510e002b9edcbeb96fc606c92a2c5a
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/Kratos/kratos/tests
for i in $(seq 1 2000); do
    echo "Running iteration $i"
    PYTHON_COVERAGE_PATH=/root/kratos_testcase/10553/python
    if [ ! -d "$PYTHON_COVERAGE_PATH" ]; then
      mkdir -p "$PYTHON_COVERAGE_PATH"
    fi
    # 清除覆盖率数据
    coverage erase

    coverage run --source=/root/Kratos/ /root/Kratos/kratos/tests/test_particles_utilities.py

    # 生成文本覆盖率报告
    coverage report -m

    # 创建HTML覆盖率报告
    coverage html -d ${PYTHON_COVERAGE_PATH}

    # 创建JSON覆盖率报告
    coverage json -o ${PYTHON_COVERAGE_PATH}/coverage.json

    # 创建XML覆盖率报告
    coverage xml -o ${PYTHON_COVERAGE_PATH}/coverage.xml

    if [ $? -ne 0 ]; then
        echo "Error encountered on iteration $i. Stopping."
        break
    fi
done
echo "BUG测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 10553
