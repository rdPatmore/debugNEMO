import xarray as xr
import matplotlib.pyplot as plt

def cut_bdy(x0, x1, y0, y1, src_dta):
    ''' cut lateral extent to match indicies x0, x1, y0, y1 '''

    in_path = '/home/users/ryapat30/NOC/genNEMO/'
    in_glos = 'OUTPUT/AMM15_bdyT_y2004m01.nc'

    glos = xr.open_dataset(in_path + in_glos) 

    lat_cut = glos.nav_lat.isel(x=slice(x0, x1), y=slice(y0, y1))
    lon_cut = glos.nav_lon.isel(x=slice(x0, x1), y=slice(y0, y1))

    src_dta_cut = src_dta.where( (src_dta.nav_lon > lon_cut.min()) &
                                 (src_dta.nav_lon < lon_cut.max()) &
                                 (src_dta.nav_lat > lat_cut.min()) &
                                 (src_dta.nav_lat < lat_cut.max()), drop=True)

    dst_dta_cut = glos.isel(x=slice(x0, x1), y=slice(y0, y1))

    return src_dta_cut, dst_dta_cut

def plot_norway_slab():
    src = '/gws/nopw/j04/jmmp/MASS/GloSea6/Daily/glosea6_grid_T_20040401.nc'

    glos = xr.open_dataset(src, chunks=-1).squeeze()
    
    for i in range(75):

        fig, axs = plt.subplots(2,2)
        glos_2d = glos.isel(deptht=i)
        glos_2d_cut, dst_cut = cut_bdy(1060, 1160, 1300, 1400, glos_2d)

        axs[0,0].pcolor(glos_2d_cut.nav_lon, glos_2d_cut.nav_lat,
                   glos_2d_cut.votemper, cmap=plt.cm.copper)
        axs[0,0].pcolor(dst_cut.nav_lon, dst_cut.nav_lat, dst_cut.bdy_msk, alpha=0.2)
        axs[1,0].pcolor(glos_2d_cut.nav_lon, glos_2d_cut.nav_lat,
                   glos_2d_cut.votemper, cmap=plt.cm.copper)
        axs[0,1].pcolor(dst_cut.nav_lon, dst_cut.nav_lat, dst_cut.bdy_msk, alpha=0.2)
        plt.savefig('parent_temp_depth_{}.png'.format(i))
        plt.close()

plot_norway_slab()

