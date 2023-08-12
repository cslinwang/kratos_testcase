# Bug url
# https://github.com/KratosMultiphysics/Kratos/issues/5458

# 预期报错：
# ModuleNotFoundError: No module named 'swimming_DEM_procedures'

# 运行文件
# /root/Kratos/applications/SwimmingDEMApplication/tests/SmallTests.py

# 运行命令

# 旧版

# 编译
echo "开始编译Kratos..."
/root/kratos_testcase/script/7_kratos.sh 85619af239211663c59cbd403d7b3252df621990
echo "Kratos编译完成。"

# 运行
echo "开始运行测试用例..."
python3 /root/Kratos/applications/SwimmingDEMApplication/tests/SmallTests.py
echo "测试用例运行完成。"

# 生成覆盖率报告
echo "开始生成覆盖率报告..."
/root/kratos_testcase/script/coverage.sh 5458
echo "覆盖率报告生成完成。"