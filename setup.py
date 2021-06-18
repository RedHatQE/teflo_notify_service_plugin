import os
import re
from setuptools import setup, find_packages


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([a-zA-Z0-9.]+)['"]''')


def get_version():
    init = open(os.path.join(ROOT, 'teflo_notify_service_plugin', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='teflo_notify_service_plugin',
    version=get_version(),
    description="Teflo plugin for integration with D&O tools's Notify Service ",
    author="Red Hat Inc",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'http',
        'urllib'
    ],
    entry_points={

            'notification_plugins': 'notify_service_plugin = teflo_notify_service_plugin:NotifyServicePlugin',

    }
)
