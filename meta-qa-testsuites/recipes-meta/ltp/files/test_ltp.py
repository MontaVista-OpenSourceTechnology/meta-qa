#!/usr/bin/env python3
#
# Author: SriHarsha (ssriram@mvista.com)
#
# License: MIT

import pytest
import sys
from pathlib import Path
sys.path.insert(0, "##QATEST_BIN_DIR##")
from apis.utils import run_cmd

ltpdir = "/opt/ltp/"
default_scen = ltpdir + "scenario_groups/default"
# network_scen = ltpdir + "scenario_groups/network"


def setup_ltp():
    if not (Path(ltpdir) / "runltp").is_file():
        pytest.skip("LTP runltp is not installed", allow_module_level=True)
    testnames = []
    commands = []
    try:
        scenarios = Path(default_scen).read_text().splitlines()
    except FileNotFoundError:
        pytest.skip("LTP default scenario list is not installed",
                    allow_module_level=True)
    for line in scenarios:
        scenario = line.split('#', 1)[0].strip()
        if not scenario:
            continue
        scenario_file = Path(ltpdir) / "runtest" / scenario
        try:
            lines = scenario_file.read_text().splitlines()
        except FileNotFoundError:
            testnames.append("missing-scenario-" + scenario)
            commands.append(pytest.param(
                None, marks=pytest.mark.skip(
                    reason="LTP scenario is not installed: %s" % scenario_file)))
            continue
        for lineno, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            entry = line.split(None, 1)
            if len(entry) != 2:
                raise ValueError("%s:%d: expected a test name and command" %
                                 (scenario_file, lineno))
            name, command = entry
            testnames.append(name)
            commands.append(command)
    return testnames, commands


if 'sphinx' in sys.modules:
    testnames, commands = [], []
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
