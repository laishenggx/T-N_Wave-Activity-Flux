# T-N Wave-Activity Flux
Python scripts for caculating the `T-N Wave-Activity Flux` derived by `Takaya and Nakamura (JAS,2001)`.
* Coder: Lai Sheng @ College of Atmospheric Science, Chengdu University of Information Technology.
* You can also visit my site for more detail: http://500hpa.cn/pyinmet/tnflux/
## Introduction 
Takaya and Nakamura generalize the Plumb Wave-Activity Flux(Plumb,1985) so as to be applicable to small-amplitude Quasi-Geostrophic(QG) disturbances, either stationary or migratory, that are superimposed on a zonally varying basic flow, and introduced the `T-N Wave-Activity Flux`('TN01' for short).<br>

TN01 is of great advantage in climate monitoring and diagnosis.
>TN01 with improved meridional component based on Plumb Wave-Activity Flux is appropriate for analyzing Rossby waves in the zonally asymmetric westerly. And it reflect the evolution of long-waves which the E-P Flux can't.<br>(Shi Chunhua,2017)

## Formulation
These Python scripts use the TN01 diagnostic formula in Spherical coordinates, <br>
which is the Eq.38 of Takaya's paper published in 2001:<br>
<p align="left">
    <img src="https://github.com/laishenggx/T-N_Wave-Activity-Flux/raw/master/eq38.png" alt="Sample"  width="700">
</p>
The first two terms in Eq.38 are taken into account while computing on the horizontal direction.<br>
And assuming the wave is stationary ,so the Cu in Eq.38 would be zero.<br>
So the formula of horizontal T-N Wave-Activity Flux could yield as followed:

<p align="left">
    <img src="https://github.com/laishenggx/T-N_Wave-Activity-Flux/raw/master/eq38_hor.png" alt="Sample"  width="700">
</p>

## Programing
We modified the GRADS script by Kazuaki Nishii into a Python3 version<br>
(http://www.atmos.rcast.u-tokyo.ac.jp/nishii/programs/index.html)<br>

* Python version
    * Python 3.6
* Data import
    * netCDF4
* Computation
    * numpy (1.16.1)
* Visualization
    * matplotlib (2.2.0)
    * basemap (1.1.0)

All computations are based on `numpy` arrays, which are very efficient.<br>
Partial differential terms in the formula are calculated by `numpy.gradient` in the central difference method. <br>
The library of Data import and Visualization could change in terms of requirements(PyNIO,PyNGL...).

### Horizontal
#### Data & Process
Horizontal TN01 caltulation require the datas below:
* Climatology average background of wind`U_c & V_c` and geopotential`pi_c`.
* Geopotential in the analysis period`pi`.

Geopotential anomalies will be used to compute pertubation stream-function`psi_p` in Quasi-Geostrophic(QG) assumption: 
* `psi_p`=(`pi`-`pi_c`)/`f`<br>
`f` is the Coriolis parameter: `f`=2\*omega\*sin(`lat`)

**Input Data is Geopotential, NOT Geopotential Height!!!**
The Re-analysis from NCEP/NCAR(NCEP1) is Geopotential Height, Geopotential Height multiplied by gravity `g` makes Geopotential.

#### Output
`px` for longitude direction<br>
`py` for latitude direction

### 3D (Horizontal + Vertical)
The script for TN01 3-Dimension is under development.

## Reliability
The output figures sample(Datas from `ECMWF ERA-Interim`)
<p align="left">
    <img src="https://github.com/laishenggx/T-N_Wave-Activity-Flux/raw/master/jan1981.png" alt="Sample"  width="400">
</p>
Results are compatible with the Wave-Activity Flux figures(JRA-55) made by JMA-TCC,<br>
(http://ds.data.jma.go.jp/tcc/tcc/products/clisys/figures/db_hist_pen_tcc.html)<br>
<p align="left">
    <img src="https://github.com/laishenggx/T-N_Wave-Activity-Flux/raw/master/psnh_mon_hist_waf300_198101.png" alt="Sample"  width="400">
</p>
and also the programs by Kazuaki Nishii @ University of Tokyo.<br>
(http://www.atmos.rcast.u-tokyo.ac.jp/nishii/programs/index.html)
