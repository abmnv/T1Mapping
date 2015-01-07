cmake_minimum_required(VERSION 2.8.9)

project(T1Mapping)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://www.example.com/Slicer/Extensions/T1Mapping")
set(EXTENSION_CATEGORY "Examples")
set(EXTENSION_CONTRIBUTORS "Artem Mamonov (MGH Matrinos)")
set(EXTENSION_DESCRIPTION "This is T1 extension")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/T1Mapping.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/T1Mapping/Screenshots/1.png")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(T1Mapping)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
