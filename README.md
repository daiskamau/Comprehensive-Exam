# CosmoDC2 Weak Lensing Profiles

This repository contains the synthesis paper and computing artifact of my comprehensive examination. The synthesis paper details the four main papers used for the study. The computing artifact contains four jupyter notebooks demonstrating how to calculate the weak lensing profile using the cosmoDC2 catalog. The notebooks are in the `Computing Artifact` folder. They include:

1. **WeakLensing**
This notebook demonstrates how we extracted cosmoDC2 catalog from <a href='https://github.com/LSSTDESC/gcr-catalogs'> Generic Catalog Reader (GCR)</a> and computed the weak lensing signal for one of the extracted halos using <a href='https://github.com/LSSTDESC/CLMM'>Cluster weak Lensing Mass Modeling (CLMM)</a>. In addition, we will also explore one of the popular astronomy python package, astropy.

GCR is an open source python package serving as a repository of various galaxy and sky catalogs for the LSST Dark Energy Science Collaboration (DESC). GCR offers a unified UI (User Interface) acccess to all the catalogs in the repository. CLMM is also an open source python library for estimating the weak lensing mass of clusters of galaxies and performing any related weak lensing analysis. CLMM has useful packages and functions that can easily be called to compute the weak lensing signal of the source galaxies.
 
The notebook has 3 sections:
- Loading the Catalog
- Computing the lensing signal for 1 Halo using CLMM
- Computing the lensing signal using a our own defined function (Parallelization)

**<font color='red'>NOTE</font>**<br>
Due to the size of the catalogs and collaboration purposes, the GCR catalogs have been mirrored at National Energy Research Scientific Computing Center (NERSC) and IN2P3-CC. This notebook was prepared and run in NERSC, which offers scientific computing resources. To access the NERSC computing resources you need to be in the LSST user group.
