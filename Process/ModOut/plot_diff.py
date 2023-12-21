import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

src = '/projectsa/NEMO/ryapat/debugNEMOout/'

def plot_norway_ssh_diff_all(m0, m1, m2, m3, bathy=None, var='sossheig'):
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
    p1 = render(axs[1], diff0, vmin=-0.3, vmax=0.3,
                title='CO10\nunscaled e3t')
    render(axs[2], diff1, vmin=-0.2, vmax=0.2,
                title='CO10\nscaled e3t')
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

def plot_norway_ssh_diff(m0, m1, m2, bathy=None, var='sossheig'):
    """ plot difference between two models in the north of norway """

    fig, axs = plt.subplots(1,3, figsize=(6,4))
    plt.subplots_adjust(bottom=0.3, top=0.9, right=0.95)

    def render(ax, m, vmin=-5, vmax=5, title=None): 
        p = ax.pcolor(m.nav_lon, m.nav_lat, m.sossheig, vmin=vmin, vmax=vmax,
                  cmap=plt.cm.RdBu)
        ax.set_title(title, size=8)
        return p

    m0 = m0.isel(time_counter=41, x=slice(1086,1109), y=slice(1252,None))
    m1 = m1.isel(time_counter=41, x=slice(1086,1109), y=slice(1252,None))
    m2 = m2.isel(time_counter=41, x=slice(1086,1109), y=slice(1252,None))
    diff0 = m0-m1
    diff1 = m0-m2

    p0 = render(axs[0], m0, title='CO9\n')
    p1 = render(axs[1], diff0, vmin=-1, vmax=1,
                title='CO10\nunscaled e3t')
    render(axs[2], diff1, vmin=-1, vmax=1,
                title='CO10\nscaled e3t')

    for ax in axs[1:3]:
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
    pos1 = axs[2].get_position()
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

    plt.savefig('Plots/e3t_compare_enda_scaling.png', dpi=600)

def plot_norway_ssh_diff_main(src):
    bathy = xr.open_dataset(src + 'GEG_SF12.nc')
    bathy = bathy.set_coords(['nav_lon','nav_lat']).bathy.squeeze()
    fn_co10 = 'CO10_1ts_20040101_20040101_shelftmb_grid_T.nc'
    fn_co9  = 'CO9_1.5b_1ts_20040101_20040101_shelftmb_grid_T.nc'
    co9 = xr.open_dataset(src + 'CO9/' + fn_co9)
    co10_no_enda = xr.open_dataset(src + 'CO10_no_enda/' + fn_co10)
    co10_enda = xr.open_dataset(src + 'CO10_enda/' + fn_co10)
    co10_enda_spg_fix = xr.open_dataset(src + 'CO10_enda_spg_fix/' + fn_co10)
    plot_norway_ssh_diff(co9, co10_no_enda, co10_enda_spg_fix)

def h_cbar(fig, ax, p, title):
    pos = ax.get_position()
    cbar_ax = fig.add_axes([pos.x0, 0.10, pos.x1 - pos.x0, 0.02])
    cbar = fig.colorbar(p, cax=cbar_ax, orientation='horizontal')
    cbar.ax.text(0.5, -2.7, title, fontsize=8,
                 transform=cbar.ax.transAxes, va='top', ha='center')
def e3t_trace(src):
    fn_co10 = 'CO10_1ts_20040101_20040101_shelftmb_grid_U.nc'
    co10 = xr.open_dataset(src + 'CO10_ldf_trace/' + fn_co10)

    fig, axs = plt.subplots(2,3, figsize=(6,5))
    plt.subplots_adjust(bottom=0.22, top=0.92, right=0.8, hspace=0.25,
                        wspace=0.2)

    co10 = co10.isel(time_counter=0, x=slice(777,813), y=slice(158,181),
                     depthu=0)
    def render(ax, m, var, vmin=-5, vmax=5, title=None, cmap=plt.cm.RdBu): 
        p = ax.pcolor(m.nav_lon, m.nav_lat, m[var], vmin=vmin, vmax=vmax,
                  cmap=cmap)
        ax.set_title(title, size=8)
        return p

    p0 = render(axs[0,0], co10, 'zu_frc',  title='dynspg_ts\nzu_frc',
                vmin=-20, vmax=20)
    p1 = render(axs[0,1], co10, 'sum_puu_ldf_a',  title='dynldf\nu_baro_b',
                vmin=-20, vmax=20)
    p2 = render(axs[0,2], co10, 'sum_puu_ldf_b',  title='dynldf\nu_baro_a',
                vmin=-20, vmax=20)
    p3 = render(axs[1,0], co10, 'zcur_tmp',  title='dynldf\nzcur',
                vmin=-3, vmax=3)
    p4 = render(axs[1,1], co10, 'zdiv_tmp',  title='dynldf\nzdiv',
                vmin=-6, vmax=6)
    p5 = render(axs[1,2], co10, 'e3u',  title='dynldf\ne3u',
                vmin=0.0, vmax=0.2, cmap=plt.cm.copper)

    pos = axs[0,2].get_position()
    cbar_ax = fig.add_axes([0.82, pos.y0, 0.02, pos.y1 - pos.y0])
    cbar = fig.colorbar(p2, cax=cbar_ax, orientation='vertical')
    cbar.ax.text(5.5, 0.5, r'u-trend (m s$^{-2}$)', fontsize=8,
                 transform=cbar.ax.transAxes, va='center', ha='right',
                 rotation=90)

    h_cbar(fig, axs[1,0], p3, r'gradient vorticity (m$^3$ s$^{-2}$)')
    h_cbar(fig, axs[1,1], p4, r'gradient divergence (m$^2$ s$^{-2}$)')
    h_cbar(fig, axs[1,2], p5, r'e3u (m)')

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

def e3t_diff(src):

    fn_co10 = 'CO10_1ts_20040101_20040101_shelftmb_grid_T.nc'
    fn_co9 = 'CO9_1.5b_1ts_20040101_20040101_shelftmb_grid_T.nc'
    co10 = xr.open_dataset(src + 'CO10_e3t/' + fn_co10).e3t
    co9 = xr.open_dataset(src + 'CO9_e3t/' + fn_co9).e3t
   
    co9 = co9.isel(time_counter=40).sum('deptht')
    co10 = co10.isel(time_counter=40).sum('deptht')

    diff = co9-co10
    print (diff.min().values)
    print (diff.max().values)

    fig, axs = plt.subplots(1,1, figsize=(6,6))
    plt.subplots_adjust(bottom=0.3, top=0.9, right=0.95)
    plt.pcolor(diff, vmin=-0.01, vmax=0.01, cmap=plt.cm.RdBu)
    plt.show()

e3t_diff(src)
#e3t_trace(src)
#e3t_profiles()
#plot_norway_ssh_diff_main(src)
    
    #m0 = m0.isel(time_counter=4)#, x=slice(1036,1159), y=slice(1172,None))
    #m1 = m1.isel(time_counter=4)#, x=slice(1036,1159), y=slice(1172,None))
