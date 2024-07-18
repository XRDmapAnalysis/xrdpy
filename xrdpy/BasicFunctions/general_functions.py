import numpy as np

## ============================================================================
class _SaveData2File:
    def __init__(self):
        pass
    
    @staticmethod
    def _default_save_settings(save_data):
        tmp_save = {'save2file': False, 'fdir': '.', 'fname': 'test', 'fname_suffix': ''}
        for ll in tmp_save:
            if ll in save_data:
                tmp_save[ll] = save_data[ll]
        return tmp_save
    
    @staticmethod
    def _save_2_file(data=None, save_dir='.', file_name:str='', file_name_suffix:str='', 
                     header_txt:str='', footer_txt:str='',comments_symbol='! ',
                     np_data_fmt='%12.8f', print_log:bool=True):
        """
        Save the generated SC kpoints to a file.

        Parameters
        ----------
        data : numpy array, optional
            Data to be saved. The default is None.
        save_dir : str/path_object, optional
            Directory to save the file. The default is current directory.
        file_name : str, optional
            Name of the file. The default is ''.
            If file_format is vasp, file_name=KPOINTS_<file_name_suffix>
        file_name_suffix : str, optional
            Suffix to add after the file_name. The default is ''.
        header_txt : str, optional
            String that will be written at the beginning of the file. The default is None.
        footer_txt : str, optional
            String that will be written at the end of the file.. The default is None.
        comments_symbol : str, optional
            String that will be prepended to the header and footer strings, 
            to mark them as comments. The default is ‘!‘. 
        np_data_fmt: str
            Data format for numpy.savetxt.
        print_log : bool, optional
            Print path of save file. The default is False.

        Returns
        -------
        String/path object
            File path where the data is saved.

        """
        if data is None: return
        fname_save_file = f'{save_dir}/{file_name}{file_name_suffix}'
        if isinstance(data, np.ndarray):
            with open(fname_save_file, 'w') as f:
                np.savetxt(f, data, header=header_txt, footer=footer_txt, 
                           fmt=np_data_fmt, comments=comments_symbol)
        return fname_save_file
