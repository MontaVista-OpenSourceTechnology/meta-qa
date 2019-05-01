inherit pypi setuptools

LICENSE = "MPL-2.0"
PYPI_PACKAGE = "pytest-metadata"

SRC_URI[md5sum] = "40a4632c639b4b95ff4f7b050b29ca51"
SRC_URI[sha256sum] = "f962d1a2ecb57162a3067ba41958e726ed6eb017f69648cb9439e7635f841bc8"


LIC_FILES_CHKSUM = "file://LICENSE;md5=5d425c8f3157dbf212db2ec53d9e5132"

DEPENDS += "python-setuptools-scm-native"
