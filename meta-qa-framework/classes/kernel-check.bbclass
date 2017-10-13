# Provides a means of checking within a recipe if particular kernel
# config options are enabled
#
# Copyright (C) 2016 Intel Corporation
#
# Example usage (within a recipe):
#
# inherit kernel-check
# REQUIRED_KERNEL_OPTIONS = "CONFIG_CGROUPS CONFIG_NAMESPACES"
#
# If one or more of the options aren't in the built kernel configuration
# you will get a warning at do_configure time.
#
# You can also use the check_kernel_config_options() function to do
# explicit checks yourself (and perform a different action).

def check_kernel_config_options(options, d):
    """
    A function you can use to do explicit checks for kernel config
    options from python code
    """

    if isinstance(options, str):
        required = options.split()
    else:
        required = options[:]
    missing = []
    diffvalue = []
    if required:
        with open(d.expand('${STAGING_KERNEL_BUILDDIR}/.config'), 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                linesplit = line.rstrip().split('=', 1)
                if len(linesplit) < 2:
                    continue
                linevalue = linesplit[1]
                for req in required:
                    found = False
                    if '|' in req:
                        for reqitem in req.split('|'):
                            if reqitem == linesplit[0]:
                                if linevalue in ['y', 'm']:
                                    found = True
                                    break
                    else:
                        reqsplit = req.split('=', 1)
                        # Can check for CONFIG_OPTION or CONFIG_OPTION=value
                        if len(reqsplit) > 1:
                            reqvalue = reqsplit[1]
                        else:
                            reqvalue = None
                        if reqsplit[0] == linesplit[0]:
                            if reqvalue is None:
                                if linevalue not in ['y', 'm']:
                                    diffvalue.append((reqsplit[0], 'y or m', linevalue))
                            elif reqvalue.strip("'\"") != linevalue.strip("'\""):
                                diffvalue.append((reqsplit[0], reqvalue, linevalue))
                            found = True

                    if found:
                        required.remove(req)
                        break

        for req in required:
            reqsplit = req.split('=', 1)
            if len(reqsplit) > 1:
                if reqsplit[1] == 'n':
                    continue
                missing.append('%s=%s' % reqsplit)
            else:
                missing.append('%s' % req)

    return missing, diffvalue


python check_kernel_config() {
    pn = d.getVar('PN', True)
    required = d.getVar('REQUIRED_KERNEL_OPTIONS', True) or ''
    if ' | ' in required:
        bb.error('Invalid REQUIRED_KERNEL_OPTIONS value - cannot have spaces around |')
    if ' = ' in required:
        bb.error('Invalid REQUIRED_KERNEL_OPTIONS value - cannot have spaces around =')
    missing, diffvalue = check_kernel_config_options(required, d)
    if missing or diffvalue:
        reqstr = '\n  '.join(missing + ['%s=%s (actual value %s)' % item for item in diffvalue])
        # Just warn here for cases like linux-dummy where we don't actually
        # know the final config
        bb.warn('The kernel you are building against is missing the following required configuration options:\n  %s' % reqstr)
}

python() {
    if d.getVar('REQUIRED_KERNEL_OPTIONS', True):
        d.appendVar('DEPENDS', ' virtual/kernel')
        d.appendVarFlag('do_configure', 'prefuncs', ' check_kernel_config')
        d.appendVarFlag('do_configure', 'depends', ' virtual/kernel:do_shared_workdir')
}
