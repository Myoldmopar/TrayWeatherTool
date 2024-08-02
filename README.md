# Tray Weather Tool - Oklahoma Edition

A little utility that can show the temperature and storm status in Oklahoma, currently for Ubuntu machines.
This was originally developed in VB.Net and ran well on Windows but now converted to Python, and focused on Ubuntu.
It wouldn't take much to run on Windows, just need to make the tray icon/gtk stuff support across platforms.

## Installation

You can install this directly from Pip: `pip install TrayWeatherTool-Oklahoma`.  This will download and install the
package into your Python installation.  Once in place, you can start the icon using one of two methods:

- A command line script is installed called: `tray_weather_tool` that you can directly execute
- You can also use module execution and call it like: `python3 -m tray_weather`

Both of these will do the same thing.  If you want the icon to start when the system boots, you can add it to your
startup applications, just remember to execute it with the Python you used to install it.  Something like:
`/path/to/venv/bin/python3 -m tray_weather`.

## Development

To debug or develop on this code, download the repo, set up a virtual environment, install dependencies, and run main:
 - `git clone https://github.com/Myoldmopar/TrayWeatherTool`
 - `cd TrayWeatherTool`
 - `python3 -m venv .venv`
 - `. .venv/bin/activate`
 - `pip3 install -r requirements.txt`
 - `python3 tray_weather/main.py`

## Testing

Well, as of now, there is no automated testing in place except code linting with flake8.  It would make me feel a 
lot better if we broke out some of the functionality into testable code and add an action script to test it.

## Deployment ![PyPI - Version](https://img.shields.io/pypi/v/trayweathertool-oklahoma?color=44cc11)

Anytime a tag is made on the repo it will build and push a wheel to PyPi.

## Documentation

As of now there are no docs, but it might be nice to make a tiny RTD page for it.
