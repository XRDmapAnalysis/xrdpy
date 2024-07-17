from .src import _xrd_read

### ===========================================================================
class xrd(xrd_read):
    def __init__(self, xrd_file_name='./test.xml', print_log=None):
        if print_log is not None:
            print_log = print_log.lower()
        
    def read_xrd_data(self):
        xrd_read.__init__(self, data_fname=xrd_file_name, log_info=print_log)
        return self._read_xrd_data()