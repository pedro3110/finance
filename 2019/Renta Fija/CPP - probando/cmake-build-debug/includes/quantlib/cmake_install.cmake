# Install script for directory: /home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/includes/quantlib

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

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/ql" TYPE FILE FILES "/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/config.hpp")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/ql/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/Examples/cmake_install.cmake")
  include("/home/pedro/Dropbox/Posgrado/Maestria en Finanzas (udesa)/Materias/Excel/probando/cmake-build-debug/includes/quantlib/test-suite/cmake_install.cmake")

endif()

