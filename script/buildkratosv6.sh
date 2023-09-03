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
-DCONVECTION_DIFFUSION_APPLICATION=ON \
-DSTRUCTURAL_MECHANICS_APPLICATION=ON \
-DCONTACT_STRUCTURAL_MECHANICS_APPLICATION=ON \
-DSOLID_MECHANICS_APPLICATION=ON \
-DCONTACT_MECHANICS_APPLICATION=OFF \
-DCONSTITUTIVE_MODELS_APPLICATION=ON \
-DCONSTITUTIVE_LAWS_APPLICATION=OFF \
-DUMAT_APPLICATION=ON \
-DFLUID_DYNAMICS_APPLICATION=ON \
-DMESH_MOVING_APPLICATION=ON \
-DFSI_APPLICATION=ON \
-DCOMPRESSIBLE_POTENTIAL_FLOW_APPLICATION=OFF \
-DSHALLOW_WATER_APPLICATION=ON \
-DPFEM2_APPLICATION=ON \
-DDEM_APPLICATION=ON \
-DSWIMMING_DEM_APPLICATION=ON \
-DPARTICLE_MECHANICS_APPLICATION=ON \
-DLAGRANGIAN_MPM_APPLICATION=OFF \
-DEXTERNAL_SOLVERS_APPLICATION=ON \
-DTRILINOS_APPLICATION=OFF \
-DMPI_SEARCH_APPLICATION=OFF \
-DMESHING_APPLICATION=OFF \
-DADJOINT_FLUID_APPLICATION=ON \
-DSHAPE_OPTIMIZATION_APPLICATION=ON \
-DMAPPING_APPLICATION=ON \
-DEIGEN_SOLVERS_APPLICATION=OFF \
-DSTABILIZED_CFD_APPLICATION=ON \
-DHDF5_APPLICATION=OFF \
-DFLUID_TRANSPORT_APPLICATION=ON \

# decomment this to have it verbose
# make VERBOSE=1 -j4
make -j$(nproc)
make install
