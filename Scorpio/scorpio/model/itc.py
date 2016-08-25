#!/usr/bin/env python

"""
Module for dealing with ITC data.

Includes ability to generate missing thermodynamic parameters, check quality
of thermodynamic data and convert between different thermodynamic units.
"""

import math
import re

# Physical constants
GAS_CONSTANT = (8.314472)  # gas constant

# Data quality checking constants
AFFINITY_MIN = 3.0794037998353931e-05 # -60 kJ/mol at 25C in uM
AFFINITY_MAX = 313.44081443683814     # -20 kJ/mol at 25C in uM
DELTA_G_MIN = -60.0  # DeltaG only reliably measured in -20 to -60 range
DELTA_G_MAX = -20.0
DELTA_H_REQ = -10.0  # DeltaH not reliably measured in -10 to 10 range
DELTA_H_REQ = 10.0
EQUALITY_ERR_TOL = 0.01  # Rounding error tolerance 

# Data quality warning levels
MISSING_DATA = 1  
INCONSISTENT_DATA = 2
DUBIOUS_DATA = 3

# Regular expression to identify new lines and white spaces used to clean up
# data quality warning messages
CLEAN_MSG = re.compile(r'\n\s*')

def _get_data_in_standard_units(affinity, delta_g, delta_h,
                                delta_s, temperature):
    """
    Returns any data as a tuple in the units below:
      * affinity - /M
      * delta_g - kJ/mol
      * delta_h - kJ/mol
      * delta_s - kJ/mol
      * temperature - K

    """
    tmp_ka = None
    tmp_delta_g = None
    tmp_delta_h = None
    tmp_delta_s = None
    tmp_t = None

    if isinstance(affinity, Affinity):
        tmp_ka = affinity.get_data('/M')[0]
    if isinstance(delta_g, DeltaG):
        tmp_delta_g = delta_g.get_data('kJ/mol')[0]
    if isinstance(delta_h, DeltaH):
        tmp_delta_h = delta_h.get_data('kJ/mol')[0]
    if isinstance(delta_s, DeltaS):
        tmp_delta_s = delta_s.get_data('kJ/mol')[0]
    if isinstance(temperature, Temperature):
        tmp_t = temperature.get_data('K')[0]
    
    return (tmp_ka, tmp_delta_g, tmp_delta_h, tmp_delta_s, tmp_t)

def derive_delta_g(affinity=None, delta_g=None, delta_h=None,
                   delta_s=None, temperature=None):
    """
    Try to derive DeltaG in kJ/mol.

    Stores new instance of :class:`DeltaG` in _derived_delta_g.
    Returns value of dervied delta_g in kJ/mol.

    """
    (affinity,
     delta_g,
     delta_h,
     delta_s,
     temperature) = _get_data_in_standard_units(affinity,
                                                delta_g,
                                                delta_h,
                                                delta_s,
                                                temperature)
    tmp_delta_g = None
    if delta_g:
        tmp_delta_g = delta_g
    elif (delta_h and delta_s):
        tmp_delta_g = delta_h - delta_s
    elif (affinity and temperature):
        # Do delta_g = -r.temperature.ln(Ka)
        tmp_delta_g = -GAS_CONSTANT*temperature*math.log(affinity)
        # Remember to convert to from J/mol to kJ/mol
        tmp_delta_g = tmp_delta_g/1000.0

    if tmp_delta_g:
        return DeltaG(tmp_delta_g, 'kJ/mol')
    return None
    
def derive_affinity(affinity=None, delta_g=None, delta_h=None,
                    delta_s=None, temperature=None):
    """
    Try to derive affinity in /M.

    Stores new instance of :class:`Affinity` /M in _derived_affinity.
    Returns value of dervied affinity in /M.

    """
    (affinity,
     delta_g,
     delta_h,
     delta_s,
     temperature) = _get_data_in_standard_units(affinity,
                                                delta_g,
                                                delta_h,
                                                delta_s,
                                                temperature)
    tmp_affinity = None
    if affinity:
        tmp_affinity = affinity
    elif (delta_g and temperature):
        # Do Ka = e^(-(delta_g/r.temperature))
        delta_g_in_joules = delta_g*1000.0
        gas_temp = GAS_CONSTANT * temperature
        delta_g_div_gas_temp = delta_g_in_joules / gas_temp
        tmp_affinity = math.exp(-delta_g_div_gas_temp)

    if tmp_affinity:
        return Affinity(tmp_affinity, '/M')
    return None

def derive_delta_h(affinity=None, delta_g=None, delta_h=None,
                   delta_s=None, temperature=None):
    """
    Try to derive delta_h in kJ/mol.

    Stores new instance of :class:`DeltaH` kJ/mol in _derived_delta_g.
    Returns value of dervied delta_h in kJ/mol.

    """
    (affinity,
     delta_g,
     delta_h,
     delta_s,
     temperature) = _get_data_in_standard_units(affinity,
                                                delta_g,
                                                delta_h,
                                                delta_s,
                                                temperature)
    tmp_delta_h = None
    if delta_h:
        tmp_delta_h = delta_h
    elif (delta_g and delta_s):
        tmp_delta_h = delta_g + delta_s 

    if tmp_delta_h:
        return DeltaH(tmp_delta_h, 'kJ/mol')
    return None

def derive_delta_s(affinity=None, delta_g=None, delta_h=None,
                   delta_s=None, temperature=None):
    """
    Try to derive delta_s in kJ/mol.

    Stores new instance of :class:`DeltaS` kJ/mol in _derived_delta_s.
    Returns value of dervied delta_s in kJ/mol.

    """
    (affinity,
     delta_g,
     delta_h,
     delta_s,
     temperature) = _get_data_in_standard_units(affinity,
                                                delta_g,
                                                delta_h,
                                                delta_s,
                                                temperature)
    tmp_delta_s = None
    if delta_s:
        tmp_delta_s = delta_s
    elif (delta_g and delta_h):
        tmp_delta_s = delta_h - delta_g 

    if (tmp_delta_s and temperature):
        temperature = Temperature(temperature, 'K')
        return DeltaS(tmp_delta_s, 'kJ/mol', temperature)
    return None

def derive_temperature(affinity=None, delta_g=None, delta_h=None,
                       delta_s=None, temperature=None):
    """
    Try to derive the temperature in K.

    Stores new instance of :class:`Temperature` in _derived_t.
    Returns value of dervied temperature in K.

    """
    (affinity,
     delta_g,
     delta_h,
     delta_s,
     temperature) = _get_data_in_standard_units(affinity,
                                                delta_g,
                                                delta_h,
                                                delta_s,
                                                temperature)
    tmp_t = None
    if temperature:
        tmp_t = temperature
    elif (affinity and delta_g):
        # delta_g = -r.temperature.ln(Ka)
        delta_g_in_joules = delta_g*1000.0
        gas_constant_ln_ka = GAS_CONSTANT*math.log(affinity)
        # temperature = -delta_g/(-r.ln(Ka))
        tmp_t = -delta_g_in_joules/gas_constant_ln_ka

    if tmp_t:
        return Temperature(tmp_t, 'K')
    return None

