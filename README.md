# Kratos 测试

<https://github.com/dealii/dealii/issues?q=is%3Aissue+is%3Aclosed+label%3ABug>

## 项目地址

<https://github.com/dealii/dealii>

## 复现

### 环境准备

Ubuntu 2204

```bash
sudo apt install net-tools
sudo apt update
sudo apt install openssh-server
sudo ufw allow ssh
sudo apt install git
sudo apt install cmake
sudo apt install g++
sudo apt install clang
sudo apt update
sudo apt install gfortran
sudo apt update
sudo apt install libtbb-dev
sudo apt update
sudo apt install libboost-all-dev
sudo apt-get install gdb
```

配置私钥

```bash
ssh-keygen -t ed25519 -C "wwwglin@163.com"
cat ~/.ssh/id_ed25519.pub
```

### 开始复现

#### 环境要求

- GNU/Linux: GCC version 5.0 or later; Clang version 5.0 or later; ICC versions 15 or later
- [CMake](https://www.cmake.org/) version 3.3.0 or later
- [GNU make](https://www.gnu.org/software/make/), version 3.78 or later (or any other generator supported by CMake)

下载

```bash
git clone https://github.com/dealii/dealii
cd dealii
```

编译

```bash
mkdir /home/my/dealiiinstall
mkdir build
cd /home/my/dealii/build
cmake -DCMAKE_INSTALL_PREFIX=/home/my/dealiiinstall /home/my/dealii
make --jobs=2 install
make test
```

## 容器编译

创建

```bash
docker run -it -d -p 7001:22 --name dealii01 ubuntu:22.04
docker run --privileged -it -d -p 7002:22 --name dealii02 new_dealii_image /bin/bash
docker exec -it dealii01 bash
```

脚本

```bash
apt-get update
apt-get install -y net-tools openssh-server git cmake g++ clang gfortran libtbb-dev libboost-all-dev gdb screen ccache
apt-get install -y ccache
ufw allow ssh
systemctl start ssh
```

下载

```bash
git clone git@github.com:dealii/dealii.git
cd dealii
```

编译

```bash
mkdir ~/dealiiinstall
cd ~/dealii
mkdir build
cd ~/dealii/build
cmake -DCMAKE_INSTALL_PREFIX=~/dealiiinstall ~/dealii
make --jobs=36 install
make test
```

![[Pasted image 20230804200401.png]]

### 旧版额外安装内容

Ubuntu 包

```bash
apt-get install liblapack-dev
```

Python 包

```bash
pip3 install mpmath
```

## 增加覆盖率

```bash
mkdir ~/dealii/build_coverage
cd ~/dealii/build_coverage
rm -r /root/dealii/build_coverage/*
cmake -DCMAKE_INSTALL_PREFIX=~/dealiiinstall -D DEAL_II_SETUP_COVERAGE=ON ~/dealii
make --jobs=36 install
make test
```

## 测试用例运行

<https://github.com/dealii/dealii/issues/15439>

复制运行文件到测试目录
进入测试目录

```bash
cmake .
make --jobs=36
make run
```

镜像保存

```bash
docker commit dealii01 new_dealii_image
docker run --privileged -it new_dealii_image /bin/bash
docker run --security-opt seccomp=unconfined -it new_dealii_image /bin/bash
```

## 其他容器

```bash
docker run --privileged -it -d -p 7001:22 --name kratosv1 cslinwang/kratos:v1 /bin/bash
```

配置git

```bash
git config --global user.name "yue ma"
git config --global user.email "yuema@mail.dlut.edu.cn"
```

### 旧版配置

## 如何修改第三方应用 Application

### 新版

修改

```bash
/root/kratos_testcase/script/buildkratos.sh
```

对应位置即可。

```bash
# Set applications to compile
export KRATOS_APPLICATIONS=
# add_app ${KRATOS_APP_DIR}/LinearSolversApplication
# add_app ${KRATOS_APP_DIR}/StructuralMechanicsApplication
add_app ${KRATOS_APP_DIR}/FluidDynamicsApplication
# add_app ${KRATOS_APP_DIR}/KratosMultiphysics.mpi
add_app ${KRATOS_APP_DIR}/FluidDynamicsBiomedicalApplication
# add_app ${KRATOS_APP_DIR}/DEMApplication
add_app ${KRATOS_APP_DIR}/MeshingApplication

```

### 旧版

编辑文件

```bash
/root/kratos_testcase/script/buildkratosv7.sh
```

选择对应三方是 ON 还是 OFF, 默认全编译。

```bash
cmake ..                                                                            \
-DCMAKE_C_COMPILER=/usr/bin/gcc                                                     \
-DCMAKE_CXX_COMPILER=/usr/bin/g++                                                   \
-DCMAKE_CXX_FLAGS="${CMAKE_CXX_FLAGS} -msse3 -std=c++11 "                           \
-DCMAKE_C_FLAGS="${CMAKE_C_FLAGS} -msse3 "                                          \
-DBOOST_ROOT="${HOME}/boost"                                                        \
-DPYTHON_EXECUTABLE="/usr/bin/python3"                                              \
-DCMAKE_BUILD_TYPE=Release                                                          \
-DMESHING_APPLICATION=ON                                                            \
-DEXTERNAL_SOLVERS_APPLICATION=ON                                                   \
-DSTRUCTURAL_MECHANICS_APPLICATION=ON                                               \
-DCONVECTION_DIFFUSION_APPLICATION=ON                                               \
-DSOLID_MECHANICS_APPLICATION=ON                                                    \
-DCONSTITUTIVE_MODELS_APPLICATION=ON                                                \
-DFLUID_DYNAMICS_APPLICATION=ON                                                     \
-DMESH_MOVING_APPLICATION=ON                                                        \
-DFSI_APPLICATION=ON                                                                \
-DDEM_APPLICATION=ON                                                               \
-DSWIMMING_DEM_APPLICATION=ON                                                      \
-DMIXED_ELEMENT_APPLICATION=ON                                                     \
-DSHAPE_OPTIMIZATION_APPLICATION=OFF                                                \
-DTOPOLOGY_OPTIMIZATION_APPLICATION=OFF                                             \
-DMETIS_APPLICATION=OFF                                                             \
-DPARMETIS_ROOT_DIR="/home/youruser/compiled_libraries/ParMetis-3.1.1"              \
-DTRILINOS_APPLICATION=OFF                                                          \
-DTRILINOS_ROOT="/home/youruser/compiled_libraries/trilinos-10.2.0"                 \
-DINSTALL_EMBEDDED_PYTHON=ON
```

## 覆盖率生成

运行如下脚本，（5458 为存放文件夹）

```bash
/root/kratos_testcase/script/coverage.sh 5458
```

## 使用说明

在复现前先看第三方库，只编译必须的。

### 情况1

针对新版：运行脚本即可, 记得增加 commit SHA。

```bash
export PYTHONPATH=$PYTHONPATH:/root/Kratos/bin/Release
/root/kratos_testcase/script/runkratos.sh
```

### 情况2

运行脚本后报错，尝试如下命令

```bash
export LD_LIBRARY_PATH=/root/Kratos/build/Release/kratos:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/root/Kratos/bin/Release/libs:$LD_LIBRARY_PATH
```

### 情况3

针对旧版，主要是2019年及以前的版本，编译方式发生变化，运行如下命令（记得增加 commit SHA）

```bash
/root/kratos_testcase/script/7_kratos.sh
```

## 大版本 hash

v9.3
b0b8655633dbaf674f99ddd2c0fc6e2d717f2819

v9.2
cc57d0b8344f6cd3fdf4b2d9b53327c1867c58cc

v9.1
9459a425b332c6ac4134933cf5ea7cfecf35185c

v9.0
0bc6047de5ca282309df5e8bb80172f19b7f270f
