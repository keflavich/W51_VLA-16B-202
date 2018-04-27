import glob
import spectral_cube
from astropy import units as u

for fn in glob.glob("*.image.pbcor.fits"):
    try:
        cube = spectral_cube.SpectralCube.read(fn)
    except Exception as ex:
        print(ex)

    if len(cube) <= 2:
        continue

    cube = cube[1:-1,:,:].minimal_subcube()
    cube.beam_threshold = 10

    mx = cube.max(axis=0)
    mx.write('maxs/{0}_max_Jy.fits'.format(fn[:-5]), overwrite=True)

    std = cube.std(axis=0)
    std.write('moments/{0}_std_Jy.fits'.format(fn[:-5]), overwrite=True)

    speclen = len(cube)

    mx_K = mx.to(u.K, u.brightness_temperature(cube.beams[int(speclen/2)], cube.spectral_axis.mean()))
    mx_K.write('maxs/{0}_max_K.fits'.format(fn[:-5]), overwrite=True)
