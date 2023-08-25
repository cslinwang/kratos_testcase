#!/bin/bash

# 获取脚本所在的路径
script_path="$(dirname "$0")"

# 创建两个空的markdown文件
output_md_detailed="$script_path/kratos_testcase_detailed.md"
output_md_names="$script_path/kratos_testcase_names.md"
echo "生成详细文件：$output_md_detailed"
echo "生成名称文件：$output_md_names"
echo -e "# Applications\n" > $output_md_names
echo -e "# Applications\n" > $output_md_detailed

if [[ -f "$output_md_detailed" ]]; then
  rm "$output_md_detailed"
fi
if [[ -f "$output_md_names" ]]; then
  rm "$output_md_names"
fi

# 用于跟踪所有文件的总数
total_files_count=0

# 遍历/root/Kratos/applications目录下的所有文件夹
for dir in /root/Kratos/applications/*; do
  if [ -d "$dir" ]; then
    app_name=$(basename "$dir")
    echo "检查目录：$dir"

    # 在每个文件夹中查找tests文件夹
    for test_dir in "$dir"/tests; do
      if [ -d "$test_dir" ]; then
        echo "找到tests文件夹：$test_dir"

        # 查找所有.py文件，但排除__init__.py文件，并存储到数组
        files=($(find "$test_dir" -type f -name "*.py" ! -name "__init__.py"))

        # 添加应用程序名称作为二级标题到详细文件
        echo -e "## $app_name\n" >> $output_md_detailed

        # 在应用程序名称旁边的括号中添加文件数量统计，并到names文件
        echo -e "## $app_name (${#files[@]} files)\n" >> $output_md_names

        # 遍历文件并添加到详细文件和名称文件
        for file_path in "${files[@]}"; do
          relative_path=${file_path#$test_dir/}
          file_name_no_ext=${relative_path%.py}
          file_name=$(basename "$file_path" .py)

          # 将文件名称（不带.py扩展名）添加到详细文件
          echo -e "### $file_name_no_ext\n  - **Full Name:** $file_name.py\n  - **Path:** $file_path\n" >> $output_md_detailed

          # 将文件名称（不带.py扩展名）添加到names文件
          echo "  - $file_name_no_ext" >> $output_md_names

          # 累计数量
          total_files_count=$((total_files_count + 1))
        done
      fi
    done
  else
    echo "忽略非目录文件：$dir"
  fi
done

# 将总体统计添加到names文件
echo -e "\n## Total PY Files ($total_files_count files)\n" >> $output_md_names

echo "完成!"
