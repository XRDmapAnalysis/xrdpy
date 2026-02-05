import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from ..BasicFunctions._general_plot_functions import _GeneratePlots

### ===========================================================================
class _xrdplot(_GeneratePlots):
    """
    Plotting xrd data.

    """
    def __init__(self, x_values=None, y_values=None, z_values=None, 
                 save_figure_dir='.'):
        
        _GeneratePlots.__init__(self, save_figure_dir=save_figure_dir)       
        if z_values is None:
            try:
                self.ZZ = self.intensity_values.copy() 
            except:
                raise ValueError('Provide intensity or count values for the map.')
        else:
            self.ZZ = z_values.copy()

        if x_values is None:
            try:
                
                self.XX = self.two_theta_values.copy() if self.plt_mode == 'omega_2theta_space_map' else self.rsm_x.copy()
            except:
                raise ValueError('Provide 2*theta values (in real space) or Qx (in reciprocal space).')
        else:
            self.XX = x_values.copy()

        if y_values is None:
            try:
                self.YY = self.omega_values.copy() if self.plt_mode == \
                    'omega_2theta_space_map' else self.rsm_y.copy()
            except:
                raise ValueError('Provide omega values (in real space) or Qz (in reciprocal space).')
        else:
            self.YY = y_values.copy()

    @classmethod
    def _data_curation_threshold(cls, full_data, threshold_weight:float=1e-5):
        result = full_data.copy()
        if threshold_weight is not None: 
            result[result < threshold_weight] = np.nan
        return result

    def _plot(self, fig=None, ax=None, save_file_name=None, CountFig=None, 
              Xmin=None, Xmax=None, Ymin=None, Ymax=None, 
              threshold_intensity:float=None,  
              mode:str="reciprocal_space_map", xaxis_label:str='Qx (rlu)',
              yaxis_label:str='Qz (rlu)', title_text=None,  
              color_map='viridis', color_scale='log', line_color='k',
              line_style='--', show_colorbar:bool=False, colorbar_label:str=None,
              vmin=None, vmax=None, show_contours:bool=True, contour_levels=None, 
              show_plot:bool=True, savefig:bool=False, **kwargs_savefig):
        """
        This function is for plottings. It supports plottings of XRD plots 
        automatically from XRD data or user specified specific 2D plots.

        Parameters
        ----------
        fig : matplotlib.pyplot figure instance, optional
            Figure instance to plot on. If None new figure
            will be created/initialized. The default is None. 
        ax : matplotlib.pyplot axis, optional
            Figure axis to plot on. If None, new figure will be created.
            The default is None.
        save_file_name : str, optional
            Name of the figure file. If None, figure will be not saved. 
            The default is None.
        CountFig: int, optional
            Figure count. The default is None.
        Xmin : float, optional
            Minimum in X-scale. The default is None.
        Xmax : float, optional
            Maximum in X-scale. The default is None.
        Ymin : float, optional
            Minimum in Y-scale. The default is None.
        Ymax : float, optional
            Maximum in Y-scale. The default is None.
        threshold_intensity : float, optional
            The rsm_intensities with intensities lower than the threshold_intensity 
            are discarded. The default is None. If None, this is ignored.
        mode : ['omega_2theta_space_map', 'reciprocal_space_map', 'simple_2d_plot'], optional
            Mode of plottings. The default is "reciprocal_space_map".
        xaxis_label : str, optional
            X-axis label text. The default is 'Qx (rlu)'.
        yaxis_label : str, optional
            Y-axis label text. The default is 'Qz (rlu)'.
        title_text : str, optional
            Title label text. The default is None. If None no title is added
        color_map: str/ matplotlib colormap
            Colormap for density plot. The default is viridis.
        color_scale : str, optional ['log', 'linear']
            The default is 'log'.
        line_color : matplotlib color, optional
            Color of border lines or for 2d line plots. The default is 'k'.
        line_style : matplotlib line style, optional
            Line style of border line or 2d line. The defult is '--'.
        show_colorbar : bool, optional
            Plot the colorbar in the figure or not. If fig=None, this is ignored.
            The default is False.
        colorbar_label : str, optional
            Colorbar label. The default is None. If None, ignored.
        vmin, vmax : float, optional
            vmin and vmax define the data range that the colormap covers. 
            By default, the colormap covers the complete value range of the supplied data.
        show_contours : bool, optional
            Show plot as contour maps. If false continous colorbar will be used.
            The default is True.
        contour_levels : int or array-like, optional
            Determines the number and positions of the contour lines / regions. 
            If an int n, use MaxNLocator, which tries to automatically choose 
            no more than n+1 "nice" contour levels between minimum and maximum 
            numeric values of Z. The values must be in increasing order.
            The default is None. If None, it is automatically determined to fit
            vmin and vmax in an optimized way.
        show_plot : bool, optional
            To show the plot when not saved. The default is True.
        savefig : bool, optional
            To save the plot. Ignored when save_file_name is None. The default is True.
        **kwargs_savefig : dict
            The matplotlib keywords for savefig function.

        Returns
        -------
        fig : matplotlib.pyplot.figure
            Figure instance. If ax is not None previously generated/passed fig instance
            will be returned. Return None, if no fig instance is inputed along with ax.
        ax : Axis instance
            Figure axis instance.
        CountFig: int or None
            Figure count.

        """
        if ax is None: 
            self.fig, ax = plt.subplots()
        else:
            self.fig = fig 
            
        if yaxis_label is None: yaxis_label=''
            
        result = self._data_curation_threshold(self.ZZ, threshold_weight=threshold_intensity)
        
        if vmin is None: vmin = np.nanmin(result)
        if vmax is None: vmax = np.nanmax(result)

        if mode == 'simple_2d_plot': 
            return_plot = ax.plot(self.XX, self.YY, color=line_color, ls=line_style)
        else:
            ax, return_plot = self._plot_colormesh(self.XX, self.YY, result, ax, 
                                                   cmap=color_map, color_scale=color_scale, 
                                                   vmin=vmin, vmax=vmax, 
                                                   show_contours=show_contours, 
                                                   contour_levels=contour_levels)
            
        if show_colorbar and (self.fig is not None):
            cbar = self.fig.colorbar(return_plot, ax=ax)
            if colorbar_label is not None:
                cbar.set_label(colorbar_label)
        
        ax.set_ylabel(yaxis_label)
        ax.set_xlabel(xaxis_label)
        if title_text is not None: ax.set_title(title_text)
        
        if mode in ["omega_2theta_space_map", "reciprocal_space_map"]:
            xx_, yy_ = self._plot_borders()
            ax.plot(xx_, yy_, c=line_color, ls=line_style)

        # set axis limits
        _xlims = [Xmin, Xmax]
        _ylims = [Ymin, Ymax]
        ax.set_xlim(_xlims)
        ax.set_ylim(_ylims)

        if _xlims.count(None) == len(_xlims):
            plt.autoscale(axis='x')
        if _ylims.count(None) == len(_ylims):
            plt.autoscale(axis='y')
       
        if save_file_name is None:
            if show_plot: plt.show()
        else:
            CountFig = self._save_figure(save_file_name, fig=self.fig, 
                                         savefig=savefig, show_plot=show_plot,
                                         CountFig=CountFig, **kwargs_savefig)
        return self.fig, ax, CountFig   

    def _plot_borders(self):
        return ((self.XX[0,0], self.XX[0,-1], self.XX[-1,-1], self.XX[-1,0], self.XX[0,0]), 
                (self.YY[0,0], self.YY[0,-1], self.YY[-1,-1], self.YY[-1,0], self.YY[0,0]))

    @classmethod
    def _get_color_scale(cls, color_scale, vmin=None, vmax=None):
        return cm.colors.LogNorm(vmin=vmin, vmax=vmax) if color_scale.lower() == 'log' \
                    else cm.colors.Normalize(vmin=vmin, vmax=vmax)
    @classmethod
    def _get_contour_levels(cls, color_scale, vmin, vmax, contour_levels:int):
        #print(vmin, vmax, np.logspace(vmin, vmax, contour_levels))
        return np.logspace(vmin, vmax, contour_levels) if color_scale.lower() == 'log' \
                    else np.linspace(vmin, vmax, contour_levels)
              
    def _plot_colormesh(self, XX, YY, ZZ, ax, 
                        cmap="jet", color_scale='linear', 
                        vmin=None, vmax=None, 
                        show_contours:bool=False,contour_levels=None):      
        """
        Plot density plot of band structure.

        Parameters
        ----------
        data_4_plot : numpy 2d array
            Data to plot.
        ax : matplotlib.pyplot axis, optional
            Figure axis to plot on. 
        cmap : str/ matplotlib colormap
            Colormap for density plot.The default is "jet".
        color_scale : str, optional ['log', 'linear']
            The default is 'linear'.
        vmin, vmax : float, optional
            vmin and vmax define the data range that the colormap covers. 
            By default, the colormap covers the complete value range of the supplied data.

        Returns
        -------
        ax : matplotlib.pyplot axis
            Figure axis to plot on. 
        pcm : matplotlib pcolormesh plot instance
            Plot instance.

        """
        norm = self._get_color_scale(color_scale, vmin=vmin, vmax=vmax)
        ax.set_aspect('auto')
        if show_contours:
            if contour_levels is None or isinstance(contour_levels, int): 
                vmin_contour = np.log10(10**np.floor(np.log10(vmin)))
                vmax_contour = np.log10(10**np.ceil(np.log10(vmax)))
                if contour_levels is None: 
                    contour_levels = 2*(int(vmax_contour - vmin_contour)) + 1
                    #print(vmax_contour, vmin_contour)
                contour_levels = self._get_contour_levels(color_scale,vmin_contour , 
                                                          vmax_contour, contour_levels)
            cset1 = ax.contourf(XX, YY, ZZ, levels=contour_levels, norm=norm,cmap=cmap)
            #cset2 = ax.contour(XX, YY, ZZ, cset1.levels, linewidths=1, colors='k')
            #cset2.set_linestyle('solid')
        else:
            cset1 = ax.pcolormesh(XX, YY, ZZ, shading='nearest', cmap=cmap, norm=norm)
        return ax, cset1
