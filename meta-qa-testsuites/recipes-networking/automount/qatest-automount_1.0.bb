LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

SRC_NAME = "test_automount.py"
QATEST_SECTION ?= "networking"

SRC_URI = "file://${SRC_NAME}"

inherit qa-framework kernel-check

do_install_qatest () {
	sed -i -e"s:##QATEST_BIN_DIR##:${QATEST_BIN_DIR}:g" ${WORKDIR}/${SRC_NAME}
	install ${WORKDIR}/${SRC_NAME} ${D}/${QATEST_SUITES_PATH}
}

REQUIRED_KERNEL_OPTIONS = "CONFIG_EXT2_FS CONFIG_EXT3_FS CONFIG_EXT4_FS CONFIG_AUTOFS4_FS"
RDEPENDS_${PN} = "autofs"