def check_affinity(affinity):
    """
    Check the quality of the :class:`Affinity` instance.

    >>> from itc import *
    >>> affinity = Affinity(10, 'uM')
    >>> check_affinity(affinity)
    >>> check_affinity(None)
    (1, 'Missing Affinity value')

    """
    warning_msg = None
    if not affinity:
        warning_msg = (MISSING_DATA, 'Missing Affinity value')
    else:
        assert isinstance(affinity, Affinity), "Requires Affinity argument"
        value = affinity.get_data('uM')[0]
        if value < AFFINITY_MIN:
            warning_msg = '''Affinity (%.4f) less than %.4f. It is difficult to
            interpred ITC data if Affinity is less than %.4f as the sigmoidal
            curve becomes too sharp. This can be overcome by performing
            displacement experiments.''' % (value, AFFINITY_MIN, AFFINITY_MIN)
            warning_msg = CLEAN_MSG.sub(' ', warning_msg)
            warning_msg = (DUBIOUS_DATA, warning_msg)
        elif value > AFFINITY_MAX:
            warning_msg = '''Affinity (%.4f) greater than %.4f. It is difficult
            to interpred ITC data if Affinity is greater than %.4f as the
            sigmoidal curve becomes too shallow.''' % (value, AFFINITY_MAX,
            AFFINITY_MAX)
            warning_msg = CLEAN_MSG.sub(' ', warning_msg)
            warning_msg = (DUBIOUS_DATA, warning_msg)
    return warning_msg

def check_delta_g(delta_g):
    """
    Check the quality of the :class:`DeltaG` instance.

    >>> from itc import *
    >>> delta_g = DeltaG(-30, 'kJ/mol')
    >>> check_delta_g(delta_g)
    >>> delta_g = DeltaG(-90, 'kJ/mol')
    >>> check_delta_g(delta_g)
    (3, 'DeltaG (-90.00) less than -60.00. It is difficult to interpred ITC
    data if DeltaG is less than -60.00 as the sigmoidal curve becomes too
    sharp.  This can be overcome by performing displacement experiments.')
    >>> delta_g = DeltaG(-5, 'kJ/mol')
    >>> check_delta_g(delta_g)
    (3, 'DeltaG (-5.00) greater than -20.00. It is difficult to interpred ITC
    data if DeltaG is greater than -20.00 as the sigmoidal curve becomes too
    shallow.')

    """
    warning_msg = None
    if not delta_g:
        warning_msg = (MISSING_DATA, 'Missing DeltaG value')
    else:
        assert isinstance(delta_g, DeltaG), "Requires DeltaH argument"
        value = delta_g.get_data('kJ/mol')[0]
        if value < DELTA_G_MIN:
            warning_msg = '''DeltaG (%.2f) less than %.2f. It is difficult to
            interpred ITC data if DeltaG is less than %.2f as the sigmoidal
            curve becomes too sharp. This can be overcome by performing
            displacement experiments.''' % (value, DELTA_G_MIN, DELTA_G_MIN)
            warning_msg = CLEAN_MSG.sub(' ', warning_msg)
            warning_msg = (DUBIOUS_DATA, warning_msg)
        elif value > DELTA_G_MAX:
            warning_msg = '''DeltaG (%.2f) greater than %.2f. It is difficult
            to interpred ITC data if DeltaG is greater than %.2f as the
            sigmoidal curve becomes too shallow.''' % (value, DELTA_G_MAX,
            DELTA_G_MAX)
            warning_msg = CLEAN_MSG.sub(' ', warning_msg)
            warning_msg = (DUBIOUS_DATA, warning_msg)
    return warning_msg

def check_delta_h(delta_h):
    """
    Check the quality of the :class:`DeltaH` instance.

    >>> from itc import *
    >>> delta_h = DeltaH(-30, 'kJ/mol')
    >>> check_delta_h(delta_h)
    >>> delta_h = DeltaH(-1, 'kJ/mol')
    >>> check_delta_h(delta_h)
    (3, 'DeltaH (-1.00) in range 10.00 to -10.00. It is difficult to interpret
    ITC data as DeltaH approaches 0.')

    """
    warning_msg = None
    if not delta_h:
        warning_msg = (MISSING_DATA, 'Missing DeltaH value')
    else:
        assert isinstance(delta_h, DeltaH), "Requires DeltaH argument"
        value = delta_h.get_data('kJ/mol')[0]
        if (value < DELTA_H_REQ and value > -DELTA_H_REQ):
            warning_msg = '''DeltaH (%.2f) in range %.2f to %.2f. It is
            difficult to interpret ITC data as DeltaH approaches 0.''' % (
            value, DELTA_H_REQ, -DELTA_H_REQ)
            warning_msg = CLEAN_MSG.sub(' ', warning_msg)
            warning_msg = (DUBIOUS_DATA, warning_msg)
    return warning_msg

def check_delta_s(delta_s):
    """
    Check the quality of the :class:`DeltaS` instance.

    >>> from itc import *
    >>> T = Temperature(25, 'C')
    >>> delta_s = DeltaS(10, 'cal/mol/K', T)
    >>> check_delta_s(delta_s)
    >>> check_delta_s(None)
    (1, 'Missing DeltaS value')

    """
    warning_msg = None
    if not delta_s:
        warning_msg = (MISSING_DATA, 'Missing DeltaS value')
    else:
        assert isinstance(delta_s, DeltaS), "Requires DeltaS argument"
    return warning_msg

def check_temperature(temperature):
    """
    Check the quality of the :class:`temperature` instance.

    >>> from itc import *
    >>> temperature = Temperature(25, 'C')
    >>> check_temperature(temperature)
    >>> check_temperature(None)
    (1, 'Missing Temperature value')

    """
    warning_msg = None
    if not temperature:
        warning_msg = (MISSING_DATA, 'Missing Temperature value')
    else:
        assert isinstance(temperature, Temperature), "Requires Temperature"
    return warning_msg

def check_affinity_eqauls_delta_g(affinity, delta_g, temperature):
    """
    Check that DeltaG = -RT.ln(Ka)

    >>> from itc import *
    >>> delta_g = DeltaG(-28.54, 'kJ/mol')
    >>> affinity = Affinity(10.0, 'uM')
    >>> temperature = Temperature(25, 'C')
    >>> check_affinity_eqauls_delta_g(affinity, delta_g, temperature)
    >>> delta_g = DeltaG(-31, 'kJ/mol')
    >>> check_affinity_eqauls_delta_g(affinity, delta_g, temperature)
    (2, 'DeltaG (-31.00) != -R.T.ln(Ka) (-28.54). Tolerance range from -31.31
    to -30.69')

    """
    missing_value = False
    if affinity:
        assert isinstance(affinity, Affinity), "Requires Affinity argument"
    else:
        missing_value = True
    if delta_g:
        assert isinstance(delta_g, DeltaG), "Requires DeltaG argument"
    else:
        missing_value = True
    if temperature:
        assert isinstance(temperature, Temperature), "Requires Temperature"
    else:
        missing_value = True
    if missing_value:
        return None


    delta_g_value = delta_g.get_data('kJ/mol')[0]
    temperature_value = temperature.get_data('K')[0]
    affinity_value = affinity.get_data('/M')[0]
    tolerance = abs(delta_g_value*EQUALITY_ERR_TOL)

    max_dg = delta_g_value + tolerance
    min_dg = delta_g_value - tolerance

    # Do delta_g = -r.temperature.ln(Ka)
    tmp_delta_g = -GAS_CONSTANT*temperature_value*math.log(affinity_value)
    # Remember to convert to from J/mol to kJ/mol
    tmp_delta_g = tmp_delta_g/1000.0
    
    warning_msg = None
    if not (tmp_delta_g < max_dg and tmp_delta_g > min_dg):
        warning_msg = '''DeltaG (%.2f) != -R.T.ln(Ka) (%.2f). Tolerance range
        from %.2f to %.2f''' % (delta_g_value, tmp_delta_g, min_dg, max_dg)
        warning_msg = CLEAN_MSG.sub(' ', warning_msg)
        warning_msg = (INCONSISTENT_DATA, warning_msg)
    return warning_msg

