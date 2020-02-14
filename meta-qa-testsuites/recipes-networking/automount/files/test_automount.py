#!/usr/bin/env python3
#
# Author: Prem Karat (pkarat@mvista.com)
# License: MIT


import pytest
import re
import time
import sys
sys.path.insert(0, "##QATEST_BIN_DIR##")
from apis.utils import check_kernel_configs
from apis.utils import log
from apis.utils import run_cmd


@pytest.fixture(scope="module")
def check_kernconfigs():
    configs = ['EXT3_FS', 'EXT4_FS', 'AUTOFS4_FS', 'NFS_FS']
    if not check_kernel_configs(configs):
        pytest.skip('Missing required kernel configs')


@pytest.fixture(scope="function")
def setup_test():
    run_cmd('/etc/init.d/autofs stop', check_rc=False)
    run_cmd('mkdir /autofsmntpnt', check_rc=False)
    run_cmd('mv /etc/auto.master /etc/auto.master.org', check_rc=False)
    run_cmd('mv /etc/exports /etc/exports.org', check_rc=False)
    log.info('test setup completed')


def verify_output(out, stat):
    found = re.findall(r"%s" % stat, out, re.M)
    if not found:
        return False
    return True


def getloopdev(fstype, imgname):
    run_cmd('dd if=/dev/zero of=/%s bs=1024 count=5000' % imgname)
    ldev = run_cmd('losetup -f')
    if not ldev:
        log.error('FAIL: No unused loop device!')
        return ''
    if not run_cmd('losetup %s /%s' % (ldev, imgname)):
        log.error('FAIL: associate %s with %s' % (ldev, imgname))
        return ''
    if not run_cmd('mkfs -t %s %s' % (fstype, ldev)):
        log.error('FAIL: create %s on %s' % (fstype, ldev))
        return ''
    return ldev


def mount_nfs_server(dname, devname):
    run_cmd('mkdir %s' % dname, check_rc=False)
    if not run_cmd('mount -t ext3 %s %s' % (devname, dname)):
        log.error('FAIL: mount %s on %s' % (devname, dname))
        return False
    return True


def exportfs_nfs_server(dname):
    run_cmd('mv /etc/exports /etc/exports.org', check_rc=False)
    fd = open("/etc/exports", "w")
    data = "%s *(rw,sync,no_root_squash,no_subtree_check,no_all_squash)\n" \
           % dname
    fd.write(data)
    fd.close()
    if not run_cmd('exportfs -ra'):
        log.error('FAIL: export NFS server')
        return False
    out = run_cmd('exportfs')
    if not verify_output(out, '%s.*world.*' % dname):
        log.error('FAIL: export NFS server')
        return False
    log.info('PASS: %s - NFS server exported' % dname)
    return True


def update_test_mapfile(mapfile, mntpnt, opts, location):
    # Updating auto.test
    fd = open(mapfile, "w")
    data = mntpnt + ' ' + opts + ' ' + location + '\n'
    fd.write(data)
    fd.close()
    out = run_cmd('cat %s' % mapfile)
    if not verify_output(out, '.*%s.*%s' % (mntpnt, location)):
        log.error('FAIL: update %s\n%s' % (mapfile, out))
        return False
    log.info('PASS: %s updated\n%s' % (mapfile, out))
    return True


def update_master_mapfile(mntpnt, mapfile, opts):
    # Updating auto.master
    fd = open('/etc/auto.master', "w")
    data = mntpnt + ' ' + mapfile + ' ' + opts + '\n'
    fd.write(data)
    fd.close()
    out = run_cmd('cat /etc/auto.master')
    if not verify_output(out, '.*%s.*%s' % (mntpnt, mapfile)):
        log.error('FAIL: /etc/auto.master update\n%s' % out)
        return False
    log.info('PASS: /etc/auto.master updated\n%s' % out)
    return True


def start_autofs():
    log.info('starting autofs service')
    return run_cmd('/etc/init.d/autofs start')


def stop_autofs():
    log.info('stopping autofs service')
    return run_cmd('/etc/init.d/autofs stop')


def is_autofs_mounted(mapfile):
    return run_cmd('mount | grep %s | grep autofs' % mapfile)


def create_file_nfs_server(dname, fname):
    return run_cmd('touch %s/%s' % (dname, fname))


def file_on_mntpnt(mntpnt, fname, rc=True):
    return run_cmd('ls %s/%s' % (mntpnt, fname), check_rc=rc)


def file_read_write_mntpnt(mntpnt, fname):
    fd = open('%s/%s' % (mntpnt, fname), "w")
    data = 'test read write on nfs client'
    fd.write(data)
    fd.close()
    out = run_cmd('cat %s/%s' % (mntpnt, fname))
    if not verify_output(out, data):
        log.error('FAIL: read/write on %s/%s' (mntpnt, fname))
        return False
    log.info('PASS: read/write on %s/%s' % (mntpnt, fname))
    return True


