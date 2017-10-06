LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

SRC_NAME = "test_ltp.py"
QATEST_SECTION ?= "core"
SRC_URI = "file://${SRC_NAME}"

inherit qa-framework

do_install_qatest () {
	sed -i -e"s:##QATEST_BIN_DIR##:${QATEST_BIN_DIR}:g" ${WORKDIR}/${SRC_NAME}
	install ${WORKDIR}/${SRC_NAME} ${D}/${QATEST_SUITES_PATH}
}

RDEPENDS_${PN} = "ltp"
