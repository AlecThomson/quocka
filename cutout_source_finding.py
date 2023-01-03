#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from astropy.io import fits
from astropy.nddata.utils import Cutout2D
from astropy.wcs import WCS

sname = sys.argv[1]

hdu = fits.open(sname)
data = hdu[0].data[0, 0]
wcs = WCS(hdu[0].header).dropaxis(3).dropaxis(2)
centre_pix_y = int(data.shape[0] / 2)
centre_pix_x = int(data.shape[1] / 2)
cutout = Cutout2D(
    hdu[0].data[0, 0], position=(centre_pix_x, centre_pix_y), size=(800, 800), wcs=wcs
)

# Here we remove two axes from the image data, to avoid conflicting with Aegean/Aplpy.

hdu[0].data = cutout.data
hdu[0].header.update(cutout.wcs.to_header())
hdr = hdu[0].header
del hdr[19:27]
cutout_filename = sname[:-4] + "cutout.fits"
fits.writeto(cutout_filename, hdu[0].data, hdr)
