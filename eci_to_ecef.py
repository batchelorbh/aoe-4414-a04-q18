#!/usr/bin/env python
# eci_to_ecef.py
#
# Converts ECI components to ECEF
#
# Usage: python3 eci_to_ecef.py year month day hour minute second
#                               eci_x_km eci_y_km eci_z_km
#
# Written by Blake Batchelor, batchelorbh@vt.edu
# Other contributors: none
#
# Parameters:
#    year                input year
#    month               input month
#    day                 input day
#    hour                input hour
#    minute              input minute
#    second              input second
#    eci_x_km            ECI x component
#    eci_y_km            ECI y component
#    eci_z_km            ECI z component
#
# Output:
#    Prints ECEF components to the screen
#
# Revision history:
#    09/29/2024          Script created
#
###############################################################################

#Import relevant modules
import sys
from math import pi, fmod, cos, sin

#Define constants
R_E_KM = 6378.137
E_E = 0.081819221456
W = 7.292115e-5

#Calculate denominator for SE and CE equations
def calc_denom(ecc, lat_rad):
   return sqrt(1 - ecc**2 * sin(lat_rad)**2)

#Pre-initialize input parameters
year = float('nan') #Input year
month = float('nan') #Input month
day = float('nan') #Input day
hour = float('nan') #Input hour
minute = float('nan') #Input minute
second = float('nan') #Input second
eci_x_km = float('nan') #ECI x component in km
eci_y_km = float('nan') #ECI y component in km
eci_z_km = float('nan') #ECI z component in km

#Arguments are strings by default
if len(sys.argv) == 10:
   year = float(sys.argv[1])
   month = float(sys.argv[2])
   day = float(sys.argv[3])
   hour = float(sys.argv[4])
   minute = float(sys.argv[5])
   second = float(sys.argv[6])
   eci_x_km = float(sys.argv[7])
   eci_y_km = float(sys.argv[8])
   eci_z_km = float(sys.argv[9])
else:
   print(('Usage: python3 ecef_to_eci.py year month day hour minute second '
                         'ecef_x_km ecef_y_km ecef_z_km'))
   sys.exit()

#Main body of script

#Calculate fractional Julian date
jd1 = day - 32075
jd2 = 1461 * (year + 4800 + (month - 14) // 12) // 4
jd3 = 367 * (month - 2 - (month - 14) // 12 * 12) // 12
jd4 = -3 * ((year + 4900 + (month - 14) // 12) / 100) // 4

jd = jd1 + jd2 + jd3 + jd4

jd_mid = jd - 0.5
d_frac = (second + 60 * (minute + 60 * hour)) / 86400
jd_frac = jd_mid + d_frac

#Calculate GMST angle
TUT1 = (jd_frac - 2451545.0) / 36525

GMST = 67310.54841 + (876600 * 60 * 60 + 8640184.812866) * TUT1 \
       + 0.093104 * TUT1**2 + -6.2e-6 * TUT1**3

GMST_rad = fmod(fmod(GMST, 86400) * W, 2 * pi)

#Calculate ECEF components
ecef_x_km = eci_x_km * cos(-GMST_rad) - eci_y_km * sin(-GMST_rad)
ecef_y_km = eci_x_km * sin(-GMST_rad) + eci_y_km * cos(-GMST_rad)
ecef_z_km = eci_z_km

#Print ECEF components
print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)
