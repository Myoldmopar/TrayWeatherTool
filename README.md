# Tray Weather Tool - Oklahoma Edition

A little utility that can show the temperature and storm status in Oklahoma, currently for Ubuntu machines.
This was originally developed in VB.Net and ran well on Windows but now converted to Python, and focused on Ubuntu.
I don't think it would take much to run on Windows or Mac, just need to make the tray icon/gtk stuff support across platforms.

## Installation ![PyPI - Version](https://img.shields.io/pypi/v/trayweathertool-oklahoma?color=44cc11) [![PyPIRelease](https://github.com/Myoldmopar/TrayWeatherTool/actions/workflows/release.yml/badge.svg)](https://github.com/Myoldmopar/TrayWeatherTool/actions/workflows/release.yml)

You can install this directly from Pip: `pip install TrayWeatherTool-Oklahoma`.  This will download and install the
package into your Python installation.  Anytime a tag is made on the repo it will build and push a wheel to PyPi, so
you can check there for the latest version number if you want a specific version.

Once in place, you can start the icon using one of two methods:

- A command line script is installed called: `tray_weather_tool` that you can directly execute
- You can also use module execution and call it like: `python3 -m tray_weather`

Both of these will do the same thing.  If you want the icon to start when the system boots, you can add it to your
startup applications, just remember to execute it with the Python you used to install it.  Something like:
`/path/to/venv/bin/python3 -m tray_weather`.

## Development [![Flake8](https://github.com/Myoldmopar/TrayWeatherTool/actions/workflows/flake8.yml/badge.svg)](https://github.com/Myoldmopar/TrayWeatherTool/actions/workflows/flake8.yml) [![Tests](https://github.com/Myoldmopar/TrayWeatherTool/actions/workflows/test.yml/badge.svg)](https://github.com/Myoldmopar/TrayWeatherTool/actions/workflows/test.yml)

To debug or develop on this code, download the repo, set up a virtual environment, install dependencies, and run main:
 - `git clone https://github.com/Myoldmopar/TrayWeatherTool`
 - `cd TrayWeatherTool`
 - `python3 -m venv .venv`
 - `. .venv/bin/activate`
 - `pip3 install -r requirements.txt`
 - `python3 tray_weather/main.py`
 
The code is processed with flake8 for formatting/style.  It is also tested with unit tests to get 100% coverage on
all the non-GUI lines of code.

## Documentation

As of now there are no docs, but it might be nice to make a tiny RTD page for it.