@pytest.mark.parametrize('fstype', ['nfs', 'ext3', 'ext4'])
def test_autofs(request, check_kernconfigs, setup_test, fstype):
    """
    Tests for kernel-based automount utility for NFS and local FS based on
    ext3 & ext4. Also the timeout feature of autofs is also tested.
    """
    mapfile = '/auto.test'
    autofs_mntpnt = '/autofsmntpnt'
    master_opts = '--timeout=20'
    ltimeout = [10, 60, 300]

    def cleanup():
        imgs = ['nfsimg', 'ext3img', 'ext4img']
        for img in imgs:
            ldev = run_cmd("losetup -j /%s | cut -d ':' -f1" % img,
                           check_rc=False)
            if img == 'nfsimg':
                run_cmd('umount /nfs_server', check_rc=False)
                run_cmd('rm -rf /nfs_server', check_rc=False)
            if ldev:
                run_cmd('losetup -d %s' % ldev, check_rc=False)
            run_cmd('rm -rf /%s' % img, check_rc=False)
        run_cmd('mv /etc/auto.master.org /etc/auto.master',
                check_rc=False)
        run_cmd('mv /etc/exports.org /etc/exports',
                check_rc=False)
        run_cmd('exportfs -ra', check_rc=False)
        run_cmd('rm -rf %s' % autofs_mntpnt, check_rc=False)
        run_cmd('rm -rf %s' % mapfile, check_rc=False)
        run_cmd('/etc/init.d/autofs stop', check_rc=False)
    request.addfinalizer(cleanup)
    if 'nfs' in fstype:
        ser_dname = '/nfs_server'
        cli_dname = 'nfs_client'
        test_opts = '-fstype=nfs,nolock'
        location = '127.0.0.1:%s' % ser_dname
        ser_fname = 'server_file'
        nfs_cli_mntpnt = autofs_mntpnt + '/' + cli_dname
        ldev = getloopdev('ext3', 'nfsimg')
        assert ldev
        assert mount_nfs_server(ser_dname, ldev)
        assert exportfs_nfs_server(ser_dname)
        assert update_test_mapfile(mapfile, cli_dname, test_opts, location)
        assert update_master_mapfile(autofs_mntpnt, mapfile, master_opts)
        assert start_autofs()
        assert is_autofs_mounted(mapfile)
        log.info('PASS: %s mounted as type autofs' % mapfile)
        assert create_file_nfs_server(ser_dname, ser_fname)
        log.info('PASS: %s/%s created on NFS server'
                 % (ser_dname, ser_fname))
        if not file_on_mntpnt(nfs_cli_mntpnt, ser_fname):
            log.error('FAIL: %s/%s: no such file on NFS client.'
                      % (nfs_cli_mntpnt, ser_fname))
        log.info('PASS: %s/%s: exits on NFS client.'
                 % (nfs_cli_mntpnt, ser_fname))
        assert file_read_write_mntpnt(nfs_cli_mntpnt, 'tempfile')
        assert stop_autofs()
        if file_on_mntpnt(nfs_cli_mntpnt, ser_fname, rc=False):
            log.error('FAIL: %s still mounted after autofs stopped'
                      % nfs_cli_mntpnt)
            assert False
        log.info('PASS: %s: unmounted' % nfs_cli_mntpnt)
        log.info('*************************************')
        log.info('Testing for automount timeout feature')
        log.info('*************************************')
        for val in ltimeout:
            master_opts = '--timeout=%s' % val
            assert update_master_mapfile(autofs_mntpnt, mapfile, master_opts)
            assert start_autofs()
            log.info('sleeping for %d seconds' % val)
            time.sleep(val + 20)
            if run_cmd('ls %s | grep %s' % (autofs_mntpnt, cli_dname),
                       check_rc=False):
                log.error('FAIL: %s still mounted after timeout %s seconds'
                          % (nfs_cli_mntpnt, val))
                assert False
            log.info('PASS: %s: unmounted after timeout %s seconds'
                     % (nfs_cli_mntpnt, val))
    else:
        img = fstype + 'img'
        cli_dname = fstype + 'mnt'
        test_opts = '-fstype=%s' % fstype
        fs_mntpnt = autofs_mntpnt + '/' + cli_dname
        ldev = getloopdev(fstype, img)
        assert ldev
        location = ':%s' % ldev
        assert update_test_mapfile(mapfile, cli_dname, test_opts, location)
        assert update_master_mapfile(autofs_mntpnt, mapfile, master_opts)
        assert start_autofs()
        assert is_autofs_mounted(mapfile)
        log.info('PASS: %s mounted as type autofs' % mapfile)
        assert file_read_write_mntpnt(fs_mntpnt, 'tempfile')
        assert stop_autofs()
        if file_on_mntpnt(fs_mntpnt, 'tempfile', rc=False):
            log.error('FAIL: %s still mounted after autofs stopped'
                      % fs_mntpnt)
            assert False
        log.info('PASS: %s: unmounted' % fs_mntpnt)
        log.info('*************************************')
        log.info('Testing for automount timeout feature')
        log.info('*************************************')
        for val in ltimeout:
            master_opts = '--timeout=%s' % val
            assert update_master_mapfile(autofs_mntpnt, mapfile, master_opts)
            assert start_autofs()
            log.info('sleeping for %d seconds' % val)
            time.sleep(val + 20)
            if run_cmd('ls %s | grep %s' % (autofs_mntpnt, cli_dname),
                       check_rc=False):
                log.error('FAIL: %s still mounted after timeout %s seconds'
                          % (fs_mntpnt, val))
                assert False
            log.info('PASS: %s: unmounted after timeout %s seconds'
                     % (fs_mntpnt, val))

