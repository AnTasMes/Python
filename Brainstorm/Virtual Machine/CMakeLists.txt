cmake_minimum_required(VERSION 3.19)
project(BrainStormVirtualMachine)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

set(CMAKE_CXX_STANDARD 20)

include_directories(include)

add_executable(BrainStormVirtualMachine source/main.cpp include/CPU.h)