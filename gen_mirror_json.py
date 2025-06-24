#!/usr/bin/env python
from __future__ import print_function
import hashlib
import json
import os
import re
import sys
import zipfile

from datetime import datetime
from time import mktime

if len(sys.argv) < 2:
    print("usage python {} /path/to/mirror/base/url".format(sys.argv[0]))
    sys.exit()

FILE_BASE = sys.argv[1]
builds = {}

for f in [os.path.join(dp, f) for dp, dn, fn in os.walk(FILE_BASE) for f in fn]:
    data = open(f, "rb")
    filename = f.split('/')[-1]
    parts = os.path.splitext(filename)[0].split('-')
    if len(parts) < 6:
        print("Invalid filename format:", filename, file=sys.stderr)
        data.close()
        continue
    # parts: [ROM_NAME, ANDROID_VERSION, DATE, DEVICE, VERSION, OFFICIAL]
    builddate = parts[-5]
    device = parts[-4]
    version = parts[-3]
    buildtype = parts[-2]
    # OFFICIAL/UNOFFICIALはparts[-1]だが、typeとして使う
    print('hashing sha256 for {}'.format(filename), file=sys.stderr)
    sha256 = hashlib.sha256()
    for buf in iter(lambda : data.read(128 * 1024), b''):
        sha256.update(buf)
    data.close()
    # 日付取得処理
    timestamp = None
    try:
        with zipfile.ZipFile(f, 'r') as update_zip:
            build_prop = update_zip.read('system/build.prop').decode('utf-8')
            timestamp = int(re.findall('ro.build.date.utc=([0-9]+)', build_prop)[0])
    except Exception as e:
        try:
            timestamp = int(mktime(datetime.strptime(builddate, '%Y%m%d').timetuple()))
        except Exception as e2:
            timestamp = int(os.path.getmtime(f))
    builds.setdefault(device, []).append({
        'sha256': sha256.hexdigest(),
        'size': os.path.getsize(f),
        'date': '{}-{}-{}'.format(builddate[0:4], builddate[4:6], builddate[6:8]) if len(builddate) == 8 and builddate.isdigit() else str(builddate),
        'datetime': timestamp,
        'filename': filename,
        'filepath': f.replace(FILE_BASE, ''),
        'version': version,
        'type': buildtype.lower()
    })
for device in builds.keys():
    builds[device] = sorted(builds[device], key=lambda x: x['date'])
print(json.dumps(builds, sort_keys=True, indent=4))
