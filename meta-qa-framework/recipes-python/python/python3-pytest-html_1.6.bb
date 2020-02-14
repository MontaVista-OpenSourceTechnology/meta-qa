inherit pypi setuptools3

LICENSE = "MPL-2.0"
PYPI_PACKAGE = "pytest-html"

SRC_URI[md5sum] = "ac956864a9b3392203dacd287ae450f0"
SRC_URI[sha256sum] = "a359de04273239587bd1a15b29b2266daeaf56b7a13f8224bc4fb3ae0ba72c3f"

# Per README.rst the license is fetched from 
# https://raw.githubusercontent.com/davehunt/pytest-html/master/LICENSE

SRC_URI += "file://LICENSE"

LIC_FILES_CHKSUM = "file://../LICENSE;md5=1dd4ea04332b4e6bbc65e59d7f2faf80"
