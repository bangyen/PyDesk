#!/usr/bin/env python3 -i

script_version = "20-217a"
# calc.py
#
# Loads a list set of functions and variables for everyday calculator
# functionality.
#
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or distribute
# this software, either in source code form or as a compiled binary, for any
# purpose, commercial or non-commercial, and by any means.
#
# In jurisdictions that recognize copyright laws, the author or authors of this
# software dedicate any and all copyright interest in the software to the public
# domain. We make this dedication for the benefit of the public at large and to
# the detriment of our heirs and successors. We intend this dedication to be an
# overt act of relinquishment in perpetuity of all present and future rights to
# this software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from collections import abc
from datetime import datetime
from decimal import Decimal
from fractions import Fraction
from random import randint
import math
import string
import re

#################
### Constants ###
#################

# General
from math import (pi, e)

# Chemistry and Thermodynamics
r_atm = 0.0820574614 # Gas constant (L*atm/mol/K)
r_mmhg = 62.3636711 # Gas constant (L*mmHg/mol/K)
r_joule = 8.314462175 # Gas constant (J/mol/K)
r_btu = 1.98588 # Gas constant (BTU/lbmol/R)
r_psia = 10.7316 # Gas constant (psia*ft^3/lbmol/R)
kw = 1.01e-14 # Equilibrium constant for auto-ionization of water
avo = 6.022e23 # Avogadro constant (mol^-1)

# Mechanics
g = 9.80665 # Acceleration due to gravity (m/s)
g_ft = 32.174049 # Acceleration due to gravity (ft/s)
G = 6.673e-11 # Gravitational constant (N*m^2/kg^2)

# Electromagnetism
ele = 1.602e-19 # Elementary charge (C)
mu_0 = math.pi / 2.5e+6 # Permiability of a vacuum (N/A^2)
epsilon_0 = 8.854e-12 # Permittivity of a vacuum (F/m)
k_e = 8.988e9 # Coulomb constant (N*m^2/C^2)
c = 2.998e8 # Speed of light in a vacuum (m/s)

# Quantum Physics
h = 6.626e-34 # Planck constant (J*s)
hbar = 1.054e-34 # h-bar constant (J*s)
m_e = 9.109e-31 # Electron mass (kg)
m_p = 1.673e-27 # Proton mass (kg)
m_n = 1.675e-27 # Neutron mass (kg)
eV = 1.602e-19 # Electron-volt (J)

#############################
### Convenience Functions ###
#############################

from math import (
	log as ln, log10, exp, sqrt, factorial, gamma, hypot, floor, ceil,
	radians as rad, degrees as deg,
	sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, asinh, acosh, atanh)

# Trigonometry in degrees
def sind(x): return sin(rad(x))
def cosd(x): return cos(rad(x))
def tand(x): return tan(rad(x))
def asind(x): return deg(asin(x))
def acosd(x): return deg(acos(x))
def atand(x): return deg(atan(x))
def sinhd(x): return sinh(rad(x))
def coshd(x): return cosh(rad(x))
def asinhd(x): return deg(asinh(x))
def acoshd(x): return deg(acosh(x))
def atanhd(x): return deg(atanh(x))

# Convert base unit to SI prefix
def exp10(x, y): return x * 10**y
def to_yotta(x): return exp10(x, -24)
def to_zetta(x): return exp10(x, -21)
def to_exa(x): return exp10(x, -18)
def to_peta(x): return exp10(x, -15)
def to_tera(x): return exp10(x, -12)
def to_giga(x): return exp10(x, -9)
def to_mega(x): return exp10(x, -6)
def to_kilo(x): return exp10(x, -3)
def to_centi(x): return exp10(x, 2)
def to_milli(x): return exp10(x, 3)
def to_micro(x): return exp10(x, 6)
def to_nano(x): return exp10(x, 9)
def to_angstrom(x): return exp10(x, 10)
def to_pico(x): return exp10(x, 12)
def to_femto(x): return exp10(x, 15)
def to_atto(x): return exp10(x, 18)
def to_zepto(x): return exp10(x, 21)
def to_yocto(x): return exp10(x, 24)

# Convert SI prefix to base unit
def from_yotta(x): return exp10(x, 24)
def from_zetta(x): return exp10(x, 21)
def from_exa(x): return exp10(x, 18)
def from_peta(x): return exp10(x, 15)
def from_tera(x): return exp10(x, 12)
def from_giga(x): return exp10(x, 9)
def from_mega(x): return exp10(x, 6)
def from_kilo(x): return exp10(x, 3)
def from_centi(x): return exp10(x, -2)
def from_milli(x): return exp10(x, -3)
def from_micro(x): return exp10(x, -6)
def from_nano(x): return exp10(x, -9)
def from_angstrom(x): return exp10(x, -10)
def from_pico(x): return exp10(x, -12)
def from_femto(x): return exp10(x, -15)
def from_atto(x): return exp10(x, -18)
def from_zepto(x): return exp10(x, -21)
def from_yocto(x): return exp10(x, -24)

