#!/bin/bash

# 定义输入的markdown文件
input_md_names="kratos_testcase_names.md"

# 输出的YAML文件
output_yaml="applications.sh"

if [[ -f "$output_yaml" ]]; then
  rm "$output_yaml"
fi

# 开始YAML文件
# echo "applications:" > "$output_yaml"

# 逐行读取kratos_testcase_names.md文件，找到以##开头的行，并从中提取应用程序名称
grep '^##' "$input_md_names" | while read -r line; do
  # 去掉行前的##和末尾的文件数量统计，然后构造所需的格式
  app_name=$(echo "$line" | sed 's/^## //; s/ ([0-9]* files)//')
  if [[ "$app_name" == "Total PY Files" ]]; then
    break
  fi
  echo "add_app \${KRATOS_APP_DIR}/$app_name" >> "$output_yaml"
done

echo "YAML文件已生成：$output_yaml"
