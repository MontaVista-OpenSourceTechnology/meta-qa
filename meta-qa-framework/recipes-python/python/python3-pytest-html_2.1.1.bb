inherit pypi setuptools3

DEPENDS += "${PYTHON_PN}-setuptools-scm-native"

LICENSE = "MPL-2.0"
PYPI_PACKAGE = "pytest-html"

SRC_URI[sha256sum] = "6a4ac391e105e391208e3eb9bd294a60dd336447fd8e1acddff3a6de7f4e57c5"

# Per README.rst the license is fetched from 
# https://raw.githubusercontent.com/davehunt/pytest-html/master/LICENSE

SRC_URI += "file://LICENSE"

LIC_FILES_CHKSUM = "file://../LICENSE;md5=1dd4ea04332b4e6bbc65e59d7f2faf80"
