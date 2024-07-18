# `xrdpy`: Python package for 2D X-ray diffraction data analysis


<!-- =========================================================== -->

<!-- =========================================================== -->
![](imgs/AlN_AlGaN_AlN_real_space.png) | ![](imgs/AlN_AlGaN_AlN_reciprocal_space.png) | ![](imgs/AlN_AlGaN_AlN_2reciprocal_space.png)
:-------------------------:|:-------------------------:|:-------------------------:
AlGaN/AlN HEMT real space XRD | AlGaN/AlN HEMT reciprocal space XRD | AlGaN/AlN HEMT reciprocal space XRD
<!-- =========================================================== -->

<!-- =========================================================== -->
## Developers and contributors
<!-- =========================================================== -->

__Developer of xrdpy :__

* [Badal Mondal](https://github.com/bmondal94)

* [Pietro Pampili](https://github.com/pampili)

__xrdpy Contributors:__  [Contributors](https://github.com/XRDmapAnalysis/xrdpy/graphs/contributors)

* We sincerely thank each and every contributor for their valuable input and support.

__Contact us:__ [Email developer/maintainer team](mailto:badalmondal.chembgc@gmail.com,pietro.pampili@tyndall.ie)

* If you would like to contribute to the development of `xrdpy` or request new functionality, please get in touch with [us](mailto:badalmondal.chembgc@gmail.com,pietro.pampili@tyndall.ie) or open a pull request. We appreciate and respect our users' views and are committed to providing the best experience possible. Your feedback is highly valued. We will be happy to support your request ASAP.

<!-- =========================================================== -->

<!-- =========================================================== -->
## Installation

### 1. Requirements
```
    1. python>=3.10
    3. numpy
    5. scipy>=1.0
    7. matplotlib
```

### 2. Installation from github repository

```
    git clone https://github.com/XRDmapAnalysis/xrdpy.git
    cd xrdpy
    pip install .  
```
Or, without cloning
```
    pip install git+https://github.com/XRDmapAnalysis/xrdpy.git #@specific_branch
```

### 3. Installation using `pip` [* not available yet]

```
    pip install xrdpy
```

<!-- =========================================================== -->

<!-- =========================================================== -->
## Usage
__Documentation__: [here](docs/USAGE.md)

The detailed documentation is available [here](docs/USAGE.md). Explore the [tutorial](tests) folder for example tutorials. Below are quick snippets showcasing what you can achieve with `xrdpy`:
```
xrdpy package:
    1. general_fns class
        1.1 alloy_parameters_from_binary()
    1. xrd class
        1.1 xrd_read_data()
        1.2 find_composition_strain_4_point()
        1.3 get_full_strain_line()
        1.4 Qxy()
        1.5 Qxy_theor()
        1.6 xrd_plot()
    3. plottings class
        3.1 xrd_plot()
        3.2 save_figure()
```

<!-- =========================================================== -->
## Tips and tricks:

__FAQs__: [here](docs/FAQs.md)

You can find a list of common user issues encountered while using this software [here](docs/FAQs.md). We appreciate and respect our users' views and are committed to providing the best experience possible. Your feedback is highly valued.

<!-- =========================================================== -->

<!-- =========================================================== -->
## Citations and references:

If you use `xrdpy` in your work, please:

  * **State EXPLICITLY that you have used the xrdpy code** (or a modified version of it, if this is the case), for instance, adding a sentence like:

         "The XRD analysis has been performed using the xrdpy code"

  * **Read and cite the following papers** (and the appropriate references therein):
    
>> 1.

__Bibliography file:__ Here is the [bibliography file](docs/REFERENCES.md) for your convenience.

<!-- =========================================================== -->

<!-- =========================================================== -->
## Version release
__Latest release: v0.0.1__

Chekout out [version release history here](docs/RELEASE.md) for the full list of updates and upgrades.

<!-- =========================================================== -->

<!-- =========================================================== -->
## License

`xrdpy` is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

`xrdpy` is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BandUP.  If not, see <http://www.gnu.org/licenses/>.
<!-- =========================================================== -->

<!-- =========================================================== -->
## Upcoming (TBD)
1. Implement peak finding algorithm
<!-- =========================================================== -->

