from typing import List, Dict, Tuple, Set, Optional, Union, Any, NoReturn
from .check import *
from .asset import *
import numpy as np

class PrimarySurfaceFlow :

    def __init__(self,
        precipitation : float,
        curve_number : float,
        rsa : bool,
        antecedent_precipitation : float,
        is_growing_season : bool
    ):
        self.precipitation = precipitation
        self.curve_number = curve_number
        self.rsa = rsa
        self.antecedent_precipitation = antecedent_precipitation
        self.is_growing_season = is_growing_season



    def scs(
        precipitation: float,
        curve_number: float,
        rsa: bool,
        antecedent_precipitation: float,
        is_growing_season: bool
    ) -> Tuple[float, float]:
        """
        Description
        -----------
        Calculate Runoff using precipitation and curve number.
        **Reference**: National Resources Conservation Service, National Engineering Handbook, Section 4 "Hydrology" (1985)

        Parameters
        ----------
        precipitation : float
            Event Rainfall Depth - Starts from 0 - mm

        curve_number : float
            An index of the land condition as indicated by soils, cover, land use - Between 0 to 100 - dimensionless

        rsa : bool
            Runoff source area - 0 or 1 - dimensionless

        antecedent_precipitation: float
            Antecedent precipitation is precipitation falling before, but influencing the runoff yields of, a given rainfall event - Starts from 0 - mm

        is_growing_season: bool
            Check whether it's growing season or not - 0 or 1 - dimensionless

        Returns
        -------
        - runoff : float
            Runoff depth resulted from precpitation - Starts from 0 - mm

        - underground_runoff: float
            Runoff depth that enters the soil - Starts from 0 - mm
        """

        check_precipitation(precipitation)
        check_curve_number(curve_number)
        check_rsa(rsa)
        
        if antecedent_precipitation:
            check_antecedent_precipitation(antecedent_precipitation)
        if is_growing_season:
            check_is_growing_season(is_growing_season)


        if antecedent_precipitation:
            modified_cn = modify_CN(curve_number, antecedent_precipitation, is_growing_season)
        else:
            modified_cn = curve_number

        if rsa:
            if precipitation + 0.8*calculate_potential_retention(modified_cn) == 0 :
                runoff = 0
            else:
                runoff = (precipitation - 0.2*calculate_potential_retention(modified_cn))**2 \
                / (precipitation + 0.8*calculate_potential_retention(modified_cn))
        else:
            runoff = 0


        underground_runoff = 0
        if gt(runoff, 0):
            underground_runoff = precipitation - runoff
        
        if lt(underground_runoff, 0):
            underground_runoff = 0


        return runoff, underground_runoff