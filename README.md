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
    * `common/` Backend python functions for storing data and user information.
    * `models/` Python functions for the optimization model
        * `gephi/` Folder containing gephi files for visualization and exploration of the network.

* `project/`. Folder containing the actual code files for the project:
    * `gephi/` Folder containing gephi files for visualization and exploration of the network.
    * `images/` Folder containing different images that are generated when running the different notebooks.
    * `fragmentation measures.py` Contains functions to compute fragmentation measures on the provided network.
    * `optimization_algorithms.py` Contains both optimization algorithms for fragmentation and information flow as well as the necessary functions to compute the respectives objective values. 
    * `data_exploration_functions.py` Contains several functions used for the import and parse of the data, creation of the network structure or identification of largest component among others.
    * `fragmentation.ipynb` Notebook containing initial data exploration as well as optimization task and results on the fragmentation problem. The provided notebook is already executed and shows the desired results.
    * `information_flow.ipynb` Notebook containing the data exploration and optimization task and results on the information diffusion problem. The provided notebook is already executed and shows the desired results. A new execution can take around 15 to 20 minutes. 
    * `adjacency.npy` Numpy file containing the structure of the adjacency matrix of the original network. Can be used to avoid creating it from scratch if a new execution of any of the two notebooks wants to be done. 

* `Report.pdf`
* `requirements.txt`


## How to execute the files.
	
Only fragmentation and information flow Notebooks are intended to be executed. All other files do not provide any directly readable result. The project has been developed so that fragmentation notebook is read first as it contains an initial exploration of the data. Nevertheless, information_flow notebook can be read and understood without need of previous consultation to the fragmentation notebook, taking into account the reader is aware of the purpose of the project.

## Authors

* **Abrate, Marco Pietro** - 
* **Bolón Brun, Natalie** - 
* **Kakavandy, Shahow** - 
* **Park, Jangwon** - 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
