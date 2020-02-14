#
# Copyright 2017-2020 MontaVista LLC.
#

inherit qa-framework-dir

include mvtest-2.0.inc

do_configure[noexec] = "1"
do_compile[noexec] = "1"

do_install () {
        install -d ${D}${QATEST_SUITES_DIR}/sample

        cp -a ${S}/suites/* ${D}${QATEST_SUITES_DIR}/sample/.
	chown -R root:root ${D}/${QATEST_SUITES_DIR}/sample
}

PACKAGES = "${PN}"
FILES_${PN} = "${QATEST_SUITES_DIR}/sample"

RDEPENDS_${PN} = "mvtest"
