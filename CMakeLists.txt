### setup project ###
cmake_minimum_required(VERSION 3.9)

project(solvaris
  VERSION 1.0
  DESCRIPTION "FIB module"
  LANGUAGES C Fortran
)

# Safety net
if(PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
  message(
    FATAL_ERROR
      "In-source builds not allowed. Please make a new directory (called a build directory) and run CMake from there.\n"
  )
endif()

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)


# Grab the variables from a local Python installation
# NumPy headers
execute_process(
  COMMAND "${PYTHON_EXECUTABLE}"
  -c "import numpy; print(numpy.get_include())"
  OUTPUT_VARIABLE NumPy_INCLUDE_DIRS
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
# F2PY headers
execute_process(
  COMMAND "${PYTHON_EXECUTABLE}"
  -c "import numpy.f2py; print(numpy.f2py.get_include())"
  OUTPUT_VARIABLE F2PY_INCLUDE_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Prepping the module
set(f2py_module_name "_solvaris")

file(GLOB fortran_src_file
     CONFIGURE_DEPENDS 
     "${CMAKE_SOURCE_DIR}/src/*.f90"
)
set(f2py_module_c "${f2py_module_name}module.c")
set(generated_module_file ${f2py_module_name}${PYTHON_EXTENSION_MODULE_SUFFIX})

# Target for enforcing dependencies
add_custom_target(genpyf
  DEPENDS ${fortran_src_file}
)

add_custom_command(
  OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/${f2py_module_c}"
  COMMAND ${PYTHON_EXECUTABLE}  -m "numpy.f2py"
                   ${fortran_src_file}
                   -m ${f2py_module_name}
                   --lower # Important
  DEPENDS ${fortran_src_file} # Fortran source
)

add_library(${generated_module_file} MODULE
            "${f2py_module_c}"
            "${F2PY_INCLUDE_DIR}/fortranobject.c"
            ${fortran_src_file})

target_include_directories(${generated_module_file} PUBLIC
                           ${F2PY_INCLUDE_DIR}
                           ${NumPy_INCLUDE_DIRS}
                          )

target_link_libraries(${generated_module_file} PRIVATE Python::Module)
set_target_properties(${generated_module_file} PROPERTIES PREFIX "")

# Linker fixes
if (UNIX)
  if (APPLE)
    set_target_properties(${generated_module_file} PROPERTIES
    LINK_FLAGS  '-Wl,-dylib,-undefined,dynamic_lookup')
  else()
    set_target_properties(${generated_module_file} PROPERTIES
  LINK_FLAGS  '-Wl,--allow-shlib-undefined')
  endif()
endif()

add_dependencies(${generated_module_file} genpyf)

install(TARGETS ${generated_module_file} DESTINATION solvaris)
