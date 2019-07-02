"""
Make sure we have our velocities correct
"""

from astropy import coordinates
from astropy import units as u
from astropy import constants
from astropy.time import Time

# observatory-centric channel-zero
date_freq = {'2016-10-02': 48955.192*u.MHz,
             '2016-12-26': 48957.667*u.MHz,
             '2016-12-30': 48957.932*u.MHz,
             '2017-01-07': 48958.478*u.MHz,
            }

cs_restfrq = 48.990957*u.GHz
casafreq_lsr = 48.98000*u.GHz # this is the middle of the channel
casafreq_lsr = 48.98044*u.GHz # this is the "top end" of the channel
print(f"CASA-reported LSR frequency: {casafreq_lsr} = {casafreq_lsr.to(u.km/u.s, u.doppler_radio(cs_restfrq))}")

target = coordinates.SkyCoord('19:23:43.910000 +14:30:34.61001', frame='fk5', unit=(u.hour, u.deg),
                              distance=5.1*u.kpc, # not relevant
                              pm_ra_cosdec=0*u.mas/u.yr, pm_dec=0*u.mas/u.yr,
                              radial_velocity=0*u.km/u.s)
bary_to_lsr = target.transform_to(coordinates.LSR).radial_velocity
print(f"Bary-to-LSR: {bary_to_lsr}")

for timestr,ch0frq in date_freq.items():

    # CS 1-0 peaks at channel #24 (indexed from zero) in spw 26
    pkch = 24
    bw = 1*u.MHz
    pkchfrq = pkch*bw + ch0frq

    obstime = Time(timestr)

    target = coordinates.SkyCoord('19:23:43.910000 +14:30:34.61001', frame='fk5', unit=(u.hour, u.deg))

    vla = coordinates.EarthLocation.of_site('Very Large Array')

    rvcorr = target.radial_velocity_correction(obstime=obstime, location=vla).to('km/s')

    rvcorr_frq = rvcorr.to(u.GHz, u.doppler_radio(ch0frq)) - ch0frq

    print(f"On {obstime}, radial velocity correction is {rvcorr} = {rvcorr_frq.to(u.MHz)}")


    pkchvel_topo = pkchfrq.to(u.km/u.s, u.doppler_radio(cs_restfrq))

    print(f"Topocentric velocity measured = {pkchvel_topo}.  Bary = {pkchvel_topo+rvcorr}  LSR = {pkchvel_topo+rvcorr+bary_to_lsr}")

    freq_lsr = pkchfrq + (rvcorr+bary_to_lsr).to(u.GHz, u.doppler_radio(cs_restfrq))-cs_restfrq

    print(f"CASA frequency - calculated frequency = {(casafreq_lsr - freq_lsr).to(u.MHz)}")
