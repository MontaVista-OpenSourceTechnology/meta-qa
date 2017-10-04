# 
# Copyright 2017 MontaVista LLC.
#
SUMMARY = "An open-source automated test suite based on pytest framework to perform a full-fledged QA"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://license.txt;md5=40bb041f1875a8c9a752e61e8c9bdd77"

SRCREV = "4ee7f34a5af6454d2d79973c3b6d849b0f3448d2"
SRC_URI = "\
	git://github.com/MontaVista-OpenSourceTechnology/mvtest.git \
	file://run-qatest \
	"

S = "${WORKDIR}/git"

inherit qa-framework-dir

QATEST_LOG ?= "qatest-${DISTRO}-${MACHINE}.html"
QATEST_CMD_OPTIONS ?= "-vv --html ${QATEST_LOG}"

do_configure () {
	cp ${WORKDIR}/run-qatest ${S}
		
	sed -i -e"s:##QATEST_PATH##:${QATEST_BIN_DIR}:g" ${S}/run-qatest
	sed -i -e"s:##QATESTS##:${QATEST_SUITES_DIR}:g" ${S}/run-qatest
	sed -i -e"s:##RESULTS_DIR##:${QATEST_RESULTS_DIR}:g" ${S}/run-qatest
	sed -i -e"s:##QATEST_CMD_OPTIONS##:${QATEST_CMD_OPTIONS}:g" ${S}/run-qatest
	sed -i -e"s:##QATEST_LOG##:${QATEST_LOG}:g" ${S}/run-qatest
}

do_compile[noexec] = "1"

do_install () {
        mkdir -p ${D}${QATEST_BIN_DIR}

        cp -a ${S}/* ${D}/${QATEST_BIN_DIR}

	install -m 755 ${S}/run-qatest ${D}${QATEST_BIN_DIR}
	chown -R root:root ${D}/${QATEST_BIN_DIR}
}

PACKAGES = "${PN}"

FILES_${PN} = "${QATEST_BIN_DIR}"

RDEPENDS_${PN} = "\
		python python-pytest python-pytest-html python-pytest-timeout python-pytest-metadata \
		python-colorlog python-paramiko python-ecdsa python-ansi2html python-pexpect \
		python-pynacl python-bcrypt python-cryptography python-asn1crypto \
		"
