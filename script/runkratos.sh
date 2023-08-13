#!/bin/bash

echo -e "\033[34m#################################################\033[0m"
echo -e "\033[34m## 开始运行  ##\033[0m"

export PYTHONPATH=$PYTHONPATH:$HOME/Kratos/bin/Release
export LD_LIBRARY_PATH=/root/Kratos/build/Release/kratos:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/root/Kratos/bin/Release/libs:$LD_LIBRARY_PATH

full_sha="$1"

echo "切换分支开始..."

# Extract short SHA from full SHA.
short_sha=$(echo "$full_sha" | cut -c 1-7)

# Reset repository and checkout master branch.
cd /root/Kratos
git reset --hard HEAD
git clean -fd
git checkout master

if [[ -d /root/Kratos/build ]]; then
  echo "build文件夹已存在，删除中..."
  rm -rf /root/Kratos/build
fi
if [[ -d /root/Kratos/bin ]]; then
  echo "bin文件夹已存在，删除中..."
  rm -rf /root/Kratos/bin
fi
if [[ -d /root/Kratos/coverage ]]; then
  echo "coverage文件夹已存在，删除中..."
  rm -rf /root/Kratos/coverage
fi

# Delete branch if it exists.
if git show-ref --quiet "refs/heads/$short_sha"; then
  git branch -D "$short_sha"
fi

# Create a new branch based on the specified SHA.
git checkout -b "$short_sha" "$full_sha"

echo "已切换到分支 $short_sha。"
echo "开始修改makefile，以支持代码覆盖率..."

# Define the path to the CMakeLists.txt file
CMAKE_FILE_PATH="/root/Kratos/CMakeLists.txt"

# Check if the file exists
if [[ ! -f $CMAKE_FILE_PATH ]]; then
    echo "Error: $CMAKE_FILE_PATH does not exist."
    exit 1
fi

sed -i 's|project (KratosMultiphysics)|project (KratosMultiphysics)\n\
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage -Wno-deprecated-declarations -Wno-unknown-pragmas")\
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fprofile-arcs -ftest-coverage")|' $CMAKE_FILE_PATH


# Echo a success message
echo "makefile修改成功。"

echo "开始编译Kratos..."
cp /root/kratos_testcase/script/buildkratos.sh /root/buildkratos.sh
sh /root/buildkratos.sh 2>&1 | tee /root/kratos_testcase/script/kratos_build.log
echo "Kratos编译完成。"
