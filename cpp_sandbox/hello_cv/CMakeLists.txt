cmake_minimum_required(VERSION 2.8)
project( code_cv )
find_package( OpenCV REQUIRED )
add_executable( code_cv code_cv.cpp )
target_link_libraries( code_cv ${OpenCV_LIBS} )