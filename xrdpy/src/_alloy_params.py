#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 18:30:35 2026

@author: badal.mondal
"""
import numpy as np

### ===========================================================================
class _cal_alloy_params:
    def __init__(self, print_log=None):
        if print_log is not None:
            print_log = print_log.lower()
        self.print_log = print_log

    @staticmethod
    def _distance_calculator(p1, p2):
        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p1[1])**2)
        
    @staticmethod
    def _ternary_extrapolation(x, a_bin, b_bin, bowing:float=0):
        return a_bin * x + b_bin * (1.0 - x) + bowing * x * (1.0 - x)

    @classmethod
    def _ternary_alloy_params(cls, t, list2Dwhat2extrapolate):
        '''
        list2Dwhat2extrapolate: [[a_lattice_parameter bin_1, a_lattice_parameter bin_2, bowing], ...]
        '''
        return (cls._ternary_extrapolation(t, what2extrapolate[0], what2extrapolate[1], bowing=what2extrapolate[2]) 
                for what2extrapolate in list2Dwhat2extrapolate)

    @staticmethod
    def _wz_elastic_distortion_coefficient(c13, c33):
        # Distortion coefficient = -2C13/C33
        return -2*c13/c33
        
    @classmethod
    def _find_distortion_coefficient(cls, c13, c33, str_typ='wz'):
        if str_typ == 'wz':
            return cls._wz_elastic_distortion_coefficient(c13, c33)
        else:
            raise ValueError("Structure type is not implemented yet. Allowed types 'wz'.")

    @classmethod 
    def _alloy_parameters_from_binary(cls, t, list2Dwhat2extrapolate, alloy_type='ternary', structure_type='wz'):
        if alloy_type == 'ternary':
            if structure_type == 'wz':
                alloy_a, alloy_c, alloy_C13, alloy_C33 = cls._ternary_alloy_params(t, list2Dwhat2extrapolate)  
                alloy_D = cls._find_distortion_coefficient(alloy_C13, alloy_C33, str_typ=structure_type) 
                return alloy_a, alloy_c, alloy_C13, alloy_C33, alloy_D
            else:
                raise ValueError("Other structure types are not implemented yet. Allowed types 'wz'.")
        else:
            raise ValueError("Other alloy types are not implemented yet. Allowed types 'ternary'.")
        return 