#
# Copyright 2017-2020 MontaVista LLC.
#


SRC_URI += "file://run-qatest"
SRC_URI += "file://init"

QATEST_LOG ?= "qatest-${DISTRO}-${MACHINE}.html"
QATEST_CMD_OPTIONS ?= "-vv --html ${QATEST_LOG}"

inherit qa-framework-dir update-rc.d update-alternatives
INITSCRIPT_NAME = "zzzmvtest"
INITSCRIPT_PARAMS = "start 99 2 3 4 5 ."

ALTERNATIVE_PRIORITY = "90"
ALTERNATIVE_${PN} = "__init__.py"
ALTERNATIVE_LINK_NAME[__init__.py] = "${QATEST_SUITES_DIR}/__init__.py"

do_configure () {
	cp ${WORKDIR}/run-qatest ${S}
	cp ${WORKDIR}/init ${S}
		
	sed -i -e"s:##QATEST_PATH##:${QATEST_BIN_DIR}:g" ${S}/run-qatest
	sed -i -e"s:##QATESTS##:${QATEST_SUITES_DIR}:g" ${S}/run-qatest
	sed -i -e"s:##RESULTS_DIR##:${QATEST_RESULTS_DIR}:g" ${S}/run-qatest
	sed -i -e"s:##QATEST_CMD_OPTIONS##:${QATEST_CMD_OPTIONS}:g" ${S}/run-qatest
	sed -i -e"s:##QATEST_LOG##:${QATEST_LOG}:g" ${S}/run-qatest

	sed -i -e"s:##QATEST_PATH##:${QATEST_BIN_DIR}:g" ${S}/init
	sed -i -e"s:##QATESTS##:${QATEST_SUITES_DIR}:g" ${S}/init
	sed -i -e"s:##RESULTS_DIR##:${QATEST_RESULTS_DIR}:g" ${S}/init
	sed -i -e"s:##QATEST_CMD_OPTIONS##:${QATEST_CMD_OPTIONS}:g" ${S}/init
	sed -i -e"s:##QATEST_LOG##:${QATEST_LOG}:g" ${S}/init
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
        install ${S}/pytest.ini ${D}/${QATEST_BIN_DIR}
        install ${S}/requirements.txt ${D}/${QATEST_BIN_DIR}
        install ${S}/README.md ${D}/${QATEST_BIN_DIR}

        install -d ${D}${QATEST_SUITES_DIR}
        install ${S}/suites/__init__.py ${D}${QATEST_SUITES_DIR}

	install -m 755 ${S}/run-qatest ${D}${QATEST_BIN_DIR}
	chown -R root:root ${D}/${QATEST_BIN_DIR}
    grep "/usr/bin/env python" ${D}${QATEST_BIN_DIR} -r  | cut -d : -f 1 | xargs -n 1 sed -i -e "s,/usr/bin/env\ python,/usr/bin/env python3,"

	# zzz prefix makesure it is sorted near the end of the S99 initscripts
	install -d ${D}${sysconfdir}/init.d/
	install -m 0755 ${S}/init ${D}${sysconfdir}/init.d/zzzmvtest
}

PACKAGES = "${PN}"

FILES_${PN} = "${QATEST_BIN_DIR} ${QATEST_SUITES_DIR} ${sysconfdir}/init.d/zzzmvtest"

RDEPENDS_${PN} = "\
		python3-core python3-pytest python3-pytest-html python3-pytest-timeout python3-pytest-metadata \
		python3-colorlog python3-paramiko python3-ecdsa python3-ansi2html python3-pexpect \
		python3-nacl python3-pyasn1 python3-bcrypt python3-cryptography python3-asn1crypto bash \
		"
