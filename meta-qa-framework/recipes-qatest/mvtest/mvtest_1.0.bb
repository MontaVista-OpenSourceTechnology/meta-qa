
include mvtest.inc

SRC_URI += "file://run-qatest"

QATEST_LOG ?= "qatest-${DISTRO}-${MACHINE}.html"
QATEST_CMD_OPTIONS ?= "-vv --html ${QATEST_LOG}"

inherit qa-framework-dir

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
        install -d ${D}${QATEST_BIN_DIR}
        install -d ${D}${QATEST_BIN_DIR}/apis
        install -d ${D}${QATEST_BIN_DIR}/docs

        install ${S}/apis/* ${D}/${QATEST_BIN_DIR}/apis/.
        install ${S}/docs/* ${D}/${QATEST_BIN_DIR}/docs/.
        install ${S}/conftest.py ${D}/${QATEST_BIN_DIR}
        install ${S}/license.txt ${D}/${QATEST_BIN_DIR}

        install -d ${D}${QATEST_SUITES_DIR}
        install ${S}/suites/__init__.py ${D}${QATEST_SUITES_DIR}

	install -m 755 ${S}/run-qatest ${D}${QATEST_BIN_DIR}
	chown -R root:root ${D}/${QATEST_BIN_DIR}
}

PACKAGES = "${PN}"

FILES_${PN} = "${QATEST_BIN_DIR} ${QATEST_SUITES_DIR}"

RDEPENDS_${PN} = "\
		python python-pytest python-pytest-html python-pytest-timeout python-pytest-metadata \
		python-colorlog python-paramiko python-ecdsa python-ansi2html python-pexpect \
		python-pynacl python-bcrypt python-cryptography python-asn1crypto \
		"
