#!/usr/bin/env python3
#
# Author: SriHarsha (ssriram@mvista.com)
#
# License: MIT

import pytest
import sys
sys.path.insert(0, "##QATEST_BIN_DIR##")
from apis.utils import run_cmd

ltpdir = "/opt/ltp/"
default_scen = ltpdir + "scenario_groups/default"
# network_scen = ltpdir + "scenario_groups/network"


def setup_ltp():
    chk_ltp = run_cmd("ls %s/runltp 2>/dev/null" % ltpdir)
    assert chk_ltp
    testnames = []
    commands = []
    files = [line.rstrip('\n') for line in open(default_scen)]
    open("testfilecmds", "w+")
    for tests in files:
        fin = open(ltpdir + "runtest/" + tests, "r")
        data2 = fin.read()
        fout = open("testfilecmds", "a")
        fout.write(data2)
        fout.close()
    f = open('testfilecmds', 'r')
    for line in f:
        if line.strip():
            if not line.lstrip().startswith('#'):
                testnames.append(line.split(None, 1)[0])
                commands.append(line.split(None, 1)[1])
    commands = [s.strip() for s in commands]
    run_cmd("rm -rf testfilecmds")
    return testnames, commands


if 'sphinx' in sys.modules:
    testnames, commands = 0, 0
else:
    testnames, commands = setup_ltp()


@pytest.mark.p1
@pytest.mark.cg7
@pytest.mark.cgx
@pytest.mark.ph2
@pytest.mark.timeout(1800)
@pytest.mark.parametrize('ltp_command', commands, ids=testnames)
def test_ltp(ltp_command):
    """
    Running ltp
    """
    if ltp_command == 'memcg_stress':
        pytest.skip('memcg_stress is skipped')
    else:
        assert run_cmd("sync; export PATH=%stestcases/bin:$PATH;"
                       "export LTPROOT=%s ; export TMPDIR=/tmp;"
                       " %s" % (ltpdir, ltpdir, ltp_command),
                       wdir=ltpdir)
