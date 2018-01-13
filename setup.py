from setuptools import setup, find_packages


setup(
    name='FastGets',
    version='0.1.6',
    url='https://github.com/ShuJuHeiKe/FastGets',
    description='Python Crawling Framework for Humans',
    author='ShuJuHeiKe',
    maintainer='XuYong',
    maintainer_email='tonyxuourlove@gmail.com',
    packages=find_packages(),
    license='BSD',
    install_requires=[
        'werkzeug==0.13',
        'mongoengine==0.15.0',
        'requests==2.18.4',
        'lxml==4.1.1',
        'redis==2.10.6',
        'mockredispy==2.9.3',
        'Flask==0.12.2',
        'python-crontab==2.2.8',
        'psutil==5.4.2',
        'xlrd==1.1.0',
        'croniter==0.3.20',
        'user-agent==0.1.9',
        'tldextract',
        'pytest==3.3.2',
        'mongomock==3.8.0',
    ],

    entry_points="""
    [console_scripts]
    fastgets_worker=fastgets.work:main
    fastgets_api_server=fastgets.api.app:run
    """
)
