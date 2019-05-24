DESCRIPTION = "SSH2 protocol library"
HOMEPAGE = "https://github.com/paramiko/paramiko/"
SECTION = "devel/python"
LICENSE = "LGPLv2.1"
LIC_FILES_CHKSUM = "file://LICENSE;md5=fd0120fc2e9f841c73ac707a30389af5"

SRCNAME = "paramiko"

SRC_URI = "https://github.com/${SRCNAME}/${SRCNAME}/archive/${PV}.tar.gz"

SRC_URI[md5sum] = "47e41c2ccde1df35cf2e8691e21bb0b7"
SRC_URI[sha256sum] = "42ae99499d33060176059ce2d9b39a3b393852051e0dd27ae498b6c4cd64d80a"

S = "${WORKDIR}/${SRCNAME}-${PV}"

inherit setuptools

RDEPENDS_${PN} += "python-pycrypto python-pyasn1"
