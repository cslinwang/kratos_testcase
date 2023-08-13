#!/bin/bash

# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/6118

# 预期报错：
# 预期：在第一个场景中，我们想通过“file_name”设置绝对路径，正如您在打印时看到的那样，我们只获取“test.dat”，这是相对路径。第二种情况通过“folder_name”设置绝对路径。如您所见，生成的文件名为“home/riccardo/folder/test.dat”，这是相对路径。

# 运行文件
# /root/kratos_testcase/6118/6118.py

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
/root/kratos_testcase/script/runkratos.sh 26db580ec7de7a30173507a7f6ad406930bd79a7
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
cd /root/kratos_testcase/6118
python3 /root/kratos_testcase/6118/6118.py
echo "BUG测试用例运行完成。"

# 生成覆盖率报告
# /root/kratos_testcase/script/coverage.sh 6118
