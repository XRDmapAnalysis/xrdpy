import xml.etree.ElementTree as ET
import numpy as np
from ..BasicFunctions.constants_ import wave_lenth_dict, degree2radian

### ===========================================================================
class _xrd_read_file:
    def __init__(self, xrd_scan_mode:str='omega_2theta_scan', 
                 read_file_mode:str="reciprocal_space_map", data_fname='./test', 
                 data_file_fmt:str = 'xrdml', log_info=None):
        """
        Initialize function for this class.

        Parameters
        ----------           
        data_fname : str or file object
            The file name. The default is './test'.
        data_file_fmt : str, optional [options: 'xrdml']
            Format for the xrd file to be read. Different file formats will be
            parsed differently. Contact developer to add support for other file
            formats. The default is 'xrdml'.
        log_info : TYPE, optional
            Level of logging. The default is None.

        Raises
        ------
        RuntimeError
            If data_file_fmt is not supported.

        Returns
        -------
        None.

        """
        if data_file_fmt not in ['xrdml']:
            raise RuntimeError(f'.{data_file_fmt} xrd file format is not supported yet. Contact developer.')
        if xrd_scan_mode not in ['omega_2theta_scan']:
            raise RuntimeError(f'.{xrd_scan_mode} xrd file scan mode is not supported yet. Contact developer.')
        self._xrd_scan_mode = xrd_scan_mode
        self._read_file_mode = read_file_mode
        # Parse the XML file
        self.xml_root = ET.parse(f'{data_fname}.{data_file_fmt}').getroot()
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

    def _read_xrd_data_from_file(self, shift=[0,0], mul_fact=[1,1]):
        self.lambda_wavelength = self._get_wavelength()
        if self.log_info is not None:
            print(f'Wavelength used (from xrd file): {self.lambda_wavelength:.7f}') 
        self.intensity_values = self._get_counts() # map intensity or counts
        col_n = np.shape(self.intensity_values)[1]
        if self._xrd_scan_mode == 'omega_2theta_scan':
            XX = np.array([np.linspace(start_, end_, num=col_n) 
                           for start_, end_ in self._get_2Theta()])
            YY = np.array([[omega_val]*col_n for omega_val in self._get_omega()])
        
        self.two_theta_values = XX * mul_fact[0] + shift[0]
        self.omega_values = YY* mul_fact[1] + shift[1]
        return 
        
    def _xrd_reciprocal_space_map(self, shift=[0,0], mul_fact=[10000,10000]):
        '''
        Definitions:
            Q_x = R(cos(omega) - cos(2*theta-omega))
            Q_z = R(sin(omega) + sin(2*theta-omega))
            degree2radian = pi/180

        '''    
        R_val = 1/self.lambda_wavelength
        
        omega_rad = self.omega_values*degree2radian
        two_theta_m_omega_rad = (self.two_theta_values - self.omega_values)*degree2radian
        
        sin_omega = np.sin(omega_rad)
        sin_2theta_omega = np.sin(two_theta_m_omega_rad)
        
        cos_omega = np.cos(omega_rad)
        cos_2theta_omega = np.cos(two_theta_m_omega_rad)
        
        self.rsm_x = R_val * (cos_omega - cos_2theta_omega) * mul_fact[0] + shift[0] 
        self.rsm_y = R_val * (sin_omega + sin_2theta_omega) * mul_fact[1] + shift[1]
        return 
      
    def _xrd_read_parse_file_(self, shift=[0,0], mul_fact_xy_axis=[1,1]):
        """
        This function reads the XRD file and/or generate reciprocal space data.

        Parameters
        ----------
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
        if self._read_file_mode == 'reciprocal_space_map':
            shift_tmp, mul_fact_tmp = shift, mul_fact_xy_axis
            shift, mul_fact_xy_axis = [0,0], [1,1]

        self._read_xrd_data_from_file(shift=shift, mul_fact=mul_fact_xy_axis)
        
        if self._read_file_mode == 'reciprocal_space_map':
            shift, mul_fact_xy_axis = shift_tmp, mul_fact_tmp
            self._xrd_reciprocal_space_map(shift=shift, mul_fact=mul_fact_xy_axis)
            return self.rsm_x, self.rsm_y, self.intensity_values
        else:
            return self.two_theta_values, self.omega_values, self.intensity_values 