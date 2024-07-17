import xml.etree.ElementTree as ET
import numpy as np
from .constants import wave_lenth_dict

### ===========================================================================
class xrd_read:
    def __init__(self, data_fname='./test.xml', log_info=None):
        # Parse the XML file
        self.xml_root = ET.parse(data_fname).getroot()
        # get XML namespaces
        self.namespaces = {'ns': root.tag.split('}')[0].split('{')[1]}
        if log_info is not None:
            log_info = log_info.lower()
        
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

    def _get_counts(self):
        count_tags = self.xml_root.findall('.//ns:xrdMeasurement/ns:scan/ns:dataPoints/ns:counts', self.namespaces)
        return np.array([count_line.text.split() for count_line in count_tags], dtype=float)

    def _read_xrd_data(self):
        lambda_wavelength = self._get_wavelength()
        if self.log_info is not None:
            print(f'Wavelenth used: {lambda_wavelength:.7f}') 
        two_theta_values = self._get_2Theta()
        omega_values = self._get_omega()
        rsm_values = self._get_counts() # reciprocal space map intensity or counts
        return lambda_wavelength, two_theta_values, omega_values, rsm_values