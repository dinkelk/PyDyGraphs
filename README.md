PyDyGraphs
-----
An interactive charting library using [Dygraphs](http://dygraphs.com/) for the [Jupyter Notebook](https://jupyter.org/).

## Intent

The [Jupyter Notebook](https://jupyter.org/) is an excellent tool for interacting with python and displaying data in real time. While tools like [matplotlib](http://matplotlib.org/) can generate static plots in the Jupyter Notebook, interactive javascript plots are often more useful for exploring the data. This module can be readily included in an Jupyter Notebook and then used to generate beautiful time series plots with [Dygraphs](http://dygraphs.com/).

## Screenshots 

Simple Example
![SinglePlot](http://i.imgur.com/etR5a21.png)

Subplot with Range Selector
![RangeSelector](http://i.imgur.com/bAL7pH6)

Pandas Dataframe Plot
![Dataframe](http://i.imgur.com/eMaCXOM.png)


## How It Works

This python module generates javascript that interacts with the [Dygraphs](http://dygraphs.com/) library, and passes it to the [Jupyter Notebook](https://jupyter.org/) kernel for execution.

Currently the *PyDyGraphs* module depends on [Pandas](http://pandas.pydata.org/) to generate a JSON representation of the data for plotting. This required dependancy may be removed with future work. Pandas can be installed via [pip](https://pypi.python.org/pypi/pip).

## Example
Run the included example:examples/PyDyGraphTester.ipynb, or paste this code into an Jupyter Notebook to generate an interactive timeseries plot:

    # Import pydygraphs and numpy
    import dygraphs.graph as dy
    import numpy as np

    # Create a figure
    fig = dy.figure(width = 600, height = 400)

    # Generate data for the plot
    x = np.array(range(100))
    y = [np.sin(np.random.rand(100)),-np.sin(np.random.rand(100))]

    # Plot the data on the figure
    fig.plot(x,y, color=['navy','magenta'])
    fig.title("Figure 1")
    fig.xlabel('Series')
    fig.ylabel('Value')

    # Show the figure in this cell of the notebook
    fig.show()

## Installation:
Simply clone this repository and include the *dygraphs.graph* module in your [Jupyter Notebooks](https://jupyter.org/). *Note: PyDyGraphs only supports Python 3*.

## Want to contribute:
Please submit a *pull request* or *issue* with any questions you might have!
