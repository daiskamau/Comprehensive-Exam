# CosmoDC2 Weak Lensing Profiles
<!-- 
This repository contains the synthesis paper and computing artifact of my comprehensive examination. The synthesis paper details the four main papers used for the study.  -->
The `Computing Artifact` folder contains jupyter notebooks demonstrating how to calculate the weak lensing profile using the cosmoDC2 catalog and `.py` file that shows how we parallelized the calculation of the weak lensing signal. They files include:

1. **`WL_Measurements` - Weak Lensing measurements**

This notebook demonstrates how we extracted cosmoDC2 catalog using <a href='https://github.com/LSSTDESC/gcr-catalogs'> Generic Catalog Reader (GCR)</a> and computed the weak lensing signal for one of the extracted halos using <a href='https://github.com/LSSTDESC/CLMM'>Cluster weak Lensing Mass Modeling (CLMM)</a>. We also compute the weak lensing signal using our own user defined function and compare to that of CLMM. In addition, we will also explore one of the popular astronomy python package, astropy.

2. **`WL_Analysis`- Weak Lensing analysis**

The notebook demonstrates the analysis done using the weak lensing measurements of the cosmoDC2 catalog. To investigate selection bias we compare the lensing measurements of the underlying halos and the richness-selected halos from the redMaPPer cosmoDC2 catalog.

3. **`redmapperCL-Halos` - Joining halos to redmapper clusters**

The notebook details extraction of the redMaPPer cosmoDC2 catalog using <a href='https://github.com/LSSTDESC/gcr-catalogs'> Generic Catalog Reader (GCR)</a>. It also demomstrates how we joined the extracted redMaPPer cluster catalog to the cosmoDC2 halos.

4. **`Color-Index_redmapperCat` Color Index of the reMaPPer cluster catalog**

The notebook illustrates the color index measurements of the red sequence galaxies. We use the redMaPPer cosmoDC2 catalog extracted using <a href='https://github.com/LSSTDESC/gcr-catalogs'> Generic Catalog Reader (GCR)</a>.


## Requirements 
Due to the size of the catalogs and collaboration purposes, they have been mirrored at National Energy Research Scientific Computing Center (NERSC) and IN2P3-CC. These notebook were prepared and run in NERSC, which also offers scientific computing resources. To access the NERSC computing resources you need to be in the LSST-DESC user group or be a member of a project that already has NERSC allocation. You are required to have an active project to be accepted in the LSST-DESC user group. Follow these [steps](https://docs.nersc.gov/accounts/) to create an account with NERSC. To join LSST-DESC user group click on [apply for DESC membership](https://lsstdesc.org/pages/apply.html).

NERSC is a shared resource and does have CLMM installed by default. To install CLMM, create a virtual envirnoment and follow the steps of [how to install CLMM in NERSC](https://github.com/LSSTDESC/CLMM/blob/main/INSTALL.md).

## How to use the notebooks

Once you have access to NERSC and have installed CLMM, you can clone this repository using

    git clone https://github.com/daiskamau/Comprehensive-Exam.git