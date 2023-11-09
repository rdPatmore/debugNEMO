import xarray as xr
import matplotlib.pyplot as plt
import cmocean

def plot_glosea_bdy():
    ''' plot bdy imput extracted from glosea data '''

    in_path = '/home/users/ryapat30/NOC/genNEMO/OUTPUT/'
    in_file = 'AMM15_bdyT_y1993m01.nc'

    ssh = xr.open_dataset(in_path + in_file, chunks=-1).sossheig
    ssh = ssh.isel(time_counter=0).squeeze()

    fig, axs = plt.subplots(2,1, figsize=(6,4))
    plt.subplots_adjust()

    axs[0].plot(ssh)
    plt.savefig('glosea_bdy_ssh.png')

def add_cbar(fig, ax, p, txt):
    pos = ax.get_position()
    cbar_ax = fig.add_axes([0.87, pos.y0, 0.02, pos.y1 - pos.y0])
    cbar = fig.colorbar(p, cax=cbar_ax, orientation='vertical')
    cbar.ax.text(4.5, 0.5, txt, fontsize=8, rotation=90,
                 transform=cbar.ax.transAxes, va='center', ha='right')

def add_cbar_multi(fig, ax0, ax1, p, txt):
    pos0 = ax0.get_position()
    pos1 = ax1.get_position()
    cbar_ax = fig.add_axes([0.82, pos0.y0, 0.02, pos1.y1 - pos0.y0])
    cbar = fig.colorbar(p, cax=cbar_ax, orientation='vertical')
    cbar.ax.text(6.0, 0.5, txt, fontsize=8, rotation=90,
                 transform=cbar.ax.transAxes, va='center', ha='right')


def plot_glosea_bdy_t_and_s():
    ''' plot bdy imput extracted from glosea data '''

    in_path = '/home/users/ryapat30/NOC/genNEMO/OUTPUT/'
    in_file = 'AMM15_bdyT_y1993m01.nc'

    grid_T = xr.open_dataset(in_path + in_file, chunks=-1)
    grid_T = grid_T.isel(time_counter=0).squeeze()
    print (grid_T.votemper)

    fig, axs = plt.subplots(2,1, figsize=(6,4))
    plt.subplots_adjust(right=0.85)

    p0 = axs[0].pcolor(grid_T.votemper)
    p1 = axs[1].pcolor(grid_T.vosaline)
    add_cbar(fig, axs[0], p0, 'temp')
    add_cbar(fig, axs[1], p1, 'sal')

    plt.savefig('glosea_bdy_t_and_s.png')

def plot_compare_bdy_t_and_s():
    ''' compare bdy temperature and salinity between co9 and GloSea '''

    in_path = '/home/users/ryapat30/NOC/genNEMO/'
    in_glos = 'OUTPUT/AMM15_bdyT_y2004m01.nc'
    in_orig = 'OUTPUT_CO9/amm15_bdyT_y2004m01d01.nc'

    glos = xr.open_dataset(in_path + in_glos, chunks=-1).squeeze()
    orig = xr.open_dataset(in_path + in_orig, chunks=-1).squeeze()
    glos = glos.isel(time_counter=0)

    fig, axs = plt.subplots(4,1, figsize=(6,5))
    plt.subplots_adjust(right=0.80, hspace=0.15)

    p0 = axs[0].pcolor(glos.votemper, vmin=-2, vmax=13, cmap=cmocean.cm.thermal)
    p1 = axs[2].pcolor(glos.vosaline, vmin=33.5, vmax=35,
                       cmap=cmocean.cm.haline)
    p2 = axs[1].pcolor(orig.votemper, vmin=-2, vmax=13, cmap=cmocean.cm.thermal)
    p3 = axs[3].pcolor(orig.vosaline, vmin=33.5, vmax=35,
                       cmap=cmocean.cm.haline)
    add_cbar_multi(fig, axs[1], axs[0], p0, 'Temperature')
    add_cbar_multi(fig, axs[3], axs[2], p1, 'Salinity')

    for ax in axs:
        ax.invert_yaxis()
        ax.set_ylabel('model level')
    for ax in axs[:-1]:
        ax.set_xticklabels([])
    axs[-1].set_xlabel('bdy pts')

    plt.savefig('glosea_compare.png')

plot_compare_bdy_t_and_s()
