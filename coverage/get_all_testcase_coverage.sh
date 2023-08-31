#!/bin/bash

# 日志文件的路径
logfile="run_all_testcase_coverage.log"

# 创建或清空日志文件
: > $logfile

# 重定向标准输出和错误，同时打印到控制台和日志文件
exec > >(tee -a "$logfile") 2>&1

# 定义输入的markdown文件
input_md_names="kratos_testcase_names.md"
input_md_detailed="kratos_testcase_detailed.md"
applications_file="8.1_all_run_application.sh"
declare -a applications_list

# 清空覆盖率文件夹/root/coverage_info
if [ -d "/root/coverage_info" ]; then
  echo "清空覆盖率文件夹/root/coverage_info"
  rm -rf /root/coverage_info
fi

# 逐行读取应用程序列表文件
while read -r app_line; do
  # 使用正则表达式提取应用程序名称，并将其添加到数组中
  current_application=$(echo "$app_line" | awk -F'/' '{print $NF}')
  applications_list+=("$current_application")
done < "$applications_file"

# 初始化应用程序变量
current_application=""

# 逐行读取kratos_testcase_names.md文件
while read -r line; do
  if [[ "$line" =~ ^## ]]; then
    # 更新当前应用程序，并从名称中去掉末尾的统计信息
    current_application=$(echo "$line" | sed 's/^## //; s/ ([0-9]* files)//')
    if [[ "$current_application" == "Total PY Files" ]]; then
      break
    fi
    if [[ " ${applications_list[*]} " == *" $current_application "* ]]; then
      echo "应用程序 $current_application 在列表中"
    else
      # echo "应用程序 $current_application 不在列表中"
      current_application=""
    fi
    # echo "应用程序：$current_application"
    # echo ""
  else
    if [[ -z "$current_application" ]]; then
      continue
    fi
    # 删除行首的空格和破折号
    file_name_no_ext=$(echo "$line" | sed 's/^[ \t-]*//')

    file_name_no_ext=$(echo "$line" | sed 's/^[ \t-]*//')

    file_name_no_ext=$(echo "$line" | sed 's/^[ \t-]*//')

    # 在详细文件中查找与文件名称匹配的部分
    application_section=$(sed -n "/^## $current_application/,/^## /p" "$input_md_detailed")
    if [[ -z "$application_section" ]]; then
        application_section=$(sed -n "/^## $current_application/,/^## /p; /## /q" "$input_md_detailed")
    fi

    # 通过精确匹配文件名来查找文件路径
    file_path=$(echo "$application_section" | grep -A 2 "^### $file_name_no_ext$" | grep 'Path:' | awk '{print substr($0, 12)}' | sed 's/^** //')



     # 如果文件名称为空或者# Applications，则跳过
    if [[ -z "$file_name_no_ext" || "$file_name_no_ext" == "# Applications" ]]; then
        continue
    fi
    # 如果找到路径，则打印文件名称和路径
    if [[ -n "$file_path" ]]; then
      echo "应用：$current_application  文件：$file_name_no_ext, 路径：$file_path"
      # 增加计时功能，如果超时停止
      timeout 600 ./run_testcase.sh "$current_application" "$file_name_no_ext" "$file_path"
      # echo ""
      continue
    else
      echo "  未找到文件：$file_name_no_ext"
      # echo ""
    fi
  fi
done < "$input_md_names"
