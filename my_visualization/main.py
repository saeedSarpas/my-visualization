"""
main.py
Main class of my_visualization package
"""


import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LogFormatter

import my_colordict as cdict


class MyVisualization:
    """Visualization class"""

    def __init__(self, aspect=1, figsize=None, tickfontsize=12,
                 labelfontsize=18, cscheme='RAINBOW'):
        """MyVisualization constructor

        Parameters
        ----------
        aspect : float, optional
            The aspect ratio of the axes
        figsize : tuple of inches, optional
            w/h size of the figure
        tickfontsize : int
            Font size of the ticks of the plot
        labelfontsize : int
            Font size of plots label
        """
        self.plt = plt
        self.tickfontsize = tickfontsize
        self.labelfontsize = labelfontsize
        self.cscheme = cdict.get(cscheme)

        figsize = figsize if figsize != None else plt.figaspect(aspect)
        self.plt.figure(random.randint(1, 100000), figsize=figsize)

        self.defaults = [
            ('label', ''),
            ('color', self.cscheme['primary_colors'][0]),
            ('ecolor', self.cscheme['helper_colors'][0]),
            ('linestyle', 'solid'),
            ('shadow', self.cscheme['primary_shadows'][0]),
            ('alpha', None),
            ('linewidth', 1),
            ('head_width', 0.05),
            ('head_length', 0.1),
            ('silent', False),
        ]


    def plot(self, xs, ys, pos="111", ax=None, **kws):
        """plot

        Parameters
        ----------
        xs, ys : list
        pos : str, optional
            Position of the subplot inside the figure
        ax : Axes obj, optional
            Axes generated by new2daxes

        Keyword Arguments
        -----------------
        label : str, optional
        color : str, optional
        shaded : bool, optional
            Shadow under the y-error bars
        linestyle : str, optional
        xscale, yscale : str, optional
            Scale of the axis, e.g., 'log', 'linear'
        xmin, xmax, ymin, ymax : float, optional
        xlabel, ylabel : str, optional
        alpha: float, optional
        """

        if ax is None: ax = self.plt.subplot(pos)

        params = self.__getparams(**kws)
        if not params['silent'] == True: self.__printargs("\"plot\"", **kws)

        ax.plot(xs, ys, color=params['color'], linestyle=params['linestyle'],
                label=params['label'], alpha=params['alpha'])

        self.__setscales(**kws)
        self.__setlabels(**kws)
        self.__setarea(**kws)
        self.__stylespines(**kws)
        self.__setaxiscolor(**kws)


    def errorbar(self, xs, ys, xerrs=None, yerrs=None, pos="111", ax=None, **kws):
        """Plotting with error bars

        Parameters
        ----------
        xs, ys, xerrs, yerrs : list
        pos : str, optional
            Position of the subplot inside the figure
        ax : Axes obj, optional
            Axes generated by new2daxes

        Keyword Arguments
        -----------------
        label : str, optional
        color : str, optional
        ecolor : str, optional
        shaded : bool, optional
        shadedcolor : string, optional
        shadedalpha : float, optional
        linestyle : str, optional
        xscale, yscale : str, optional
        xmin, xmax, ymin, ymax : float, optional
        xlabel, ylabel : str, optional
        """
        k = kws.get

        if ax is None: ax = self.plt.subplot(pos)

        params = self.__getparams(**kws)
        if not params['silent'] == True: self.__printargs("\"errorbar\"", **kws)

        ax.errorbar(xs, ys, xerr=xerrs, yerr=yerrs,
            color=params['color'], ecolor=params['ecolor'],
            linestyle=params['linestyle'], label=params['label'])

        if 'shaded' in kws and k('shaded') is True and yerrs != None:
            ylow = [y - yerr for y, yerr in zip(ys, yerrs)]
            yhigh = [y + yerr for y, yerr in zip(ys, yerrs)]

            c = k('shadedcolor') if 'shadedcolor' in kws else params['shadow']
            alpha = k('shadedalpha') if 'shadedalpha' in kws else 1.0

            ax.fill_between(xs, ylow, yhigh, facecolor=c, edgecolor=c,
                            alpha=alpha, interpolate=interpolate)

        self.__setscales(**kws)
        self.__setlabels(**kws)
        self.__setarea(**kws)
        self.__stylespines(**kws)
        self.__setaxiscolor(**kws)


    def image(self, xys, pos="111", ax=None, vmin=None, vmax=None,
                interpolation=None, **kws):
        """Density plot

        Parameters:
        ----------
        xys : 2D Array
        pos : str, optional
        ax : Axes obj, optional
        vmin, vmax : float or None
        interpolation: str, optional
            anti aliasing, default: None

        Keyword Arguments
        -----------------
        label : str, optional
        xscale, yscale : str, optional
        xmin, xmax, ymin, ymax : float, optional
        xlabel, ylabel : str, optional
        """

        if ax is None: ax = self.plt.subplot(pos)

        params = self.__getparams(**kws)
        if not params['silent'] == True: self.__printargs("\"image\"", **kws)

        cmap = mcolors.LinearSegmentedColormap('CustomMap', self.cscheme['dict'])

        if vmin is None: vmin = np.amin(xys)
        if vmax is None: vmax = np.amax(xys)

        ax.imshow(xys, cmap=cmap, vmin=vmin, vmax=vmax, interpolation=interpolation)

        self.__setscales(**kws)
        self.__setlabels(**kws)
        self.__setarea(**kws)
        self.__stylespines(**kws)
        self.__setaxiscolor(**kws)


    def scatter(self, xs, ys, pos="111", ax=None, s=10, **kws):
        """Scatter plot with histogram

        Parameters:
        ----------
        xs, ys : list
        pos : str, optional
        ax : Axes obj, optional
        s : int, optional

        Keyword Arguments
        -----------------
        label : str, optional
        color : str, optional
        xscale, yscale : str, optional
        xmin, xmax, ymin, ymax : float, optional
        xlabel, ylabel, zlabel : str, optional
        alpha : float
        """
        k = kws.get
        if ax is None: ax = self.plt.subplot(pos)

        params = _getparams(**kws)
        if not params['silent'] == True: self.__printargs("\"scatter\"", **kws)

        alpha = k('alpha') if 'alpha' in kws else None

        xmin = k('xmin') if 'xmin' in kws else np.min(xs)
        xmax = k('xmax') if 'xmax' in kws else np.max(xs)
        ymin = k('ymin') if 'ymin' in kws else np.min(ys)
        ymax = k('ymax') if 'ymax' in kws else np.max(ys)

        xlim = (np.min([xmin, self.plt.gca().get_xlim()[0]]),
                np.max([xmax, self.plt.gca().get_xlim()[1]]))

        ylim = (np.min([ymin, self.plt.gca().get_ylim()[0]]),
                np.max([ymax, self.plt.gca().get_ylim()[1]]))

        self.plt.gca().set_xlim(xlim)
        self.plt.gca().set_ylim(ylim)

        self.plt.scatter(xs, ys, c=params['color'], marker='o', s=s,
                         edgecolors='none', lw=0, alpha=alpha)

        self.__setscales(**kws)
        self.__setlabels(**kws)
        self.__setaxiscolor(**kws)
        self.__stylespines(**kws)
        self.__setarea(**kws)


    def arrow(self, xi, yi, xf, yf, pos="111", ax=None, **kws):
        """plot

        Parameters
        ----------
        xi, yi, xf, yf : number
        pos : str, optional
        ax : Axes obj, optional

        Keyword Arguments
        -----------------
        color : str, optional
        alpha: float, optional
        """

        if ax is None: ax = self.plt.subplot(pos)

        params = self.__getparams(**kws)

        if not params['silent'] == True: _printargs("\"arrow\"", **kws)

        ax.arrow(xi, yi, xf - xi, yf - yi, **dict({'color': params['color']}))

        self.__setscales(**kws)
        self.__setlabels(**kws)
        self.__setarea(**kws)
        self.__stylespines(**kws)
        self.__setaxiscolor(**kws)


    def plot3d(self, xs, ys, zs, pos="111", ax=None, **kws):
        """plot

        Parameters
        ----------
        xs, ys, zs : list
        pos : str, optional
        ax : 3DAxes obj, optional
            Axes generated by new3daxes

        Keyword Arguments
        -----------------
        label : str, optional
        color : str, optional
        xscale, yscale : str, optional
        xmin, xmax, ymin, ymax : float, optional
        xlabel, ylabel : str, optional
        alpha: float, optional
        """
        if ax is None: ax = self.new3daxes(pos=pos)

        params = _getparams(**kws)

        if not params['silent'] == True: self.__printargs("\"plot3d\"", **kws)

        ax.plot(xs, ys, zs, color=params['color'],
                linestyle=params['linestyle'], label=params['label'],
                alpha=params['alpha'], lw=params['linewidth'])

        self.__setscales(**kws)
        self.__setlabels(**kws)
        self.__setarea(**kws)
        self.__stylespines(**kws)
        self.__setaxiscolor(**kws)


    def scatter3d(self, xs, ys, zs, pos='111', ax=None, s=10, **kws):
        """Scatter3d plot

        Parameters:
        ----------
        xs, ys, zs : list
        pos : str, optional
        axes : plt.Axes3D obj, optional
        s : int, optional

        Keyword Arguments
        ----------------
        label : str, optional
        xscale, yscale : str, optional
        xmin, xmax, ymin, ymax : float, optional
        xlabel, ylabel, zlabel : str, optional
        alpha : float
        """
        k = kws.get

        if ax is None:
            ax = self.plt.gcf().add_subplot(pos, projection='3d')

        params = self.__getparams(**kws)
        if not params['silent'] == True: _printargs("\"scatter3d\"", **kws)

        alpha = k('alpha') if 'alpha' in kws else None

        ax.scatter(xs, ys, zs, c=params['color'], marker='o', s=s,
                   edgecolors='none', lw=0, alpha=alpha)

        if 'xlabel' in kws: ax.set_xlabel(k('xlabel'))
        if 'ylabel' in kws: ax.set_ylabel(k('ylabel'))
        if 'zlabel' in kws: ax.set_zlabel(k('zlabel'))

        if 'xmin' in kws and 'xmax' in kws: ax.set_xlim(k('xmin'), k('xmax'))
        if 'ymin' in kws and 'ymax' in kws: ax.set_ylim(k('ymin'), k('ymax'))
        if 'zmin' in kws and 'zmax' in kws: ax.set_zlim(k('zmin'), k('zmax'))

        self._setscales(**kws)
        self._setaxiscolor3d(**kws)


    def new2daxes(self, pos='111', sharex=None, sharey=None):
        """Creatign new 2d axes for plotting

        Parameters
        ----------
        pos : str, optional
            Position of the subplot inside the figure
        sharex, sharey : Axes, optional
            Sharing axes with other plots
        """
        return self.plt.gcf().add_subplot(pos, sharex=sharex, sharey=sharey)


    def new3daxes(self, pos='111'):
        """Creatign new 3d axes for plotting

        Parameters
        ----------
        pos : str, optional
            Position of the subplot inside the figure
        """
        return self.plt.gcf().add_subplot(pos, projection='3d')


    def coaxis(self, ticksloc, ticklabels, label, ax=None,
               axis='x', scale='linear', showminorticks=True, **kws):
        """Creating a new twin x axis at the top of the plot

        Parameters
        ----------
        pos : list of numbers
            Positions of ticks
        labels : list of labels
            Could be numbers of strings
        ax : Axes2D object, optional
        axis : string, optional
            Specifies for which axis we want to add a twin scale
        scale : string, optional
            Specifies the type of the axis (log, linear)
        showminorticks : bool
        colorscheme : string, optional
            The name of colorscheme from mycolordict module
        """
        if ax is None: ax = self.plt.gca()

        twinax = ax.twiny() if axis is 'x' else ax.twinx()

        set_scale = twinax.set_xscale if axis is 'x' else twinax.set_yscale
        set_label = twinax.set_xlabel if axis is 'x' else twinax.set_ylabel
        set_lim = twinax.set_xlim if axis is 'x' else twinax.set_ylim
        limit = ax.get_xlim() if axis is 'x' else ax.get_ylim()
        axformatter = twinax.xaxis if axis is 'x' else twinax.yaxis

        set_scale(scale)

        if scale is 'log':
            formatter = LogFormatter(10, labelOnlyBase=True)
            axformatter.set_major_formatter(formatter)
            axformatter.set_minor_formatter(formatter)

        set_lim(limit)
        twinax.set_xticks(ticksloc)
        twinax.set_xticklabels(ticklabels)
        set_label(label)

        if showminorticks is False:
            twinax.minorticks_off()

        twinax.spines["top"].set_visible(True)
        twinax.spines["right"].set_visible(True)
        twinax.spines['top'].set_color(self.cscheme['axiscolor'])
        twinax.spines['right'].set_color(self.cscheme['axiscolor'])

        self.__setaxiscolor(ax=ax, **kws)
        self.__setaxiscolor(ax=twinax, **kws)


    def setgrid(self, ax=None, **kws):
        """Setting plot grid and background"""
        if ax is None: ax = self.plt.gca()

        ax.set_axis_bgcolor(self.cscheme['background'])
        ax.grid(color=self.cscheme['gridcolor'],
                  linestyle='solid', linewidth=1)

        # set grid lines behind the plot
        ax.set_axisbelow(True)


    def legend(self, pos="111", ax=None, loc="upper right",
               fontsize='medium', framealpha=0.7, frameon=False,
               bgcolor=cdict.get('RAINBOW')['gridcolor']):
        """Add legend to plot

        Parameters
        ----------
        pos : str, optional
            Position of the subplot inside the figure
        ax : Axes obj, optional
            Axes generated by new2daxes or new3daxes
        loc : string
            Location of the legend frame
        fontsize : int, float or ('x-small', etc.), optional
            Font size of the legend
        framealpha : None or bool, optional
        bgcolor : str, optional
            Background color of the legend
        """
        if ax is None: ax = self.plt.subplot(pos)

        ax.legend(loc=loc, fontsize=fontsize, frameon=None,
                  framealpha=framealpha, facecolor=bgcolor)


    def save(self, name, dpi=360, transparent=True):
        """Saving plot

        Parameters
        ----------
        name : str
            name and extension of the plot
        dpi : integer
            dots per inch
        transparent : bool
            Transparet background
        """
        self.plt.savefig(name, dpi=dpi, bbox_inches='tight',
                         transparent=transparent)


    def __setscales(self, ax=None, **kws):
        """Setting plot scale parameters if available"""
        if ax is None: ax = self.plt.gca()

        if 'xscale' in kws: ax.set_xscale(kws.get('xscale'))
        if 'yscale' in kws: ax.set_yscale(kws.get('yscale'))
        if 'zscale' in kws: ax.set_zscale(kws.get('zscale'))


    def __setlabels(self, ax=None, **kws):
        """Setting plot labels parameters if available"""
        if ax is None: ax = self.plt.gca()

        if 'xlabel' in kws: ax.set_xlabel(kws.get('xlabel'))
        if 'ylabel' in kws: ax.set_ylabel(kws.get('ylabel'))
        if 'yscale' in kws: ax.set_ylabel(kws.get('ylabel'))


    def __setarea(self, ax=None, **kws):
        """Setting plot area if available"""
        if ax is None: ax = self.plt.gca()

        if 'xmin' in kws: ax.set_xlim(left=kws.get('xmin'))
        if 'xmax' in kws: ax.set_xlim(right=kws.get('xmax'))
        if 'ymin' in kws: ax.set_ylim(bottom=kws.get('ymin'))
        if 'ymax' in kws: ax.set_ylim(top=kws.get('ymax'))

    def __stylespines(self, ax=None, **kws):
        """Removing plot top and right spines"""
        if ax is None: ax = self.plt.gca()

        ax.spines['top'].set_color(self.cscheme['axiscolor'])
        ax.spines['left'].set_color(self.cscheme['axiscolor'])
        ax.spines['right'].set_color(self.cscheme['axiscolor'])
        ax.spines['bottom'].set_color(self.cscheme['axiscolor'])


    def __setaxiscolor(self, ax=None, **kws):
        """Setting plot axis color if available"""
        if ax is None: ax = self.plt.gca()

        ax.xaxis.label.set_color(self.cscheme['axiscolor'])
        ax.tick_params(axis='x', colors=self.cscheme['axiscolor'])
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_color(self.cscheme['axiscolor'])
            tick.label.set_fontsize(self.tickfontsize)
        for label in ax.xaxis.get_majorticklabels():
            label.set_color(self.cscheme['axiscolor'])
            label.set_fontsize(self.tickfontsize)
        ax.xaxis.label.set_fontsize(self.labelfontsize)

        ax.yaxis.label.set_color(self.cscheme['axiscolor'])
        ax.tick_params(axis='y', colors=self.cscheme['axiscolor'])
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_color(self.cscheme['axiscolor'])
            tick.label.set_fontsize(self.tickfontsize)
        for label in ax.yaxis.get_majorticklabels():
            label.set_color(self.cscheme['axiscolor'])
            label.set_fontsize(self.tickfontsize)
        ax.yaxis.label.set_fontsize(self.labelfontsize)


    def __setaxiscolor3d(self, ax=None, **kws):
        """Setting plot axis color if available"""
        if ax is None: ax = self.plt.gca()

        self.__setaxiscolor(ax=ax, **kws)

        ax.zaxis.label.set_color(self.cscheme['axiscolor'])
        ax.tick_params(axis='z', colors=self.cscheme['axiscolor'])
        for tick in ax.zaxis.get_major_ticks():
            tick.label.set_fontsize(self.tickfontsize)
        for label in ax.zaxis.get_majorticklabels():
            label.set_color(self.cscheme['axiscolor'])
            label.set_fontsize(self.tickfontsize)
        ax.zaxis.label.set_fontsize(self.labelfontsize)


    def __printargs(self, title, **kws):
        """Printing used keyword arguments for a specific plot"""
        if len(dict(kws).keys()) > 0:
            print(str(title) + ' is plotting using following parameters:')
            for key, value in dict(kws).items():
                print('\t {:15s}'.format(str(key)) + str(value))
                print('')


    def __getparams(self, **kws):
        """Extract keyword parameters"""
        params = {}
        k = kws.get

        for elem in self.defaults:
            params[elem[0]] = k(elem[0]) if elem[0] in kws else elem[1]

        return params