def check_dg_eq_dh_ds(delta_g, delta_h, delta_s):
    """
    Check that DeltaG = DeltaH - T.DeltaS

    >>> delta_g = DeltaG(-28.54, 'kJ/mol')
    >>> delta_h = DeltaH(13.30, 'kJ/mol')
    >>> temperature = Temperature(25, 'C')
    >>> delta_s = DeltaS(41.84, 'kJ/mol', temperature)
    >>> check_dg_eq_dh_ds(delta_g, delta_h, delta_s)
    >>>
    >>> delta_g = DeltaG(-30.00, 'kJ/mol')
    >>> check_dg_eq_dh_ds(delta_g, delta_h, delta_s)
    (2, 'DeltaG (-30.00) != DeltaH (13.30) - T.DeltaS (41.84) (=-28.54).
    Tolerance range from -30.30 to -29.70')

    """
    missing_value = False
    if delta_g:
        assert isinstance(delta_g, DeltaG), "Requires DeltaG argument"
    else:
        missing_value = True
    if delta_h:
        assert isinstance(delta_h, DeltaH), "Requires DeltaH argument"
    else:
        missing_value = True
    if delta_s:
        assert isinstance(delta_s, DeltaS), "Requires DeltaS argument"
    else:
        missing_value = True
    if missing_value:
        return None

    delta_g_value = delta_g.get_data('kJ/mol')[0]
    delta_h_value = delta_h.get_data('kJ/mol')[0]
    delta_s_value = delta_s.get_data('kJ/mol')[0]
    tolerance = abs(delta_g_value*EQUALITY_ERR_TOL)

    max_dg = delta_g_value + tolerance
    min_dg = delta_g_value - tolerance

    # Do delta_g = delta_h - T.delta_s
    tmp_delta_g = delta_h_value - delta_s_value
    
    warning_msg = None
    if not (tmp_delta_g < max_dg and tmp_delta_g > min_dg):
        warning_msg = '''DeltaG (%.2f) != DeltaH (%.2f) - T.DeltaS (%.2f)
        (=%.2f).  Tolerance range from %.2f to %.2f''' % (delta_g_value,
        delta_h_value, delta_s_value, tmp_delta_g, min_dg, max_dg)
        warning_msg = CLEAN_MSG.sub(' ', warning_msg)
        warning_msg = (INCONSISTENT_DATA, warning_msg)
    return warning_msg
 
def run_all_checks(affinity, delta_g, delta_h, delta_s, temperature):
    """
    Run all the data quality checks. Return list of warnings.

    >>> from itc import *
    >>> affinity = Affinity(10.0, 'uM')
    >>> delta_g = DeltaG(-28.54, 'kJ/mol')
    >>> delta_h = DeltaH(13.30, 'kJ/mol')
    >>> delta_s = None
    >>> temperature = Temperature(25, 'C')
    >>> run_all_checks(affinity, delta_g, delta_h, delta_s, temperature)
    [(1, 'Missing DeltaS value')]
    >>> affinity = Affinity(12.0, 'uM')
    >>> run_all_checks(affinity, delta_g, delta_h, delta_s, temperature)
    [(1, 'Missing DeltaS value'), (2, 'DeltaG (-28.54) != -R.T.ln(Ka)
    (-28.09). Tolerance range from -28.83 to -28.25')]

    """
    warnings = []
    warnings.append(check_affinity(affinity))
    warnings.append(check_delta_g(delta_g))
    warnings.append(check_delta_h(delta_h))
    warnings.append(check_delta_s(delta_s))
    warnings.append(check_temperature(temperature))
    warnings.append(check_affinity_eqauls_delta_g(affinity, delta_g,
                                                  temperature))
    warnings.append(check_dg_eq_dh_ds(delta_g, delta_h,
                                                         delta_s))
    warnings = [warning for warning in warnings if warning]
    warnings.sort()
    return warnings

class AbstractThermyodynamicParameter(object):
    """
    Abstract base class for thermodynamic data.
    
    Subclasses are Affinity, Temperature and AbstractDeltaParameter.
    The AbstractdeltaParameter has the subclasses DeltaG, DeltaH and DeltaS.

    All subclasses must implement:
      * _allowed_units - Tuple describing the allowd units
      * _convert_datum - Classmethod for converting raw data into a specified
                         unit. This method should call _check_unit to make
                         sure that the sepcified unit is valid.

    The thermodynamic datum is stored along with its associated unit. However,
    it is possible to get the data out in a different unit.

    """

    _allowed_units = ()
    
    def __init__(self, datum, unit):
        self._datum = float(datum)
        self._check_unit(unit)
        self._unit = unit
    
    def __composite_values__(self):
        return (self._datum, self._unit)

    @classmethod
    def _check_unit(cls, unit):
        """
        Check that the unit exists for the specified class.
        """
        if not unit in cls._allowed_units:
            raise TypeError, "Unknown unit: '%s'" % unit

    def _convert_datum(self, new_unit):
        """
        Abstract function to convert the datum to new_unit.
        """
        pass

    def get_data(self, unit):
        """
        Get datum in specified unit.
        """
        return self._convert_datum(unit)
    
    def get_raw_data(self):
        """
        Get raw data.
        """
        return (self._datum, self._unit)

class Temperature(AbstractThermyodynamicParameter):
    """
    Class for storing and retrieving the temperature.
    
    Supported units are degrees Celcius and Kelvin.

    Methods:
      * get_data     - Return (temperature, unit tuple) in specified unit
      * get_raw_data - Return (temperature, unit tuple) in input unit

    >>> from itc import *
    >>> temp = Temperature(0, 'K')
    >>> '%.2f, %s' % temp.get_data('C')
    '-273.15, C'
    >>> '%.2f, %s' % temp.get_raw_data()
    '0.00, K'

    """

    _allowed_units = ('C', 'K')
    _kelvin_to_celcius_offset = (-273.15)
    
    def _kelvin_to_celcius_converter(self, datum):
        "Convert Kelvin to degrees Celcius"
        return datum + self._kelvin_to_celcius_offset

    def _celcius_to_kelvin_converter(self, datum):
        "Convert degrees Celcius to Kelvin"
        return datum - self._kelvin_to_celcius_offset

    def _convert_datum(self, new_unit='K'):
        """
        Convert temperature scales.
        """
        self._check_unit(new_unit)
        if new_unit == self._unit:
            return (self._datum, self._unit)
        elif new_unit == 'C':
            return (self._kelvin_to_celcius_converter(self._datum), new_unit)
        elif new_unit == 'K':
            return (self._celcius_to_kelvin_converter(self._datum), new_unit)
        else:
            raise TypeError, "Unknown temperature unit: '%s'" % new_unit

class AbstractDeltaParameter(AbstractThermyodynamicParameter):
    """
    Abstract base class for DeltaG, DeltaH and DeltaS.
    """

    _allowed_units = ('kJ/mol', 'J/mol', 'kcal/mol', 'cal/mol')
    _joules_per_calorie = (4.184)
    _kilo = (1000.0)

    def _joules_to_calories_converter(self, datum):
        "Convert Joules to calories"
        return datum/self._joules_per_calorie

    def _calories_to_joules_converter(self, datum):
        "Convert calories to Joules"
        return datum*self._joules_per_calorie

    def _to_kilo_converter(self, datum):
        "Convert to kilo"
        return datum/self._kilo

    def _from_kilo_converter(self, datum):
        "Convert from kilo"
        return datum*self._kilo

    def _convert_joules_and_kilos(self, 
                    new_unit_is_kilo,
                    org_unit_is_kilo,
                    new_unit_is_joules,
                    org_unit_is_joules):
        """
        Convert Joules, calories and kilos

        """
        new_datum = self._datum

        # To and from kilo conversion
        if new_unit_is_kilo == org_unit_is_kilo:
            pass
        elif new_unit_is_kilo:
            new_datum = self._to_kilo_converter(new_datum)
        else:
            new_datum = self._from_kilo_converter(new_datum)

        # To and from Joules and calories conversion
        if new_unit_is_joules == org_unit_is_joules:
            pass
        elif new_unit_is_joules:
            new_datum = self._calories_to_joules_converter(new_datum)
        else:
            new_datum = self._joules_to_calories_converter(new_datum)

        return new_datum

    def _convert_datum(self, new_unit):
        """
        Convert thermodynamic units.
        """
        self._check_unit(new_unit)
        new_unit_is_kilo = new_unit.startswith('k')
        org_unit_is_kilo = self._unit.startswith('k')
        new_unit_is_joules = new_unit.endswith('J/mol')
        org_unit_is_joules = self._unit.endswith('J/mol')
        new_value = self._convert_joules_and_kilos(new_unit_is_kilo,
                                     org_unit_is_kilo,
                                     new_unit_is_joules,
                                     org_unit_is_joules)
        return (new_value, new_unit)

