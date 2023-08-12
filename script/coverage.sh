#!/bin/bash

# 获取当前命令行目录

current_directory = $1

# 如果没有指定目录，则使用当前目录
if [[ -z "$current_directory" ]]; then
  current_directory=$(pwd)
fi

# 如果指定目录，则拼接成绝对路径
if [[ ! "$current_directory" = /* ]]; then
  current_directory="/root/kratos_testcase/$current_directory"
fi

# 执行 fastcov 命令，将输出文件保存在当前目录下
fastcov --gcov gcov --exclude /usr/include --include /root/Kratos -o "$current_directory/coverage.json"
fastcov --lcov -o "$current_directory/coverage.info"

# 执行 genhtml 命令，将输出文件保存在当前目录下的 coverage 文件夹中
genhtml "$current_directory/coverage.info" --output-directory "$current_directory/coverage"
