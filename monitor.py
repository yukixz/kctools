#!/usr/bin/env python3

import random
import subprocess
import sys
import time
import traceback

import requests


SERVERS = [
    '203.104.209.71',
    '203.104.209.87',
    '125.6.184.16',
    '125.6.187.205',
    '125.6.187.229',
    '125.6.187.253',
    '125.6.188.25',
    '203.104.248.135',
    '125.6.189.7',
    '125.6.189.39',
    '125.6.189.71',
    '125.6.189.103',
    '125.6.189.135',
    '125.6.189.167',
    '125.6.189.215',
    '125.6.189.247',
    '203.104.209.23',
    '203.104.209.39',
    '203.104.209.55',
    '203.104.209.102',
]

PATHS = [
    ('/kcs/Core.swf', 200919),

    ('/kcs/resources/image/slotitem/card/194.png', 0),
    ('/kcs/resources/image/slotitem/card/195.png', 0),
    ('/kcs/resources/image/slotitem/card/196.png', 0),
    ('/kcs/resources/image/slotitem/card/197.png', 0),
    ('/kcs/resources/image/slotitem/card/198.png', 0),
    ('/kcs/resources/image/slotitem/card/199.png', 0),
    ('/kcs/resources/image/slotitem/card/200.png', 0),

    ('/kcs/resources/swf/ships/mhqqhhvvpzxg.swf', 364350),  # 3
    ('/kcs/resources/swf/ships/rzgndzraoddu.swf', 366662),  # 4
    ('/kcs/resources/swf/ships/hbhkiyykheeq.swf', 0),  # 5
    ('/kcs/resources/swf/ships/boxlrnnmjkhb.swf', 0),  # 8
    ('/kcs/resources/swf/ships/jqvoyyolpqgv.swf', 0),  # 162
    ('/kcs/resources/swf/ships/igezlfrivcar.swf', 375343),  # 315
    ('/kcs/resources/swf/ships/fwywlrdttcoc.swf', 0),  # 333
    ('/kcs/resources/swf/ships/fuzvvipztlod.swf', 0),  # 335
    ('/kcs/resources/swf/ships/nyveugfueqrn.swf', 0),  # 336
    ('/kcs/resources/swf/ships/ospkpclnhxkj.swf', 0),  # 337
    ('/kcs/resources/swf/ships/yotuoourymyr.swf', 0),  # 338
    ('/kcs/resources/swf/ships/utbekttrwkug.swf', 0),  # 339
    ('/kcs/resources/swf/ships/tmodouudtfbl.swf', 0),  # 340
    ('/kcs/resources/swf/ships/zzjoppqteksh.swf', 0),  # 341
    ('/kcs/resources/swf/ships/rybmohpldpuq.swf', 0),  # 342
    ('/kcs/resources/swf/ships/qtuuhjmqmvfh.swf', 0),  # 433
    ('/kcs/resources/swf/ships/wmebertagnxm.swf', 0),  # 438
    ('/kcs/resources/swf/ships/tvieoobotato.swf', 0),  # 457
    ('/kcs/resources/swf/ships/fmsaumjkejlm.swf', 0),  # 472
    ('/kcs/resources/swf/ships/uesladlyqrru.swf', 0),  # 474
    ('/kcs/resources/swf/ships/sbvnvwfihmrd.swf', 0),  # 475
]


while True:
    server = random.choice(SERVERS)
    random.shuffle(PATHS)

    for path_t in PATHS:
        path, klen = path_t
        try:
            print("try", server, path)

            url = ''.join(('http://', server, path))
            resp = requests.head(url, timeout=4)
            rlen = int(resp.headers.get('Content-Length', -1))
            if resp.status_code != 200 or rlen == klen:
                continue

            # Monitored path changed!
            PATHS.remove(path_t)
            args = ['wget', url]
            print("!!", *args)
            # subprocess.Popen(args, stderr=subprocess.DEVNULL)
            p = subprocess.Popen(args)
            p.wait()

        except (requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout):
            print('timeout')
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            traceback.print_exc()

        time.sleep(1)
