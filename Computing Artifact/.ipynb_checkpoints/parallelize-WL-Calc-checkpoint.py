import numpy as np
import pandas as pd
import math

import GCRCatalogs as gcr
import healpy as hp
from astropy.table import Table, setdiff
from astropy.io import fits
from astropy.cosmology import FlatLambdaCDM
from astropy.coordinates import SkyCoord
from astropy.table import Table

import fitsio
from fitsio import FITS #,FITSHDR
from multiprocessing import Pool, cpu_count
import argparse
# import timeit

# start = timeit.default_timer()

c = 3e5
G = 4.302e-9
cosmo = FlatLambdaCDM(H0=70.1, Om0=0.266)
z_interp = np.linspace(0, 5, 200)
chi_interp = cosmo.comoving_distance(z_interp).value
from scipy.interpolate import interp1d
comoving_distance_interp= interp1d(z_interp, chi_interp)


# Load the cosmoDC2 catalog
catalog_440 = gcr.load_catalog('cosmoDC2_v1.1.4')


# Get the neighbouring pixels 
hpix_list = catalog_440.available_healpix_pixels   # Load all the available pixels of cosmoDC2 catalog---131
parser = argparse.ArgumentParser()
parser.add_argument("pixel_index", type=int)
args = parser.parse_args()
hpix = hpix_list[args.pixel_index]
s_ds = pd.DataFrame(columns=['halo_id','radius','sigma','DS']) #columns=['halo_id','radius','sigma','DS']
s_ds.to_pickle('/global/homes/k/kamau/SE-CLMM-LSSTDESC/cosmoDC2/Data/pixel-{}.csv'.format(hpix))

hpix_neighbors = hp.pixelfunc.get_all_neighbours(32, hpix)
hpix_toread = list(set(hpix_list) & set(hpix_neighbors)) + [hpix]


# Get all the source galaxies in the hpix_toread
ra_gal = []
dec_gal = []
z_gal = []
kappa = []
shear1 = []
shear2 = []

## getting galaxies
for hpix_i in hpix_toread:
    galaxy_data = catalog_440.get_quantities(['ra', 'dec', 'redshift_true', 'convergence', 'shear_1', 'shear_2'], 
                                             filters=['convergence != 0'],  native_filters=f'healpix_pixel == {hpix_i}')
    ra_gal.extend(galaxy_data['ra'])
    dec_gal.extend(galaxy_data['dec'])
    z_gal.extend(galaxy_data['redshift_true'])
    kappa.extend(galaxy_data['convergence'])
    shear1.extend(galaxy_data['shear_1'])
    shear2.extend(galaxy_data['shear_2'])
    # print(hpix_i, "Done!")

ra_gal = np.array(ra_gal)
dec_gal = np.array(dec_gal)
z_gal = np.array(z_gal)
kappa = np.array(kappa)
shear1 = np.array(shear1)
shear2 = np.array(shear2)
chi_s =  comoving_distance_interp(z_gal)   #cosmo.comoving_distance(z_gal).value #this step takes some time

# Reading the halo
cluster_data = Table.read('/global/homes/k/kamau/SE-CLMM-LSSTDESC/cosmoDC2/Data/clusters/clusters_{}.dat'.format(hpix), format='ascii')
print(len(cluster_data['ra']))

# getting the halos
def compute_sigma_ds(df_chunks):
    for halo in range(len(df_chunks)): #len(df_chunks)

    # Compute Sigma and DS for each halo  
        m, dec_cl, haloid, ra_cl, z_cl = df_chunks[halo]
        
        sel = (z_gal > z_cl + 0.01) & (z_gal < 2 * z_cl)
        ra_gal_sel = ra_gal[sel] 
        dec_gal_sel = dec_gal[sel]
        chi_s_sel = chi_s[sel]

        c1 = SkyCoord(ra_gal_sel, dec_gal_sel, unit='degree')
        c2 = SkyCoord(ra_cl, dec_cl, unit='degree')
        sep = c1.separation(c2).degree

        pa = c1.position_angle(c2).rad
        chi_l = cosmo.comoving_distance(z_cl).value

        Sigma_crit = c**2 /(4 * np.pi* G) * chi_s_sel * (1+ z_cl) / chi_l / (chi_s_sel - chi_l)

        w = Sigma_crit**(-2)
        Sigma = kappa[sel] * Sigma_crit

        gammat = + shear1[sel] * np.cos(-2*pa) - shear2[sel] * np.sin(-2*pa)
        DS = gammat * Sigma_crit

        rp = sep * np.pi / 180. * chi_l / (1 + z_cl)

        # making profiles
        nbins = 15
        rp_bins = np.logspace(-1, 1.8, nbins+1) # pMpc
        mean_Sigma = np.zeros(nbins)
        mean_rp = np.zeros(nbins)
        mean_DS = np.zeros(nbins)
        for ibin in range(nbins):
            sel = (rp > rp_bins[ibin])&(rp <= rp_bins[ibin+1])
            mean_Sigma[ibin] = np.sum(Sigma[sel]*w[sel])/np.sum(w[sel])
            mean_rp[ibin] = np.sum(rp[sel]*w[sel])/np.sum(w[sel])
            mean_DS[ibin] = np.sum(DS[sel]*w[sel])/np.sum(w[sel])

        df1 = pd.read_pickle('/global/homes/k/kamau/SE-CLMM-LSSTDESC/cosmoDC2/Data/pixel-{}.csv'.format(hpix))
        dataa = np.array([haloid, mean_rp, mean_Sigma, mean_DS])
        df2 = pd.DataFrame([dataa.tolist()],columns=['halo_id','radius','sigma','DS'])
        s_ds7 = pd.concat([df1,df2])
        s_ds7.to_pickle('/global/homes/k/kamau/SE-CLMM-LSSTDESC/cosmoDC2/Data/pixel-{}.csv'.format(hpix))
    print('Done!!!')
        
        
               
procs = 10
df_chunks = np.array_split(cluster_data ,procs)
# df_chunks
if __name__ == '__main__':
    # mp.set_start_method('spawn')
    with Pool(processes=procs) as p:
        p.map(compute_sigma_ds, df_chunks)