#!/usr/bin/env python3

from math import sqrt

# `Il` is extracted from 'core.apis._APIBaseS_/Il'
Il = [2966, 7966, 1553, 2139, 3299, 4131817, 1033183, 5855, 7803, 6443, 13,
      7157, 3791, 10, 9187, 9115, 1000, 1876163]
# Maigc number is calculated from 'core.apis._APIBaseS_/I1'
MAGIC_13 = str(sqrt(13))
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
