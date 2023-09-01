#!/bin/sh

# this is an example file...please DO NOT MODIFY if you don't want to do it for everyone
# to use it, copy it to another file and run it

# additional compiler flags could be added customizing the corresponding var, for example
# -DCMAKE_CXX_FLAGS="${CMAKE_CXX_FLAGS} -msse3 ". Note that the "defaults are already correctly coded"
# so we should add here only machine specific stuff

# an effort is made to autodetect all of the libraries needed HOWEVER:
# METIS_APPLICATION needs the var PARMETIS_ROOT_DIR to be specified by the user (not needed if the app is set to OFF)
# TRILINOS_APPLICATION needs the var PARMETIS_ROOT_DIR to be specified by the user (not needed if the app is set to OFF)

#the user should also note that the symbol "\" marks that the command continues on the next line. IT SHOULD ONLY BE FOLLOWED
#BY the "ENTER" and NOT by any space!!

clear

# you may want to decomment this the first time you compile
rm CMakeCache.txt
rm *.cmake
rm -rf CMakeFiles\

cmake ..                                                                            \
-DCMAKE_C_COMPILER=/usr/bin/gcc                                                     \
-DCMAKE_CXX_COMPILER=/usr/bin/g++                                                   \
-DCMAKE_CXX_FLAGS="${CMAKE_CXX_FLAGS} -msse3 -std=c++11 "                           \
-DCMAKE_C_FLAGS="${CMAKE_C_FLAGS} -msse3 "                                          \
-DBOOST_ROOT="${HOME}/boost"                                                        \
-DPYTHON_EXECUTABLE="/usr/bin/python3"                                              \
-DCMAKE_BUILD_TYPE=Release                                                          \
-DMESHING_APPLICATION=OFF                                                            \
-DEXTERNAL_SOLVERS_APPLICATION=ON                                                   \
-DSTRUCTURAL_MECHANICS_APPLICATION=ON                                               \
-DCONVECTION_DIFFUSION_APPLICATION=ON                                               \
-DSOLID_MECHANICS_APPLICATION=OFF                                                    \
-DCONSTITUTIVE_MODELS_APPLICATION=ON                                                \
-DFLUID_DYNAMICS_APPLICATION=ON                                                     \
-DMESH_MOVING_APPLICATION=ON                                                        \
-DFSI_APPLICATION=ON                                                                \
-DDEM_APPLICATION=OFF                                                               \
-DSWIMMING_DEM_APPLICATION=OFF                                                      \
-DMIXED_ELEMENT_APPLICATION=ON                                                     \
-DSHAPE_OPTIMIZATION_APPLICATION=ON                                                \
-DTOPOLOGY_OPTIMIZATION_APPLICATION=OFF                                             \
-DMETIS_APPLICATION=OFF                                                             \
-DPARMETIS_ROOT_DIR="/home/youruser/compiled_libraries/ParMetis-3.1.1"              \
-DTRILINOS_APPLICATION=OFF                                                          \
-DTRILINOS_ROOT="/home/youruser/compiled_libraries/trilinos-10.2.0"                 \
-DINSTALL_EMBEDDED_PYTHON=ON                                                        \
-DELAUNAY_MESHING_APPLICATION=ON\
-DCONVECTION_DIFFUSION_APPLICATION=ON \
-DPURE_DIFFUSION_APPLICATION=ON \
-DSTRUCTURAL_APPLICATION=OFF \
-DSTRUCTURAL_MECHANICS_APPLICATION=ON \
-DCONTACT_STRUCTURAL_MECHANICS_APPLICATION=ON \
-DSOLID_MECHANICS_APPLICATION=OFF \
-DCONTACT_MECHANICS_APPLICATION=OFF \
-DCONSTITUTIVE_MODELS_APPLICATION=ON \
-DCONSTITUTIVE_LAWS_APPLICATION=OFF \
-DUMAT_APPLICATION=ON \
-DMULTISCALE_APPLICATION=OFF \
-DSTRING_DYNAMICS_APPLICATION=OFF \
-DTHERMO_MECHANICAL_APPLICATION=ON \
-DPOROMECHANICS_APPLICATION=OFF \
-DFREEZING_SOIL_APPLICATION=OFF \
-DDAM_APPLICATION=OFF \
-DFLUID_DYNAMICS_APPLICATION=ON \
-DINCOMPRESSIBLE_FLUID_APPLICATION=OFF \
-DTURBULENT_FLOW_APPLICATION=OFF \
-DBLOOD_FLOW_APPLICATION=OFF \
-DMESH_MOVING_APPLICATION=ON \
-DFSI_APPLICATION=ON \
-DCOMPRESSIBLE_POTENTIAL_FLOW_APPLICATION=ON \
-DSHALLOW_WATER_APPLICATION=ON \
-DEMPIRE_APPLICATION=ON \
-DMIXED_ELEMENT_APPLICATION=ON \
-DPFEM_APPLICATION=OFF \
-DPFEM_SOLID_MECHANICS_APPLICATION=OFF \
-DPFEM_FLUID_DYNAMICS_APPLICATION=OFF \
-DPFEM2_APPLICATION=ON \
-DMACHINING_APPLICATION=OFF \
-DFORMING_APPLICATION=OFF \
-DDEM_APPLICATION=OFF \
-DSWIMMING_DEM_APPLICATION=OFF \
-DPARTICLE_MECHANICS_APPLICATION=ON \
-DLAGRANGIAN_MPM_APPLICATION=OFF \
-DEXTERNAL_SOLVERS_APPLICATION=ON \
-DTRILINOS_APPLICATION=OFF \
-DMPI_SEARCH_APPLICATION=OFF \
-DMETIS_APPLICATION=OFF \
-DMESHLESS_APPLICATION=OFF \
-DMESHING_APPLICATION=OFF \
-DCLICK2CAST_APPLICATION=OFF \
-DSHAPE_OPTIMIZATION_APPLICATION=ON \
-DTOPOLOGY_OPTIMIZATION_APPLICATION=OFF \
-DMAPPING_APPLICATION=OFF \
-DEIGEN_SOLVERS_APPLICATION=OFF \

# decomment this to have it verbose
# make VERBOSE=1 -j4
make -j$(nproc)
make install