class DeltaG(AbstractDeltaParameter):
    """
    Class for storing and retrieving the Delta G in various units.

    Units:
      * kJ/mol
      * J/mol
      * kcal/mol
      * cal/mol

    Methods:
     * get_data - Return (Deta G, unit) tuple in specified unit
     * get_raw_data - Return (Deta G, unit) tuple in input unit

    >>> from itc import *
    >>> delta_g = DeltaG(-30, 'kJ/mol')
    >>> '%.2f, %s' % delta_g.get_data('kcal/mol')
    '-7.17, kcal/mol'
    >>> '%.2f, %s' % delta_g.get_raw_data()
    '-30.00, kJ/mol'

    """
    pass

class DeltaH(AbstractDeltaParameter):
    """
    Class for storing and retrieving the Delta H in various units.

    Units:
      * kJ/mol
      * J/mol
      * kcal/mol
      * cal/mol

    Methods:
      * get_data - Return (Deta H, unit) tuple in specified unit
      * get_raw_data - Return (Deta H, unit) tuple in input unit

    Examples:
      >>> from itc import *
      >>> delta_h = DeltaH(65, 'cal/mol')
      >>> '%.2f, %s' % delta_h.get_data('kJ/mol')
      '0.27, kJ/mol'
      >>> '%.2f, %s' % delta_h.get_raw_data()
      '65.00, cal/mol'

    """
    pass

class DeltaS(AbstractDeltaParameter):
    """
    Class for storing and retrieving the Delta S in various units.
    
    Units:
      * kJ/mol
      * J/mol
      * kcal/mol
      * cal/mol
      * -kJ/mol
      * -J/mol
      * -kcal/mol
      * -cal/mol
      * kJ/mol/K
      * J/mol/K
      * kcal/mol/K
      * cal/mol/K
      * -kJ/mol/K
      * -J/mol/K
      * -kcal/mol/K
      * -cal/mol/K

    Methods:
      get_data - Return (Deta S, unit) tuple in specified unit
      get_raw_data - Return (Deta S, unit) tuple in input unit

    Examples:
      >>> from itc import *
      >>> T = Temperature(25, 'C')
      >>> delta_s = DeltaS(10, 'cal/mol/K', T)
      >>> '%.2f, %s' % delta_s.get_data('kJ/mol')
      '12.47, kJ/mol'
      >>> '%.2f, %s' % delta_s.get_raw_data()
      '10.00, cal/mol/K'

    
    """
    _allowed_units = (
        'kJ/mol',
        'J/mol',
        'kcal/mol',
        'cal/mol',
        '-kJ/mol',
        '-J/mol',
        '-kcal/mol',
        '-cal/mol',
        'kJ/mol/K',
        'J/mol/K',
        'kcal/mol/K',
        'cal/mol/K',
        '-kJ/mol/K',
        '-J/mol/K',
        '-kcal/mol/K',
        '-cal/mol/K')

    def __init__(self, datum, unit, temperature):
        AbstractDeltaParameter.__init__(self, datum, unit)
        if isinstance(temperature, Temperature):
            self._temperature = temperature.get_data('K')[0]
        elif isinstance(temperature, float):
            self._temperature = temperature
        else:
            raise TypeError, "Incorrect temperature type %r" % temperature
        
    def _add_temperature(self, value):
        "Add temperature to change in entropy value"
        return value/self._temperature
  
    def _remove_temperature(self, value):
        "Remove temperature from change in entropy value"
        return value*self._temperature

    def _convert_datum(self, new_unit):
        """
        Convert change in entropy units.
        """
        new_unit_is_kilo = False
        if new_unit.find('k') != -1:
            new_unit_is_kilo = True
        org_unit_is_kilo = False
        if self._unit.find('k') != -1:
            org_unit_is_kilo = True
        new_unit_is_negative = new_unit.startswith('-')
        org_unit_is_negative = self._unit.startswith('-')
        new_unit_has_temperature = new_unit.endswith('/K')
        org_unit_has_temperature = self._unit.endswith('/K')
        new_unit_is_joules = False
        if new_unit.find('cal') == -1:
            new_unit_is_joules = True
        org_unit_is_joules = False
        if self._unit.find('cal') == -1:
            org_unit_is_joules = True

        # Perfrom any kilo, Joules and/or calorie conversions
        new_value = self._convert_joules_and_kilos(new_unit_is_kilo,
                                     org_unit_is_kilo,
                                     new_unit_is_joules,
                                     org_unit_is_joules)

        # Make any corrections for temperature
        if new_unit_has_temperature == org_unit_has_temperature:
            pass
        elif new_unit_has_temperature:
            new_value = self._add_temperature(new_value)
        else:
            new_value = self._remove_temperature(new_value)
        
        # Deal with any change in sign
        if new_unit_is_negative != org_unit_is_negative:
            new_value = -new_value

        return (new_value, new_unit)

class DeltaCp(AbstractDeltaParameter):
    """
    Class for storing and retrieving the Delta Cp in various units.

    Units:
      * kJ/mol/K
      * J/mol/K
      * kcal/mol/K
      * cal/mol/K

    Methods:
      get_data     - Return (Deta Cp, unit) tuple in specified unit
      get_raw_data - Return (Deta Cp, unit) tuple in input unit

    Examples:
      >>> from itc import *
      >>> delta_cp = DeltaCp(10, 'kcal/mol/K')
      >>> '%.2f, %s' % delta_cp.get_data('kJ/mol/K')
      '41.84, kJ/mol/K'
      >>> '%.2f, %s' % delta_cp.get_raw_data()
      '10.00, kcal/mol/K'

    
    """
    _allowed_units = ('kJ/mol/K', 'J/mol/K', 'kcal/mol/K', 'cal/mol/K')

    def _convert_datum(self, new_unit):
        """
        Convert thermodynamic units.
        """
        self._check_unit(new_unit)
        new_unit_is_kilo = new_unit.startswith('k')
        org_unit_is_kilo = self._unit.startswith('k')
        new_unit_is_joules = new_unit.endswith('J/mol/K')
        org_unit_is_joules = self._unit.endswith('J/mol/K')
        new_value = self._convert_joules_and_kilos(new_unit_is_kilo,
                                     org_unit_is_kilo,
                                     new_unit_is_joules,
                                     org_unit_is_joules)
        return (new_value, new_unit)

