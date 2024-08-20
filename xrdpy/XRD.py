import numpy as np
from .src import _general_fns, _xrd_read, _xrd_reciprocal, _xrdplot, _PeaksDetection
from .BasicFunctions import _GeneratePlots

### ===========================================================================
class general_fns(_general_fns):
    def __init__(self, print_log=None):
        if print_log is not None:
            print_log = print_log.lower()
        self.print_log = print_log
        _general_fns.__init__(self)
        
    def alloy_parameters_from_binary(self, x, list_binary_parameters, 
                                     alloy_type='ternary', structure_type='wz'):
        return self._alloy_parameters_from_binary(x, list_binary_parameters, 
                                                  alloy_type=alloy_type, 
                                                  structure_type=structure_type)
        
class xrd(_xrd_read, _xrd_reciprocal, _xrdplot, _PeaksDetection):
    def __init__(self, print_log=None):
        if print_log is not None:
            print_log = print_log.lower()
        self.print_log = print_log
        
    def xrd_read_data(self, xrd_file_name='./test.xml'):
        _xrd_read.__init__(self, data_fname=xrd_file_name, log_info=self.print_log)
        return self._read_xrd_data()

    def Qxy(self, omega=None, two_theta=None, total_two_theta_in_row=2, 
            xrd_file_name='./test.xml', shift=[0,0], R=1, mul_fact=10000):
        _xrd_reciprocal.__init__(self, log_info=self.print_log)
        if omega is None or two_theta is None:
            _, two_theta, omega, _ = self.xrd_read_data(xrd_file_name)
            total_two_theta_in_row = np.shape(self.rsm_intesity)[1]
        return self._Qxy(omega, two_theta, total_two_theta_in_row, 
                         shift=shift, R_val=R, mul_fact=mul_fact)

    @classmethod
    def Qxy_theor(cls, a, c, mul_fact=10000, shift=[0,0], hkl=(1,0,5), structure_type='wz'):
        return cls._Qxy_theor(a, c, mul_fact=mul_fact, shift=shift, hkl=hkl, structure_type=structure_type)

    @classmethod
    def get_full_strain_line(cls, Qxs, composition, binary_parameters, mul_fact, alloy_type, str_type, hkl):
        return cls._calculate_full_strain_line(Qxs, composition, binary_parameters, mul_fact, alloy_type, str_type, hkl)

    def xrd_plot(self, save_figure_dir='.', fig=None, ax=None, save_file_name=None,  
                 CountFig=None, Xmin=None, Xmax=None, Ymin=None, Ymax=None, 
                 threshold_intensity:float=None, mode:str="real_space", 
                 xaxis_label:str=r'2$\mathrm{\theta}$',
                 yaxis_label:str=r'$\omega$ / $2\theta$', title_text:str=None, 
                 color_map='jet', color_scale='linear', line_color='k',
                 line_style='--', vmin=None, vmax=None, show_colorbar:bool=True,   
                 colorbar_label:str=None, show_plot:bool=True,  
                 savefig:bool=False, **kwargs_savefig):
        
        _xrdplot.__init__(self, save_figure_dir=save_figure_dir)
        return self._plot(fig=fig, ax=ax, save_file_name=save_file_name, 
                          CountFig=CountFig, Xmin=Xmin, Xmax=Xmax, Ymin=Ymin, Ymax=Ymax, 
                          threshold_intensity=threshold_intensity, mode=mode, 
                          xaxis_label=xaxis_label, yaxis_label=yaxis_label, 
                          title_text=title_text, color_scale=color_scale,
                          line_color=line_color, line_style=line_style,
                          color_map=color_map, show_colorbar=show_colorbar, 
                          colorbar_label=colorbar_label, vmin=vmin, vmax=vmax, 
                          show_plot=show_plot, savefig=savefig, 
                          **kwargs_savefig)
        
    def find_composition_strain_4_point(self, find_results_4_peak, reference_peak, optimize_f_args, 
                                        comp_interval=[0, 1], root_finding_method='brentq',
                                        fprime=None, fprime2=None, x0=None, x1=None, xtol=None, 
                                        rtol=None, maxiter=None, show_optimization_fn:bool=False):
        _xrd_reciprocal.__init__(self, log_info=self.print_log)
        
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
        

    def find_peaks(self, x_values, y_values, z_values,
                   apply_filter:bool=False, threshold:float=None, 
                   sigma:float=1, filter_type='gaussian'):
        _PeaksDetection.__init__(self, apply_filter=apply_filter, threshold=threshold, 
                                 sigma=sigma, filter_type=filter_type)
        return self._xrd_find_peaks(x_values, y_values, z_values)       

class plottings(_xrdplot, _GeneratePlots):
    def __init__(self, save_figure_dir='.', print_log=None):
        if print_log is not None:
            print_log = print_log.lower()
        self.print_log = print_log
        self.save_fig_dir = save_figure_dir

    def xrd_plot(self, x_values=None, y_values=None, z_values=None, 
                 fig=None, ax=None,save_file_name=None, CountFig=None,  
                 Xmin=None, Xmax=None, Ymin=None, Ymax=None,
                 threshold_intensity:float=None, mode:str="real_space", 
                 xaxis_label:str=r'2$\mathrm{\theta}$',
                 yaxis_label:str=r'$\omega$ / $2\theta$', title_text:str=None, 
                 color_map='jet', color_scale='linear', line_color='k',
                 line_style='--', show_colorbar:bool=True, colorbar_label:str=None,  
                 vmin=None, vmax=None, show_plot:bool=True, savefig:bool=False, 
                 show_contours:bool=False, **kwargs_savefig):
        
        _xrdplot.__init__(self, save_figure_dir=self.save_fig_dir, x_values=x_values, 
                          y_values=y_values, z_values=z_values)
        return self._plot(fig=fig, ax=ax, save_file_name=save_file_name, 
                          CountFig=CountFig, Xmin=Xmin, Xmax=Xmax, Ymin=Ymin, Ymax=Ymax, 
                          threshold_intensity=threshold_intensity, mode=mode, 
                          xaxis_label=xaxis_label, yaxis_label=yaxis_label, 
                          title_text=title_text, color_scale=color_scale, 
                          line_color=line_color, line_style=line_style,
                          color_map=color_map, show_colorbar=show_colorbar, 
                          colorbar_label=colorbar_label, vmin=vmin, vmax=vmax, 
                          show_plot=show_plot, show_contours=show_contours,
                          savefig=savefig, **kwargs_savefig)

    def save_figure(self,fig_name, fig=None, savefig:bool=True, show_plot:bool=True, 
                    CountFig=None, **kwargs_savefig):
        return self._save_figure(fig_name, fig=fig, savefig=savefig, show_plot=show_plot, 
                                 CountFig=CountFig, **kwargs_savefig)
        
