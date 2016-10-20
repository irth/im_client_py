from distutils.core import setup

setup(
    name='IMClient',
    version='0.1dev',
    packages=['im_client'],
    license='MIT license',
    long_description=open('README.txt').read(),
    install_requires=['protobuf']
)
