from collections import OrderedDict
import os


def cpu_info():
    """
    Get cpuinfo from /proc/cpuinfo.

    :return: cpu info
    :rtype: OrderedDict
    """
    cpuinfo = OrderedDict()
    procinfo = OrderedDict()
    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                # end of one processor
                cpuinfo['proc%s' % nprocs] = procinfo
                nprocs = nprocs + 1
                # Reset
                procinfo = OrderedDict()
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0].strip()] = ''

    return cpuinfo


def load_stat():
    """
    Get average load stat from /proc/loadavg.

    :return:
    :rtype: dict
    """
    loadavg = {}
    f = open("/proc/loadavg")
    con = f.read().split()
    f.close()
    loadavg['lavg_1'] = con[0]
    loadavg['lavg_5'] = con[1]
    loadavg['lavg_15'] = con[2]
    loadavg['nr'] = con[3]
    loadavg['last_pid'] = con[4]
    return loadavg


def mem_info():
    """
    Get memory info from /proc/meminfo.

    :return:
    :rtype: OrderedDict
    """
    meminfo = OrderedDict()
    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo


def service_info(service=None):
    """
    Get service status by systemctl.

    :param service:
    :return:
    :rtype: OrderedDict
    """
    if service:
        res = OrderedDict()
        for s in service:
            cmd = 'systemctl list-units %s' % s
            p = os.popen(cmd)
            lines = p.readlines()
            if len(lines) > 2 and lines[0][0:4] == 'UNIT':
                l = lines[1].strip().split()
                res[s] = {'load': l[1], 'active': l[2], 'sub': l[3], 'description': ' '.join(l[4:])}
            else:
                res[s] = {'load': 'not-found', 'active': 'inactive', 'sub': 'dead', 'description': ''}
    else:
        res = OrderedDict()
        cmd = 'systemctl list-units'
        p = os.popen(cmd)
        lines = p.readlines()
        if len(lines) > 2 and lines[0].strip()[0:4] == 'UNIT':
            for l in lines:
                l = l.strip()
                if not l:
                    break
                ls = l.split()
                res[ls[0]] = {'load': ls[1], 'active': ls[2], 'sub': ls[3], 'description': ' '.join(ls[4:])}
    return res

