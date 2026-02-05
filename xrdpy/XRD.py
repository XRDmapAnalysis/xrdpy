import numpy as np
from .src import _cal_alloy_params, _cal_strain_comp_rsm, _xrd_read_file
from .src import _PeaksDetection, _peack_alignment, _xrdplot
from .BasicFunctions import _GeneratePlots

### ===========================================================================
class general_fns(_cal_alloy_params):
    def __init__(self, print_log=None):
        if print_log is not None:
            print_log = print_log.lower()
        self.print_log = print_log
        _cal_alloy_params.__init__(self)
        
    def alloy_parameters_from_binary(self, composition, list_binary_parameters, 
                                     alloy_type:str='ternary', structure_type:str='wz'):
        """
        This function calculates alloy parameters from its binaries.

        Parameters
        ----------
        composition : float
            Composition of the alloy to be evaluated.
        list_binary_parameters : list of 3 floats [bin_1, bin_2, and bowing]
            List of parameters for binary systems. It can be nested list, e.g. 
            [[AlN_a, GaN_a, bowing_a], [AlN_c, GaN_c, bowing_c]]
        alloy_type : str, optional [options: 'ternary']
            Type of ally. The default is 'ternary'.
        structure_type : str, optional [options: 'wz']
            Crytal structure of the alloy. The default is 'wz'.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self._alloy_parameters_from_binary(composition, list_binary_parameters, 
                                                  alloy_type=alloy_type, 
                                                  structure_type=structure_type)
#==============================================================================        
class xrd(_xrd_read_file, _cal_strain_comp_rsm, _xrdplot, _PeaksDetection, _peack_alignment):
    def __init__(self, print_log=None):
        if print_log is not None:
            print_log = print_log.lower()
        self.print_log = print_log
      
    def xrd_read_file(self, xrd_file_name, xrd_file_fmt:str = 'xrdml', 
                      xrd_scan_mode:str='omega_2theta_scan',
                      read_file_mode:str="reciprocal_space_map", 
                      shift=[0,0], mul_fact_xy_axis=[1,1]):
        """
        This function reads the XRD file and/or generate reciprocal space data.

        Parameters
        ----------
        xrd_file_name : str or file object
            The file name. 
        xrd_file_fmt : str, optional [options: 'xrdml']
            Format for the xrd file to be read. Different file formats will be
            parsed differently. Contact developer to add support for other file
            formats. The default is 'xrdml'.
        xrd_scan_mode : str, optional [options: 'omega_2theta_scan'] # 'omega_scan' have not implemented yet.
            The data collection mode of XRD scan. 
            If  The default is "omega_2theta_scan"
        read_file_mode : str, optional [options: 'omega_2theta_space_map', 'reciprocal_space_map']
            The mode of reading file. 'omega_2theta_space_map' will read the file and
            output results in real space. 'reciprocal_space_map' will read the file and
            and convert them to resiprocal space and output results in resiprocal space.
            If  The default is "reciprocal_space_map".
        shift : list of 2 floats, optional
            Shift the x and y-cordinates of the data points by shift amount, i.e.,
            x_val += shift[0], y_val += shift[1].
            The default is [0,0].
        mul_fact_xy_axis : list of 2 floats, optional
            Multipy the x and y-cordinates of the data points by this amount, i.e.,
            x_val *= shift[0], y_val *= shift[1]. 
            The default is [1,1].

        Returns
        -------
        ndarrays [x, y, intensity_values]
            This ndarrays can be directly passed to the xrd_plot function.
            For xrd_file_fmt = 'xrdml':
                For 'reciprocal_space_map' returns the X, Y, and Z/intensity-values for the RSM.
                For 'omega_2theta_space_map' return 2-theta, Omega/2-theta, and intensity values.

        """
        _xrd_read_file.__init__(self, xrd_scan_mode=xrd_scan_mode, 
                                read_file_mode=read_file_mode, 
                                data_fname=xrd_file_name, 
                                data_file_fmt=xrd_file_fmt,
                                log_info=self.print_log)
        return self._xrd_read_parse_file_(shift=shift, mul_fact_xy_axis=mul_fact_xy_axis)

    def xrd_plot(self, save_figure_dir='.', fig=None, ax=None, save_file_name=None,  
                 CountFig=None, Xmin=None, Xmax=None, Ymin=None, Ymax=None, 
                 threshold_intensity:float=None, mode:str="reciprocal_space_map", 
                 xaxis_label:str='Qx (rlu)', yaxis_label:str='Qz (rlu)', 
                 title_text:str=None, color_map='jet', color_scale='log', line_color='k',
                 line_style='--', vmin=None, vmax=None, show_colorbar:bool=True,   
                 colorbar_label:str=None, show_contours:bool=True, contour_levels=None,
                 show_plot:bool=True, savefig:bool=False, **kwargs_savefig):
        """
        This function is for plottings. It supports plottings of XRD plots 
        automatically from XRD data or user specified specific 2D plots.
        
        Parameters
        ----------
        save_figure_dir : str, optional
            The folder path where to save the figure. Default is current folder.
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
        self.plt_mode = mode
        _xrdplot.__init__(self, save_figure_dir=save_figure_dir)
        return self._plot(fig=fig, ax=ax, save_file_name=save_file_name, 
                          CountFig=CountFig, Xmin=Xmin, Xmax=Xmax, Ymin=Ymin, Ymax=Ymax, 
                          threshold_intensity=threshold_intensity, mode=mode, 
                          xaxis_label=xaxis_label, yaxis_label=yaxis_label, 
                          title_text=title_text, color_scale=color_scale,
                          line_color=line_color, line_style=line_style,
                          color_map=color_map, show_colorbar=show_colorbar, 
                          colorbar_label=colorbar_label, vmin=vmin, vmax=vmax, 
                          show_contours=show_contours, contour_levels=contour_levels,
                          show_plot=show_plot, savefig=savefig, **kwargs_savefig)
        
    ###################### Analysis of RSM ####################################
    def find_peaks(self, x_values, y_values, z_values, apply_filter:bool=True, 
                   threshold:float=None, sigma:float=1, filter_type='gaussian'):
        """
        This function find peaks where intensity are high. It applies image filter,
        to reduce noice in the image. Then applies peak detection algorithm to
        find peaks in the noise filtered image.
        
        NOTE: You have to play with threshold and sigma value for finding all peaks. 
        Need enough "threshold" to get-rid-of low intensity peaks, otherwise a lot of 
        local peaks will be detected. "Sigma" then applies smoothening on the noise 
        filtered image to simplify the peak detection. 

        Parameters
        ----------
        x_values : ndarray
            x-values of the image. 
        y_values : ndarray
            y-values of the image.
        z_values : ndarray
            Intensity/z-values of the image.
        apply_filter : bool, optional
            If to apply filter. The default is True.
        threshold : float, optional
            It helps to reduce low intensity noise intensity data. 
            The default is None.
        sigma : float, optional
            The gausian width when applying Gaussian filter. This smoothen out the
            image to help the peak detection. The default is 1.
        filter_type : TYPE, optional [options: 'gaussian']
            Type of filter to reduce noise in the image. The default is 'gaussian'.

        Returns
        -------
        Tuple of ndarray (peaks_x, peaks_y, peaks_z, image_z_filter in data coordinate)
            x-cordinates, y-coordinates, z-coordinates of the peaks. It also return
            z-coordinates/intensity of the image after filter.

        """
        _PeaksDetection.__init__(self, apply_filter=apply_filter, threshold=threshold, 
                                 sigma=sigma, filter_type=filter_type)
        return self._xrd_find_peaks(x_values, y_values, z_values) 

    def align_peaks(self, xrd_files, xrd_file_fmt:str = 'xrdml', 
                    xrd_scan_mode:str='omega_2theta_scan',
                    read_file_mode:str="reciprocal_space_map",
                    peaks_2_align=0,
                    use_peaks_2_align_as_angle:bool=False,
                    alignment_mode:str="omega_rotation",
                    shift=[0,0], mul_fact_xy_axis=[1,1], 
                    apply_filter:bool=True, threshold:float=None, 
                    sigma:float=1, filter_type='gaussian',
                    return_data_4_all:bool=False):
        """
        This function allows to align multiple RSM plots along target position.

        Parameters
        ----------
        xrd_files : list of str or file path
            List of file paths and name.
        xrd_file_fmt : str, optional [options: 'xrdml']
            Format for the xrd file to be read. Different file formats will be
            parsed differently. Contact developer to add support for other file
            formats. The default is 'xrdml'.
        xrd_scan_mode : str, optional [options: 'omega_2theta_scan'] # 'omega_scan' have not implemented yet.
            The data collection mode of XRD scan. 
            If  The default is "omega_2theta_scan"
        read_file_mode : str, optional [options: 'omega_2theta_space_map', 'reciprocal_space_map']
            The mode of reading file. 'omega_2theta_space_map' will read the file and
            output results in real space. 'reciprocal_space_map' will read the file and
            and convert them to resiprocal space and output results in resiprocal space.
            If  The default is "reciprocal_space_map".
        peaks_2_align : int, float, or 2d numpy array, optional
            If integer specific peaks will be in that index will be aligned.
            If array, peak positions ([x,y]) of the RSM plots should be supplied.
            It can be a single float that can be pass as rotation angle in radian.
            In this case, one single xrd file should be fine.
            For 'rotation angle', it should be in radian.
            The default is 0.
        use_peaks_2_align_as_angle : bool, optional
            If to treat the peaks_2_align as an angle rather than peak index.
            The default is False.
        alignment_mode : str, optional [options: "omega_rotation"]
            The mode to align the peaks. The default is "omega_rotation".
        shift : list of 2 floats, optional
            Shift the x and y-cordinates of the data points by shift amount, i.e.,
            x_val += shift[0], y_val += shift[1].
            The default is [0,0].
        mul_fact_xy_axis : list of 2 floats, optional
            Multipy the x and y-cordinates of the data points by this amount, i.e.,
            x_val *= shift[0], y_val *= shift[1]. 
            The default is [1,1].
        apply_filter : bool, optional
            If to apply filter. The default is True.
        threshold : float, optional
            It helps to reduce low intensity noise intensity data. 
            The default is None.
        sigma : float, optional
            The gausian width when applying Gaussian filter. This smoothen out the
            image to help the peak detection. The default is 1.
        filter_type : str or matplotlib filter, optional [options: 'gaussian']
            Type of filter to reduce noise in the image. The default is 'gaussian'.
        return_data_4_all : bool, optional
            Determines if to return full data for all the files. If False only
            full data for only the first file will be returned. The default is False.

        Returns
        -------
        Nested disctionary 
            Dictionary containing supplied data values, the peaks found, and the 
            final changed data values after application of alignment.
            Here, the keys are in this order: ['x_initial_sup','y_initial_sup', 
            'intesity_sup', 'peak_xs', 'peak_ys', 'peak_zs', 'x_final','y_final',
            'peaks_x_final','peaks_y_final'] 
            Additionally upper level dictionary with dictionary key as number 
            1,2,.. mimicking the files read in order will be nested around, when
            return_data_4_all is True.

        """
        _peack_alignment.__init__(self, log_info=self.print_log)
        return self._align_xrd_peaks(xrd_files, 
                                     xrd_file_fmt = xrd_file_fmt, 
                                     xrd_scan_mode=xrd_scan_mode,
                                     read_file_mode=read_file_mode,
                                     peaks_2_align=peaks_2_align,
                                     use_peaks_2_align_as_angle=
                                     use_peaks_2_align_as_angle,
                                     shift=shift, mul_fact_xy_axis=
                                     mul_fact_xy_axis, apply_filter=apply_filter,  
                                     threshold=threshold, sigma=sigma, 
                                     filter_type=filter_type, 
                                     return_data_4_all=return_data_4_all)
        
    ###################### Properties from RSM ################################
    @classmethod
    def Qxy_theor(cls, a, c, mul_fact=[10000,10000], shift=[0,0], hkl=(1,0,5), structure_type='wz'):
        return cls._Qxy_theor(a, c, mul_fact=mul_fact, shift=shift, hkl=hkl, structure_type=structure_type)

    @classmethod
    def get_full_strain_line(cls, Qxs, composition, binary_parameters, mul_fact, alloy_type, str_type, hkl):
        return cls._calculate_full_strain_line(Qxs, composition, binary_parameters, mul_fact, alloy_type, str_type, hkl)
        
    def find_composition_strain_4_point(self, find_results_4_peak, reference_peak, optimize_f_args, 
                                        comp_interval=[0, 1], root_finding_method='brentq',
                                        fprime=None, fprime2=None, x0=None, x1=None, xtol=None, 
                                        rtol=None, maxiter=None, show_optimization_fn:bool=False):
        if show_optimization_fn:
            Qxs = np.linspace(0, 1, 11)
            Qys = self._find_zero_of_function(Qxs, find_results_4_peak, *optimize_f_args)
            _xrdplot.__init__(self, save_figure_dir='.', x_values=Qxs, 
                              y_values=Qys, z_values=[[None]])
            fig, ax, _ = self._plot(fig=None, ax=None, save_file_name=None, CountFig=None,
                                   Xmin=0, Xmax=1, Ymin=None, Ymax=None, threshold_intensity=None,  
                                   mode="simple_2d_plot", xaxis_label=r'composition (t)',
                                   yaxis_label=r'f$_{opt} (Q^{\prime}_x, Q^{\prime}_y, t, f_{qx}, f_{qy})$', title_text=None,
                                   line_color='k', line_style='-', show_plot=True, 
                                   savefig=False, dpi=75)
            ax.axhline(y=0, c='k', ls='--')
        return self._find_composition_strain_4_point(find_results_4_peak, reference_peak, optimize_f_args, 
                                                     comp_interval=comp_interval,
                                                     root_finding_method=root_finding_method,
                                                     fprime=fprime, fprime2=fprime2, x0=x0, x1=x1,
                                                     xtol=xtol, rtol=rtol, maxiter=maxiter)
    
