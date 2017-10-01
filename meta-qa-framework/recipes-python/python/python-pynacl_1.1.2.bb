DESCRIPTION = "Python binding to the Networking and Cryptography (NaCl) library"
HOMEPAGE = "https://github.com/pyca/pynacl"
SECTION = "devel/python"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=8cc789b082b3d97e1ccc5261f8594d3f"

DEPENDS = "libsodium-native python-cffi-native"

PYPI_PACKAGE = "PyNaCl"

SRC_URI[md5sum] = "1963c14272a42585676e74cf6292f4e3"
SRC_URI[sha256sum] = "32f52b754abf07c319c04ce16905109cab44b0e7f7c79497431d3b2000f8af8c"

inherit setuptools pypi

do_compile_prepend () {
	sed -i -e 's:configure, "--dis:configure, "--host=${TARGET_SYS}", "--dis:g' \
	-e 's:.*make.*check.*:#&:g' \
	${S}/setup.py

}

RDEPENDS_${PN} = "libsodium"
