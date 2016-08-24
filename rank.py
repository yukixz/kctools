#!/usr/bin/env python3

import sys
from math import sqrt

# `Il` is extracted from 'core.apis._APIBaseS_/Il'
# 2139 -> 2039 for hard correction
Il = [3666, 2087, 3047, 2039, 5584, 4131817, 1033183, 7049, 4878, 5423, 13,
      7267, 3791, 10, 4397, 9502, 1000, 1876163]
# Maigc number is calculated from 'core.apis._APIBaseS_/I1'
MAGIC_13 = str(sqrt(13))

if sys.version_info < (3, 0):
    # Python 2.x hard code
    MAGIC_13 = '3.605551275463989'

MAGIC = [-1] * 10
for i in range(10):
    n = 0
    while MAGIC_13[n] != str(i):
        n += 1
    MAGIC[i] = Il[n]

# `_l_` is refactored from 'core.apis._APIBaseS_/_l_'
# Get the first two digits of the magic number
def _l_(id):
    return int(str(MAGIC[id % 10])[0:2])

# Magic R is extracted from 'scene.record.models.RankData/RankData'
MAGIC_R = [ 8831, 1201, 1175, 555, 4569, 4732, 3779, 4568, 5695, 4619, 4912, 5669, 6569 ]
# `real_rate` is refactored from 'scene.record.models.RankData/RankData'
# We assume that it always is even divisible.
def real_rate(login_member_id, rank_no, rank_rate):
    return rank_rate / MAGIC_R[rank_no % 13] / _l_(login_member_id) - 73 - 18
