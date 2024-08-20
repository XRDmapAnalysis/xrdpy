import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from ..BasicFunctions._general_plot_functions import _GeneratePlots

### ===========================================================================
class _xrdplot(_GeneratePlots):
    """
    Plotting xrd data.

    """
    def __init__(self, x_values=None, y_values=None, z_values=None, 
                 save_figure_dir='.'):
        """
        Initialize the band structure plotting class.

        Parameters
        ----------
        rsm_intesity : 2D array, optional
            Reciprocal map intensity values. The default is None.
        save_figure_dir : str/path, optional
            Directory where to save the figure. The default is current directory.
            
        Returns
        -------
        

        """
        _GeneratePlots.__init__(self, save_figure_dir=save_figure_dir)
        
        if z_values is None:
            try:
                self.ZZ = self.rsm_values.copy()
            except:
                raise ValueError('Provide reciprocal map intensity values.')
        else:
            self.ZZ = z_values.copy()

        if x_values is None:
            try:
                self.XX = self.two_theta_values.copy()
            except:
                raise ValueError('Provide 2 theta values (in real space) or Qx (in reciprocal space).')
        else:
            self.XX = x_values.copy()

        if y_values is None:
            try:
                self.YY = self.omega_values.copy()
            except:
                raise ValueError('Provide omega values (in real space) or Qy (in reciprocal space).')
        else:
            self.YY = y_values.copy()

        self.row_n, self.col_n = np.shape(self.ZZ)

    @classmethod
    def _data_curation_threshold(cls, full_data, threshold_weight:float=1e-5):
        result = full_data.copy()
        if threshold_weight is not None: 
            result[result < threshold_weight] = np.nan
        return result

    def _plot(self, fig=None, ax=None, save_file_name=None, CountFig=None, 
              Xmin=None, Xmax=None, Ymin=None, Ymax=None, 
              threshold_intensity:float=None,  
              mode:str="real_space", xaxis_label:str=r'2$\mathrm{\theta}$',
              yaxis_label:str=r'$\omega$ / $2\theta$', title_text=None,  
              color_map='viridis', color_scale='linear', line_color='k',
              line_style='--', show_colorbar:bool=False, colorbar_label:str=None,
              vmin=None, vmax=None, show_plot:bool=True, show_contours:bool=False,
              savefig:bool=False, **kwargs_savefig):
        """
        Plot of the maps.

        Parameters
        ----------
        fig : matplotlib.pyplot figure instance, optional
            Figure instance to plot on. The default is None.
        ax : matplotlib.pyplot axis, optional
            Figure axis to plot on. If None, new figure will be created.
            The default is None.
        save_file_name : str, optional
            Name of the figure file. If None, figure will be not saved. 
            The default is None.
        CountFig: int, optional
            Figure count. The default is None.
        Ymin : float, optional
            Minimum in Y-scale. The default is None.
        Ymax : float, optional
            Maximum in Y-scale. The default is None.
        threshold_intensity : float, optional
            The rsm_intensities with intensities lower than the threshold_intensity 
            are discarded. The default is None. If None, this is ignored.
        mode : ['real_space', 'reciprocal_space', 'simple_2d_plot'], optional
            Mode of plot. The default is "real_space".
        xaxis_label : str, optional
            X-axis label text. The default is '2theta'.
        yaxis_label : str, optional
            Y-axis label text. The default is 'omega/2theta'.
        color_map: str/ matplotlib colormap
            Colormap for density plot. The default is viridis.
        color_scale : str, optional ['log', 'linear']
            The default is 'linear'.
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
        show_plot : bool, optional
            To show the plot when not saved. The default is True.
        savefig : bool, optional
            To save the plot. Ignored when save_file_name is None. The default is True.
        **kwargs_savefig : dict
            The matplotlib keywords for savefig function.
        
        Raises
        ------
        ValueError
            If plot mode is unknown.

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
        
        # Plot as fat band
        if "real_space" in mode:
            self.XX = np.array([np.linspace(start_, end_, num=self.col_n) for start_, end_ in self.XX])
            self.YY = np.array([[omega_val]*self.col_n for ii, omega_val in enumerate(self.YY)])
            ax, return_plot = self._plot_colormesh(self.XX, self.YY, result, ax, cmap=color_map, color_scale=color_scale, 
                                                    vmin=vmin, vmax=vmax, show_contours=show_contours)
        elif "reciprocal_space" in mode:
            ax, return_plot = self._plot_colormesh(self.XX, self.YY, result, ax, cmap=color_map, color_scale=color_scale, 
                                                    vmin=vmin, vmax=vmax, show_contours=show_contours)
        elif mode == 'simple_2d_plot': 
            return_plot = ax.plot(self.XX, self.YY, color=line_color, ls=line_style)
        else:
            raise ValueError("Unknownplot mode: '{}'".format(mode))
            
        if show_colorbar and (self.fig is not None):
            cbar = self.fig.colorbar(return_plot, ax=ax)
            if colorbar_label is not None:
                cbar.set_label(colorbar_label)
        
        ax.set_ylabel(yaxis_label)
        ax.set_xlabel(xaxis_label)
        if title_text is not None: ax.set_title(title_text)
        
        if mode in ["real_space", "reciprocal_space"]:
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
        if color_scale.lower() == 'log': 
            return colors.LogNorm(vmin=vmin, vmax=vmax) # logarithmic
        else: 
            return colors.Normalize(vmin=vmin, vmax=vmax) # linear
              
    def _plot_colormesh(self, two_theta, omega_list, data_4_plot, ax, 
                        cmap="jet", color_scale='linear', 
                        vmin=None, vmax=None, show_contours:bool=False):      
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
        pcm = ax.pcolormesh(two_theta, omega_list, data_4_plot, shading='nearest', 
                            cmap=cmap, norm=self._get_color_scale(color_scale, vmin=vmin, vmax=vmax))
        ax.set_aspect('auto')
        if show_contours:
            CS = ax.contour(two_theta, omega_list, data_4_plot, colors='k', linewidths=1)
            #ax.clabel(CS, inline=True, fontsize=10)
        return ax, pcm
