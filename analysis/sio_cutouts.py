import pyregion
from spectral_cube import SpectralCube, lower_dimensional_structures
from astropy import constants, units as u, table, stats, coordinates, wcs
#from paths import rpath
rpath = lambda x: x

for line, freq, spw in (
                        ('SiO_v=2', 42.82057, 40),
                        ('SiO_v=1', 43.12209, 43),
                        ('SiO_v=0', 43.42385, 46),
                        ('SiO_v=3', 42.51937, 38),
                       ):
    for epoch in range(4):

        output = imagename = myimagebase = 'W51North_QbandAarray_{0}_epoch{1}'.format(line, epoch)

        cube = SpectralCube.read(output+".image.pbcor.fits")
        vcube = cube.with_spectral_unit(u.km/u.s, velocity_convention='radio',
                                        rest_value=freq*u.GHz)

        cutout = vcube.subcube_from_ds9region(pyregion.open(rpath('siomaserbox.reg')))
        slab = cutout.spectral_slab(35*u.km/u.s, 75*u.km/u.s)

        slab.write('siocutouts/{0}_cutout.image.pbcor.fits'.format(output))
