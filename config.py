import os


class Config(object):
    GERRIT_URL = os.environ.get('GERRIT_URL', 'https://gerrit.witaqua.org')
    WIKI_INSTALL_URL = os.environ.get('WIKI_INSTALL_URL', 'https://wiki.witaqua.org/devices/{device}.html')
    WIKI_INFO_URL = os.environ.get('WIKI_INFO_URL', 'https://wiki.witaqua.org/devices/{device}.html')
    STATUS_URL = os.environ.get('STATUS_URL', '#')

    UPSTREAM_URL = os.environ.get('UPSTREAM_URL', 'http://api.witaqua.org/builds.json')
    DOWNLOAD_BASE_URL = os.environ.get('DOWNLOAD_BASE_URL', 'https://download.witaqua.org/builds')

    DEVICES_JSON_PATH = os.environ.get('DEVICES_JSON_PATH', 'devices.json')
    DEVICES_LOCAL_JSON_PATH = os.environ.get('DEVICES_LOCAL_JSON_PATH', 'devices_local.json')
    OFFICIAL_DEVICES_JSON_URL = os.environ.get('OFFICIAL_DEVICES_JSON_URL', 'https://raw.githubusercontent.com/witaqua/hudson/main/updater/devices.json')
    DEVICE_DEPS_PATH = os.environ.get('DEVICE_DEPS_PATH', 'device_deps.json')
    OFFICIAL_DEVICE_DEPS_JSON_URL = os.environ.get('OFFICIAL_DEVICE_DEPS_JSON_URL', 'https://raw.githubusercontent.com/witaqua/hudson/main/updater/device_deps.json')
    LINEAGE_BUILD_TARGETS_PATH = os.environ.get('LINEAGE_BUILD_TARGETS_PATH', 'witaqua-build-targets')
    OFFICIAL_LINEAGE_BUILD_TARGETS_URL = os.environ.get('OFFICIAL_LINEAGE_BUILD_TARGETS_URL', 'https://raw.githubusercontent.com/witaqua/hudson/main/witaqua-build-targets')


class FlaskConfig(object):
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', '3600'))
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST', 'redis')
    CACHE_REDIS_DB = os.environ.get('CACHE_REDIS_DB', 4)
    CACHE_REDIS_PASSWORD = os.environ.get("CACHE_REDIS_PASSWORD", None)
