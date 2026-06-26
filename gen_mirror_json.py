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

def read_android_metadata(path, *keys):
    ret = [None] * len(keys)
    try:
        with zipfile.ZipFile(path, 'r') as f:
            if "META-INF/com/android/metadata" in f.namelist():
                metadata_content = f.read("META-INF/com/android/metadata").decode('utf-8')
                for line in metadata_content.splitlines():
                    if "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    if key in keys:
                        ret[keys.index(key)] = value

    except Exception as e:
        print("Failed to read metadata for {}: {}".format(path, e), file=sys.stderr)

    return ret

if len(sys.argv) < 2:
    print("usage python {} /path/to/mirror/base/url".format(sys.argv[0]))
    sys.exit()

FILE_BASE = sys.argv[1]
builds = {}

for f in [os.path.join(dp, f) for dp, dn, fn in os.walk(FILE_BASE) for f in fn]:
    filename = f.split('/')[-1]
    if not filename.endswith('.zip'):
        continue

    data = open(f, "rb")
    filename = f.split('/')[-1]
    parts = os.path.splitext(filename)[0].split('-')
    if len(parts) < 6:
        print("Invalid filename format:", filename, file=sys.stderr)
        data.close()
        continue

    builddate = parts[-4]
    device = parts[-3]
    version = parts[-2].lstrip('v')

    print('hashing sha256 for {}'.format(filename), file=sys.stderr)
    sha256 = hashlib.sha256()
    for buf in iter(lambda : data.read(128 * 1024), b''):
        sha256.update(buf)
    data.close()

    ota_property_files, os_sdk_level, os_patch_level, post_timestamp = read_android_metadata(
        f,
        "ota-property-files",
        "post-sdk-level",
        "post-security-patch-level",
        "post-timestamp"
    )

    if os_sdk_level:
        try:
            os_sdk_level = int(os_sdk_level)
        except ValueError:
            pass

    timestamp = None

    if post_timestamp:
        try:
            timestamp = int(post_timestamp)
        except ValueError:
            pass

    if not timestamp:
        try:
            with zipfile.ZipFile(f, 'r') as update_zip:
                if 'system/build.prop' in update_zip.namelist():
                    build_prop = update_zip.read('system/build.prop').decode('utf-8')
                    matches = re.findall(r'ro\.build\.date\.utc=([0-9]+)', build_prop)
                    if matches:
                        timestamp = int(matches[0])
        except Exception:
            pass

    if not timestamp:
        try:
            timestamp = int(mktime(datetime.strptime(builddate, '%Y%m%d').timetuple()))
        except Exception:
            timestamp = int(os.path.getmtime(f))

    if len(builddate) == 8 and builddate.isdigit():
        formatted_date = '{}-{}-{}'.format(builddate[0:4], builddate[4:6], builddate[6:8])
    else:
        formatted_date = "unknown"

    files_list = [{
        'sha256': sha256.hexdigest(),
        'size': os.path.getsize(f),
        'date': formatted_date,
        'filename': filename,
        'filepath': '/' + f.replace(FILE_BASE, '').lstrip('/'),
    }]

    folder = os.path.dirname(f)
    for img_file in os.listdir(folder):
        if img_file.endswith('.img'):
            img_path = os.path.join(folder, img_file)
            with open(img_path, 'rb') as img_data:
                img_sha256 = hashlib.sha256()
                for buf in iter(lambda: img_data.read(128*1024), b''):
                    img_sha256.update(buf)
            files_list.append({
                'sha256': img_sha256.hexdigest(),
                'size': os.path.getsize(img_path),
                'date': formatted_date,
                'filename': img_file,
                'filepath': '/' + img_path.replace(FILE_BASE, '').lstrip('/'),
            })

    build_entry = {
        'datetime': timestamp,
        'date': formatted_date,
        'version': version,
        'ota_property_files': ota_property_files,
        'os_sdk_level': os_sdk_level,
        'os_patch_level': os_patch_level,
        'files': files_list
    }
    builds.setdefault(device, []).append(build_entry)
for device in builds.keys():
    builds[device] = sorted(builds[device], key=lambda x: x['datetime'])
print(json.dumps(builds, sort_keys=True, indent=4))
