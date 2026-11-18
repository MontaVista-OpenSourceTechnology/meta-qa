inherit pypi python_hatchling

LICENSE = "MPL-2.0"
PYPI_PACKAGE = "pytest_metadata"

SRC_URI[sha256sum] = "d2a29b0355fbc03f168aa96d41ff88b1a3b44a3b02acbe491801c98a048017c8"

LIC_FILES_CHKSUM = "file://LICENSE;md5=5d425c8f3157dbf212db2ec53d9e5132"

DEPENDS += "${PYTHON_PN}-hatch-vcs-native"
