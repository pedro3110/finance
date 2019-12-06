# Install script for directory: /home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/includes/quantlib/Examples

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Debug")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/BasketLosses/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/BermudanSwaption/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/Bonds/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/CallableBonds/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/CDS/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/ConvertibleBonds/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/CVAIRS/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/DiscreteHedging/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/EquityOption/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/FittedBondCurve/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/FRA/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/Gaussian1dModels/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/GlobalOptimizer/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/LatentModel/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/MarketModels/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/MultidimIntegral/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/MulticurveBootstrapping/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/Replication/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/Repo/cmake_install.cmake")

endif()

