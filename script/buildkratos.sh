# The example scripts for every system are shown next.

# GNU/Linux
# Function to add apps
add_app () {
    export KRATOS_APPLICATIONS="${KRATOS_APPLICATIONS}$1;"
}

# Set compiler
export CC=gcc
export CXX=g++

# Set variables
export KRATOS_SOURCE="${KRATOS_SOURCE:-"$( cd "$(dirname "$0")" ; pwd -P )"/Kratos}"
export KRATOS_BUILD="${KRATOS_SOURCE}/build"
export KRATOS_APP_DIR="${KRATOS_SOURCE}/applications"

# Set basic configuration
export KRATOS_BUILD_TYPE="Release"
export PYTHON_EXECUTABLE="/usr/bin/python3"

# Set applications to compile
export KRATOS_APPLICATIONS=
# add_app ${KRATOS_APP_DIR}/LinearSolversApplication
# add_app ${KRATOS_APP_DIR}/StructuralMechanicsApplication
add_app ${KRATOS_APP_DIR}/FluidDynamicsApplication
# add_app ${KRATOS_APP_DIR}/KratosMultiphysics.mpi
add_app ${KRATOS_APP_DIR}/FluidDynamicsBiomedicalApplication
# add_app ${KRATOS_APP_DIR}/DEMApplication
add_app ${KRATOS_APP_DIR}/MeshingApplication



# Clean
clear
rm -rf "${KRATOS_BUILD}/${KRATOS_BUILD_TYPE}/cmake_install.cmake"
rm -rf "${KRATOS_BUILD}/${KRATOS_BUILD_TYPE}/CMakeCache.txt"
rm -rf "${KRATOS_BUILD}/${KRATOS_BUILD_TYPE}/CMakeFiles"

# Configure
cmake -H"${KRATOS_SOURCE}" -B"${KRATOS_BUILD}/${KRATOS_BUILD_TYPE}" -DUSE_MPI=ON -DUSE_EIGEN_MKL=ON

# Buid
cmake --build "${KRATOS_BUILD}/${KRATOS_BUILD_TYPE}" --target install -- -j$(nproc)
