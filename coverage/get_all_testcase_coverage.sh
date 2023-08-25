#!/bin/bash

# 定义输入的markdown文件
input_md_names="kratos_testcase_names.md"
input_md_detailed="kratos_testcase_detailed.md"

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
    echo "应用程序：$current_application"
    # echo ""
  else
    # 删除行首的空格和破折号
    file_name_no_ext=$(echo "$line" | sed 's/^[ \t-]*//')

    # 在详细文件中查找与文件名称匹配的部分
    application_section=$(sed -n "/^## $current_application/,/^## /p" "$input_md_detailed")
    if [[ -z "$application_section" ]]; then
        application_section=$(sed -n "/^## $current_application/,/^## /p; /## /q" "$input_md_detailed")
    fi

    file_path=$(echo "$application_section" | grep -A 2 "### $file_name_no_ext" | grep 'Path:' | awk '{print substr($0, 12)}')

    # 如果找到路径，则打印文件名称和路径
    if [[ -n "$file_path" ]]; then
      # echo "  文件：$file_name_no_ext"
      # echo "  路径：$file_path"
      # echo ""
      continue
    else
      # 如果文件名称为空或者# Applications，则跳过
      if [[ -z "$file_name_no_ext" || "$file_name_no_ext" == "# Applications" ]]; then
        continue
      else
        echo "  未找到文件：$file_name_no_ext"
        # echo ""
      fi
    fi
  fi
done < "$input_md_names"
