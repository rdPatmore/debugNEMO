import xarray as xr
import matplotlib.pyplot as plt

def compare_bathys():
    """
    Compare input bathys for AMM15:
        (1) raw bathy
        (2) bathy in domain_cfg
    """

    # get data
    cfg_path = "/gws/nopw/j04/jmmp/public/AMM15/DOMAIN_CFG/GEG_SF12.nc"
    cfg_bathy = xr.open_dataset(cfg_path, chunks=-1).squeeze()
    bathy_path = "/home/users/ryapat30/NOC/genNEMO/INPUT/GLOSEA6/AMM15_P2.0_bathy.nc"
    bathy = xr.open_dataset(bathy_path, chunks=-1).set_coords(
                     ["nav_lon","nav_lat"]).to_array().squeeze()

    x0, x1, y0, y1 = 1060, 1160, 1300, 1400
    cfg_bathy = cfg_bathy.isel(x=slice(x0, x1), y=slice(y0, y1))
    bathy = bathy.isel(x=slice(x0, x1), y=slice(y0, y1))

    # initialise plots
    fig, axs = plt.subplots(4)

    #cfg_bathy['bottom_level'] = xr.where(cfg_bathy.bottom_level > 0, 1, 0)
    bathy = xr.where(bathy > 0, 1, 0)
    axs[0].pcolor(cfg_bathy.nav_lon, cfg_bathy.nav_lat, cfg_bathy.top_level,
                  vmin=0, vmax=1, shading='nearest')
    axs[1].pcolor(cfg_bathy.nav_lon, cfg_bathy.nav_lat, cfg_bathy.bottom_level,
                  vmin=0, vmax=50, shading='nearest')
    diff = bathy - cfg_bathy.top_level
    #diff = cfg_bathy.bottom_level - cfg_bathy.top_level
    p = axs[2].pcolor(cfg_bathy.nav_lon, cfg_bathy.nav_lat, diff,
                  vmin=-1, vmax=1, shading='nearest')
    p = axs[3].pcolor(bathy.nav_lon, bathy.nav_lat, bathy,
                  vmin=-1, vmax=1, shading='nearest')
    #plt.colorbar(p)
    plt.savefig('bathy_compare.png')
compare_bathys()