########################
### Unit Conversions ###
########################

import subprocess # Used for calling out to GNU units
gnu_units_output = re.compile(
    r'(?:\t?(?P<reci_note>reciprocal conversion)?\n?'
    '\t\* (?P<normal>[\d\.\-\+e]+)\n'
    '\t/ (?P<reciprocal>[\d\.\-\+e]+))|'
    '(?:(?P<conform_note>conformability error)\n'
    '\t[\d\.\-\+e]+ (?P<in_unit>[^\n]+)\n'
    '\t[\d\.\-\+e]+ (?P<out_unit>[^\n]+))')
gnu_units_executable = 'gunits'

# Evaluate a query using [GNU Units](en.wikipedia.org/wiki/GNU_Units),
# returning a tuple containing the direct conversion, and the reciprocal
# conversion, respectively.
#   v: Number to convert
#   a: Unit to convert from
#   b: Unit to convert to
# If any errors occur, or if the output does not match the expected format, the
# output of GNU Units will be returned directly as a string.
def units(v, a, b):
    result = subprocess.run([gnu_units_executable, f'{v}{a}', b],
        stdout=subprocess.PIPE).stdout.decode('utf-8')
    m = gnu_units_output.match(result)
    if m:
        if m.group('conform_note'):
            return (m.group('conform_note'), m.group('in_unit'),
                m.group('out_unit'))
        if m.group('reci_note'):
            return (float(m.group('normal')), float(m.group('reciprocal')),
                m.group('reci_note'))
        return (float(m.group('normal')), float(m.group('reciprocal')))
    return result

# This is a shortcut for the `units()` function. It is defined separately in
# this manner because it is likely that the variable `u` may be used in
# calculations. If that is the case, `units()` can still be called by its full
# name.
def u(v, a, b): return units(v, a, b)

# Perform a unit conversion, but only return the normal conversion instead of a
# tuple. If the conversion results in a conformability or unknown error, `None`
# is returned. In addition, the full output of `units()` is printed unles
# `silent=True` is specified.
def uu(v, a, b, silent=False):
    conv = units(v, a, b)
    if not silent:
        print(conv)
    if not isinstance(conv, tuple) or conv[0] == 'conformability error':
        return None
    return conv[0]

####################
### General Math ###
####################

# Evaluate the quadratic formula for ax^2+bx+c=0
def quad_det(a, b, c):
    return b**2-4*a*c
def quad(a, b, c):
    return ((-b+sqrt(quad_det(a, b, c)))/(2*a),
            (-b-sqrt(quad_det(a, b, c)))/(2*a))

# Get the midpoint
def mid(a, b):
    return (a+b)/2
def mid2(x1, y1, x2, y2):
    return (mid(x1, x2), mid(y1, y2))
# Distance
def dist(a, b):
    return b-a
def dist2(x1, y1, x2, y2):
    return (dist(x1, x2)**2 + dist(y1, y2)**2)**0.5

# Linear interpolation
def lint(x1, xn, x2, y1, y2):
    return (y2 - y1) / (x2 - x1) * (xn - x1) + y1

# Pythagorean theorem
def pythleg(c, a):
    return sqrt(c**2 - a**2)

# Generate diceware values
def diceware(n = 5):
    for i in range(0, n):
        print(str(i + 1) + ": ", end="")
        for i in range(0, 5):
            print(randint(1, 6), end="")
        print()

######################
### Thermodynamics ###
######################

# Calculate enthalpy specific heat on a mole basis
def heat_cp_mol(T, *coeff):
    coeff = flatten_list(coeff)
    c_p = 0;
    for i in range(0, 3):
        c_p += coeff[i] * T**i
    return c_p

# Calculate internal energy specific heat on a mole basis
def heat_cv_mol(R, T, *coeff):
    return heat_cp_mol(T, coeff) - R

# Calculate enthalpy on a mole basis
def heat_h_mol(T, *coeff):
    coeff = flatten_list(coeff)
    h = 0
    for i in range(0, 3):
        h += coeff[i] * T**(i + 1) / (i + 1)
    return h

# Calculate internal energy on a mole basis
def heat_u_mol(R, T, *coeff):
    coeff = flatten_list(coeff)
    h =  heat_h_mol(T, coeff)
    return h - R * T

#########################
### Number Formatting ###
#########################

# Convert x to scientific notation
def sci(x, sigfig = 6):
    sigfig
    if sigfig < 1:
        sigfig = 1
    string = "{:." + str(sigfig - 1) + "e}"
    return string.format(x)

