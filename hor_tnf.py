"""
#################################################################################################
Caculating the Horizontal Wave-Activity Flux (HOR-TN01-WAF)
derived by Takaya and Nakamura (JAS,2001)

•Coder: Lai Sheng @ College of Atmospheric Science ,Chengdu University of Information Technology.
•E-mail: laish12@lzu.edu.cn

This Python script use the TN01 diagnostic formula in Spherical coordinates,
which is the Eq.38 of Takaya's paper published in 2001.

The first two terms in Eq.38 are taken into account while computing on the horizontal direction.
And assuming the wave is stationary ,so the C_u in Eq.38 would be zero.

Results are compatible with the Wave-Activity Flux figures made by JMA-TCC,
(http://ds.data.jma.go.jp/tcc/tcc/products/clisys/figures/db_hist_pen_tcc.html)
and also the programs by Kazuaki Nishii @ University of Tokyo.
(http://www.atmos.rcast.u-tokyo.ac.jp/nishii/programs/index.html)

-- Program Process --
1.Read in data:
    - Climatology average background of wind(U_c & V_c) and geopotential(phi_c).
    - Geopotential in the analysis period.
2.Compute the pertubation stream-function(psi_p) and the HOR-TN01-WAF.
3.Plot & Output the results.

You can also check out the guidebook along with this script for more information.
Bug reports are appreciated.
#################################################################################################
"""
import numpy as np
import netCDF4 as nc
from mpl_toolkits.basemap import Basemap,addcyclic
import matplotlib.pyplot as plt
from copy import copy

a=6.37e6 #Earth Radius
omega=7.292e-5 #Rotational angular velocity of the Earth

#Read in data
climate_data = nc.Dataset('1979_2017_1.nc')
print(climate_data)
lon=climate_data.variables['longitude'][:]
lat=climate_data.variables['latitude'][:]

dlon=np.gradient(lon)*np.pi/180.0
dlat=np.gradient(lat)*np.pi/180.0
f=np.array(list(map(lambda x : 2*omega*np.sin(x*np.pi/180.0),lat))) #Coriolis parameter: f=2*omgega*sin(lat)
cos_lat=np.array(list(map(lambda x : np.cos(x*np.pi/180.0),lat))) #cos(lat)

u_c=np.average(climate_data.variables['u'][:,:,:],axis=0)
v_c=np.average(climate_data.variables['v'][:,:,:],axis=0)
phi_c=np.average(climate_data.variables['z'][:,:,:],axis=0)
psi_p=((climate_data.variables['z'][2,:,:]-phi_c).T/f).T #Pertubation stream-function

#5 partial differential terms
dpsi_dlon=np.gradient(psi_p,dlon[1])[1]
dpsi_dlat=np.gradient(psi_p,dlat[1])[0]
d2psi_dlon2=np.gradient(dpsi_dlon,dlon[1])[1]
d2psi_dlat2=np.gradient(dpsi_dlat,dlat[1])[0]
d2psi_dlondlat=np.gradient(dpsi_dlat,dlon[1])[1]

termxu=dpsi_dlon*dpsi_dlon-psi_p*d2psi_dlon2
termxv=dpsi_dlon*dpsi_dlat-psi_p*d2psi_dlondlat
termyv=dpsi_dlat*dpsi_dlat-psi_p*d2psi_dlat2

#coefficient
p_lev=300.0 #unit in hPa
p=p_lev/1000.0
magU=np.sqrt(u_c**2+v_c**2)
coeff=((p*cos_lat)/(2*magU.T)).T
#x-component of TN-WAF
px=(coeff.T/(a*a*cos_lat)).T * (((u_c.T)/cos_lat).T*termxu+v_c*termxv)
#y-component of TN-WAF
py=(coeff.T/(a*a)).T * (((u_c.T)/cos_lat).T*termxv+v_c*termyv)
#end of computation
############################################
fig,ax=plt.subplots()
m=Basemap(projection='nplaea',boundinglat=10.5,lon_0=90,resolution='l',round=True)
m.readshapefile('D:\\dt\\bou1_4l', 'china', color='crimson')
m.drawcoastlines(linewidth=0.3,color='gray')
m.drawparallels(np.arange(0.,81.,20.),linewidth=0.4,color='gray')
m.drawmeridians(np.arange(0.,360.,60.),linewidth=0.4,color='gray',labels=[True,True,True,True])

my_map = copy(plt.cm.RdBu_r)
my_map.set_under((18/255, 73/255, 132/255), 1.0)
my_map.set_over((131/255, 11/255, 37/255), 1.0)

psi_p1,lon1=addcyclic(psi_p,lon)
lonsn, latsn = np.meshgrid(lon1, lat[0:160])
x_cyc,y_cyc=m(lonsn,latsn)

#Plot Pertubation stream-function
lev=np.arange(-24,28,4)
cf=m.contourf(x_cyc,y_cyc,psi_p1[0:160,:]/1e6,levels=lev,cmap=my_map,extend='both')
c=m.contour(x_cyc,y_cyc,psi_p1[0:160,:]/1e6,colors='black',linewidths=0.5,levels=lev)

#plot T-N Flux vector on a Polar Lambert Azimuthal Projection map
lons, lats = np.meshgrid(lon, lat[0:160])
# the vector must be rotated to fit in the projection
px_r, py_r, x_r, y_r = m.rotate_vector(px[0:160,:], py[0:160,:], lons, lats, returnxy=True)
step=10
step90_60=20
Q=m.quiver(x_r[0:59:step,::step90_60],y_r[0:59:step,::step90_60],px_r[0:59:step,::step90_60],py_r[0:59:step,::step90_60],pivot='mid',width=0.0025,scale=500,headwidth=3)
qk = ax.quiverkey(Q, 0.76, 0.8, 25, r'25 m$^2$/s$^2$', labelpos='E',coordinates='figure')
m.quiver(x_r[60::step,::step],y_r[60::step,::step],px_r[60:160:step,::step],py_r[60:160:step,::step],pivot='mid',width=0.0025,scale=500,headwidth=3)

ax1 = fig.add_axes([0.25, 0.05, 0.55, 0.02])
cb=plt.colorbar(cf, cax=ax1, shrink=0.0, orientation='horizontal')
cb.ax.tick_params(labelsize='small')
ax1.set_xlabel('Stream function anomalies $\mathcal{\psi}$$^\prime$(10$^6$ m$^2$/s)')

ax.text(0.005, 1.045, 'ECMWF ERA-Interim [T$_L$255L60 Cy31r2@4D-Var]\nWave Activity Flux (${Takaya & Nakamura,2001}$)',color='blue',fontsize=7,transform=ax.transAxes)
ax.text(0.83, 1.063, 'January,1981',color='red',fontsize=10,transform=ax.transAxes)


plt.savefig('jan1981.png', dpi=300, bbox_inches='tight')
plt.show()