class Affinity(AbstractThermyodynamicParameter):
    """
    Class for storing affinities in various units.

    Units:
      * M
      * mM
      * uM
      * nM
      * pM
      * /M

    Examples:
      >>> from itc import *
      >>> affinity = Affinity(10, 'uM')
      >>> '%.3f, %s' % affinity.get_data('mM')
      '0.010, mM'
      >>> '%.2f, %s' % affinity.get_raw_data()
      '10.00, uM'

    """

    _allowed_units = ('M', 'mM', 'uM', 'nM', 'pM', '/M')
    _kilo = (1000)


    def _to_molar(self):
        """
        Convert value to M
        """
        if self._unit == 'M':
            return self._datum
        elif self._unit == 'mM':
            return self._datum / self._kilo
        elif self._unit == 'uM':
            return self._datum / (self._kilo*self._kilo)
        elif self._unit == 'nM':
            return self._datum / (self._kilo*self._kilo*self._kilo)
        elif self._unit == 'pM':
            return self._datum / (self._kilo*self._kilo*self._kilo*self._kilo)
        elif self._unit == '/M':
            return 1/self._datum

    def _to_new_unit(self, new_unit):
        """
        Return affinity in a different unit.
        """
        new_value = self._to_molar()

        if new_unit == 'M':
            pass
        elif new_unit == 'mM':
            new_value = new_value * self._kilo
        elif new_unit == 'uM':
            new_value = new_value * (self._kilo*self._kilo)
        elif new_unit == 'nM':
            new_value = new_value * (self._kilo*self._kilo*self._kilo)
        elif new_unit == 'pM':
            new_value = new_value * (self._kilo*self._kilo
                                     *self._kilo*self._kilo)
        elif new_unit == '/M':
            if self._unit == '/M':
                new_value = self._datum
            else:
                new_value = 1/new_value
        
        return new_value

    def _convert_datum(self, new_unit):
        """
        Convert affinity value.
        """
        self._check_unit(new_unit)
        new_value = self._to_new_unit(new_unit)
        return (new_value, new_unit)

class TemperatureErr(Temperature):
    """
    Experimental error in Temperature.
    """
    pass

class DeltaGExpErr(DeltaG):
    """
    Experimental error in Delta G.
    """
    pass

class DeltaHExpErr(DeltaH):
    """
    Experimental error in Delta H.
    """
    pass

class DeltaSExpErr(DeltaS):
    """
    Experimental error in Delta S.
    """
    pass

class DeltaCpExpErr(DeltaCp):
    "Experimental error in Delta Cp"
    pass

class AffinityExpErr(Affinity):
    """
    Experimental error in Affinity.
    """
    pass

