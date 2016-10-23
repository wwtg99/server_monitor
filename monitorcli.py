import argparse
import json


def parse_args():
    parse = argparse.ArgumentParser(prog='Server Monitor', description='Get server information.')
    parse.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')
    parse.add_argument('--system', default='linux', help='set operating system of server, default linux', choices=['linux'])
    parse.add_argument('-s', '--service', nargs='*', help='services to show in service info')
    parse.add_argument('info', nargs='+', help='which kind of info to show', choices=['cpu', 'mem', 'load', 'service', 'all'])
    return parse.parse_args()


def get_info(monitor, info, param=None):
    infos = {
        'cpu': monitor.cpu_info,
        'load': monitor.load_stat,
        'mem': monitor.mem_info,
        'service': monitor.service_info
    }
    res = {}
    if 'all' in info:
        for i in infos:
            if i == 'service':
                p = param['service'] if 'service' in param else None
                res[i] = infos[i](p)
            else:
                res[i] = infos[i]()
    else:
        for i in info:
            if i == 'service':
                pa = param['service'] if 'service' in param else None
                res[i] = infos[i](pa)
            else:
                res[i] = infos[i]()
    return res


if __name__ == '__main__':
    args = parse_args()
    if args.system == 'linux':
        from monitors import linux
        p = {}
        if args.service:
            p['service'] = args.service
        res = get_info(linux, args.info, p)
        print(json.dumps(res))
        

