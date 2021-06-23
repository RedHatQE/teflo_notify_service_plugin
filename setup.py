import os
import re
import io
from setuptools import setup, find_packages


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([a-zA-Z0-9.]+)['"]''')


def get_version():
    init = open(os.path.join(ROOT, 'teflo_notify_service_plugin', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


# reading description from README.md
with io.open(os.path.join(ROOT, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='teflo_notify_service_plugin',
    version=get_version(),
    description="Teflo plugin for integration with D&O tools's Notify Service ",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Red Hat Inc",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    entry_points={

            'notification_plugins': 'notify_service_plugin = teflo_notify_service_plugin:NotifyServicePlugin',

    }
)
