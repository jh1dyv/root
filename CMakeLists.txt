# CMakeLists.txt for Springhead

cmake_minimum_required(VERSION 3.1)

include("make.func.cmake")

#set(OPT "F:/tmp/CMakeTest/CMakeLists.txt")
read_params(RC "OPT" "F:/tmp/CMakeTest/Base", "F:/Project/Springhead/core")
message(STATUS ${RC})





# end: Springhead