# Convert x to engineering notation
def eng(x, sigfig = 6):
    sci_string = sci(x)
    components = sci_string.split('e')
    exponent = int(components[1])
    offset = exponent % 3
    head = components[0].replace('.', '')
    is_negative = False
    if head[0] == '-':
        is_negative = True
        head = head[1:]
    head = head[:(offset + 1)] + ('.' if sigfig > 1 else '') + \
            head[(offset + 1):]
    new_exponent = exponent - offset
    out = ('-' if is_negative else '') + head + 'e' + \
            ('+' if new_exponent >= 0 else '-') + \
            ('0' if abs(new_exponent) < 10 else '') + str(abs(new_exponent))
    return out

# Convert an int n to an arbitrary base b (as string)
def to_base(n, b):
    num_dict = string.digits + string.ascii_lowercase
    if n < 0:
        sign = -1
    elif n == 0:
        return num_dict[0]
    else:
        sign = 1
    n *= sign
    digits = []
    while n:
        digits.append(num_dict[n % b])
        n //= b # Double-slash forces integer division
    if sign < 0:
        digits.append('-')
    digits.reverse()
    return ''.join(digits)

###############################
### Temperature Conversions ###
###############################

# Absolute zero checks
abs_zero_f = -459.67
abs_zero_c = -273.15
abs_zero_k = 0
def temp_check_zero(temp, zero):
    if temp < zero:
        print("Invalid. Result is below absolute zero.")
        return float('NaN')
    return round(temp, 8)

# Conversions
def temp_fc(f):
    c = (f-32) * (5/9)
    return temp_check_zero(c, abs_zero_c)
def temp_cf(c):
    f = c * (9/5) + 32
    return temp_check_zero(f, abs_zero_f)
def temp_ck(c):
    k = c + 273.15
    return temp_check_zero(k, abs_zero_k)
def temp_kc(k):
    c = k - 273.15
    return temp_check_zero(c, abs_zero_c)
def temp_fk(f):
    k = (f+459.67) * (5/9)
    return temp_check_zero(k, abs_zero_k)
def temp_kf(k):
    f = k * (9/5) - 459.67
    return temp_check_zero(f, abs_zero_f)

#################
### Fractions ###
#################

# Creates a Fraction object
def getfrac(x):
    return Fraction(x).limit_denominator()

# Prints a string representation of x as a fraction
def frac(x):
    print(getfrac(x))

# Prints a mixed number representation of x
def mix(x):
    fraction = getfrac(x)
    numerator = fraction.numerator
    denominator = fraction.denominator
    if numerator > denominator:
        whole = math.floor(x)
        mixed_numerator = numerator - whole * denominator
        print("%d %d/%d" % (whole, mixed_numerator, denominator))
    else:
        print("%d/%d" % (numerator, denominator))

###############
### Vectors ###
###############

# Convert an n-dimensional vector to a 3-dimensional one
def vector_to_3d(a):
    n = len(a)
    if n == 1:
        return (a[0], 0, 0)
    if n == 2:
        return (a[0], a[1], 0)
    if n >= 3:
        return (a[0], a[1], a[2])
    return (0, 0, 0) # This should only happen if n == 0

def vcross(a, b): # cross (vector) product of vector a and vector b
    a_ = vector_to_3d(a)
    b_ = vector_to_3d(b)
    return (a_[1] * b_[2] - a_[2] * b_[1], \
            a_[2] * b_[0] - a_[0] * b_[2], \
            a_[0] * b_[1] - a_[1] * b_[0])
def vadd(a, b): # add vector a to vector b
    a_ = vector_to_3d(a)
    b_ = vector_to_3d(b)
    return (a_[0] + b_[0], a_[1] + b_[1], a_[2] + b_[2])
def vneg(a): # negate vector a
    a_ = vector_to_3d(a)
    return (-a_[0], -a_[1], -a_[2])
def vsub(a, b): # subtract vector b from vector a
    return vadd(a, vneg(b))
def vdot(a, b): # dot (scalar) product of vector a and vector b
    a_ = vector_to_3d(a)
    b_ = vector_to_3d(b)
    return a_[0] * b_[0] + a_[1] * b_[1] + a_[2] * b_[2]
def vscale(a, alpha): # scale vector a by scalar alpha
    a_ = vector_to_3d(a)
    return (a_[0] * alpha, a_[1] * alpha, a_[2] * alpha)
def vlen(a): # get absolute value
    a_ = vector_to_3d(a)
    return sqrt(a_[0]**2 + a_[1]**2 + a_[2]**2)
def vproj(a, b): # projection of a onto b
    return vscale(b, vdot(a, b) / vdot(b, b))