class ITCData(object):
    """
    Class for storing and manipulating ITC data.

    Standardised data is:
      * Affinity    - uM
      * DeltaG      - kJ/mol
      * DeltaH      - kJ/mol
      * DeltaS      - kJ/mol (so that DeltaG = DeltaH - DeltaS)
      * Temperature - K

    Examples:
      >>> from itc import *
      >>> affinity = Affinity(10.0, 'uM')
      >>> temperature = Temperature(25, 'C')
      >>> delta_s = DeltaS(10.0, 'kJ/mol', temperature)
      >>> itc_data = ITCData(affinity=affinity,
      ...                    delta_s=delta_s, temperature=temperature)
      >>> print itc_data
      <ITCData(Kd=10.000, DG=-28.54, DH=-18.54, TDS=10.00, T=298.15)>
      >>>
      >>> delta_g = DeltaG(-28.54, 'kJ/mol')
      >>> itc_data = ITCData(delta_g=delta_g,
      ...                    delta_s=delta_s, temperature=temperature)
      >>> print itc_data
      <ITCData(Kd=10.000, DG=-28.54, DH=-18.54, TDS=10.00, T=298.15)>
      >>>
      >>> delta_h = DeltaH(-18.54, 'kJ/mol')
      >>> itc_data = ITCData(delta_g=delta_g,
      ...                    delta_h=delta_h, temperature=temperature)
      >>> print itc_data
      <ITCData(Kd=10.000, DG=-28.54, DH=-18.54, TDS=10.00, T=298.15)>

    """

    def __init__(self,
                 affinity=None,
                 delta_g=None,
                 delta_h=None,
                 delta_s=None,
                 stoich_param=None,
                 temperature=None,
                 affinity_exp_err=None,
                 delta_g_exp_err=None,
                 delta_h_exp_err=None,
                 delta_s_exp_err=None,
                 stoich_param_exp_err=None,
                 temperature_exp_err=None):
        """
        Initialise an instance of the class
        """

        # Experimental data
        self._stoich_param = stoich_param
        self._stoich_param_exp_err = stoich_param_exp_err

        self._raw_affinity = affinity
        self._raw_delta_g = delta_g
        self._raw_delta_h = delta_h
        self._raw_delta_s = delta_s
        self._raw_t = temperature

        self._raw_affinity_exp_err = affinity_exp_err
        self._raw_delta_g_exp_err = delta_g_exp_err
        self._raw_delta_h_exp_err = delta_h_exp_err
        self._raw_delta_s_exp_err = delta_s_exp_err
        self._raw_t_exp_err = temperature_exp_err

        # Derived data
        self._derived_affinity = None
        self._derived_delta_g = None
        self._derived_delta_h = None
        self._derived_delta_s = None
        self._derived_t = None

        self._derived_affinity_exp_err = None
        self._derived_delta_g_exp_err = None
        self._derived_delta_h_exp_err = None
        self._derived_delta_s_exp_err = None
        self._derived_t_exp_err = None

        # Process data
        self._standardise_data()
        self._propagate_errors()

        # Data quality
        self._data_quality_warnings = []
        self._check_data_quality()

    def __repr__(self):
        affinity = 'NA'
        delta_g = 'NA'
        delta_h = 'NA'
        delta_s = 'NA'
        temperature = 'NA'
        if isinstance(self._derived_affinity, Affinity):
            affinity = '%.3f' % self._derived_affinity.get_data('uM')[0]
        if isinstance(self._derived_delta_g, DeltaG):
            delta_g = '%.2f' % self._derived_delta_g.get_data('kJ/mol')[0]
        if isinstance(self._derived_delta_h, DeltaH):
            delta_h = '%.2f' % self._derived_delta_h.get_data('kJ/mol')[0]
        if isinstance(self._derived_delta_s, DeltaS):
            delta_s = '%.2f' % self._derived_delta_s.get_data('kJ/mol')[0]
        if isinstance(self._derived_t, Temperature):
            temperature = '%.2f' % self._derived_t.get_data('K')[0]
        return "<ITCData(Kd=%s, DG=%s, DH=%s, TDS=%s, T=%s)>" % (
            affinity, delta_g, delta_h, delta_s, temperature)

    def _standardise_data(self):
        """
        Standardise units and generate missing data.
        """

        tmp_delta_g = self._raw_delta_g
        tmp_ka = self._raw_affinity
        tmp_delta_h = self._raw_delta_h
        tmp_delta_s = self._raw_delta_s
        tmp_t = self._raw_t

        tmp_delta_g = derive_delta_g(tmp_ka, tmp_delta_g, tmp_delta_h,
                                     tmp_delta_s, tmp_t)
        tmp_ka = derive_affinity(tmp_ka, tmp_delta_g, tmp_delta_h,
                                 tmp_delta_s, tmp_t)
        tmp_t = derive_temperature(tmp_ka, tmp_delta_g, tmp_delta_h,
                                   tmp_delta_s, tmp_t)
        tmp_delta_h = derive_delta_h(tmp_ka, tmp_delta_g, tmp_delta_h,
                                     tmp_delta_s, tmp_t)
        tmp_delta_s = derive_delta_s(tmp_ka, tmp_delta_g, tmp_delta_h,
                                     tmp_delta_s, tmp_t)

        self._derived_delta_g = tmp_delta_g
        self._derived_affinity = tmp_ka
        self._derived_delta_h = tmp_delta_h
        self._derived_delta_s = tmp_delta_s
        self._derived_t = tmp_t

    def _check_data_quality(self):
        """
        Check the quality of the ITC data.
        """
        warnings = run_all_checks(self._derived_affinity,
                                  self._derived_delta_g,
                                  self._derived_delta_h,
                                  self._derived_delta_s,
                                  self._derived_t)
        self._data_quality_warnings = warnings


    def _propagate_errors(self):
        """
        Propagate any reported errors to other thermodynamic parameters.

        Not yet implemented.
        """
        self._derived_affinity_exp_err = self._raw_affinity_exp_err
        self._derived_delta_g_exp_err = self._raw_delta_g_exp_err
        self._derived_delta_h_exp_err = self._raw_delta_h_exp_err
        self._derived_delta_s_exp_err = self._raw_delta_s_exp_err
        self._derived_t_exp_err = self._raw_t_exp_err

    @property
    def stoich_param(self):
        """
        Return affinity in uM.
        """
        return self._stoich_param

    @property
    def stoich_param_exp_err(self):
        """
        Return affinity in uM.
        """
        return self._stoich_param_exp_err

    @property
    def affinity(self):
        """
        Return affinity in uM.
        """
        value = None
        unit = 'uM'
        if self._derived_affinity:
            value = self._derived_affinity.get_data(unit)[0]
        return value

    @property
    def affinity_exp_err(self):
        """
        Return affinity error in uM.
        """
        value = None
        unit = 'uM'
        if self._derived_affinity_exp_err:
            value = self._derived_affinity_exp_err.get_data(unit)[0]
        return value

    @property
    def affinity_unit(self):
        """
        Return affinity unit in uM.
        """
        unit = 'uM'
        return unit
        
    @property
    def delta_g(self):
        """
        Return delta_g in kJ/mol.
        """
        value = None
        unit = 'kJ/mol'
        if self._derived_delta_g:
            value = self._derived_delta_g.get_data(unit)[0]
        return value

    @property
    def delta_g_exp_err(self):
        """
        Return delta_g error in kJ/mol.
        """
        value = None
        unit = 'kJ/mol'
        if self._derived_delta_g_exp_err:
            value = self._derived_delta_g_exp_err.get_data(unit)[0]
        return value

    @property
    def delta_g_unit(self):
        """
        Return delta_g unit in kJ/mol.
        """
        unit = 'kJ/mol'
        return unit

    @property
    def delta_h(self):
        """
        Return delta_h unit in kJ/mol.
        """
        value = None
        unit = 'kJ/mol'
        if self._derived_delta_h:
            value = self._derived_delta_h.get_data(unit)[0]
        return value

    @property
    def delta_h_exp_err(self):
        """
        Return delta_h error in kJ/mol.
        """
        value = None
        unit = 'kJ/mol'
        if self._derived_delta_h_exp_err:
            value = self._derived_delta_h_exp_err.get_data(unit)[0]
        return value

    @property
    def delta_h_unit(self):
        """
        Return delta_h unit in kJ/mol.
        """
        unit = 'kJ/mol'
        return unit

    @property
    def delta_s(self):
        """
        Return delta_s in kJ/mol.
        """
        value = None
        unit = 'kJ/mol'
        if self._derived_delta_s:
            value = self._derived_delta_s.get_data(unit)[0]
        return value

    @property
    def delta_s_exp_err(self):
        """
        Return delta_s error in kJ/mol.
        """
        value = None
        unit = 'kJ/mol'
        if self._derived_delta_s_exp_err:
            value = self._derived_delta_s_exp_err.get_data(unit)[0]
        return value

    @property
    def delta_s_unit(self):
        """
        Return delta_s unit in kJ/mol.
        """
        unit = 'kJ/mol'
        return unit

    @property
    def temperature(self):
        """
        Return temperature in K.
        """
        value = None
        unit = 'K'
        if self._derived_t:
            value = self._derived_t.get_data(unit)[0]
        return value

    @property
    def temperature_exp_err(self):
        """
        Return temperature error in K.
        """
        value = None
        unit = 'K'
        if self._derived_t_exp_err:
            value = self._derived_t_exp_err.get_data(unit)[0]
        return value

    @property
    def temperature_unit(self):
        """
        Return temperature unit in K.
        """
        unit = 'K'
        return unit

    @property
    def affinity_raw(self):
        """
        Return affinity in uM.
        """
        value = None
        if self._raw_affinity:
            value = self._raw_affinity.get_raw_data()[0]
        return value

    @property
    def affinity_exp_err_raw(self):
        """
        Return affinity error in uM.
        """
        value = None
        if self._raw_affinity_exp_err:
            value = self._raw_affinity_exp_err.get_raw_data()[0]
        return value

    @property
    def affinity_unit_raw(self):
        """
        Return affinity unit in uM.
        """
        value = None
        if self._raw_affinity:
            value = self._raw_affinity.get_raw_data()[1]
        return value
        
    @property
    def delta_g_raw(self):
        """
        Return delta_g in kJ/mol.
        """
        value = None
        unit = 'kJ/mol'
        if self._raw_delta_g:
            value = self._raw_delta_g.get_raw_data()[0]
        return value

    @property
    def delta_g_exp_err_raw(self):
        """
        Return delta_g error in kJ/mol.
        """
        value = None
        unit = 'kJ/mol'
        if self._raw_delta_g_exp_err:
            value = self._raw_delta_g_exp_err.get_raw_data()[0]
        return value

    @property
    def delta_g_unit_raw(self):
        """
        Return delta_g unit in kJ/mol.
        """
        value = None
        if self._raw_delta_g:
            value = self._raw_delta_g.get_raw_data()[1]
        return value

    @property
    def delta_h_raw(self):
        """
        Return delta_h unit in kJ/mol.
        """
        value = None
        unit = 'kJ/mol'
        if self._raw_delta_h:
            value = self._raw_delta_h.get_raw_data()[0]
        return value

    @property
    def delta_h_exp_err_raw(self):
        """
        Return delta_h error in kJ/mol.
        """
        value = None
        unit = 'kJ/mol'
        if self._raw_delta_h_exp_err:
            value = self._raw_delta_h_exp_err.get_raw_data()[0]
        return value

    @property
    def delta_h_unit_raw(self):
        """
        Return delta_h unit in kJ/mol.
        """
        value = None
        if self._raw_delta_h:
            value = self._raw_delta_h.get_raw_data()[1]
        return value

    @property
    def delta_s_raw(self):
        """
        Return delta_s in kJ/mol.
        """
        value = None
        unit = 'kJ/mol'
        if self._raw_delta_s:
            value = self._raw_delta_s.get_raw_data()[0]
        return value

    @property
    def delta_s_exp_err_raw(self):
        """
        Return delta_s error in kJ/mol.
        """
        value = None
        unit = 'kJ/mol'
        if self._raw_delta_s_exp_err:
            value = self._raw_delta_s_exp_err.get_raw_data()[0]
        return value

    @property
    def delta_s_unit_raw(self):
        """
        Return delta_s unit in kJ/mol.
        """
        value = None
        if self._raw_delta_s:
            value = self._raw_delta_s.get_raw_data()[1]
        return value

    @property
    def temperature_raw(self):
        """
        Return temperature in K.
        """
        value = None
        unit = 'K'
        if self._raw_t:
            value = self._raw_t.get_raw_data()[0]
        return value

    @property
    def temperature_exp_err_raw(self):
        """
        Return temperature error in K.
        """
        value = None
        unit = 'K'
        if self._raw_t_exp_err:
            value = self._raw_t_exp_err.get_raw_data()[0]
        return value

    @property
    def temperature_unit_raw(self):
        """
        Return temperature unit in K.
        """
        value = None
        if self._raw_t:
            value = self._raw_t.get_raw_data()[1]
        return value

    @property
    def data_quality_warnings(self):
        """
        Return list of data quality warnings.
        """
        return self._data_quality_warnings

