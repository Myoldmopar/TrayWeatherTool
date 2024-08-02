from pathlib import Path
from setuptools import setup

from tray_weather import VERSION, PACKAGE_NAME, DESCRIPTION, SOURCE_NAME
readme_file = Path(__file__).parent.resolve() / 'README.md'
readme_contents = readme_file.read_text()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=[SOURCE_NAME],
    description=DESCRIPTION,
    package_data={},
    include_package_data=False,
    long_description=readme_contents,
    long_description_content_type='text/markdown',
    author='Edwin Lee',
    url='https://github.com/Myoldmopar/TrayWeatherTool',
    license='ModifiedBSD',
    install_requires=['matplotlib', 'requests', 'pygobject', 'pyperclip', 'pillow', 'solar-angles>=0.26'],
    entry_points={
        'gui_scripts': [],
        'console_scripts': ['tray_weather_tool=tray_weather.main:run_main']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Utilities',
    ],
    platforms=[
        'Linux (Tested on Ubuntu)', 'MacOSX', 'Windows'
    ],
    keywords=[
        'Solar Angles',
        'Building Simulation', 'Whole Building Energy Simulation',
        'Heat Transfer', 'Modeling',
    ]
)