def vunit(a): # makes a unit vector
    return vscale(a, 1 / vlen(a))
def vtheta(a, b): # find the angle between two vectors in radians
    return acos(vdot(a, b) / (vlen(a) * vlen(b)))
def dvtheta(a, b): # find the angle between two vectors in degrees
    return deg(vtheta(a, b))

#############
### Lists ###
#############

# Given a list containing some combination of (possibly deeply nested) Iterables
# and non-iterables, produce a single list of non-iterables. No guarentees are
# made regarding the order of the output values with respect to the input
# structure.
def flatten_list(*x):
    n = x
    m = []
    is_flat = False
    while not is_flat:
        is_flat = True
        for i in n:
            if isinstance(i, abc.Iterable):
                is_flat = False
                for j in i:
                    m.append(j)
            else:
                m.append(i)
        n = m
        m = []
    return n

# Given a (possibly deeply nested) list of numbers, produce a flattened list of
# floating-point numbers. No guarentees are made regarding the order of the
# output values with respect to the input structure.
def to_float_list(*x):
    n = flatten_list(x)
    m = []
    for i in n:
        m.append(float(i))
    return m

# Similar to to_float_list(), but casts all numbers to int().
def to_int_list(*x):
    n = flatten_list(x)
    m = []
    for i in n:
        m.append(int(i))
    return m

# Floating-point sum of a list
def fsum(*x):
    return math.fsum(to_float_list(x))

# Integer sum of a list
def isum(*x):
    n = to_int_list(x)
    sum = 0
    for i in n:
        sum += i
    return int(sum)

# Arithmetic mean of a list
def mean(*x):
    n = flatten_list(x)
    return fsum(n) / len(n)

# Population Standard Deviation of a list
def stdDev(*x):
    n = to_float_list(x)
    avg = mean(n)
    total_deviation = 0
    for i in n:
        total_deviation += (i - avg) ** 2
    return sqrt(1 / len(n) * total_deviation)

# %RSD of a list
def pctRSD(*x):
    try:
        return stdDev(x) / mean(x) * 100
    except ZeroDivisionError:
        return float('NaN')

################################
### Cellular Data Statistics ###
################################

# Given an integer from 1 to 12 (inclusive) representing a month, or the name
# of a month return the number of days in that month, ignoring leap years. If
# an invalid input is received, the function will not throw an exception, but
# will silently return 31.
def days_in_month(month):
    month_names = { 'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
    shortmonths = [4, 6, 9, 11]
    try:
        month_number = int(month)
    except ValueError:
        try:
            month_number = month_names[str(month).lower()[:3]]
        except KeyError: # Will default to 31 days
            month_number = 0
    if month_number in shortmonths:
        return 30
    elif month_number == 2: # Februrary
        return 28
    else: # For simplicity, assume 31 days if input is invalid.
        return 31


# Given the current amount of data used (in Gigabytes), and the total data
# allowance for each month (also in Gigabytes), calculate statistics for how
# much data should be used to yield a uniform usage pattern throughout the
# month.
def data(gb, total, reset_day = 11):
    now = datetime.now()
    if now.day >= reset_day:
        totalDays = days_in_month(now.month)
        cycleDay = now.day - (reset_day - 1)
    else:
        totalDays = days_in_month(now.month - 1)
        cycleDay = now.day + totalDays - (reset_day - 1)

    cycleUsage = gb * 1024
    idealRate = total * 1024 / totalDays
    idealUsage = idealRate * cycleDay
    cycleRate = cycleUsage / cycleDay
    netUsage = idealUsage - cycleUsage
    netRate = idealRate - cycleRate
    coefficient = cycleRate / idealRate
    daysUsed = cycleUsage / idealRate

    print("     Cycle Usage: %d MiB" % cycleUsage)
    print("     Ideal Usage: %d MiB" % idealUsage)
    print("       Net Usage: %d MiB" % netUsage)
    print("      Cycle Rate: %d MiB/day" % cycleRate)
    print("      Ideal Rate: %d MiB/day" % idealRate)
    print("        Net Rate: %d MiB/day" % netRate)
    print(" Use Coefficient: %f" % coefficient)
    print("       Cycle Day: %d / %d" % (cycleDay, totalDays))
    print("       Ideal Day: %d" % daysUsed)

    if netUsage < 0:
        daysBehind = -netUsage / idealRate + 1
        print("        Catch up: %d" % daysBehind)

######################
### Exit functions ###
######################

# Each of the following functions may be used to cleanly exit the Python
# interpreter. These can be useful in terminal emulators which do not exit upon
# reciept of a ^D signal.
def exit():
    import sys
    sys.exit()
def quit(): exit()
def bye(): exit()

print("PyDesk, version " + script_version)
