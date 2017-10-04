SUMMARY_${PN} ?= "${SUMMARY} - Package QA test files"
DESCRIPTION_${PN} ?= "${DESCRIPTION}  \
This package contains a test directory ${QATEST_PATH} for QA test purposes."

inherit qa-framework-dir

QATEST_SECTION ?= "meta"
QATEST_SUITES_PATH ?= "${QATEST_SUITES_DIR}/${QATEST_SECTION}"
FILES_${PN} = "${QATEST_SUITES_PATH}"
SECTION_${PN} = "QA/Testsuites"
ALLOW_EMPTY_${PN} = "1"
QATEST_ENABLED = "${@bb.utils.contains('DISTRO_FEATURES', 'qatest', '1', '0', d)}"
QATEST_ENABLED_class-native = ""
QATEST_ENABLED_class-nativesdk = ""
QATEST_ENABLED_class-cross-canadian = ""
RDEPENDS_${PN}-qatest_class-native = ""
RDEPENDS_${PN}-qatest_class-nativesdk = ""
RRECOMMENDS_${PN} = "mvtest"

PACKAGES = "${@bb.utils.contains('QATEST_ENABLED', '1', '${PN}', '', d)}"

do_configure_qatest() {
    :
}

do_configure_qatest_base() {
    do_configure_qatest
}

do_compile_qatest() {
    :
}

do_compile_qatest_base() {
    do_compile_qatest
}

do_install_qatest() {
    :
}

do_install_qatest_base() {
    install -d ${D}/${QATEST_SUITES_DIR}
    touch ${D}/${QATEST_SUITES_PATH}/__init__.py
    do_install_qatest
    chown -R root:root ${D}${QATEST_SUITES_PATH}
}

do_configure_qatest_base[dirs] = "${B}"
do_compile_qatest_base[dirs] = "${B}"
do_install_qatest_base[dirs] = "${B}"
do_install_qatest_base[cleandirs] = "${D}${QATEST_SUITES_PATH}"

addtask configure_qatest_base after do_configure before do_compile
addtask compile_qatest_base   after do_compile   before do_install
addtask install_qatest_base   after do_install   before do_package do_populate_sysroot

python () {
    if not bb.data.inherits_class('native', d) and not bb.data.inherits_class('cross', d):
        d.setVarFlag('do_install_qatest_base', 'fakeroot', '1')

    # Remove all '*qatest_base' tasks when qatest is not enabled
    if not(d.getVar('QATEST_ENABLED') == "1"):
        for i in ['do_configure_qatest_base', 'do_compile_qatest_base', 'do_install_qatest_base']:
            bb.build.deltask(i, d)
}