class ITC(object):
    """
    ITC class.

    Contains thermodynamic data extracted from ITCData.

    Also contains references to:
      * protein
      * ligand
      * citation
      * itc instrument

    """

    def __init__(self,
                 itc_data,
                 protein=None,
                 ligand=None,
                 citation=None,
                 instrument=None,
                 buffer=None,
                 comments=None,
                 itc_delta_cp=None,
                 ph=None,
                 cell_content=None,
                 protonation_state_examined=None,
                 interaction_type=None):
        """
        Initialise an instance of the class
        """
        # Protein and ligand
        self._protein = protein
        self._ligand = ligand
        self._citation = citation
        self._instrument = instrument
        self._buffer = buffer
        if not comments:
            self._comments = []
        else:
            self._comments = comments
        self._itc_delta_cp = itc_delta_cp
        self._ph = ph
        self._cell_content = cell_content
        self._protonation_state_examined = protonation_state_examined
        self._interaction_type = interaction_type

        # Set the rest
        self._stoich_param = itc_data.stoich_param
        self._stoich_param_exp_err = itc_data.stoich_param_exp_err

        self._affinity = itc_data.affinity
        self._delta_g = itc_data.delta_g
        self._delta_h = itc_data.delta_h
        self._delta_s = itc_data.delta_s
        self._temperature = itc_data.temperature

        self._affinity_exp_err = itc_data.affinity_exp_err
        self._delta_g_exp_err = itc_data.delta_g_exp_err
        self._delta_h_exp_err = itc_data.delta_h_exp_err
        self._delta_s_exp_err = itc_data.delta_s_exp_err
        self._temperature_exp_err = itc_data.temperature_exp_err

        self._affinity_unit = itc_data.affinity_unit
        self._delta_g_unit = itc_data.delta_g_unit
        self._delta_h_unit = itc_data.delta_h_unit
        self._delta_s_unit = itc_data.delta_s_unit
        self._temperature_unit = itc_data.temperature_unit

        self._affinity_raw = itc_data.affinity_raw
        self._delta_g_raw = itc_data.delta_g_raw
        self._delta_h_raw = itc_data.delta_h_raw
        self._delta_s_raw = itc_data.delta_s_raw
        self._temperature_raw = itc_data.temperature_raw

        self._affinity_exp_err_raw = itc_data.affinity_exp_err_raw
        self._delta_g_exp_err_raw = itc_data.delta_g_exp_err_raw
        self._delta_h_exp_err_raw = itc_data.delta_h_exp_err_raw
        self._delta_s_exp_err_raw = itc_data.delta_s_exp_err_raw
        self._temperature_exp_err_raw = itc_data.temperature_exp_err_raw

        self._affinity_unit_raw = itc_data.affinity_unit_raw
        self._delta_g_unit_raw = itc_data.delta_g_unit_raw
        self._delta_h_unit_raw = itc_data.delta_h_unit_raw
        self._delta_s_unit_raw = itc_data.delta_s_unit_raw
        self._temperature_unit_raw = itc_data.temperature_unit_raw

    def __repr__(self):
        affinity = 'NA'
        delta_g = 'NA'
        delta_h = 'NA'
        delta_s = 'NA'
        temperature = 'NA'
        if isinstance(self._affinity, float):
            affinity = '%.3f' % self._affinity
        if isinstance(self._delta_g, float):
            delta_g = '%.2f' % self._delta_g
        if isinstance(self._delta_h, float):
            delta_h = '%.2f' % self._delta_h
        if isinstance(self._delta_s, float):
            delta_s = '%.2f' % self._delta_s
        if isinstance(self._temperature, float):
            temperature = '%.2f' % self._temperature
        return "<ITC(Kd=%s, DG=%s, DH=%s, TDS=%s, T=%s)>" % (
            affinity, delta_g, delta_h, delta_s, temperature)

    
    @property
    def ligand(self):
        """
        Return ligand.
        """
        return self._ligand

    @property
    def protein(self):
        """
        Return protein.
        """
        return self._protein

    @property
    def citation(self):
        """
        Return citation.
        """
        return self._citation

    @property
    def instrument(self):
        """
        Return instrument.
        """
        return self._instrument
    @property
    def interaction_type(self):
        """
        Return interaction type.
        """
        return self._interaction_type
    
    @property
    def comments(self):
        """
        Return comments.
        """
        return self._comments
    
    @property
    def buffer(self):
        """
        Return buffer.
        """
        return self._buffer
    
    @property
    def stoich_param(self):
        """
        Return affinity in uM.
        """
        return self._stoich_param

    @property
    def stoich_param_exp_err(self):
        """
        Return affinity in uM.
        """
        return self._stoich_param_exp_err

    @property
    def affinity(self):
        """
        Return affinity.
        """
        return self._affinity

    @property
    def delta_g(self):
        """
        Return delta_g.
        """
        return self._delta_g

    @property
    def delta_h(self):
        """
        Return delta_h.
        """
        return self._delta_h

    @property
    def delta_s(self):
        """
        Return delta_s.
        """
        return self._delta_s

    @property
    def delta_cp(self):
        """
        Return delta_cp.
        """
        if self._itc_delta_cp:
            return self._itc_delta_cp.delta_cp
        else:
            return None

    @property
    def temperature(self):
        """
        Return temperature.
        """
        return self._temperature


    @property
    def affinity_exp_err(self):
        """
        Return affinity exp_err.
        """
        return self._affinity_exp_err

    @property
    def delta_g_exp_err(self):
        """
        Return delta_g_exp_err.
        """
        return self._delta_g_exp_err

    @property
    def delta_h_exp_err(self):
        """
        Return delta_h_exp_err.
        """
        return self._delta_h_exp_err

    @property
    def delta_s_exp_err(self):
        """
        Return delta_s_exp_err.
        """
        return self._delta_s_exp_err

    @property
    def delta_cp_exp_err(self):
        """
        Return delta_cp_exp_err.
        """
        if self._itc_delta_cp:
            return self._itc_delta_cp.delta_cp_exp_err
        else:
            return None

    @property
    def temperature_exp_err(self):
        """
        Return temperature_exp_err.
        """
        return self._temperature_exp_err

    @property
    def affinity_unit(self):
        """
        Return affinity unit.
        """
        return self._affinity_unit

    @property
    def delta_g_unit(self):
        """
        Return delta_g_unit.
        """
        return self._delta_g_unit

    @property
    def delta_h_unit(self):
        """
        Return delta_h_unit.
        """
        return self._delta_h_unit

    @property
    def delta_s_unit(self):
        """
        Return delta_s_unit.
        """
        return self._delta_s_unit

    @property
    def delta_cp_unit(self):
        """
        Return delta_cp_unit.
        """
        if self._itc_delta_cp:
            return self._itc_delta_cp.delta_cp_unit
        else:
            return None

    @property
    def temperature_unit(self):
        """
        Return temperature_unit.
        """
        return self._temperature_unit

    @property
    def affinity_raw(self):
        """
        Return affinity_raw.
        """
        return self._affinity_raw

    @property
    def delta_g_raw(self):
        """
        Return delta_g_raw.
        """
        return self._delta_g_raw

    @property
    def delta_h_raw(self):
        """
        Return delta_h_raw.
        """
        return self._delta_h_raw

    @property
    def delta_s_raw(self):
        """
        Return delta_s_raw.
        """
        return self._delta_s_raw

    @property
    def delta_cp_raw(self):
        """
        Return delta_cp_raw.
        """
        if self._itc_delta_cp:
            return self._itc_delta_cp.delta_cp_raw
        else:
            return None

    @property
    def temperature_raw(self):
        """
        Return temperature_raw.
        """
        return self._temperature_raw


    @property
    def affinity_exp_err_raw(self):
        """
        Return affinity exp_err_raw.
        """
        return self._affinity_exp_err_raw

    @property
    def delta_g_exp_err_raw(self):
        """
        Return delta_g_exp_err_raw.
        """
        return self._delta_g_exp_err_raw

    @property
    def delta_h_exp_err_raw(self):
        """
        Return delta_h_exp_err_raw.
        """
        return self._delta_h_exp_err_raw

    @property
    def delta_s_exp_err_raw(self):
        """
        Return delta_s_exp_err_raw.
        """
        return self._delta_s_exp_err_raw

    @property
    def delta_cp_exp_err_raw(self):
        """
        Return delta_cp_exp_err_raw.
        """
        if self._itc_delta_cp:
            return self._itc_delta_cp.delta_cp_exp_err_raw
        else:
            return None

    @property
    def temperature_exp_err_raw(self):
        """
        Return temperature_exp_err_raw.
        """
        return self._temperature_exp_err_raw

    @property
    def affinity_unit_raw(self):
        """
        Return affinity unit_raw.
        """
        return self._affinity_unit_raw

    @property
    def delta_g_unit_raw(self):
        """
        Return delta_g_unit_raw.
        """
        return self._delta_g_unit_raw

    @property
    def delta_h_unit_raw(self):
        """
        Return delta_h_unit_raw.
        """
        return self._delta_h_unit_raw

    @property
    def delta_s_unit_raw(self):
        """
        Return delta_s_unit_raw.
        """
        return self._delta_s_unit_raw

    @property
    def delta_cp_unit_raw(self):
        """
        Return delta_cp_unit_raw.
        """
        if self._itc_delta_cp:
            return self._itc_delta_cp.delta_cp_unit_raw
        else:
            return None

    @property
    def temperature_unit_raw(self):
        """
        Return temperature_unit_raw.
        """
        return self._temperature_unit_raw


    def copy(self, other):
        """
        Copy values from another instance of the ITC class.
        """
        # Protein and ligand
        self._protein = other.protein
        self._ligand = other.ligand
        self._citation = other.citation
        self._instrument = other.instrument
        self._buffer = other.buffer
        self._comments = other.comments
        self._itc_delta_cp = other._itc_delta_cp
        self._ph = other.ph
        self._cell_content = other.cell_content
        self._protonation_state_examined = other.protonation_state_examined
        self._interaction_type = other.interaction_type

        # Set the rest
        self._stoich_param = other.stoich_param
        self._stoich_param_exp_err = other.stoich_param_exp_err

        self._affinity = other.affinity
        self._delta_g = other.delta_g
        self._delta_h = other.delta_h
        self._delta_s = other.delta_s
        self._temperature = other.temperature

        self._affinity_exp_err = other.affinity_exp_err
        self._delta_g_exp_err = other.delta_g_exp_err
        self._delta_h_exp_err = other.delta_h_exp_err
        self._delta_s_exp_err = other.delta_s_exp_err
        self._temperature_exp_err = other.temperature_exp_err

        self._affinity_unit = other.affinity_unit
        self._delta_g_unit = other.delta_g_unit
        self._delta_h_unit = other.delta_h_unit
        self._delta_s_unit = other.delta_s_unit
        self._temperature_unit = other.temperature_unit

        self._affinity_raw = other.affinity_raw
        self._delta_g_raw = other.delta_g_raw
        self._delta_h_raw = other.delta_h_raw
        self._delta_s_raw = other.delta_s_raw
        self._temperature_raw = other.temperature_raw

        self._affinity_exp_err_raw = other.affinity_exp_err_raw
        self._delta_g_exp_err_raw = other.delta_g_exp_err_raw
        self._delta_h_exp_err_raw = other.delta_h_exp_err_raw
        self._delta_s_exp_err_raw = other.delta_s_exp_err_raw
        self._temperature_exp_err_raw = other.temperature_exp_err_raw

        self._affinity_unit_raw = other.affinity_unit_raw
        self._delta_g_unit_raw = other.delta_g_unit_raw
        self._delta_h_unit_raw = other.delta_h_unit_raw
        self._delta_s_unit_raw = other.delta_s_unit_raw
        self._temperature_unit_raw = other.temperature_unit_raw

