# `xrdpy`: Python package 2D x-ray diffraction data analysis


<!-- =========================================================== -->

<!-- =========================================================== -->
![](imgs/test.png)  |  ![](imgs/test.png) |  ![](imgs/test.png)
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
Unfolded band structure - flatband mode (Si0.5Ge0.5) |  Unfolded band structure - density mode (Si0.5Ge0.5) | Band structures overlay (Si0.5Ge0.5: Red, pure Si: black, pure Ge: blue)
<!-- =========================================================== -->

<!-- =========================================================== -->
## Developers and contributors
<!-- =========================================================== -->

__Developer of xrdpy :__

* [Badal Mondal](https://github.com/bmondal94)

* [Pietro Pampili](https://github.com/pampili)

__xrdpy Contributors:__  [Contributors](https://github.com/XRDmapAnalysis/graphs/contributors)

* We sincerely thank each and every contributor for their valuable input and support.

__Contact us:__ [Email developer/maintainer team](mailto:badalmondal.chembgc@gmail.com,pietro.pampili@tyndall.ie)

* If you would like to contribute to the development of `xrdpy` or request new functionality, please get in touch with [us](mailto:badalmondal.chembgc@gmail.com,pietro.pampili@tyndall.ie) or open a pull request. We appreciate and respect our users' views and are committed to providing the best experience possible. Your feedback is highly valued. We will be happy to support your request ASAP.

<!-- =========================================================== -->

<!-- =========================================================== -->
## Installation

### 1. Requirements
```
    1. python>=3.7
    3. numpy
    5. scipy>=1.0
    7. matplotlib
```

### 2. Installation using `pip`

```
    pip install xrdpy
```

### 3. Installation from github repository

```
    git clone https://github.com/band-unfolding/banduppy.git
    cd xrdpy
    pip install .  
```
Or, without cloning
```
    pip install git+https://github.com/band-unfolding/banduppy.git #@specific_branch
```

### 4. Installation using `setup.py` [deprecated]
Alternatively you can clone the repository and run `setup.py` in the usual manner:

```
    git clone https://github.com/band-unfolding/banduppy.git
    cd banduppy
    python setup.py install
```
<!-- =========================================================== -->

<!-- =========================================================== -->
## Usage
__Documentation__: [here](docs/USAGE.md)

The detailed documentation is available [here](docs/USAGE.md). Explore the [tutorial](tutorials) folder for example tutorials. Below are quick snippets showcasing what you can achieve with `xrdpy`:
```
xrdpy package:
    1. Unfolding class 
        1.1 propose_maximum_minimum_folding()
        1.2 generate_SC_Kpts_from_pc_kpts()
        1.3 generate_SC_Kpts_from_pc_k_path()
        1.3 Unfold()
        1.4 plot_ebs() [Note: Similar in Plotting class but can not plot band centers]
```

<!-- =========================================================== -->
## Tips and tricks:

__FAQs__: [here](docs/FAQs.md)

You can find a list of common user issues encountered while using this software [here](docs/FAQs.md). We appreciate and respect our users' views and are committed to providing the best experience possible. Your feedback is highly valued.

<!-- =========================================================== -->

<!-- =========================================================== -->
## Citations and references:

If you use `BandUPpy` in your work, please:

  * **State EXPLICITLY that you have used the BandUP code** (or a modified version of it, if this is the case), for instance, adding a sentence like: 

         "The unfolding has been performed using the BandUP(py) code"

  * **Read and cite the following papers** (and the appropriate references therein):
    
>> 1. Paulo V. C. Medeiros, Sven Stafström, and Jonas Björk,
   [Phys. Rev. B **89**, 041407(R) (2014)](http://doi.org/10.1103/PhysRevB.89.041407)  
>> 2. Paulo V. C. Medeiros, Stepan S. Tsirkin, Sven Stafström, and Jonas Björk,
   [Phys. Rev. B **91**, 041116(R) (2015)](http://doi.org/10.1103/PhysRevB.91.041116)  
>> 3. Mikel Iraola, Juan L. Mañes, Barry Bradlyn, Titus Neupert, Maia G. Vergniory, Stepan S. Tsirkin,
   "IrRep: Symmetry eigenvalues and irreducible representations of ab initio band structures", [Comput. Phys. Commun. **272**, 108226 (2022)](https://doi.org/10.1016/j.cpc.2021.108226)

__Bibliography file:__ Here is the [bibliography file](docs/REFERENCES.md) for your convenience.

<!-- =========================================================== -->

<!-- =========================================================== -->
## Version release
__Latest release: v0.3.4__

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

