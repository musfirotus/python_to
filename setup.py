from setuptools import setup

setup(
    name='cliweather_fira', # beri nama openweater_yourname
    version='0.1',
    py_modules = ['cliweather'],
    install_requires=[
        'click',
        'asyncio',
        'datetime',
        'aiohttp'
        # tambahkan package yang kalian gunakan untuk membangun aplikasi disini!
    ],
    # buatlah nama app nya cliweather
    entry_points='''
        [console_scripts]
        cliweather=main:cli
    ''',
)