#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 09:56:21 2026

@author: badal.mondal
"""
import numpy as np
from ._get_xrd import _xrd_read_file
from ._peak_detection import _PeaksDetection

### ===========================================================================
class _peack_alignment:
    def __init__(self, log_info=None):
        if log_info is not None:
            log_info = log_info.lower()
        self.log_info = log_info
    
    @classmethod
    def return_rotation_needed(cls, peak1, peak2, in_degree:bool=False):
        # peak1 corresponds to the point in 1st quadrant
        # peak2 corresponds to the point in 2nd quadrant
        angle_rotate_rad = 0.5*(np.pi - np.arctan2(peak2[1], peak2[0]) - 
                                np.arctan2(peak1[1], peak1[0]))
        if in_degree:
            return np.degrees(angle_rotate_rad) 
        else:
            return angle_rotate_rad
    @classmethod
    def rotate_vector_2d(cls, v, theta_rad):
        rotation_matrix = np.array([
            [np.cos(theta_rad), -np.sin(theta_rad)],
            [np.sin(theta_rad),  np.cos(theta_rad)]
        ])
        return rotation_matrix @ v
    
    @classmethod
    def rotate_vector_2d_xy(cls, X, Y, theta_rad):
        x_rotate = X*np.cos(theta_rad) - Y*np.sin(theta_rad)
        y_rotate = X*np.sin(theta_rad) + Y*np.cos(theta_rad)
        return x_rotate, y_rotate
    
    def _correct_omega_rotation(self, xrd_files, 
                                xrd_file_fmt:str = 'xrdml', 
                                xrd_scan_mode:str='omega_2theta_scan',
                                read_file_mode:str="reciprocal_space_map", 
                                peaks_2_align=0,
                                use_peaks_2_align_as_angle:bool=False,
                                shift=[0,0], mul_fact_xy_axis=[10000,10000], 
                                apply_filter:bool=True, threshold:float=None, 
                                sigma:float=1, filter_type='gaussian',
                                return_data_4_all:bool=False):
        
        _PeaksDetection.__init__(self, apply_filter=apply_filter, threshold=threshold, 
                                 sigma=sigma, filter_type=filter_type) 
        rec_space_data, align_peaks = {}, []
        for ii, xrd_file in enumerate(xrd_files):
            if self.log_info is not None: print(f'o Reading file: {xrd_file}')
            ############# Reading xrd files ###################################
            _xrd_read_file.__init__(self, xrd_scan_mode=xrd_scan_mode, 
                                    read_file_mode=read_file_mode, 
                                    data_fname=xrd_file, 
                                    data_file_fmt=xrd_file_fmt,
                                    log_info=self.print_log)   
            rsm_x, rsm_y, rsm_intesity = self._xrd_read_parse_file_(shift=shift, 
                                                                    mul_fact_xy_axis=
                                                                     mul_fact_xy_axis)
            peaks_x, peaks_y, peaks_z, _ = self._xrd_find_peaks(rsm_x, rsm_y, rsm_intesity)
            if isinstance(peaks_2_align, int):
                align_peaks.append([peaks_x[peaks_2_align], peaks_y[peaks_2_align]])
            elif isinstance(peaks_2_align, np.ndarray):
                align_peaks.append(peaks_2_align[ii])
            rec_space_data[ii] = {'x_initial_sup': rsm_x, 'y_initial_sup': rsm_y, 
                                       'intesity_sup': rsm_intesity, 
                                       'peak_xs': peaks_x, 'peak_ys': peaks_y, 
                                       'peak_zs': peaks_z}
        align_peaks = np.array(align_peaks)
        if use_peaks_2_align_as_angle:
            rotation_angle_rad = peaks_2_align
        else:
            rotation_angle_rad = self.return_rotation_needed(align_peaks[0], align_peaks[1])
        if self.log_info is not None:   
            for align_peaks_ in align_peaks:
                print(f'-Distance from origin for target peak {ii} = {np.sqrt(np.sum(np.array(align_peaks_)**2)):.5f}')
            print(f'Rotation needed: {rotation_angle_rad:.6f} rad = {np.degrees(rotation_angle_rad):.2f} degree')
        
        data_keys_ = list(rec_space_data.keys())
        if not return_data_4_all: data_keys_ = [data_keys_[0]]
            
        for key, rec_spec in rec_space_data.items():
            ## Rotate all peaks
            peaks_x_rotate, peaks_y_rotate = \
                self.rotate_vector_2d_xy(rec_spec['peak_xs'], rec_spec['peak_ys'], rotation_angle_rad)
            ## Rotate full reciprocal xrd maps
            rec_space_x_rotate, rec_space_y_rotate =\
                self.rotate_vector_2d_xy(rec_spec['x_initial_sup'], rec_spec['y_initial_sup'], rotation_angle_rad)
            
            rec_space_data[key]['x_final'] = rec_space_x_rotate
            rec_space_data[key]['y_final'] = rec_space_y_rotate
            rec_space_data[key]['peaks_x_final'] = peaks_x_rotate
            rec_space_data[key]['peaks_y_final'] = peaks_y_rotate

        return rec_space_data if return_data_4_all else rec_space_data[0]
    
    def _align_xrd_peaks(self, xrd_files, xrd_file_fmt:str = 'xrdml', 
                         xrd_scan_mode:str='omega_2theta_scan',
                         read_file_mode:str="reciprocal_space_map",
                         peaks_2_align=0,
                         use_peaks_2_align_as_angle:bool=False,
                         alignment_mode:str="omega_rotation", 
                         shift=[0,0], mul_fact_xy_axis=[10000,10000], 
                         apply_filter:bool=True, threshold:float=None, 
                         sigma:float=1, filter_type='gaussian',
                         return_data_4_all:bool=False):
        if alignment_mode == 'omega_rotation':
            return self._correct_omega_rotation(xrd_files, 
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
                                                return_data_4_all=
                                                return_data_4_all)
