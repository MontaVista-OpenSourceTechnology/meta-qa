DESCRPTION = "ansi2html - Convert text with ANSI color codes to HTML or to LaTeX"
HOMEPAGE = "https://github.com/ralphbean/ansi2html"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d32239bcb673463ab874e80d47fae504"
LICENSE = "GPLv3"

inherit pypi setuptools

PYPI_PACKAGE = "ansi2html"

SRC_URI[md5sum] = "cc59801e85ad559084373c43176e7751"
SRC_URI[sha256sum] = "3e5d5ada557e0bbe3e204a686f959de17f76c86c20615c034767e5ebdc0740f1"

RDEPENDS_${PN} = "python-six"