#==============================================================================
class plottings(_xrdplot, _GeneratePlots):
    def __init__(self, save_figure_dir='.', print_log=None):
        if print_log is not None:
            print_log = print_log.lower()
        self.print_log = print_log
        self.save_fig_dir = save_figure_dir

    def xrd_plot(self, x_values, y_values, z_values, 
                 fig=None, ax=None,save_file_name=None, CountFig=None,  
                 Xmin=None, Xmax=None, Ymin=None, Ymax=None,
                 threshold_intensity:float=None, mode:str="reciprocal_space_map", 
                 xaxis_label:str='Qx (rlu)', yaxis_label:str='Qy (rlu)',  
                 title_text:str=None, color_map='jet', color_scale='log', line_color='k',
                 line_style='--', show_colorbar:bool=True, colorbar_label:str=None,  
                 vmin=None, vmax=None, show_contours:bool=True, contour_levels=None, 
                 show_plot:bool=True, savefig:bool=False, **kwargs_savefig):
        """
        This function is for plottings. It supports plottings of XRD plots 
        automatically from XRD data or user specified specific 2D plots.

        Parameters
        ----------
        x_values : ndarray
            The X-coordinates of the map. For XRD maps it is grid format.
            1D numpy array in 'simple_2d_plot' mode. x_values, y_values, and 
            z_values should be of the same ndarray shape.
        y_values : ndarray
            The X-coordinates of the map. For XRD maps it is grid format.
            1D numpy array in 'simple_2d_plot' mode. x_values, y_values, and 
            z_values should be of the same ndarray shape.
        z_values : ndarray
            The X-coordinates of the map. For XRD maps it is grid format.
            1D numpy array in 'simple_2d_plot' mode. x_values, y_values, and 
            z_values should be of the same ndarray shape.
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
        
        _xrdplot.__init__(self, save_figure_dir=self.save_fig_dir, x_values=x_values, 
                          y_values=y_values, z_values=z_values)
        self.plt_mode = ''
        return self._plot(fig=fig, ax=ax, save_file_name=save_file_name, 
                          CountFig=CountFig, Xmin=Xmin, Xmax=Xmax, Ymin=Ymin, Ymax=Ymax, 
                          threshold_intensity=threshold_intensity, mode=mode, 
                          xaxis_label=xaxis_label, yaxis_label=yaxis_label, 
                          title_text=title_text, color_scale=color_scale, 
                          line_color=line_color, line_style=line_style,
                          color_map=color_map, show_colorbar=show_colorbar, 
                          colorbar_label=colorbar_label, vmin=vmin, vmax=vmax, 
                          show_contours=show_contours, contour_levels=contour_levels, 
                          show_plot=show_plot, savefig=savefig, **kwargs_savefig)

    def save_figure(self,fig_name, fig=None, savefig:bool=True, show_plot:bool=True, 
                    CountFig=None, **kwargs_savefig):
        """
        

        Parameters
        ----------
        fig_name : str
            Name of the figure including extension.
        fig : matplotlib figure instance, optional
            matplotlib figure instance. The default is None.
        savefig : bool, optional
            If to save figure. The default is True.
        show_plot : bool, optional
            If to show plot or not. The default is True.
        CountFig : TYPE, optional
            Figure count. The default is None.
        **kwargs_savefig : TYPE
            The matplotlib keywords for savefig function..

        Returns
        -------
        CountFig: int or None
            Figure count.

        """
        return self._save_figure(fig_name, fig=fig, savefig=savefig, show_plot=show_plot, 
                                 CountFig=CountFig, **kwargs_savefig)
        
