#!/usr/bin/python

from IPython.display import HTML
from IPython.display import display
import string
import pandas as pd
import sys

__PYDYGRAPH__FIGURE__NUMBER__ = 0
global __PYDYGRAPH__FIGURE__JSON__
__PYDYGRAPH__FIGURE__JSON__ = []
__PYDYGRAPH__DYGRAPHS_LIB_STRING__ = "http://dygraphs.com/dygraph-combined.js"

class __figure__:
    def __init__(self):
        global __PYDYGRAPH__FIGURE__NUMBER__
        self._fignum = __PYDYGRAPH__FIGURE__NUMBER__
        self._divname = "Figure" + str(self._fignum)

        # Set configurable variable to none:
        self._color = None
        self._title = None
        self._xlabel = None
        self._ylabel = None

        #print "Making figure", self._fignum
        __PYDYGRAPH__FIGURE__NUMBER__ += 1
        __PYDYGRAPH__FIGURE__JSON__.append("")

    def xlabel(self, xlabel):
        self._xlabel = xlabel

    def ylabel(self, ylabel):
        self._ylabel = ylabel

    def title(self, title):
        self._title = title

    def plotDataFrame(self, dataframe, xaxis, color=None, rangeselector=False, logscale=False, showroller=True):
        self._jsondata = dataframe.to_json()
        self._x_axis = xaxis
        self._rangeselector = rangeselector
        self._logscale = logscale
        self._showroller = showroller
        if color:
            if isinstance(color, str):
                self._color = [color]
            else:
                self._color = color
        __PYDYGRAPH__FIGURE__JSON__[self._fignum] = self._jsondata


    def plot(self, x, y=[], ylabels=[], color=None, rangeselector=False, logscale=False, showroller=True):

        if not isinstance(y,list):
            y=[y]
        labelizer = lambda a: (['Y' + str(x) for x in a])

        if not ylabels:
            ylabels = labelizer(list(range(len(y))))

        if len(ylabels) != len(y):
            ylabels.extend(labelizer(list(range(len(y) - len(ylabels)))))

        # Form dataframe:
        xlabel = "_x_axis_label_"        
        table = {}
        table[xlabel] = x
        for label,data in zip(ylabels,y):
            table[label] = data

        dataframe = pd.DataFrame(table)

        # Return plot:
        return self.plotDataFrame(dataframe, xaxis=xlabel, color=color, rangeselector=rangeselector, logscale=logscale, showroller=showroller)

    def show(self):
        javascript = self.generateJS()
        display(HTML(javascript))

    def printJS(self):
        print ((self.generateJS()))

    def generateJS(self):

        dygraphs = ""

        dygraphs += """
        <script type="text/javascript">
        function convertToDataTable_%(0)s(d) {
          var columns = _.keys(d);
          var x_col = '%(1)s';
          columns.splice(columns.indexOf(x_col), 1);  // Get index column. (prob index). Don't need to do this just to plot all
          var out = [];
          var i = 0;
          for (var k in d[x_col]) {
            var row = [d[x_col][k]];
            columns.forEach(function(col) {
              row.push(d[col][k]);
            });
            out.push(row);
          }
          return {data:out, labels:[x_col].concat(columns)};
        }

        function handle_output_%(0)s(out) {
          var json = out.content.data['text/plain'];
          var data = JSON.parse(eval(json));
          var tabular = convertToDataTable_%(0)s(data);
          """%{'0':self._divname, '1':self._x_axis}

        dygraphs += """
            g = new Dygraph(document.getElementById('%s'), tabular.data, {
                legend: 'always',
                labels: tabular.labels,
                labelsDivStyles: { 'textAlign': 'right' },
                rollPeriod: 1,
                showRoller: true,
                animatedZooms: true,
            """%(self._divname)

        dygraphs += "showRoller: '{}',".format(str(self._showroller).lower())

        if self._color:
            dygraphs+= """
                colors: ["""+','.join(['"'+c+'"' for c in self._color])+"""],
            """

        dygraphs += "title: '{}',".format(self._title) if self._title else ""

        dygraphs += "xlabel: '{}',".format(self._xlabel) if self._xlabel else ""

        dygraphs += "ylabel: '{}',".format(self._ylabel) if self._xlabel else ""

        dygraphs += "showRangeSelector: true, rangeSelectorHeight: 65," if self._rangeselector else ""

        dygraphs += "logscale: true," if self._logscale else ""

        dygraphs+="""
               labelsDiv: '%(0)s_legend',
               errorBars: false
          })
        }
        var kernel = IPython.notebook.kernel;
        var callbacks_%(0)s = { 'iopub' : {'output' : handle_output_%(0)s}};
        kernel.execute("sys.modules['dygraphs.graph'].__PYDYGRAPH__FIGURE__JSON__[%(1)s]", callbacks_%(0)s, {silent:false});
        </script>
        """%{'0':self._divname, '1':self._fignum}
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