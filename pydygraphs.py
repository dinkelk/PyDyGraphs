#!/usr/bin/python

from IPython.display import HTML
from IPython.display import display
import string
import pandas as pd

__PYDYGRAPH__FIGURE__NUMBER__ = 0
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
        function convertToDataTable_""" + self._divname + """(d) {
          var columns = _.keys(d);
          var x_col = '""" + self._x_axis +"""';
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

        function handle_output_""" + self._divname + """(out) {
          var json = out.content.data['text/plain'];
          var data = JSON.parse(eval(json));
          var tabular = convertToDataTable_""" + self._divname + """(data);
          """

        dygraphs += """
            g = new Dygraph(document.getElementById('""" + self._divname + """'), tabular.data, {
                legend: 'always',
                labels: tabular.labels,
                labelsDivStyles: { 'textAlign': 'right' },
                rollPeriod: 1,
                showRoller: true,
                animatedZooms: true,
            """

        if self._showroller:
            dygraphs+= """
                showRoller: true,
            """
        else:
            dygraphs+= """
                showRoller: false,
            """

        if self._color:
            dygraphs+= """
                colors: ["""+','.join(['"'+c+'"' for c in self._color])+"""],
            """

        if self._title:
            dygraphs+= """
                title: '""" + self._title + """',"""
        if self._xlabel:
            dygraphs+= """
                xlabel: '""" + self._xlabel + """',
            """
        if self._ylabel:
            dygraphs+= """
                ylabel: '""" + self._ylabel + """',
            """

        if self._rangeselector:
            dygraphs += """
                showRangeSelector: true,
                rangeSelectorHeight: 65,
            """

        if self._logscale:
            dygraphs+="""
                logscale: true,
            """

        dygraphs+="""
               labelsDiv: '"""+self._divname+"""_legend',
               errorBars: false
          })
        }
        var kernel = IPython.notebook.kernel;
        var callbacks_""" + self._divname + """ = { 'iopub' : {'output' : handle_output_""" + self._divname + """}};
        kernel.execute("pydygraphs.__PYDYGRAPH__FIGURE__JSON__[""" + str(self._fignum) + """]", callbacks_""" + self._divname + """, {silent:false});
        </script>
        """
        return dygraphs

def __create_table_for_pydygraph_figure__(divname, width, height):
    return """
    <script src=\"""" + str(__PYDYGRAPH__DYGRAPHS_LIB_STRING__) + """\"></script>
    <table style="width: """ + str(width) + """px; border-style: hidden;">
    <tr><td style="border-style: hidden;"><div id='"""+str(divname)+"""' style="width: """ + str(width) + """px; height: """ + str(height) + """px;"></div></td></tr>
    <tr><td style="border-style: hidden;"><div style="text-align:right; width: """ + str(width) + """px; height: auto;"; id='"""+str(divname)+"""_legend'></div></td></tr>
    </table>
    """

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

    javascript = """<script src=\"""" + str(__PYDYGRAPH__DYGRAPHS_LIB_STRING__) + """\"></script>
                    <table style="width: """ + str(width) + """px; border-style: hidden;">"""

    # Generate optional subplot title:
    if title:
        javascript += """
                        <tr>
                            <th COLSPAN='"""+str(h)+"""'>
                                <h1 align="center">"""+title+"""</h1>
                            </th>
                        <tr>"""

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