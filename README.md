PyDyGraphs
-----
[Dygraphs](http://dygraphs.com/) in the [Ipython Notebook](http://ipython.org/notebook.html).

## Intent

The [Ipython Notebook](http://ipython.org/notebook.html) is a great interactive tool for python development that involves displaying plots. While tools like matplotlib can generate static images of plots in the notebook, interactive javascript plots are more desireable. This module can be readily included in an ipython notebook and then used to generate beautiful time series plots using the [Dygraphs](http://dygraphs.com/) javascript charting library.

## How It Works

This python module dynamically generates javascript that interacts with the [Dygraphs](http://dygraphs.com/) library, and passes it to the ipython notebook kernel for execution.

Currently the PyDyGraphs module depends on [Pandas](http://pandas.pydata.org/) to generate a JSON representation of data for plotting. This required dependancy may be removed in the future. Pandas can be installed via [pip](https://pypi.python.org/pypi/pip).

## Example

Running this code in an ipython notebook will generate a timeseries plot using Dygraphs.

    # Import pydygraphs and numpy
    import pydygraphs
    import numpy as np

    # Subplot example
    fig = pydygraphs.figure(width = 600, height = 400)

    # Form data for plot
    x = np.array(range(100))
    y = [np.sin(np.random.rand(100)),-np.sin(np.random.rand(100))]

    # Plot figure
    fig.plot(x,y, color=['navy','magenta'])
    fig.title("Figure 1")
    fig.xlabel('Series')
    fig.ylabel('Value')

    # Show figure:
    fig.show()

## Installation:
Simply clone this repository and include the pydygraphs.py module in your project.


