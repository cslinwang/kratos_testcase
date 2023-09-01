#!/bin/bash

# 定义输入的markdown文件
input_md_names="kratos_testcase_names.md"

# 输出的Shell脚本文件
output_sh="applications.sh"

# 如果输出文件已存在，先删除它
if [[ -f "$output_sh" ]]; then
  rm "$output_sh"
fi

# Function to convert application name
convert_app_name() {
    local app_name="$1"
    local converted_name=""
    local prev_char=""

    for (( i=0; i<${#app_name}; i++ )); do
        char="${app_name:$i:1}"
        if [[ "$char" =~ [A-Z] ]]; then
            if [ "$prev_char" != "" ]; then
                converted_name+="_"
            fi
            converted_name+="$char"
        else
            converted_name+="$(echo "$char" | tr '[:lower:]' '[:upper:]')"
        fi
        prev_char="$char"
    done

    echo "-D${converted_name}=ON\\"
}

# 逐行读取kratos_testcase_names.md文件，找到以##开头的行，并从中提取应用程序名称
grep '^##' "$input_md_names" | while read -r line; do
  # 去掉行前的##和末尾的文件数量统计，然后构造所需的格式
  app_name=$(echo "$line" | sed 's/^## //; s/ ([0-9]* files)//')

  # 跳过特定的行，例如"Total PY Files"
  if [[ "$app_name" == "Total PY Files" ]]; then
    continue
  fi

  # 调用函数进行应用名称的转换
  converted_app_name=$(convert_app_name "$app_name")

  # 补充空格到固定长度，并在结尾增加反斜杠
  formatted_app_name=$(printf "%-60s" "$converted_app_name")

  # 将转化后的app_name写入到Shell脚本文件中
  echo "$formatted_app_name" >> "$output_sh"
done

echo "Shell脚本已生成：$output_sh"
