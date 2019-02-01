# Finewbie: Personal Investment Advisor for Beginners
Capstone Project, December 2017, University of Toronto

This is the directory of the Capstone Project, fall 2017, University of Toronto. This directory contains practical information on the project implementation and how to run it.

The proposed challenge is to design a personal asset-liability management tool which recommends the optimal investment strategy for any individual with any unique financial circumstances and profile, and for any type of goal he/she aspires to achieve through investing. The final outcome is a **web-based robo-advisor** which works on a complex, sophisticated optimization method, accounting for many realistic factors.

(`Report.pdf`) is a 69-page document, fullying underlying all details of the project development. For a brief overview, please refer to (`Presentation.pdf`). For a well-documented demonstration of the web application, refer to (`Demonstration.pdf`).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The required environment for running the code and reproducing the results is a computer with a valid installation of Python 3. More specifically, [Python 3.6](https://docs.python.org/3.6/) is used.

Besides that (and the built-in Python libraries), the following packages are used and have to be installed:

* [Bokeh 0.12.0](https://bokeh.pydata.org/en/0.12.10/docs/releases/0.12.0.html) `pip3 install --user bokeh==0.12.0`
* [cxvopt 1.2](https://cvxopt.org/) `pip3 install --user cvxopt==1.2`
* [datetime 4.2](https://pypi.org/project/DateTime/4.2/) `pip3 install --user datetime==4.2`
* [flask 0.12.2](https://pypi.org/project/Flask/0.12.2/) `pip3 install --user flask==0.12.2`
* [Jinja2 2.9.6](https://pypi.org/project/Jinja2/2.9.6/) `pip3 install --user jinja2==2.9.6`
* [NumPy 1.13.3](http://www.numpy.org) `pip3 install --user numpy==1.13.3`
* [Matplotlib 2.0.2](https://matplotlib.org) `pip3 install --user matplotlib==2.0.2`
* [Pandas 0.20.3](https://pandas.pydata.org) `pip install --user pandas==0.20.3`
* [pandas-datareader 0.5.0](https://pandas-datareader.readthedocs.io/en/latest/whatsnew.html#v0-5-0-july-25-2017) `pip install --user pandas-datareader==0.5.0`
* [passlib 1.7.1](https://passlib.readthedocs.io/en/stable/) `pip install --user passlib==1.7.1`
* [pymongo 3.5.1](http://api.mongodb.com/python/3.5.1/) `pip install --user pymongo==3.5.1`
* [requests 2.14.2](https://pypi.org/project/requests/2.14.2/) `pip install --user requests==2.14.2`
* [uwsgi 2.0.18](https://uwsgi-docs.readthedocs.io/en/latest/Changelog-2.0.17.html) `pip install --user uwsgi==2.0.18`

### Installing

To install the previously mentioned libraries a requirements.txt file is provided. The user is free to use it for installing the previously mentioned libraries.  

## Project Structure

The project has the following folder (and file) structure:

* `src/`. Source directory.
    * `common/` Backend functions for storing data and user information.
    * `models/` Python functions for the optimization model
        * `portfolios/` Functions for optimizing portfolio via geometric Brownian moion simulation and stochastic programming.
	* `profiles/` Functions for accepting user profile information such as attitude to risk.
	* `user/` Frontend functions for login pages
    * `static/` CSS design and images used in the web application interface.
    * `templates/` Jinja2 templates for the design of the web application interface.
* `Demonstration.pdf` Screenshots of the web application
* `Report.pdf` 69-page report
* `Presentation.pdf`
* `requirements.txt`

## How to execute the files
	
The web application can be launched by visting [Finewbie](http://finewbie.herokuapp.com/). The walk-through of how to use the web application is described in `Demonstration.pdf`. 

## Authors

* **Jangwon Park** (algorithm/logic developer)
* **Sowmya Tata** (frontend developer)
* **Kai Zhang** (backend developer)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
