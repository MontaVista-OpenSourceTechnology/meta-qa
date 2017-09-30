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

do_configure[noexec] = "1"
do_compile[noexec] = "1"

QATEST_PATH ?= "/opt/qatest"
RESULTS_DIR ?= "/results"
QATESTS ?= "suites"
QATEST_LOG ?= "qatest-${DISTRO}-${MACHINE}.html"
QATEST_CMD_OPTIONS ?= "-vv --html ${QATEST_LOG}"

do_install () {
        mkdir -p ${D}${QATEST_PATH}
        cp -a ${S}/* ${D}${QATEST_PATH}
	chown -R root:root ${D}${QATEST_PATH}

	install  ${WORKDIR}/run-qatest ${S}
		
	sed -i -e"s:##QATEST_PATH##:${QATEST_PATH}:g" ${S}/run-qatest
	sed -i -e"s:##QATESTS##:${QATESTS}:g" ${S}/run-qatest
	sed -i -e"s:##RESULTS_DIR##:${RESULTS_DIR}:g" ${S}/run-qatest
	sed -i -e"s:##QATEST_CMD_OPTIONS##:${QATEST_CMD_OPTIONS}:g" ${S}/run-qatest
	sed -i -e"s:##QATEST_LOG##:${QATEST_LOG}:g" ${S}/run-qatest

	install -m 755  ${S}/run-qatest ${D}${QATEST_PATH}/run-qatest
}

PACKAGES = "${PN}"

FILES_${PN} = "${QATEST_PATH}"

RDEPENDS_${PN} = "\
		python python-pytest python-pytest-html python-pytest-timeout python-pytest-metadata \
		python-colorlog python-paramiko python-ecdsa python-ansi2html python-pexpect \
		python-pynacl python-bcrypt python-cryptography python-asn1crypto \
		"
