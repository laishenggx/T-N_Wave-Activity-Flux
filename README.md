# T-N Wave-Activity Flux
Python scripts for caculating the `Wave-Activity Flux` derived by `Takaya and Nakamura (JAS,2001)`.
## Introduction 
Takaya and Nakamura generalize the Plumb Wave-Activity Flux(Plumb,1985) so as to be applicable to small-amplitude Quasi-Geostrophic(QG) disturbances, either stationary or migratory, that are superimposed on a zonally varying basic flow, and introduced the `T-N Wave-Activity Flux`('TN01' for short).
## Formulation
These Python scripts use the TN01 diagnostic formula in Spherical coordinates, which is the Eq.38 of Takaya's paper published in 2001.<br>
The first two terms in Eq.38 are taken into account while computing on the horizontal direction.<br>
And assuming the wave is stationary ,so the Cu in Eq.38 would be zero.
## Reliability
The output figures sample
<p align="left">
    <img src="https://github.com/laishenggx/T-N_Wave-Activity-Flux/raw/master/jan1981.png" alt="Sample"  width="400">
</p>
Results are compatible with the Wave-Activity Flux figures made by JMA-TCC,<br>
(http://ds.data.jma.go.jp/tcc/tcc/products/clisys/figures/db_hist_pen_tcc.html)<br>
<p align="left">
    <img src="https://github.com/laishenggx/T-N_Wave-Activity-Flux/raw/master/psnh_mon_hist_waf300_198101.png" alt="Sample"  width="400">
</p>
and also the programs by Kazuaki Nishii @ University of Tokyo.<br>
(http://www.atmos.rcast.u-tokyo.ac.jp/nishii/programs/index.html)
