import matplotlib.pyplot as plt

### ===========================================================================

class _GeneratePlots:
    def __init__(self, save_figure_dir='.'):
        """
        Initialize the plotting class.

        Parameters
        ----------
        save_figure_dir : str/path, optional
            Directory where to save the figure. The default is current directory.

        Returns
        -------
        None.

        """
        self.save_figure_folder = save_figure_dir
        params = {'figure.figsize': (8, 6),
                  'legend.fontsize': 18,
                  'axes.labelsize': 18,
                  'axes.titlesize': 18,
                  'xtick.labelsize':18,
                  'xtick.major.width':2,
                  'xtick.major.size':5,
                  'xtick.minor.width':1,
                  'xtick.minor.size':3,
                  'ytick.labelsize': 18,
                  'ytick.major.width':2,
                  'ytick.major.size':5,
                  'ytick.minor.width':1,
                  'ytick.minor.size':3,
                  'errorbar.capsize':2}
        plt.rcParams.update(params)
        plt.rc('font', size=10)

    def _save_figure(self,fig_name, fig=None, savefig:bool=True, show_plot:bool=True, 
                     CountFig=None, **kwargs_savefig):
        if not savefig: 
            if show_plot: plt.show()
            return CountFig
        if fig is not None:
            fig.savefig(f'{self.save_figure_folder}/{fig_name}', 
                        bbox_inches='tight', **kwargs_savefig)
        else:
            plt.savefig(f'{self.save_figure_folder}/{fig_name}', 
                        bbox_inches='tight', **kwargs_savefig)
        plt.close()
        if CountFig is not None: CountFig += 1
        return CountFig