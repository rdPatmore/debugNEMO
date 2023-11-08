import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

def plot_norway_ssh_diff(m0, m1, m2, m3, bathy=None, var='sossheig'):
    """ plot difference between two models in the north of norway """

    fig, axs = plt.subplots(1,4, figsize=(6,4))
    plt.subplots_adjust(bottom=0.3, top=0.9, right=0.95)

    def render(ax, m, vmin=-5, vmax=5, title=None): 
        p = ax.pcolor(m.nav_lon, m.nav_lat, m.sossheig, vmin=vmin, vmax=vmax,
                  cmap=plt.cm.RdBu)
        ax.set_title(title, size=8)
        return p

    m0 = m0.isel(time_counter=41, x=slice(1086,1109), y=slice(1252,None))
    m1 = m1.isel(time_counter=41, x=slice(1086,1109), y=slice(1252,None))
    m2 = m2.isel(time_counter=41, x=slice(1086,1109), y=slice(1252,None))
    m3 = m3.isel(time_counter=41, x=slice(1086,1109), y=slice(1252,None))
    diff0 = m0-m1
    diff1 = m0-m2
    diff2 = m0-m3

    p0 = render(axs[0], m0, title='CO9\n')
    p1 = render(axs[1], diff0, vmin=-0.3, vmax=0.3, title='CO10\nunscaled e3t')
    render(axs[2], diff1, vmin=-0.2, vmax=0.2, title='CO10\nscaled e3t')
    render(axs[3], diff2, vmin=-0.2, vmax=0.2,
           title='CO10\nscaled e3t debugged')

    for ax in axs[1:4]:
        ax.set_yticklabels([])

    for ax in axs:
        ax.set_xlabel('Longitude')
    axs[0].set_ylabel('Latitude')

    pos = axs[0].get_position()
    cbar_ax = fig.add_axes([pos.x0, 0.14, pos.x1 - pos.x0, 0.02])
    cbar = fig.colorbar(p0, cax=cbar_ax, orientation='horizontal')
    cbar.ax.text(0.5, -3.5, 'Sea Surface Height (m)', fontsize=8,
                 transform=cbar.ax.transAxes, va='top', ha='center')

    pos0 = axs[1].get_position()
    pos1 = axs[3].get_position()
    cbar_ax = fig.add_axes([pos0.x0, 0.14, pos1.x1 - pos0.x0, 0.02])
    cbar = fig.colorbar(p1, cax=cbar_ax, orientation='horizontal')
    cbar.ax.text(0.5, -3.5, 'Sea Surface Height Anomaly from CO9 (m)',
                 fontsize=8,
                 transform=cbar.ax.transAxes, va='top', ha='center')

    if bathy:
        bathy = bathy.isel(x=slice(1086,1109), y=slice(1252,None))
        for ax in axs:
            ax.pcolor(bathy.nav_lon, bathy.nav_lat, bathy.where(bathy ==0),
                      cmap=plt.cm.copper)

    plt.savefig('Plots/e3t_compare.png', dpi=600)

def plot_norway_ssh_diff_main():
    bathy = xr.open_dataset('../Data/GEG_SF12.nc')
    bathy = bathy.set_coords(['nav_lon','nav_lat']).bathy.squeeze()
    fn_co10 = 'CO10_1ts_20040101_20040101_shelftmb_grid_T.nc'
    fn_co9  = 'CO9_1.5b_1ts_20040101_20040101_shelftmb_grid_T.nc'
    co9 = xr.open_dataset('../Data/CO9/' + fn_co9)
    co10_no_enda = xr.open_dataset('../Data/CO10_no_enda/' + fn_co10)
    co10_enda = xr.open_dataset('../Data/CO10_enda/' + fn_co10)
    co10_enda_spg_fix = xr.open_dataset('../Data/CO10_enda_spg_fix/' + fn_co10)
    plot_norway_ssh_diff(co9, co10_no_enda, co10_enda, co10_enda_spg_fix)

def e3t_trace():
    fn_co10 = 'CO10_1ts_20040101_20040101_shelftmb_grid_U.nc'
    co10 = xr.open_dataset('../Data/CO10_ldf_trace/' + fn_co10)

    fig, axs = plt.subplots(2,3, figsize=(6,4))
    plt.subplots_adjust(bottom=0.15, top=0.88, right=0.95, hspace=0.3,
                        wspace=0.1)

    co10 = co10.isel(time_counter=0, x=slice(777,813), y=slice(139,181),
                     depthu=0)
    print (co10)
    def render(ax, m, var, vmin=-5, vmax=5, title=None): 
        p = ax.pcolor(m.nav_lon, m.nav_lat, m[var], vmin=vmin, vmax=vmax,
                  cmap=plt.cm.RdBu)
        ax.set_title(title, size=8)
        return p

    p0 = render(axs[0,0], co10, 'zu_frc',  title='dynspg_ts\nzu_frc')
    p1 = render(axs[0,1], co10, 'sum_puu_ldf_a',  title='dynldf\nu_baro_b')
    p2 = render(axs[0,2], co10, 'sum_puu_ldf_b',  title='dynldf\nu_baro_a')
    p3 = render(axs[1,0], co10, 'zcur_tmp',  title='dynldf\nzcur')
    p4 = render(axs[1,1], co10, 'zdiv_tmp',  title='dynldf\nzdiv')
    p5 = render(axs[1,2], co10, 'e3u',  title='dynldf\ne3u', vmin=-0.3, vmax=0.3)

    for ax in axs[1]:
        ax.set_xlabel('Longitude')
    for ax in axs[:,0]:
        ax.set_ylabel('Latitude')

    for ax in axs[:, 1:3].flatten():
        ax.set_yticklabels([])

    for ax in axs[0].flatten():
        ax.set_xticklabels([])
    plt.savefig('Plots/e3t_trace.png', dpi=600)


def e3t_profiles():

    fn_co10 = 'CO10_1ts_20040101_20040101_shelftmb_grid_U.nc'
    co10 = xr.open_dataset('../Data/CO10_ldf_trace/' + fn_co10)

    fig, axs = plt.subplots(1,3, figsize=(6,4))
    plt.subplots_adjust(bottom=0.3, top=0.9, right=0.95)

    co10_blow = co10.isel(time_counter=0, x=slice(802,805), y=168)
    #co10_blow = co10_blow.stack(hor=['x','y'])
    print (co10_blow)

    axs[0].plot(co10_blow.zcur_tmp, co10_blow.depthu)
    axs[1].plot(co10_blow.zdiv_tmp, co10_blow.depthu)
    axs[2].plot(co10_blow.e3u, co10_blow.depthu)

    axs[0].set_xlabel('zcur_tmp')
    axs[1].set_xlabel('zdiv_tmp')
    axs[2].set_xlabel('e3u')

    for ax in axs:
        ax.invert_yaxis()
        ax.axvline(0, color='k', linestyle='--')

    axs[0].set_ylabel('Depth (m)')
    for ax in axs[1:3].flatten():
        ax.set_yticklabels([])
    plt.savefig('Plots/e3t_profiles.png', dpi=600)

#e3t_trace()
e3t_profiles()
    
    #m0 = m0.isel(time_counter=4)#, x=slice(1036,1159), y=slice(1172,None))
    #m1 = m1.isel(time_counter=4)#, x=slice(1036,1159), y=slice(1172,None))
