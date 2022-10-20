"""
Created on Wed Feb  3 19:41:38 2021

@author: Zhuoran Zhang
"""


# LCOW equation for quick analysis
                          # Unit      Input name
def lcow(capacity = 1000, # m3/day    Capacity
         capex    = 2755, # k$        Capex
         opex     = 0.3,  # $/m3      Opex
         lcoe     = 0.05, # $/kWh-e   LCOE
         lcoh     = 0.015,# $/kWh-th  LCOH
         sec      = 1.8,  # kWh/m3    SEC
         stec     = 55,   # kWh/m3    STEC
         life_yr  = 20,   # yrs       Plant life time
         int_rate = 4     # %         Interest rate
         ):
    
    unit_capex = capex * 1000 * int_rate / 100 * (1+int_rate/100) ** life_yr / ((1+int_rate/100)**life_yr -1) / (0.9*365*capacity)
    lcow = unit_capex + opex + lcoe * sec + lcoh * stec
    
    
    return lcow, unit_capex
