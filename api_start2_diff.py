#!/usr/bin/env python3

'''
Diff api_start2
Usage: api_start2_diff.py api_start2.old.json api_start2.new.json
'''

import json
import sys

SERVER = '203.104.209.102'
SRC = sys.argv[1]
DST = sys.argv[2]
JSON_KWARGS = {
    'ensure_ascii': False,
    'sort_keys': True,
}
# ^.+http://.+\n

with open(SRC, 'r') as f:
    src = json.loads(f.read())
with open(DST, 'r') as f:
    dst = json.loads(f.read())


################
# diff_ship
################

def print_ship(title, item):
    if 'api_sortno' in item:
        tmpl = '''\
ID: {api_id}, No. {api_sortno}
艦娘: {api_name}
耐久: {api_taik[0]} / {api_taik[1]}
火力: {api_houg[0]} / {api_houg[1]}
雷装: {api_raig[0]} / {api_raig[1]}
対空: {api_tyku[0]} / {api_tyku[1]}
装甲: {api_souk[0]} / {api_souk[1]}
運　: {api_luck[0]} / {api_luck[1]}
搭載: {_slot}
改造: Lv {api_afterlv} / 鋼材 {api_afterfuel} / 弾薬 {api_afterbull}
SWF: http://{SERVER}/kcs/resources/swf/ships/{api_filename}.swf
'''
        item['_slot'] = ', '.join(
            str(i) for i in item['api_maxeq'][:item['api_slot_num']])
    else:
        tmpl = '''\
ID: {api_id}
艦娘: {api_name}
wget http://{SERVER}/kcs/resources/swf/ships/{api_filename}.swf
'''
    print('==>', title)
    print(tmpl.format(SERVER=SERVER, **item))


def diff_ship(src, dst):
    ids = set()
    src_ship = {}
    dst_ship = {}
    for ship in src['api_mst_ship']:
        id_ = ship['api_id']
        ids.add(id_)
        src_ship[id_] = ship
    for ship in src['api_mst_shipgraph']:
        id_ = ship['api_id']
        if id_ in src_ship:
            src_ship[id_]['api_filename'] = ship['api_filename']
    for ship in dst['api_mst_ship']:
        id_ = ship['api_id']
        ids.add(id_)
        dst_ship[id_] = ship
    for ship in dst['api_mst_shipgraph']:
        id_ = ship['api_id']
        if id_ in dst_ship:
            dst_ship[id_]['api_filename'] = ship['api_filename']

    for id_ in sorted(ids):
        if id_ in src_ship and id_ in dst_ship:
            pass
        if id_ not in src_ship and id_ in dst_ship:
            print_ship('New Ship', dst_ship[id_])
        if id_ in src_ship and id_ not in dst_ship:
            print_ship('Removed Ship', src_ship[id_])

diff_ship(src, dst)


################
# diff_slotitem
################
SLOTITEM_KWS = (
    ('api_name', '装備'),
    ('api_houg', '火力'),
    ('api_raig', '雷装'),
    ('api_baku', '爆装'),
    ('api_tyku', '対空'),
    ('api_tais', '対潜'),
    ('api_souk', '装甲'),
    ('api_houm', '命中'),
    ('api_houk', '回避'),
    ('api_saku', '索敵'),
)


def print_item(title, item):
    print('==>', title)
    print("ID: {api_id}, No. {api_sortno}".format(**item))
    for k, d in SLOTITEM_KWS:
        if item.get(k, 0) != 0:
            print("{}: {}".format(d, item[k]))
    print('''\
wget http://{SERVER}/kcs/resources/image/slotitem/card/{id}.png -O {id}-card.png
wget http://{SERVER}/kcs/resources/image/slotitem/item_up/{id}.png -O {id}-up.png
wget http://{SERVER}/kcs/resources/image/slotitem/item_on/{id}.png -O {id}-on.png
wget http://{SERVER}/kcs/resources/image/slotitem/item_character/{id}.png -O {id}-character.png
'''.format(SERVER=SERVER, id=item['api_id']))


def diff_slotitem(src, dst):
    ids = set()
    src_item = {}
    dst_item = {}
    for item in src['api_mst_slotitem']:
        id_ = item['api_id']
        ids.add(id_)
        src_item[id_] = item
    for item in dst['api_mst_slotitem']:
        id_ = item['api_id']
        ids.add(id_)
        dst_item[id_] = item

    for id_ in sorted(ids):
        if id_ in src_item and id_ in dst_item:
            pass
        if id_ not in src_item and id_ in dst_item:
            print_item('New Item', dst_item[id_])
        if id_ in src_item and id_ not in dst_item:
            print_item('Removed Item', src_item[id_])

diff_slotitem(src, dst)
