#!/usr/bin/python

from IPython.display import HTML
from IPython.display import display
import string
import numpy as np
import json
import sys

__PYDYGRAPH__FIGURE__NUMBER__ = 0
__PYDYGRAPH__FIGURE__JSON__ = []
__PYDYGRAPH__DYGRAPHS_LIB_STRING__ = "http://dygraphs.com/dygraph-combined.js"

class __figure__:
    def __init__(self):
        global __PYDYGRAPH__FIGURE__NUMBER__
        self._fignum = __PYDYGRAPH__FIGURE__NUMBER__
        self._divname = "Figure" + str(self._fignum)
        self._data = []
        self._options = {}
        # Set configurable variable to none:

        #print "Making figure", self._fignum
        __PYDYGRAPH__FIGURE__NUMBER__ += 1
        __PYDYGRAPH__FIGURE__JSON__.append("")

    def xlabel(self, xlabel):
        self._options.update({'xlabel': xlabel})

    def ylabel(self, ylabel):
        self._options.update({'ylabel': ylabel})

    def title(self, title):
        self._options.update({'title': title})

    def plotDataFrame(self, dataframe, **kwargs):

        self._data = dataframe.values.tolist()
        self._options = kwargs
        self._options.update({'labels': dataframe.columns.values.tolist()})

        __PYDYGRAPH__FIGURE__JSON__[self._fignum] = ""


    def plot(self, x=[], y=[], **kwargs):

        x = np.array(x)

        if type(y) is not np.ndarray:
            y = np.column_stack(y)

        elif type(y) is np.ndarray and y.shape[0] is not x.shape[0]:
            y = np.column_stack(y)

        self._data = np.column_stack((x, y)).tolist()
        self._options = kwargs

    def show(self):
        javascript = self.generateJS()
        display(HTML(javascript))

    def printJS(self):
        print ((self.generateJS()))

    def generateJS(self):

        dygraphs = """
        <script type="text/javascript">

        function handle_output_%(0)s(out) {

            g = new Dygraph(document.getElementById('%(0)s'), %(2)s, 
            
            %(3)s

            );
        }
        var kernel = IPython.notebook.kernel;
        var callbacks_%(0)s = { 'iopub' : {'output' : handle_output_%(0)s}};
        kernel.execute("sys.modules['dygraphs.graph'].__PYDYGRAPH__FIGURE__JSON__[%(1)s]", callbacks_%(0)s, {silent:false});
        </script>"""%{'0':self._divname, '1':self._fignum, '2':json.dumps(self._data), '3':json.dumps(self._options)}

        return dygraphs

def __create_table_for_pydygraph_figure__(divname, width, height):
    return """
    <script src=\"%(0)s\"></script>
    <table style="width: %(2)spx; border-style: hidden;">
    <tr><td style="border-style: hidden;"><div id='%(1)s' style="width: %(2)spx; height: %(3)spx;"></div></td></tr>
    <tr><td style="border-style: hidden;"><div style="text-align:right; width: %(2)spx; height: auto;"; id='%(1)s_legend'></div></td></tr>
    </table>
    """%{'0':__PYDYGRAPH__DYGRAPHS_LIB_STRING__, '1':divname, '2':width, '3':height}

def figure(width=1050, height=400):
    ''' This public function returns a pydygraph figure that holds a single plot '''

    # Create figure:
    fig = __figure__()

    # Create javascript for figure:
    javascript = __create_table_for_pydygraph_figure__(fig._divname, width, height)

    # Display the figure:
    display(HTML(javascript))

    # Return the handle:
    return fig

def subplot(v=1, h=1, width=1050, height=400, title=None):
    ''' This public function returns a list of pydygraph figures. Each table cell holds a single plot '''

    figureWidth = width/h
    figureHeight = height/v

    javascript = """<script src=\"%(0)s\"></script>
                    <table style="width: %(1)spx; border-style: hidden;">"""%{'0':__PYDYGRAPH__DYGRAPHS_LIB_STRING__, '1':width}

    # Generate optional subplot title:
    if title:
        javascript += """
                        <tr>
                            <th COLSPAN='%(0)s'>
                                <h1 align="center">%(1)s</h1>
                            </th>
                        <tr>"""%{'0':h, '1':title}

    # Generate subplot table:
    figs = []
    for i in range(v):
        javascript += "<tr>"
        temp = []
        for j in range(h):
            fig = __figure__()
            javascript += """<td style="border-style: hidden;">"""
            javascript += __create_table_for_pydygraph_figure__(fig._divname, figureWidth, figureHeight)
            javascript += "</td>"
            temp.append(fig)
        javascript += "</tr>"
        figs.append(temp)
    javascript += "</table>"

    # Display the subplot table:
    display(HTML(javascript))
    
    # Return all the figure handles:
    return figs

# Set a different remote or local dygraphs library than the default
def useDygraphsLib(dygraphslib):
    global __PYDYGRAPH__DYGRAPHS_LIB_STRING__
    __PYDYGRAPH__DYGRAPHS_LIB_STRING__ = dygraphslib

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='This utility does all of the awesome.')
    # parser.add_argument('config', metavar='configfile', type=str, help='a SBPP packet definition file to ingest')
    # parser.add_argument('fname', metavar='binaryfile', type=str, help='a SBPP binary file to ingest')
    # args = parser.parse_args()
    a = figure()
    b = figure()
    c = figure()
#   d = subfigure(2,2)