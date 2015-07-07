#!/usr/bin/python3.4

import os
import re

from portage import settings
from grs.Execute import Execute

def scan_profile_stack(pfile):
    datoms = []
    for profile in portage.settings.profiles:
        fpath = os.path.join(profile, pfile)
        datoms.append(portage.grabfile_package(fpath))
    atoms = []
    for d in portage.stack_lists(datoms, incremental=1):
        m = re.search('^\*?(.*)', d)
        atoms.append(m.group(1))
    return atoms


def get_blist():
    plist = scan_profile_stack('packages')
    blist = scan_profile_stack('packages.build')
    for p in plist:
        try:
            i = blist.index(portage.dep_getkey(p))
            blist[i] = p
        except ValueError:
            pass
    return ' '.join(blist)


use_flags = '-* bindist build %s' % settings['BOOTSTRAP_USE']
subchroot = '/tmp/stage1root'
cpu_flags = 'mmx sse sse2'
emerge_env = { 'USE' : use_flags, 'ROOT' : subchroot, 'CPU_FLAGS_X86' : cpu_flags }

cmd = 'emerge -bkNu1q sys-apps/baselayout'
Execute(cmd, timeout=None, extra_env=emerge_env)

cmd = 'emerge -bkNu1q %s' % get_blist()
Execute(cmd, timeout=None, extra_env=emerge_env)