class ITCDeltaCp(object):
    """
    Class for storing heat capacity data.

    """

    def __init__(self,
                 delta_cp,
                 delta_cp_exp_err=None,
                 protein=None,
                 ligand=None,
                 citation=None,
                 buffer=None,
                 ph=None):
        self._delta_cp_unit = 'kJ/mol/K'
        self._delta_cp = delta_cp.get_data(self._delta_cp_unit)[0]
        self._delta_cp_raw = delta_cp.get_raw_data()[0]
        self._delta_cp_unit_raw = delta_cp.get_raw_data()[1]
        self._delta_cp_exp_err = None
        self._delta_cp_exp_err_raw = None
        if delta_cp_exp_err:
            self._delta_cp_exp_err = delta_cp_exp_err.get_data('kJ/mol/K')[0]
            self._delta_cp_exp_err_raw = delta_cp_exp_err.get_raw_data()[0]
        self._protein = protein
        self._ligand = ligand
        self._citation = citation
        self._buffer = buffer
        self._ph = ph

    def __repr__(self):
        return "<ITCDeltaCp(DCp=%.2f)>" % self._delta_cp

    @property
    def delta_cp(self):
        """
        Return delta_cp.
        """
        return self._delta_cp

    @property
    def delta_cp_exp_err(self):
        """
        Return delta_cp experimental error.
        """
        return self._delta_cp_exp_err

    @property
    def delta_cp_unit(self):
        """
        Return delta_cp unit.
        """
        return self._delta_cp_unit

    @property
    def delta_cp_raw(self):
        """
        Return delta_cp_raw.
        """
        return self._delta_cp_raw

    @property
    def delta_cp_exp_err_raw(self):
        """
        Return delta_cp experimental error raw.
        """
        return self._delta_cp_exp_err_raw

    @property
    def delta_cp_unit_raw(self):
        """
        Return delta_cp unit raw.
        """
        return self._delta_cp_unit_raw


    @property
    def protein(self):
        """
        Return protein.
        """
        return self._protein

    @property
    def ligand(self):
        """
        Return ligand.
        """
        return self._ligand

    @property
    def citation(self):
        """
        Return citation.
        """
        return self._citation

    @property
    def buffer(self):
        """
        Return buffer.
        """
        return self._buffer

    @property
    def ph(self):
        """
        Return ph.
        """
        return self._ph

    def copy(self, other):
        """
        Copy data from another ITCDeltaCp instance.
        """
        assert isinstance(other, ITCDeltaCp)
        self._delta_cp = other.delta_cp
        self._delta_cp_exp_err = other.delta_cp_exp_err
        self._delta_cp_unit = other.delta_cp_unit
        self._delta_cp_raw = other.delta_cp_raw
        self._delta_cp_exp_err_raw = other.delta_cp_exp_err_raw
        self._delta_cp_unit_raw = other.delta_cp_unit_raw
        self._protein = other.protein
        self._ligand = other.ligand
        self._citation = other.citation
        self._buffer = other.buffer
        self._ph = other.ph

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
    import unittest
    TEST_SUITE = doctest.DocFileSuite('tests/test_itc.txt',
        optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)
    unittest.TextTestRunner().run(TEST_SUITE)

