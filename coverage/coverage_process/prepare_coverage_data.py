import subprocess

'''
将压缩的数据解压到指定目录

'''

def prepare_data():
    """
    数据准备
    数据准备，解压覆盖率文件到指定目录
    解压数据
    tar -I pigz -xvf /root/kratos_6_coverage_info.tar.gz -C /root/coverage_info_all/kratos_6_coverage_info
    tar -I pigz -xvf /root/kratos_7.1_coverage_info.tar.gz -C /root/coverage_info_all/kratos_7.1_coverage_info
    tar -I pigz -xvf /root/kratos_8.1_coverage_info.tar.gz -C /root/coverage_info_all/kratos_8.1_coverage_info
    tar -I pigz -xvf /root/kratos_9.3.2_coverage_info.tar.gz -C /root/coverage_info_all/kratos_9.3.2_coverage_info

    :return:
    """
    # 构建目录
    run_command("rm -rf /root/coverage_info_all")
    run_command("mkdir -p /root/coverage_info_all/kratos_6_coverage_info")
    run_command("mkdir -p /root/coverage_info_all/kratos_7.1_coverage_info")
    run_command("mkdir -p /root/coverage_info_all/kratos_8.1_coverage_info")
    run_command("mkdir -p /root/coverage_info_all/kratos_9.3.2_coverage_info")

    # 解压数据
    run_command(
        "tar -I pigz -xvf /root/kratos_6_coverage_info.tar.gz -C /root/coverage_info_all/kratos_6_coverage_info")
    run_command(
        "tar -I pigz -xvf /root/kratos_7.1_coverage_info.tar.gz -C /root/coverage_info_all/kratos_7.1_coverage_info")
    run_command(
        "tar -I pigz -xvf /root/kratos_8.1_coverage_info.tar.gz -C /root/coverage_info_all/kratos_8.1_coverage_info")
    run_command(
        "tar -I pigz -xvf /root/kratos_9.3.2_coverage_info.tar.gz -C /root/coverage_info_all/kratos_9.3.2_coverage_info")

    pass


def run_command(command):
    """
    运行命令
    """
    process = subprocess.Popen(command, shell=True)
    process.wait()

if __name__ == '__main__':
    print("数据准备, 仅运行一次")
    print("将数据全部解压到指定目录：/root/coverage_info_all")
    prepare_data()
    print("数据准备完成~~~~")
    print("准备去计算Jaccard相似度矩阵啦")