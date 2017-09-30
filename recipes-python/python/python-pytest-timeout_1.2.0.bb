SUMMARY = "py.test plugin to abort hanging tests"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d8048cd156eda3df2e7f111b0ae9ceff"

PYPI_PACKAGE = "pytest-timeout"

SRC_URI[md5sum] = "83607d91aa163562c7ee835da57d061d"
SRC_URI[sha256sum] = "c29e3168f10897728059bd6b8ca20b28733d7fe6b8f6c09bb9d89f6146f27cb8"

inherit pypi setuptools

RDEPENDS_${PN} = "python-py"
