import xml.etree.ElementTree as ET
import numpy as np
from scipy import optimize
from ..BasicFunctions.constants_ import wave_lenth_dict, degree2radian

### ===========================================================================
class _general_fns:
    def __init__(self, print_log=None):
        if print_log is not None:
            print_log = print_log.lower()
        self.print_log = print_log

    @staticmethod
    def _distance_calculator(p1, p2):
        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p1[1])**2)
        
    @staticmethod
    def _ternary_extrapolation(x, a_bin, b_bin, bowing:float=0):
        return a_bin * x + b_bin * (1.0 - x) + bowing * x * (1-x)

    @classmethod
    def _ternary_alloy_params(cls, t, list2Dwhat2extrapolate):
        '''
        list2Dwhat2extrapolate: [[a_lattice_parameter bin_1, a_lattice_parameter bin_2, bowing], ...]
        '''
        return (_general_fns._ternary_extrapolation(t, what2extrapolate[0], what2extrapolate[1], bowing=what2extrapolate[2]) 
                for what2extrapolate in list2Dwhat2extrapolate)

    @staticmethod
    def _wz_elastic_distortion_coefficient(c13, c33):
        # Distortion coefficient = -2C13/C33
        return -2*c13/c33
        
    @classmethod
    def _find_distortion_coefficient(cls, c13, c33, str_typ='wz'):
        if str_typ == 'wz':
            return _general_fns._wz_elastic_distortion_coefficient(c13, c33)
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
        
class _xrd_read:
    def __init__(self, data_fname='./test.xml', log_info=None):
        # Parse the XML file
        self.xml_root = ET.parse(data_fname).getroot()
        # get XML namespaces
        self.namespaces = {'ns': self.xml_root.tag.split('}')[0].split('{')[1]}
        if log_info is not None:
            log_info = log_info.lower()
        self.log_info = log_info
        
    def _get_wavelength(self):
        usedWavelength_tag = self.xml_root.find('.//ns:xrdMeasurement/ns:usedWavelength', self.namespaces)
        return wave_lenth_dict.get(usedWavelength_tag.attrib['intended'])

    def _get_2Theta(self):
        twoThetas_tags = self.xml_root.findall(".//ns:xrdMeasurement/ns:scan/ns:dataPoints/ns:positions/[@axis='2Theta']", self.namespaces) 
        startPositions = np.array([twoTheta_tag.find('.//ns:startPosition', self.namespaces).text 
                                   for twoTheta_tag in twoThetas_tags], dtype=float)
        endPositions = np.array([twoTheta_tag.find('.//ns:endPosition', self.namespaces).text 
                                 for twoTheta_tag in twoThetas_tags], dtype=float)
        return np.column_stack((startPositions, endPositions))

    def _get_omega(self):
        omega_tags = self.xml_root.findall(".//ns:xrdMeasurement/ns:scan/ns:dataPoints/ns:positions/[@axis='Omega']/ns:commonPosition", self.namespaces) 
        return np.array([omega_tag.text for omega_tag in omega_tags], dtype=float)

    def _assert_same_units(self, for_xml_tags, error_text=''):
        _unit_found = list(set([for_xml_tag.attrib['unit'] for for_xml_tag in for_xml_tags]))
        assert len(_unit_found) == 1, f'{error_text}: {_unit_found}'
        return _unit_found[0]

    def _get_scan_time(self):
        count_time_tags = self.xml_root.findall('.//ns:xrdMeasurement/ns:scan/ns:dataPoints/ns:commonCountingTime', self.namespaces)
        _unit_found = self._assert_same_units(count_time_tags, error_text='Multiple units found for commonCountingTime')
        return np.array([count_time.text.split() for count_time in count_time_tags], dtype=float), _unit_found

    def _get_counts(self):
        count_tags = self.xml_root.findall('.//ns:xrdMeasurement/ns:scan/ns:dataPoints/ns:counts', self.namespaces)
        scan_time_values, time_unit_found = self._get_scan_time()
        count_unit_found = self._assert_same_units(count_tags, error_text='Multiple units found for counts')
        if self.log_info is not None:
            print(f'Intensity unit (from xrd file): {count_unit_found}/{time_unit_found}')
        read_intensity_values = np.array([count_line.text.split() for count_line in count_tags], dtype=float)
        return read_intensity_values/scan_time_values

    def _read_xrd_data(self):
        self.lambda_wavelength = self._get_wavelength()
        if self.log_info is not None:
            print(f'Wavelength used (from xrd file): {self.lambda_wavelength:.7f}') 
        self.two_theta_values = self._get_2Theta()
        self.omega_values = self._get_omega()
        self.rsm_values = self._get_counts() # reciprocal space map intensity or counts
        return self.lambda_wavelength, self.two_theta_values, self.omega_values, self.rsm_values

class _xrd_reciprocal(_general_fns):
    def __init__(self, log_info=None):
        if log_info is not None:
            log_info = log_info.lower()
        self.log_info = log_info

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
    def _Qxy_xrd(cls, omega, two_theta, col_n, shift=[0,0], R_val=1, mul_fact=[10000,10000]):
        '''
        Definitions:
            Q_x = R(cos(omega) - cos(2*theta-omega))
            Q_y = R(sin(omega) + sin(2*theta-omega))
            degree2radian = pi/180
            Return: Q_x, Q_y

        Parameters
        ----------
        omega : TYPE
            DESCRIPTION.
        two_theta : TYPE
            DESCRIPTION.
        col_n : TYPE
            DESCRIPTION.
        shift : TYPE, optional
            DESCRIPTION. The default is [0,0].
        R_val : TYPE, optional
            DESCRIPTION. The default is 1.
        mul_fact : TYPE, optional
            DESCRIPTION. The default is [10000,10000].

        Returns
        -------
        Q_x : TYPE
            DESCRIPTION.
        Q_y : TYPE
            DESCRIPTION.

        '''
        two_theta_ = np.array([np.linspace(start_, end_, num=col_n) for start_, end_ in two_theta])
        omega_list = np.array([[omega_val]*col_n for omega_val in omega])
        
        omega_rad = omega_list*degree2radian
        two_theta_m_omega_rad = (two_theta_ - omega_list)*degree2radian
        
        sin_omega = np.sin(omega_rad)
        sin_2theta_omega = np.sin(two_theta_m_omega_rad)
        
        cos_omega = np.cos(omega_rad)
        cos_2theta_omega = np.cos(two_theta_m_omega_rad)
        return R_val * (cos_omega - cos_2theta_omega) * mul_fact[0] + shift[0], R_val * (sin_omega + sin_2theta_omega) * mul_fact[1] + shift[1]

    @classmethod
    def _calc_alloy_params(cls, t, binary_parameters, mul_fact, alloy_type, str_type, hkl):
        alloy_a, alloy_c, _, _, alloy_D = \
            _general_fns._alloy_parameters_from_binary(t, binary_parameters, alloy_type=alloy_type, structure_type=str_type)    
        Qx_theor, Qy_theor = cls._Qxy_theor(alloy_a, alloy_c, mul_fact=mul_fact, hkl=hkl, structure_type=str_type)
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
