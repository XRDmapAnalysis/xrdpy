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
        
    def alloy_parameters_from_binary(self, x, list_binary_parameters, alloy_type='ternary', structure_type='wz'):
        return self._alloy_parameters_from_binary(x, list_binary_parameters, alloy_type=alloy_type, structure_type=structure_type)
        
class xrd(_xrd_read, _xrd_reciprocal, _xrdplot, _PeaksDetection):
    def __init__(self, print_log=None):
        if print_log is not None:
            print_log = print_log.lower()
        self.print_log = print_log
        
    def xrd_read_data(self, xrd_file_name='./test.xml'):
        _xrd_read.__init__(self, data_fname=xrd_file_name, log_info=self.print_log)
        return self._read_xrd_data()

    def Qxy(self, omega=None, two_theta=None, total_two_theta_in_row=2, xrd_file_name='./test.xml', 
            shift=[0,0], R=1, mul_fact=10000):
        _xrd_reciprocal.__init__(self, log_info=self.print_log)
        if omega is None or two_theta is None:
            _, two_theta, omega, _ = self.xrd_read_data(xrd_file_name)
            total_two_theta_in_row = np.shape(self.rsm_intesity)[1]
        return self._Qxy(omega, two_theta, total_two_theta_in_row, 
                         shift=shift, R_val=R, mul_fact=mul_fact)

    @classmethod
    def Qxy_theor(cls, a, c, mul_fact=10000, shift=[0,0], hkl='105'):
        return cls._Qxy_theor(a, c, mul_fact=mul_fact, shift=shift, hkl=hkl)

    def get_full_strain_line(self, reference_peak, no_strain_point, D):
        '''
        (x1, y1) = reference point
        (x2, y2) = point on no-strain line
        No-relaxation (fully strained) line: considering elastic relaxation
        Deformation potential = D 
        ==> point on full-strain line = (x1, y2+D(x1-x2))
        '''
        return self._calculate_full_strain_line(reference_peak, no_strain_point, D)

    def xrd_plot(self, save_figure_dir='.', fig=None, ax=None, 
                 save_file_name=None, CountFig=None, Ymin=None, Ymax=None, 
                 pad_y_scale:float=0.5, threshold_intensity:float=None,
                 mode:str="real_space_calc_omega_by_2theta", xaxis_label:str=r'2$\mathrm{\theta}$',
                 yaxis_label:str=r'$\omega$ / $2\theta$', marker='o', fatfactor=20,
                 smear:float=0.05, color='gray', color_map='jet', color_scale='linear',
                 show_legend:bool=True, show_colorbar:bool=True, colorbar_label:str=None,
                 vmin=None, vmax=None, show_plot:bool=True, **kwargs_savefig):
        
        _xrdplot.__init__(self, save_figure_dir=save_figure_dir)
        return self._plot(fig=fig, ax=ax, save_file_name=save_file_name, CountFig=CountFig,
                          Ymin=Ymin, Ymax=Ymax, pad_y_scale=pad_y_scale, threshold_intensity=threshold_intensity, 
                          mode=mode, xaxis_label=xaxis_label, yaxis_label=yaxis_label, color_scale=color_scale,
                          marker=marker, fatfactor=fatfactor, smear=smear, color=color, color_map=color_map, 
                          show_legend=show_legend, show_colorbar=show_colorbar, colorbar_label=colorbar_label,
                          vmin=vmin, vmax=vmax, show_plot=show_plot, **kwargs_savefig)
        
    def find_composition_strain_4_point(self, find_results_4_peak, reference_peak, optimize_f_args, 
                                        comp_interval=[0, 1], root_finding_method='brentq',
                                        fprime=None, fprime2=None, x0=None, x1=None, xtol=None, 
                                        rtol=None, maxiter=None):
        _xrd_reciprocal.__init__(self, log_info=self.print_log)
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
                 pad_y_scale:float=0.5, threshold_intensity:float=None,
                 mode:str="real_space_calc_omega_by_2theta", xaxis_label:str=r'2$\mathrm{\theta}$',
                 yaxis_label:str=r'$\omega$ / $2\theta$', title_text:str=None, marker='o', fatfactor=20,
                 smear:float=0.05, color='gray', color_map='jet',color_scale='linear',
                 show_legend:bool=True, show_colorbar:bool=True, colorbar_label:str=None,
                 vmin=None, vmax=None, show_plot:bool=True, 
                 show_contours:bool=False, **kwargs_savefig):
        
        _xrdplot.__init__(self, save_figure_dir=self.save_fig_dir, x_values=x_values, 
                          y_values=y_values, z_values=z_values)
        return self._plot(fig=fig, ax=ax, save_file_name=save_file_name, CountFig=CountFig,
                          Xmin=Xmin, Xmax=Xmax, Ymin=Ymin, Ymax=Ymax, 
                          pad_y_scale=pad_y_scale, threshold_intensity=threshold_intensity, 
                          mode=mode, xaxis_label=xaxis_label, yaxis_label=yaxis_label, 
                          title_text=title_text, color_scale=color_scale, 
                          marker=marker, fatfactor=fatfactor, smear=smear, color=color, color_map=color_map, 
                          show_legend=show_legend, show_colorbar=show_colorbar, colorbar_label=colorbar_label,
                          vmin=vmin, vmax=vmax, show_plot=show_plot, show_contours=show_contours,
                          **kwargs_savefig)

    def save_figure(self,fig_name, fig=None, CountFig=None, **kwargs_savefig):
        return self._save_figure(fig_name, fig=fig, CountFig=CountFig, **kwargs_savefig)
        
