#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 18:27:06 2026

@author: badal.mondal
"""

import numpy as np
from scipy import optimize
from ._alloy_params import _cal_alloy_params

### ===========================================================================
class _cal_strain_comp_rsm(_cal_alloy_params):
    @classmethod
    def _Qxy_theor(cls, a, c, mul_fact=[10000,10000], shift=[0,0], hkl=(1,0,5), structure_type:str='wz'):
        '''
        Definitions of Q_x and Q_y:
            Q_x_theor = qx_factor(str,hkl) / a_lattice_params_alloy(composition)
            Q_y_theor = qy_factor(str,hkl) / c_lattice_params_alloy(composition)
        
        Often Q_x and Q_y are rescalled by some factor, mul_fact:
            Q_x_theor = Q_x_theor * mul_fact[0]
            Q_y_theor = Q_y_theor * mul_fact[1]
            
        If needed the Q_x and Q_y values can be shifted along respective axes:
            Q_x_theor = Q_x_theor + shift[0]
            Q_y_theor = Q_y_theor + shift[1]

        Parameters
        ----------
        a : TYPE
            DESCRIPTION.
        c : TYPE
            DESCRIPTION.
        mul_fact : TYPE, optional
            DESCRIPTION. The default is [10000,10000].
        shift : TYPE, optional
            DESCRIPTION. The default is [0,0].
        hkl : TYPE, optional
            DESCRIPTION. The default is (1,0,5).
        structure_type : str, optional
            DESCRIPTION. The default is 'wz'.

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        Q_x_theor : TYPE
            DESCRIPTION.
        Q_y_theor : TYPE
            DESCRIPTION.

        '''
        if structure_type == 'wz':
            # qx_factor = 2/sqrt(3) * (h^2 + k^2 + h*k)
            # qy_factor = l (this is not one, it is 'L')
            qx_factor = 1.1547005383792517 * (hkl[0]*hkl[0] + hkl[1]*hkl[1] + hkl[0]*hkl[1]) 
            qy_factor = hkl[2]
        else:
            raise ValueError("Other structure types are not implemented yet. Allowed types 'wz'.")
        Q_x_theor, Q_y_theor = qx_factor/a*mul_fact[0] + shift[0], qy_factor/c*mul_fact[1] + shift[1]
        return Q_x_theor, Q_y_theor
    
    
    @classmethod
    def _calc_alloy_params(cls, t, binary_parameters, mul_fact, alloy_type, str_type, hkl):
        alloy_a, alloy_c, _, _, alloy_D = \
            _cal_alloy_params._alloy_parameters_from_binary(t, binary_parameters, 
                                                            alloy_type=alloy_type, 
                                                            structure_type=str_type)    
        Qx_theor, Qy_theor = cls._Qxy_theor(alloy_a, alloy_c, mul_fact=mul_fact, 
                                            hkl=hkl, structure_type=str_type)
        return alloy_D, Qx_theor, Qy_theor
    
    @classmethod
    def _calculate_FG_factors(cls, alloy_D, Qx, Qy):
        # F_fact, G_fact = alloy_D * Qx / Qy, (1. - alloy_D) / Qy
        return alloy_D * Qx / Qy, (1. - alloy_D) / Qy
    
    @classmethod
    def _calculate_full_strain_line(cls, Qxs, composition, binary_parameters, mul_fact, alloy_type, str_type, hkl):
        alloy_D, Qx_theor, Qy_theor  = \
            cls._calc_alloy_params(composition, binary_parameters, mul_fact, alloy_type, str_type, hkl)   
        F_fact, G_fact = cls._calculate_FG_factors(alloy_D, Qx_theor, Qy_theor) 
        return Qxs / (F_fact + Qxs * G_fact)
        
    @classmethod
    def _find_zero_of_function(cls, t, qxy_for_point, binary_parameters, mul_fact, alloy_type, str_type, hkl):
        alloy_D, Qx_theor, Qy_theor  = \
            cls._calc_alloy_params(t, binary_parameters, mul_fact, alloy_type, str_type, hkl)   
        F_fact, G_fact = cls._calculate_FG_factors(alloy_D, Qx_theor, Qy_theor)
        return qxy_for_point[1] * (F_fact + qxy_for_point[0] * G_fact) - qxy_for_point[0] 
        
    def _find_composition_strain_4_point(self, find_results_4_peak, reference_peak, f_args, comp_interval=[0, 1], 
                                         root_finding_method='brentq', fprime=None, fprime2=None, 
                                         x0=None, x1=None, xtol=None, rtol=None, maxiter=None):
        sol = optimize.root_scalar(self._find_zero_of_function, args=((find_results_4_peak,) + f_args), 
                                   bracket=comp_interval, method=root_finding_method, 
                                   fprime=fprime, fprime2=fprime2, x0=x0, x1=x1, xtol=xtol, rtol=rtol, maxiter=maxiter)
        assert sol.converged, 'Root finding not converged. Try other methods.'
        _, Qx2, _ = self._calc_alloy_params(sol.root, f_args[0], f_args[1], f_args[2], f_args[3], f_args[4])
        relaxation = (1 - reference_peak[0]/find_results_4_peak[0]) / (1 - reference_peak[0]/Qx2)
        if self.log_info is not None:
            print(f'Solution for requested peak/point: {find_results_4_peak}')
            print(f'\t{"-Composition (%)":<25}: {sol.root*100:.2f}')
            print(f'\t{"-Strain-relaxation (%)":<25}: {relaxation*100:.2f}')
        return sol, relaxation
