cmake_minimum_required(VERSION 3.13)
project(libarithmetic C)

set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR})
set(CMAKE_C_STANDARD 11)
set(CMAKE_BUILD_TYPE Debug)

find_package(Criterion REQUIRED)

add_library(arithmetic SHARED
        src/arithmetic.c
        )

include_directories(include/)


# TESTS

set(TEST_LIBS arithmetic ${CRITERION_LIBRARY})

# Buffer tests
add_executable(test-arithmetic 
        tests/main.c
        tests/test_add.c
        tests/test_multiply.c)
target_link_libraries(test-arithmetic ${TEST_LIBS})


add_custom_target(grade
        DEPENDS ./build/results.json
        COMMAND python3 ../tests/grade.py --report-file results.json)
