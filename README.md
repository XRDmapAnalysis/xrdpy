# `xrdpy`: Python package for 2D X-ray diffraction data analysis


<!-- =========================================================== -->

<!-- =========================================================== -->
![](https://raw.githubusercontent.com/XRDmapAnalysis/xrdpy/refs/heads/main/imgs/real_space.png) | ![](https://raw.githubusercontent.com/XRDmapAnalysis/xrdpy/refs/heads/main/imgs/reciprocal_space.png) | ![](https://raw.githubusercontent.com/XRDmapAnalysis/xrdpy/refs/heads/main/imgs/detect_peaks.png)
:-------------------------:|:-------------------------:|:-------------------------:
Real space map | Reciprocal space map | Detecting RSM peaks (example-1)

![](https://raw.githubusercontent.com/XRDmapAnalysis/xrdpy/refs/heads/main/imgs/sensitive_peaks.png) | ![](https://raw.githubusercontent.com/XRDmapAnalysis/xrdpy/refs/heads/main/imgs/reciprocal_space_overlay.png) | ![](https://raw.githubusercontent.com/XRDmapAnalysis/xrdpy/refs/heads/main/imgs/rsm_rotation.png)
:-------------------------:|:-------------------------:|:-------------------------:
Detecting sensitive RSM peaks (peak detection at low intesity) | Merged RSM maps (including strain calculations) | Aligning RSM maps using $\omega$ rotation (2nd sample is relaxed)
<!-- =========================================================== -->

<!-- =========================================================== -->
## Developers and contributors
<!-- =========================================================== -->

__Developer of xrdpy :__ [Badal Mondal](https://github.com/bmondal94), [Pietro Pampili](https://github.com/pampili)

__xrdpy Contributors:__  [Contributors](https://github.com/XRDmapAnalysis/xrdpy/graphs/contributors)

* We sincerely thank each and every contributor for their valuable input and support.

__Contact us:__ [Email developer/maintainer team](mailto:badalmondal.chembgc@gmail.com,pietro.pampili@tyndall.ie)

* If you would like to contribute to the development of `xrdpy` or request new functionality, please get in touch with [us](mailto:badalmondal.chembgc@gmail.com,pietro.pampili@tyndall.ie) or open a pull request or discuss [here](https://github.com/XRDmapAnalysis/xrdpy/discussions). We appreciate and respect our users' views and are committed to providing the best experience possible. Your feedback is highly valued. We will be happy to support your request ASAP.


<!-- =========================================================== -->

<!-- =========================================================== -->
## Installation

### 1. Requirements
```
    1. python>=3.12
    3. numpy>=1.13
    5. scipy>=1.26
    7. matplotlib
```

### 3. Installation using `pip` [*recommended]

```
    pip install xrdpy
```

### 2. Installation from github repository

```
    git clone https://github.com/XRDmapAnalysis/xrdpy.git
    cd xrdpy
    pip install .  
```
Or,
```
    pip install git+https://github.com/XRDmapAnalysis/xrdpy.git@specific_branch
```



<!-- =========================================================== -->

<!-- =========================================================== -->
## Usage

__Wiki page__: [Welcome to xrdpy](https://github.com/XRDmapAnalysis/xrdpy/wiki)

__Documentation__: [Package documentation](https://github.com/XRDmapAnalysis/xrdpy/wiki/01.-Package-documentation)

__Discussions__: [Discuss more about the package here](https://github.com/XRDmapAnalysis/xrdpy/discussions)

__Tutorials__: [tutorial](https://github.com/XRDmapAnalysis/xrdpy/tree/main/tutorials)

__Theoretical details__: [TBA](https://github.com/XRDmapAnalysis/xrdpy/blob/main/docs/models.pdf)
<!-- =========================================================== -->
## Tips and tricks:

__FAQs__: [here](https://github.com/XRDmapAnalysis/xrdpy/wiki/02.-Frequently-asked-questions-(FAQs))

You can find a list of common user issues encountered while using this software [here](https://github.com/XRDmapAnalysis/xrdpy/wiki/02.-Frequently-asked-questions-(FAQs)). We appreciate and respect our users' views and are committed to providing the best experience possible. Your feedback is highly valued.

<!-- =========================================================== -->

<!-- =========================================================== -->
## Citations and references:

If you use `xrdpy` in your work, please:

  * **State EXPLICITLY that you have used the xrdpy code** (or a modified version of it, if this is the case), for instance, adding a sentence like:

         "The XRD analysis is performed using the xrdpy code."

  * **How to cite the package:** (use appropriate version number and doi corresponding to your installed xrdpy)
>> Badal Mondal and Pietro Pampili, "XRDmapAnalysis/xrdpy: version-0.0.5 (v0.5.5))". Zenodo, 2026. doi:[10.5281/zenodo.18498887](https://doi.org/10.5281/zenodo.18498887)

  * **Read and cite the following papers** (and the appropriate references therein):
    
>> P. Pampili, V. Z. Zubialevich, B. Mondal, J. Mukherjee, S. Schulz, D. A. J. Moran, and P. J. Parbrook, [Appl. Phys. Lett. 128,262108 (2026).](https://doi.org/10.1063/5.0325471)

__Bibliography file:__ Here is the [bibliography file](https://github.com/XRDmapAnalysis/xrdpy/wiki/03.-References-(bibliography-style)) for your convenience.

<!-- =========================================================== -->

<!-- =========================================================== -->
## Version release

Chekout out [version release history here](https://github.com/XRDmapAnalysis/xrdpy/wiki/04.-Release-history) for the full list of updates and upgrades.

<!-- =========================================================== -->

<!-- =========================================================== -->
## License

* [GNU General Public License v3.0](https://raw.githubusercontent.com/XRDmapAnalysis/xrdpy/refs/heads/main/LICENSE)
<!-- =========================================================== -->

<!-- =========================================================== -->
## Upcoming (TBD)
1. ZB structure
2. Implement arbritraty 1D line scan capability on 2D RSM plots
2. Quaternary alloy
<!-- =========================================================== -->

