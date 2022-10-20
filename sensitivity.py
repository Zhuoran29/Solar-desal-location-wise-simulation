# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:42:16 2021

@author: zzrfl
"""
import csv

'''
For each run, we collect the following information for sensitivity analysis
'''

# Locationwise analysis
def weather_info(weatherfile_path):
    with open(r''+ weatherfile_path, newline = '') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')

        row_count = 0
        DNI = []
        GHI = []
        Tdry = []
        Wspd = []
        day = []
        # Split of seasons (hour)
        spring = (31+28) * 24 
        summer = spring + (31 + 30 + 31) * 24
        autumn = summer + (30 + 31 + 31) * 24
        winter = autumn + (30 + 31 + 30) * 24
        
        for row in csvreader:
            if row_count == 1:
                # Record the city/region/state/country names
                              #    city,   state, country, latitude, longitude
                location_info = [row[2],  row[3],  row[4],   row[5],   row[6]]
            elif row_count > 2:
                # Collect average values
                DNI.append(float(row[5]))
                GHI.append(float(row[4]))
                Tdry.append(float(row[7]))
                Wspd.append(float(row[11]))
                day.append(1 if float(row[5]) > 0 else 0)
            
            row_count += 1

        
        # Record the key information from the weather data
        length = len(DNI)
        avg_DNI = sum(DNI) / length * 24 / 1000 # kW/m2/day
        avg_GHI = sum(GHI) / length * 24 / 1000 # kW/m2/day
        avg_Tdry= sum(Tdry)/ length     # oC
        avg_Wspd= sum(Wspd)/ length     # m/s
        avg_day = sum(day) / length     # hours
        
        # Collect the seasonal information
        seasonal_DNI = [sum(DNI[spring-1 : summer]) / 91,
                        sum(DNI[summer-1 : autumn])/ 92,
                        sum(DNI[autumn-1 : winter])/ 91,
                        (sum(DNI[winter-1:])+sum(DNI[:spring])) / 90] # kW/m2/day
        
        seasonal_GHI = [sum(GHI[spring-1 : summer]) / 91,
                        sum(GHI[summer-1 : autumn])/ 92,
                        sum(GHI[autumn-1 : winter])/ 91,
                        (sum(GHI[winter-1:])+sum(GHI[:spring])) / 90] # kW/m2/day
        
        seasonal_Tdry = [sum(Tdry[spring-1 : summer]) / 91 / 24,
                         sum(Tdry[summer-1 : autumn])/ 92 / 24,
                         sum(Tdry[autumn-1 : winter])/ 91 /24,
                         (sum(Tdry[winter-1:])+sum(Tdry[:spring])) / 90/24]  # oC      

        seasonal_Wspd = [sum(Wspd[spring-1 : summer]) / 91 / 24,
                         sum(Wspd[summer-1 : autumn])/ 92 / 24,
                         sum(Wspd[autumn-1 : winter])/ 91/24,
                         (sum(Wspd[winter-1:])+sum(Wspd[:spring])) / 90/24]  # m/s
        
        seasonal_day = [sum(day[spring-1 : summer]) / 91 ,
                         sum(day[summer-1 : autumn])/ 92 ,
                         sum(day[autumn-1 : winter])/ 91 ,
                         (sum(day[winter-1:])+sum(day[:spring])) / 90]  # hours


        ave_info = [avg_DNI, avg_GHI, avg_Tdry, avg_Wspd, avg_day]
        seasonal_info = [seasonal_DNI, seasonal_GHI, seasonal_Tdry, seasonal_Wspd, seasonal_day]
        
        return location_info, ave_info, seasonal_info
        

#%%  SAM IPH LFDS model
from PySSC import PySSC
def IPH_LFDS(weatherfile_path):
    if __name__ == "__main__":
    	ssc = PySSC()
    	# print ('Current folder = D:/PhD/DOE/Sensitivity')
    	# print ('SSC Version = ', ssc.version())
    	# print ('SSC Build Information = ', ssc.build_info().decode("utf - 8"))
    	data = ssc.data_create()
    	ssc.data_set_string( data, b'file_name',  b'' + weatherfile_path.encode("ascii", "backslashreplace"));
    	ssc.data_set_number( data, b'I_bn_des', 950 )
    	ssc.data_set_number( data, b'T_cold_ref', 100 )
    	ssc.data_set_number( data, b'P_turb_des', 20 )
    	ssc.data_set_number( data, b'T_hot', 393 )
    	ssc.data_set_number( data, b'x_b_des', 0.75 )
    	ssc.data_set_number( data, b'q_pb_des', 2.1800000000000002 )
    	ssc.data_set_number( data, b'fP_hdr_c', 0.01 )
    	ssc.data_set_number( data, b'fP_sf_boil', 0.074999999999999997 )
    	ssc.data_set_number( data, b'fP_hdr_h', 0.025000000000000001 )
    	ssc.data_set_number( data, b'nModBoil', 6 )
    	ssc.data_set_number( data, b'nLoops', 1 )
    	ssc.data_set_number( data, b'eta_pump', 0.84999999999999998 )
    	ssc.data_set_number( data, b'theta_stow', 10 )
    	ssc.data_set_number( data, b'theta_dep', 10 )
    	ssc.data_set_number( data, b'T_fp', 10 )
    	ssc.data_set_number( data, b'Pipe_hl_coef', 0.0035000000000000001 )
    	ssc.data_set_number( data, b'SCA_drives_elec', 0.20000000000000001 )
    	ssc.data_set_number( data, b'ColAz', 0 )
    	ssc.data_set_number( data, b'e_startup', 2.7000000000000002 )
    	ssc.data_set_number( data, b'T_amb_des_sf', 42 )
    	ssc.data_set_number( data, b'V_wind_max', 20 )
    	ssc.data_set_number( data, b'csp.lf.sf.water_per_wash', 0.02 )
    	ssc.data_set_number( data, b'csp.lf.sf.washes_per_year', 12 )
    	A_aperture = [[ 513.60000000000002 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'A_aperture', A_aperture );
    	L_col = [[ 44.799999999999997 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'L_col', L_col );
    	OptCharType = [[ 1 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'OptCharType', OptCharType );
    	IAM_T = [[ 0.98960000000000004,   0.043999999999999997,   -0.072099999999999997,   -0.23269999999999999,   0 ], [ 0,   0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'IAM_T', IAM_T );
    	IAM_L = [[ 1.0031000000000001,   -0.22589999999999999,   0.53680000000000005,   -1.6434,   0.72219999999999995 ], [ 0,   0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'IAM_L', IAM_L );
    	TrackingError = [[ 1 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'TrackingError', TrackingError );
    	GeomEffects = [[ 0.83999999999999997 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'GeomEffects', GeomEffects );
    	rho_mirror_clean = [[ 0.93500000000000005 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'rho_mirror_clean', rho_mirror_clean );
    	dirt_mirror = [[ 0.94999999999999996 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'dirt_mirror', dirt_mirror );
    	error = [[ 1 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'error', error );
    	HLCharType = [[ 1 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'HLCharType', HLCharType );
    	HL_dT = [[ 0,   0.67200000000000004,   0.0025560000000000001,   0,   0 ], [ 0,   0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'HL_dT', HL_dT );
    	HL_W = [[ 1,   0,   0,   0,   0 ], [ 0,   0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'HL_W', HL_W );
    	D_2 = [[ 0.066000000000000003 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'D_2', D_2 );
    	D_3 = [[ 0.070000000000000007 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'D_3', D_3 );
    	D_4 = [[ 0.115 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'D_4', D_4 );
    	D_5 = [[ 0.12 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'D_5', D_5 );
    	D_p = [[ 0 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'D_p', D_p );
    	Rough = [[ 4.5000000000000003e-05 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'Rough', Rough );
    	Flow_type = [[ 1 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'Flow_type', Flow_type );
    	AbsorberMaterial = [[ 1 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'AbsorberMaterial', AbsorberMaterial );
    	HCE_FieldFrac = [[ 0.98499999999999999,   0.01,   0.0050000000000000001,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'HCE_FieldFrac', HCE_FieldFrac );
    	alpha_abs = [[ 0.95999999999999996,   0.95999999999999996,   0.80000000000000004,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'alpha_abs', alpha_abs );
    	b_eps_HCE1 = [[ 0 ], [ 0.1384 ]];
    	ssc.data_set_matrix( data, b'b_eps_HCE1', b_eps_HCE1 );
    	b_eps_HCE2 = [[ 0 ], [ 0.65000000000000002 ]];
    	ssc.data_set_matrix( data, b'b_eps_HCE2', b_eps_HCE2 );
    	b_eps_HCE3 = [[ 0 ], [ 0.65000000000000002 ]];
    	ssc.data_set_matrix( data, b'b_eps_HCE3', b_eps_HCE3 );
    	b_eps_HCE4 = [[ 0 ], [ 0.1384 ]];
    	ssc.data_set_matrix( data, b'b_eps_HCE4', b_eps_HCE4 );
    	sh_eps_HCE1 = [[ 0 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'sh_eps_HCE1', sh_eps_HCE1 );
    	sh_eps_HCE2 = [[ 0 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'sh_eps_HCE2', sh_eps_HCE2 );
    	sh_eps_HCE3 = [[ 0 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'sh_eps_HCE3', sh_eps_HCE3 );
    	sh_eps_HCE4 = [[ 0 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'sh_eps_HCE4', sh_eps_HCE4 );
    	alpha_env = [[ 0.02,   0.02,   0,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'alpha_env', alpha_env );
    	EPSILON_4 = [[ 0.85999999999999999,   0.85999999999999999,   1,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'EPSILON_4', EPSILON_4 );
    	Tau_envelope = [[ 0.96299999999999997,   0.96299999999999997,   1,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'Tau_envelope', Tau_envelope );
    	GlazingIntactIn = [[ 1,   1,   0,   1 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'GlazingIntactIn', GlazingIntactIn );
    	AnnulusGas = [[ 1,   1,   1,   1 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'AnnulusGas', AnnulusGas );
    	P_a = [[ 0.0001,   750,   750,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'P_a', P_a );
    	Design_loss = [[ 150,   1100,   1500,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'Design_loss', Design_loss );
    	Shadowing = [[ 0.95999999999999996,   0.95999999999999996,   0.95999999999999996,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'Shadowing', Shadowing );
    	Dirt_HCE = [[ 0.97999999999999998,   0.97999999999999998,   1,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'Dirt_HCE', Dirt_HCE );
    	b_OpticalTable = [[ -180,   -160,   -140,   -120,   -100,   -80,   -60,   -40,   -20,   0,   20,   40,   60,   80,   100,   120,   140,   160,   180,   -999.89999999999998 ], [ 0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 10,   0.97999999999999998,   0.97444500000000001,   0.97197599999999995,   0.97284700000000002,   0.97690999999999995,   0.97690999999999995,   0.97284700000000002,   0.97197599999999995,   0.97444500000000001,   0.97999999999999998,   0.97444500000000001,   0.97197599999999995,   0.97284700000000002,   0.97690999999999995,   0.97690999999999995,   0.97284700000000002,   0.97197599999999995,   0.97444500000000001,   0.97999999999999998 ], [ 20,   0.93000000000000005,   0.92297600000000002,   0.92893000000000003,   0.94600499999999998,   0.95401899999999995,   0.95401899999999995,   0.94600499999999998,   0.92893000000000003,   0.92297600000000002,   0.93000000000000005,   0.92297600000000002,   0.92893000000000003,   0.94600499999999998,   0.95401899999999995,   0.95401899999999995,   0.94600499999999998,   0.92893000000000003,   0.92297600000000002,   0.93000000000000005 ], [ 30,   0.83999999999999997,   0.83861799999999997,   0.87069099999999999,   0.91302099999999997,   0.94091100000000005,   0.94091100000000005,   0.91302099999999997,   0.87069099999999999,   0.83861799999999997,   0.83999999999999997,   0.83861799999999997,   0.87069099999999999,   0.91302099999999997,   0.94091100000000005,   0.94091100000000005,   0.91302099999999997,   0.87069099999999999,   0.83861799999999997,   0.83999999999999997 ], [ 40,   0.71999999999999997,   0.72994700000000001,   0.80368700000000004,   0.86696099999999998,   0.90003900000000003,   0.90003900000000003,   0.86696099999999998,   0.80368700000000004,   0.72994700000000001,   0.71999999999999997,   0.72994700000000001,   0.80368700000000004,   0.86696099999999998,   0.90003900000000003,   0.90003900000000003,   0.86696099999999998,   0.80368700000000004,   0.72994700000000001,   0.71999999999999997 ], [ 50,   0.55000000000000004,   0.59125499999999998,   0.70745400000000003,   0.79350900000000002,   0.83955999999999997,   0.83955999999999997,   0.79350900000000002,   0.70745400000000003,   0.59125499999999998,   0.55000000000000004,   0.59125499999999998,   0.70745400000000003,   0.79350900000000002,   0.83955999999999997,   0.83955999999999997,   0.79350900000000002,   0.70745400000000003,   0.59125499999999998,   0.55000000000000004 ], [ 60,   0.34000000000000002,   0.43217800000000001,   0.59747799999999995,   0.66400599999999999,   0.69351099999999999,   0.69351099999999999,   0.66400599999999999,   0.59747799999999995,   0.43217800000000001,   0.34000000000000002,   0.43217800000000001,   0.59747799999999995,   0.66400599999999999,   0.69351099999999999,   0.69351099999999999,   0.66400599999999999,   0.59747799999999995,   0.43217800000000001,   0.34000000000000002 ], [ 70,   0.13,   0.26525399999999999,   0.42558600000000002,   0.46449600000000002,   0.47710599999999997,   0.47710599999999997,   0.46449600000000002,   0.42558600000000002,   0.26525399999999999,   0.13,   0.26525399999999999,   0.42558600000000002,   0.46449600000000002,   0.47710599999999997,   0.47710599999999997,   0.46449600000000002,   0.42558600000000002,   0.26525399999999999,   0.13 ], [ 80,   0.01,   0.113694,   0.20891000000000001,   0.23325499999999999,   0.23882800000000001,   0.23882800000000001,   0.23325499999999999,   0.20891000000000001,   0.113694,   0.01,   0.113694,   0.20891000000000001,   0.23325499999999999,   0.23882800000000001,   0.23882800000000001,   0.23325499999999999,   0.20891000000000001,   0.113694,   0.01 ], [ 90,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'b_OpticalTable', b_OpticalTable );
    	sh_OpticalTable = [[ 0,   0 ], [ 0,   0 ]];
    	ssc.data_set_matrix( data, b'sh_OpticalTable', sh_OpticalTable );
    	ssc.data_set_number( data, b'heat_sink_dP_frac', 0.01 )
    	ssc.data_set_number( data, b'adjust:constant', 4 )
    	module = ssc.module_create(b'linear_fresnel_dsg_iph')	
    	ssc.module_exec_set_print( 0 );
    	if ssc.module_exec(module, data) == 0:
    		print ('linear_fresnel_dsg_iph simulation error')
    		idx = 1
    		msg = ssc.module_log(module, 0)
    		while (msg != None):
    			print ('	: ' + msg.decode("utf - 8"))
    			msg = ssc.module_log(module, idx)
    			idx = idx + 1
    		SystemExit( "Simulation Error" );
    	ssc.module_free(module)
    	ssc.data_set_number( data, b'electricity_rate', 0.059999999999999998 )
    	ssc.data_set_number( data, b'fixed_operating_cost', 17073.759765625 )
    	module = ssc.module_create(b'iph_to_lcoefcr')	
    	ssc.module_exec_set_print( 0 );
    	if ssc.module_exec(module, data) == 0:
    		print ('iph_to_lcoefcr simulation error')
    		idx = 1
    		msg = ssc.module_log(module, 0)
    		while (msg != None):
    			print ('	: ' + msg.decode("utf - 8"))
    			msg = ssc.module_log(module, idx)
    			idx = idx + 1
    		SystemExit( "Simulation Error" );
    	ssc.module_free(module)
    	ssc.data_set_number( data, b'capital_cost', 1195163.125 )
    	ssc.data_set_number( data, b'variable_operating_cost', 0.0010000000474974513 )
    	ssc.data_set_number( data, b'fixed_charge_rate', 0.055353961884975433 )
    	module = ssc.module_create(b'lcoefcr')	
    	ssc.module_exec_set_print( 0 );
    	if ssc.module_exec(module, data) == 0:
    		print ('lcoefcr simulation error')
    		idx = 1
    		msg = ssc.module_log(module, 0)
    		while (msg != None):
    			print ('	: ' + msg.decode("utf - 8"))
    			msg = ssc.module_log(module, idx)
    			idx = idx + 1
    		SystemExit( "Simulation Error" );
    	ssc.module_free(module)
    	annual_energy = ssc.data_get_number(data, b'annual_energy');
    	annual_gross_energy = ssc.data_get_number(data, b'annual_gross_energy');
    	annual_thermal_consumption = ssc.data_get_number(data, b'annual_thermal_consumption');
    	capacity_factor = ssc.data_get_number(data, b'capacity_factor');
    	annual_electricity_consumption = ssc.data_get_number(data, b'annual_electricity_consumption');
    	lcoe_fcr = ssc.data_get_number(data, b'lcoe_fcr');
    	gen = ssc.data_get_array(data, b'gen')
    	ssc.data_free(data);
    	# print(type(gen))
    	return gen, lcoe_fcr, capacity_factor

# weatherfile_path = 'D:/PhD/DOE/Sensitivity/US_solar_data/USA AK Ambler (TMY3).csv'
# SAM_results = IPH_LFDS(weatherfile_path)
# print(type(SAM_results))
#%%  SAM IPH Parabolic trough model
def IPH_parabolic(weatherfile_path):
    from PySSC import PySSC
    if __name__ == "__main__":
    	ssc = PySSC()
    	# print ('Current folder = D:/PhD/DOE/Sensitivity')
    	# print ('SSC Version = ', ssc.version())
    	# print ('SSC Build Information = ', ssc.build_info().decode("utf - 8"))
    	ssc.module_exec_set_print(0)
    	data = ssc.data_create()
    	# ssc.data_set_string( data, b'file_name',  b'' + weatherfile_path.encode("ascii", "backslashreplace"));
    	ssc.data_set_string( data, b'file_name',  b'' + weatherfile_path.encode("ascii", "backslashreplace"));
    	ssc.data_set_number( data, b'track_mode', 1 )
    	ssc.data_set_number( data, b'tilt', 0 )
    	ssc.data_set_number( data, b'azimuth', 0 )
    	ssc.data_set_number( data, b'I_bn_des', 950 )
    	ssc.data_set_number( data, b'solar_mult', 1.5927602052688599 )
    	ssc.data_set_number( data, b'T_loop_in_des', 100 )
    	ssc.data_set_number( data, b'T_loop_out', 150 )
    	ssc.data_set_number( data, b'q_pb_design', 2.1800000000000002 )
    	ssc.data_set_number( data, b'tshours', 10 )
    	ssc.data_set_number( data, b'nSCA', 4 )
    	ssc.data_set_number( data, b'nHCEt', 4 )
    	ssc.data_set_number( data, b'nColt', 4 )
    	ssc.data_set_number( data, b'nHCEVar', 4 )
    	ssc.data_set_number( data, b'nLoops', 2 )
    	ssc.data_set_number( data, b'eta_pump', 0.84999999999999998 )
    	ssc.data_set_number( data, b'HDR_rough', 4.57e-05 )
    	ssc.data_set_number( data, b'theta_stow', 170 )
    	ssc.data_set_number( data, b'theta_dep', 10 )
    	ssc.data_set_number( data, b'Row_Distance', 15 )
    	ssc.data_set_number( data, b'FieldConfig', 1 )
    	ssc.data_set_number( data, b'is_model_heat_sink_piping', 0 )
    	ssc.data_set_number( data, b'L_heat_sink_piping', 50 )
    	ssc.data_set_number( data, b'm_dot_htfmin', 1 )
    	ssc.data_set_number( data, b'm_dot_htfmax', 12 )
    	ssc.data_set_number( data, b'Fluid', 31 )
    	ssc.data_set_number( data, b'wind_stow_speed', 25 )
    	field_fl_props = [[ 20,   4.1799999999999997,   999,   0.001,   9.9999999999999995e-07,   0.58699999999999997,   85.299999999999997 ], [ 40,   4.1799999999999997,   993,   0.00065300000000000004,   6.5799999999999999e-07,   0.61799999999999999,   169 ], [ 60,   4.1799999999999997,   984,   0.00046700000000000002,   4.75e-07,   0.64200000000000002,   252 ], [ 80,   4.1900000000000004,   972,   0.00035500000000000001,   3.65e-07,   0.65700000000000003,   336 ], [ 100,   4.21,   959,   0.00028200000000000002,   2.9400000000000001e-07,   0.66600000000000004,   420 ], [ 120,   4.25,   944,   0.000233,   2.4600000000000001e-07,   0.67000000000000004,   505 ], [ 140,   4.2800000000000002,   927,   0.00019699999999999999,   2.1199999999999999e-07,   0.67000000000000004,   590 ], [ 160,   4.3399999999999999,   908,   0.00017100000000000001,   1.8799999999999999e-07,   0.66700000000000004,   676 ], [ 180,   4.4000000000000004,   887,   0.00014999999999999999,   1.6899999999999999e-07,   0.66100000000000003,   764 ], [ 200,   4.4900000000000002,   865,   0.000134,   1.55e-07,   0.65100000000000002,   852 ], [ 220,   4.5800000000000001,   842,   0.000118,   1.4100000000000001e-07,   0.64100000000000001,   941 ]];
    	ssc.data_set_matrix( data, b'field_fl_props', field_fl_props );
    	ssc.data_set_number( data, b'T_fp', 10 )
    	ssc.data_set_number( data, b'Pipe_hl_coef', 0.45000000000000001 )
    	ssc.data_set_number( data, b'SCA_drives_elec', 125 )
    	ssc.data_set_number( data, b'water_usage_per_wash', 0.69999999999999996 )
    	ssc.data_set_number( data, b'washing_frequency', 12 )
    	ssc.data_set_number( data, b'accept_mode', 0 )
    	ssc.data_set_number( data, b'accept_init', 0 )
    	ssc.data_set_number( data, b'accept_loc', 1 )
    	ssc.data_set_number( data, b'mc_bal_hot', 0.20000000000000001 )
    	ssc.data_set_number( data, b'mc_bal_cold', 0.20000000000000001 )
    	ssc.data_set_number( data, b'mc_bal_sca', 4.5 )
    	W_aperture =[ 6, 6, 6, 6 ];
    	ssc.data_set_array( data, b'W_aperture',  W_aperture);
    	A_aperture =[ 656, 656, 656, 656 ];
    	ssc.data_set_array( data, b'A_aperture',  A_aperture);
    	TrackingError =[ 0.98799999999999999, 0.98799999999999999, 0.98799999999999999, 0.98799999999999999 ];
    	ssc.data_set_array( data, b'TrackingError',  TrackingError);
    	GeomEffects =[ 0.95199999999999996, 0.95199999999999996, 0.95199999999999996, 0.95199999999999996 ];
    	ssc.data_set_array( data, b'GeomEffects',  GeomEffects);
    	Rho_mirror_clean =[ 0.93000000000000005, 0.93000000000000005, 0.93000000000000005, 0.93000000000000005 ];
    	ssc.data_set_array( data, b'Rho_mirror_clean',  Rho_mirror_clean);
    	Dirt_mirror =[ 0.96999999999999997, 0.96999999999999997, 0.96999999999999997, 0.96999999999999997 ];
    	ssc.data_set_array( data, b'Dirt_mirror',  Dirt_mirror);
    	Error =[ 1, 1, 1, 1 ];
    	ssc.data_set_array( data, b'Error',  Error);
    	Ave_Focal_Length =[ 2.1499999999999999, 2.1499999999999999, 2.1499999999999999, 2.1499999999999999 ];
    	ssc.data_set_array( data, b'Ave_Focal_Length',  Ave_Focal_Length);
    	L_SCA =[ 115, 115, 115, 115 ];
    	ssc.data_set_array( data, b'L_SCA',  L_SCA);
    	L_aperture =[ 14.375, 14.375, 14.375, 14.375 ];
    	ssc.data_set_array( data, b'L_aperture',  L_aperture);
    	ColperSCA =[ 8, 8, 8, 8 ];
    	ssc.data_set_array( data, b'ColperSCA',  ColperSCA);
    	Distance_SCA =[ 1, 1, 1, 1 ];
    	ssc.data_set_array( data, b'Distance_SCA',  Distance_SCA);
    	IAM_matrix = [[ 1,   0.0327,   -0.1351 ], [ 1,   0.0327,   -0.1351 ], [ 1,   0.0327,   -0.1351 ], [ 1,   0.0327,   -0.1351 ]];
    	ssc.data_set_matrix( data, b'IAM_matrix', IAM_matrix );
    	HCE_FieldFrac = [[ 1,   0,   0,   0 ], [ 1,   0,   0,   0 ], [ 1,   0,   0,   0 ], [ 1,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'HCE_FieldFrac', HCE_FieldFrac );
    	D_2 = [[ 0.075999999999999998,   0.075999999999999998,   0.075999999999999998,   0.075999999999999998 ], [ 0.075999999999999998,   0.075999999999999998,   0.075999999999999998,   0.075999999999999998 ], [ 0.075999999999999998,   0.075999999999999998,   0.075999999999999998,   0.075999999999999998 ], [ 0.075999999999999998,   0.075999999999999998,   0.075999999999999998,   0.075999999999999998 ]];
    	ssc.data_set_matrix( data, b'D_2', D_2 );
    	D_3 = [[ 0.080000000000000002,   0.080000000000000002,   0.080000000000000002,   0.080000000000000002 ], [ 0.080000000000000002,   0.080000000000000002,   0.080000000000000002,   0.080000000000000002 ], [ 0.080000000000000002,   0.080000000000000002,   0.080000000000000002,   0.080000000000000002 ], [ 0.080000000000000002,   0.080000000000000002,   0.080000000000000002,   0.080000000000000002 ]];
    	ssc.data_set_matrix( data, b'D_3', D_3 );
    	D_4 = [[ 0.115,   0.115,   0.115,   0.115 ], [ 0.115,   0.115,   0.115,   0.115 ], [ 0.115,   0.115,   0.115,   0.115 ], [ 0.115,   0.115,   0.115,   0.115 ]];
    	ssc.data_set_matrix( data, b'D_4', D_4 );
    	D_5 = [[ 0.12,   0.12,   0.12,   0.12 ], [ 0.12,   0.12,   0.12,   0.12 ], [ 0.12,   0.12,   0.12,   0.12 ], [ 0.12,   0.12,   0.12,   0.12 ]];
    	ssc.data_set_matrix( data, b'D_5', D_5 );
    	D_p = [[ 0,   0,   0,   0 ], [ 0,   0,   0,   0 ], [ 0,   0,   0,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'D_p', D_p );
    	Flow_type = [[ 1,   1,   1,   1 ], [ 1,   1,   1,   1 ], [ 1,   1,   1,   1 ], [ 1,   1,   1,   1 ]];
    	ssc.data_set_matrix( data, b'Flow_type', Flow_type );
    	Rough = [[ 4.5000000000000003e-05,   4.5000000000000003e-05,   4.5000000000000003e-05,   4.5000000000000003e-05 ], [ 4.5000000000000003e-05,   4.5000000000000003e-05,   4.5000000000000003e-05,   4.5000000000000003e-05 ], [ 4.5000000000000003e-05,   4.5000000000000003e-05,   4.5000000000000003e-05,   4.5000000000000003e-05 ], [ 4.5000000000000003e-05,   4.5000000000000003e-05,   4.5000000000000003e-05,   4.5000000000000003e-05 ]];
    	ssc.data_set_matrix( data, b'Rough', Rough );
    	alpha_env = [[ 0.02,   0.02,   0,   0 ], [ 0.02,   0.02,   0,   0 ], [ 0.02,   0.02,   0,   0 ], [ 0.02,   0.02,   0,   0 ]];
    	ssc.data_set_matrix( data, b'alpha_env', alpha_env );
    	epsilon_3_11 = [[ 100,   0.064000000000000001 ], [ 150,   0.066500000000000004 ], [ 200,   0.070000000000000007 ], [ 250,   0.074499999999999997 ], [ 300,   0.080000000000000002 ], [ 350,   0.086499999999999994 ], [ 400,   0.094 ], [ 450,   0.10249999999999999 ], [ 500,   0.112 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_11', epsilon_3_11 );
    	epsilon_3_12 = [[ 0.65000000000000002 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_12', epsilon_3_12 );
    	epsilon_3_13 = [[ 0.65000000000000002 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_13', epsilon_3_13 );
    	epsilon_3_14 = [[ 0 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_14', epsilon_3_14 );
    	epsilon_3_21 = [[ 100,   0.064000000000000001 ], [ 150,   0.066500000000000004 ], [ 200,   0.070000000000000007 ], [ 250,   0.074499999999999997 ], [ 300,   0.080000000000000002 ], [ 350,   0.086499999999999994 ], [ 400,   0.094 ], [ 450,   0.10249999999999999 ], [ 500,   0.112 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_21', epsilon_3_21 );
    	epsilon_3_22 = [[ 0.65000000000000002 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_22', epsilon_3_22 );
    	epsilon_3_23 = [[ 0.65000000000000002 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_23', epsilon_3_23 );
    	epsilon_3_24 = [[ 0 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_24', epsilon_3_24 );
    	epsilon_3_31 = [[ 100,   0.064000000000000001 ], [ 150,   0.066500000000000004 ], [ 200,   0.070000000000000007 ], [ 250,   0.074499999999999997 ], [ 300,   0.080000000000000002 ], [ 350,   0.086499999999999994 ], [ 400,   0.094 ], [ 450,   0.10249999999999999 ], [ 500,   0.112 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_31', epsilon_3_31 );
    	epsilon_3_32 = [[ 0.65000000000000002 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_32', epsilon_3_32 );
    	epsilon_3_33 = [[ 0.65000000000000002 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_33', epsilon_3_33 );
    	epsilon_3_34 = [[ 0 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_34', epsilon_3_34 );
    	epsilon_3_41 = [[ 100,   0.064000000000000001 ], [ 150,   0.066500000000000004 ], [ 200,   0.070000000000000007 ], [ 250,   0.074499999999999997 ], [ 300,   0.080000000000000002 ], [ 350,   0.086499999999999994 ], [ 400,   0.094 ], [ 450,   0.10249999999999999 ], [ 500,   0.112 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_41', epsilon_3_41 );
    	epsilon_3_42 = [[ 0.65000000000000002 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_42', epsilon_3_42 );
    	epsilon_3_43 = [[ 0.65000000000000002 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_43', epsilon_3_43 );
    	epsilon_3_44 = [[ 0 ]];
    	ssc.data_set_matrix( data, b'epsilon_3_44', epsilon_3_44 );
    	alpha_abs = [[ 0.96299999999999997,   0.96299999999999997,   0.80000000000000004,   0 ], [ 0.96299999999999997,   0.96299999999999997,   0.80000000000000004,   0 ], [ 0.96299999999999997,   0.96299999999999997,   0.80000000000000004,   0 ], [ 0.96299999999999997,   0.96299999999999997,   0.80000000000000004,   0 ]];
    	ssc.data_set_matrix( data, b'alpha_abs', alpha_abs );
    	Tau_envelope = [[ 0.96399999999999997,   0.96399999999999997,   1,   0 ], [ 0.96399999999999997,   0.96399999999999997,   1,   0 ], [ 0.96399999999999997,   0.96399999999999997,   1,   0 ], [ 0.96399999999999997,   0.96399999999999997,   1,   0 ]];
    	ssc.data_set_matrix( data, b'Tau_envelope', Tau_envelope );
    	EPSILON_4 = [[ 0.85999999999999999,   0.85999999999999999,   1,   0 ], [ 0.85999999999999999,   0.85999999999999999,   1,   0 ], [ 0.85999999999999999,   0.85999999999999999,   1,   0 ], [ 0.85999999999999999,   0.85999999999999999,   1,   0 ]];
    	ssc.data_set_matrix( data, b'EPSILON_4', EPSILON_4 );
    	EPSILON_5 = [[ 0.85999999999999999,   0.85999999999999999,   1,   0 ], [ 0.85999999999999999,   0.85999999999999999,   1,   0 ], [ 0.85999999999999999,   0.85999999999999999,   1,   0 ], [ 0.85999999999999999,   0.85999999999999999,   1,   0 ]];
    	ssc.data_set_matrix( data, b'EPSILON_5', EPSILON_5 );
    	GlazingIntactIn = [[ 1,   1,   0,   1 ], [ 1,   1,   0,   1 ], [ 1,   1,   0,   1 ], [ 1,   1,   0,   1 ]];
    	ssc.data_set_matrix( data, b'GlazingIntactIn', GlazingIntactIn );
    	P_a = [[ 0.0001,   750,   750,   0 ], [ 0.0001,   750,   750,   0 ], [ 0.0001,   750,   750,   0 ], [ 0.0001,   750,   750,   0 ]];
    	ssc.data_set_matrix( data, b'P_a', P_a );
    	AnnulusGas = [[ 27,   1,   1,   1 ], [ 27,   1,   1,   1 ], [ 27,   1,   1,   27 ], [ 27,   1,   1,   27 ]];
    	ssc.data_set_matrix( data, b'AnnulusGas', AnnulusGas );
    	AbsorberMaterial = [[ 1,   1,   1,   1 ], [ 1,   1,   1,   1 ], [ 1,   1,   1,   1 ], [ 1,   1,   1,   1 ]];
    	ssc.data_set_matrix( data, b'AbsorberMaterial', AbsorberMaterial );
    	Shadowing = [[ 0.93500000000000005,   0.93500000000000005,   0.93500000000000005,   0.96299999999999997 ], [ 0.93500000000000005,   0.93500000000000005,   0.93500000000000005,   0.96299999999999997 ], [ 0.93500000000000005,   0.93500000000000005,   0.93500000000000005,   0.96299999999999997 ], [ 0.93500000000000005,   0.93500000000000005,   0.93500000000000005,   0.96299999999999997 ]];
    	ssc.data_set_matrix( data, b'Shadowing', Shadowing );
    	Dirt_HCE = [[ 0.97999999999999998,   0.97999999999999998,   1,   0.97999999999999998 ], [ 0.97999999999999998,   0.97999999999999998,   1,   0.97999999999999998 ], [ 0.97999999999999998,   0.97999999999999998,   1,   0.97999999999999998 ], [ 0.97999999999999998,   0.97999999999999998,   1,   0.97999999999999998 ]];
    	ssc.data_set_matrix( data, b'Dirt_HCE', Dirt_HCE );
    	Design_loss = [[ 190,   1270,   1500,   0 ], [ 190,   1270,   1500,   0 ], [ 190,   1270,   1500,   0 ], [ 190,   1270,   1500,   0 ]];
    	ssc.data_set_matrix( data, b'Design_loss', Design_loss );
    	SCAInfoArray = [[ 1,   1 ], [ 1,   1 ], [ 1,   1 ], [ 1,   1 ]];
    	ssc.data_set_matrix( data, b'SCAInfoArray', SCAInfoArray );
    	SCADefocusArray =[ 4, 3, 2, 1 ];
    	ssc.data_set_array( data, b'SCADefocusArray',  SCADefocusArray);
    	ssc.data_set_number( data, b'pb_pump_coef', 0.55000000000000004 )
    	ssc.data_set_number( data, b'init_hot_htf_percent', 30 )
    	ssc.data_set_number( data, b'h_tank', 15 )
    	ssc.data_set_number( data, b'cold_tank_max_heat', 0.5 )
    	ssc.data_set_number( data, b'u_tank', 0.29999999999999999 )
    	ssc.data_set_number( data, b'tank_pairs', 1 )
    	ssc.data_set_number( data, b'cold_tank_Thtr', 60 )
    	ssc.data_set_number( data, b'h_tank_min', 0.5 )
    	ssc.data_set_number( data, b'hot_tank_Thtr', 110 )
    	ssc.data_set_number( data, b'hot_tank_max_heat', 1 )
    	weekday_schedule = [[ 6,   6,   6,   6,   6,   6,   5,   5,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   5,   5,   5 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   5,   5,   5 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   5,   5,   5 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   5,   5,   5 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   5,   5,   5 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   2,   2,   2,   3,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   2,   2,   2,   3,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   2,   2,   2,   3,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   2,   2,   2,   2,   1,   1,   1,   1,   1,   1,   2,   2,   2,   3,   3,   3 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   5,   5,   5 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   5,   5,   5 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   5,   5,   5 ]];
    	ssc.data_set_matrix( data, b'weekday_schedule', weekday_schedule );
    	weekend_schedule = [[ 6,   6,   6,   6,   6,   6,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3 ], [ 3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3,   3 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5 ], [ 6,   6,   6,   6,   6,   6,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5 ]];
    	ssc.data_set_matrix( data, b'weekend_schedule', weekend_schedule );
    	ssc.data_set_number( data, b'is_tod_pc_target_also_pc_max', 0 )
    	ssc.data_set_number( data, b'is_dispatch', 0 )
    	ssc.data_set_number( data, b'disp_frequency', 24 )
    	ssc.data_set_number( data, b'disp_horizon', 48 )
    	ssc.data_set_number( data, b'disp_max_iter', 35000 )
    	ssc.data_set_number( data, b'disp_timeout', 5 )
    	ssc.data_set_number( data, b'disp_mip_gap', 0.001 )
    	ssc.data_set_number( data, b'disp_time_weighting', 0.98999999999999999 )
    	ssc.data_set_number( data, b'disp_rsu_cost', 950 )
    	ssc.data_set_number( data, b'disp_csu_cost', 10000 )
    	ssc.data_set_number( data, b'disp_pen_delta_w', 0.10000000000000001 )
    	ssc.data_set_number( data, b'is_wlim_series', 0 )
    	f_turb_tou_periods =[ 1.05, 1, 1, 1, 1, 1, 1, 1, 1 ];
    	ssc.data_set_array( data, b'f_turb_tou_periods',  f_turb_tou_periods);
    	ssc.data_set_number( data, b'is_dispatch_series', 0 )
    	dispatch_series =[ 0 ];
    	ssc.data_set_array( data, b'dispatch_series',  dispatch_series);
    	ssc.data_set_number( data, b'pb_fixed_par', 0.0054999999999999997 )
    	bop_array =[ 0, 1, 0, 0.48299999999999998, 0 ];
    	ssc.data_set_array( data, b'bop_array',  bop_array);
    	aux_array =[ 0.023, 1, 0.48299999999999998, 0.57099999999999995, 0 ];
    	ssc.data_set_array( data, b'aux_array',  aux_array);
    	ssc.data_set_number( data, b'calc_design_pipe_vals', 1 )
    	ssc.data_set_number( data, b'V_hdr_cold_max', 3 )
    	ssc.data_set_number( data, b'V_hdr_cold_min', 2 )
    	ssc.data_set_number( data, b'V_hdr_hot_max', 3 )
    	ssc.data_set_number( data, b'V_hdr_hot_min', 2 )
    	ssc.data_set_number( data, b'N_max_hdr_diams', 10 )
    	ssc.data_set_number( data, b'L_rnr_pb', 25 )
    	ssc.data_set_number( data, b'L_rnr_per_xpan', 70 )
    	ssc.data_set_number( data, b'L_xpan_hdr', 20 )
    	ssc.data_set_number( data, b'L_xpan_rnr', 20 )
    	ssc.data_set_number( data, b'Min_rnr_xpans', 1 )
    	ssc.data_set_number( data, b'northsouth_field_sep', 20 )
    	ssc.data_set_number( data, b'N_hdr_per_xpan', 2 )
    	ssc.data_set_number( data, b'offset_xpan_hdr', 1 )
    	K_cpnt = [[ 0.90000000000000002,   0,   0.19,   0,   0.90000000000000002,   -1,   -1,   -1,   -1,   -1,   -1 ], [ 0,   0.59999999999999998,   0.050000000000000003,   0,   0.59999999999999998,   0,   0.59999999999999998,   0,   0.41999999999999998,   0,   0.14999999999999999 ], [ 0.050000000000000003,   0,   0.41999999999999998,   0,   0.59999999999999998,   0,   0.59999999999999998,   0,   0.41999999999999998,   0,   0.14999999999999999 ], [ 0.050000000000000003,   0,   0.41999999999999998,   0,   0.59999999999999998,   0,   0.59999999999999998,   0,   0.41999999999999998,   0,   0.14999999999999999 ], [ 0.050000000000000003,   0,   0.41999999999999998,   0,   0.59999999999999998,   0,   0.59999999999999998,   0,   0.41999999999999998,   0,   0.14999999999999999 ], [ 0.050000000000000003,   0,   0.41999999999999998,   0,   0.59999999999999998,   0,   0.59999999999999998,   0,   0.14999999999999999,   0.59999999999999998,   0 ], [ 0.90000000000000002,   0,   0.19,   0,   0.90000000000000002,   -1,   -1,   -1,   -1,   -1,   -1 ]];
    	ssc.data_set_matrix( data, b'K_cpnt', K_cpnt );
    	D_cpnt = [[ 0.085000000000000006,   0.063500000000000001,   0.085000000000000006,   0.063500000000000001,   0.085000000000000006,   -1,   -1,   -1,   -1,   -1,   -1 ], [ 0.085000000000000006,   0.085000000000000006,   0.085000000000000006,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.085000000000000006 ], [ 0.085000000000000006,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.085000000000000006 ], [ 0.085000000000000006,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.085000000000000006 ], [ 0.085000000000000006,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.085000000000000006 ], [ 0.085000000000000006,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.063500000000000001,   0.085000000000000006,   0.085000000000000006,   0.085000000000000006 ], [ 0.085000000000000006,   0.063500000000000001,   0.085000000000000006,   0.063500000000000001,   0.085000000000000006,   -1,   -1,   -1,   -1,   -1,   -1 ]];
    	ssc.data_set_matrix( data, b'D_cpnt', D_cpnt );
    	L_cpnt = [[ 0,   0,   0,   0,   0,   -1,   -1,   -1,   -1,   -1,   -1 ], [ 0,   0,   0,   1,   0,   0,   0,   1,   0,   1,   0 ], [ 0,   1,   0,   1,   0,   0,   0,   1,   0,   1,   0 ], [ 0,   1,   0,   1,   0,   0,   0,   1,   0,   1,   0 ], [ 0,   1,   0,   1,   0,   0,   0,   1,   0,   1,   0 ], [ 0,   1,   0,   1,   0,   0,   0,   1,   0,   0,   0 ], [ 0,   0,   0,   0,   0,   -1,   -1,   -1,   -1,   -1,   -1 ]];
    	ssc.data_set_matrix( data, b'L_cpnt', L_cpnt );
    	Type_cpnt = [[ 0,   1,   0,   1,   0,   -1,   -1,   -1,   -1,   -1,   -1 ], [ 1,   0,   0,   2,   0,   1,   0,   2,   0,   2,   0 ], [ 0,   2,   0,   2,   0,   1,   0,   2,   0,   2,   0 ], [ 0,   2,   0,   2,   0,   1,   0,   2,   0,   2,   0 ], [ 0,   2,   0,   2,   0,   1,   0,   2,   0,   2,   0 ], [ 0,   2,   0,   2,   0,   1,   0,   2,   0,   0,   1 ], [ 0,   1,   0,   1,   0,   -1,   -1,   -1,   -1,   -1,   -1 ]];
    	ssc.data_set_matrix( data, b'Type_cpnt', Type_cpnt );
    	ssc.data_set_number( data, b'custom_sf_pipe_sizes', 0 )
    	sf_rnr_diams = [[ -1 ]];
    	ssc.data_set_matrix( data, b'sf_rnr_diams', sf_rnr_diams );
    	sf_rnr_wallthicks = [[ -1 ]];
    	ssc.data_set_matrix( data, b'sf_rnr_wallthicks', sf_rnr_wallthicks );
    	sf_rnr_lengths = [[ -1 ]];
    	ssc.data_set_matrix( data, b'sf_rnr_lengths', sf_rnr_lengths );
    	sf_hdr_diams = [[ -1 ]];
    	ssc.data_set_matrix( data, b'sf_hdr_diams', sf_hdr_diams );
    	sf_hdr_wallthicks = [[ -1 ]];
    	ssc.data_set_matrix( data, b'sf_hdr_wallthicks', sf_hdr_wallthicks );
    	sf_hdr_lengths = [[ -1 ]];
    	ssc.data_set_matrix( data, b'sf_hdr_lengths', sf_hdr_lengths );
    	ssc.data_set_number( data, b'adjust:constant', 4 )
    	module = ssc.module_create(b'trough_physical_process_heat')	
    	ssc.module_exec_set_print( 0 );
    	if ssc.module_exec(module, data) == 0:
    		print ('trough_physical_process_heat simulation error')
    		idx = 1
    		msg = ssc.module_log(module, 0)
    		while (msg != None):
    			print ('	: ' + msg.decode("utf - 8"))
    			msg = ssc.module_log(module, idx)
    			idx = idx + 1
    		SystemExit( "Simulation Error" );
    	ssc.module_free(module)
    	ssc.data_set_number( data, b'electricity_rate', 0.059999999999999998 )
    	ssc.data_set_number( data, b'fixed_operating_cost', 27729.6015625 )
    	module = ssc.module_create(b'iph_to_lcoefcr')	
    	ssc.module_exec_set_print( 0 );
    	if ssc.module_exec(module, data) == 0:
    		print ('iph_to_lcoefcr simulation error')
    		idx = 1
    		msg = ssc.module_log(module, 0)
    		while (msg != None):
    			print ('	: ' + msg.decode("utf - 8"))
    			msg = ssc.module_log(module, idx)
    			idx = idx + 1
    		SystemExit( "Simulation Error" );
    	ssc.module_free(module)
    	ssc.data_set_number( data, b'capital_cost', 2506062.75 )
    	ssc.data_set_number( data, b'variable_operating_cost', 0.0010000000474974513 )
    	ssc.data_set_number( data, b'fixed_charge_rate', 0.055353961884975433 )
    	module = ssc.module_create(b'lcoefcr')	
    	ssc.module_exec_set_print( 0 );
    	if ssc.module_exec(module, data) == 0:
    		print ('lcoefcr simulation error')
    		idx = 1
    		msg = ssc.module_log(module, 0)
    		while (msg != None):
    			print ('	: ' + msg.decode("utf - 8"))
    			msg = ssc.module_log(module, idx)
    			idx = idx + 1
    		SystemExit( "Simulation Error" );
    	ssc.module_free(module)
    	annual_energy = ssc.data_get_number(data, b'annual_energy');
    	annual_gross_energy = ssc.data_get_number(data, b'annual_gross_energy');
    	annual_thermal_consumption = ssc.data_get_number(data, b'annual_thermal_consumption');
    	capacity_factor = ssc.data_get_number(data, b'capacity_factor');
    	annual_electricity_consumption = ssc.data_get_number(data, b'annual_electricity_consumption');
    	lcoe_fcr = ssc.data_get_number(data, b'lcoe_fcr');
    	gen = ssc.data_get_array(data, b'gen')
    	ssc.data_free(data);
    	return gen, lcoe_fcr, capacity_factor
    	# return [annual_energy, capacity_factor, annual_electricity_consumption, lcoe_fcr]



#%% Run for the map
import csv
from PySSC import PySSC
import os
import time

US_solar_directory = 'D:/PhD/DOE/Sensitivity/US_solar_data_test/'
files = os.listdir(US_solar_directory)

# Create the csv outfile and the csv writer object
csv_outfile = 'D:/PhD/DOE/Sensitivity/US_IPH_parabolic.csv'
data_file = open(csv_outfile, 'w', newline='') 
csv_writer = csv.writer(data_file)

# Write the header
csv_writer.writerow(["City", "State", "Country", "Latitude", "Longitude",
                     "avg_DNI", "avg_GHI", "avg_Tdry", "avg_Wspd", "avg_day",
                     "spring_DNI", "summer_DNI", "autumn_DNI", "winter_DNI",
                     "spring_GHI", "summer_GHI", "autumn_GHI", "winter_GHI",
                     "spring_Tdry", "summer_Tdry", "autumn_Tdry", "winter_Tdry",
                     "spring_Wspd", "summer_Wspd", "autumn_Wspd", "winter_Wspd",
                     "spring_day", "summer_day", "autumn_day", "winter_day",
                     "annual_energy", "capacity_factor", "annual_electricity_consumption", "lcoh"])

start_time = time.time()
progress = 0
# Run solar model for each location in the US and write to the csv
for path in files:
    weatherfile_path = US_solar_directory + path 
    location_info, ave_info, seasonal_info = weather_info(weatherfile_path)
    s_DNI, s_GHI, s_Tdry, s_Wspd, s_day = seasonal_info
    SAM_results = [IPH_parabolic(weatherfile_path)]

    csv_writer.writerow(location_info + ave_info + s_DNI + s_GHI + s_Tdry + s_Wspd + s_day + SAM_results)
    progress += 1
    if progress%5 == 0:
        print('Progress: ', progress, '/', len(files), 'Processing time: ', round((time.time()-start_time)/60,1), 'min')
    
data_file.close()      

#%% Run VAGMD for the map

from VAGMD_PSA import VAGMD_PSA
from VAGMD_cost import VAGMD_cost
import os
import time
US_solar_directory = 'D:/PhD/DOE/Sensitivity/US_solar_data/'
files = os.listdir(US_solar_directory)

csv_outfile1 = 'D:/PhD/DOE/Sensitivity/US_LFDS_VAGMD(SM=0.98).csv'
# csv_outfile2 = 'D:/PhD/DOE/Sensitivity/US_LFDS_VAGMD(SM=1.96,6hr).csv'
# csv_outfile3 = 'D:/PhD/DOE/Sensitivity/US_LFDS_VAGMD(SM=1.96,6hr,fossil).csv'
data_file1 = open(csv_outfile1, 'w', newline='')
# data_file2 = open(csv_outfile2, 'w', newline='') 
# data_file3 = open(csv_outfile3, 'w', newline='') 
csv_writer1 = csv.writer(data_file1)
# csv_writer2 = csv.writer(data_file2)
# csv_writer3 = csv.writer(data_file3)
csv_writer1.writerow(["City", "State", "Country", "Latitude", "Longitude", "LCOH from solar field", "Capacity Factor", "% of solar energy", "% of external energy", "Water production", "Cost of heat per unit", "LCOW", "CAPEX", "OPEX"])
# csv_writer2.writerow(["City", "State", "Country", "Latitude", "Longitude", "LCOH from solar field", "Capacity Factor", "% of solar energy", "% of external energy", "Water production", "Cost of heat per unit", "LCOW", "CAPEX", "OPEX"])
# csv_writer3.writerow(["City", "State", "Country", "Latitude", "Longitude", "LCOH from solar field", "Capacity Factor", "% of solar energy", "% of external energy", "Water production", "Cost of heat per unit", "LCOW", "CAPEX", "OPEX"])
start_time = time.time()
progress = 0
for path in files:
    weatherfile_path = US_solar_directory + path
    location_info, ave_info, seasonal_info = weather_info(weatherfile_path)     
    generation, lcoh, CF = IPH_LFDS(weatherfile_path)

    VAGMD1 = VAGMD_PSA(Fossil_f = 0)
    VAGMD1.design()
    VAGMD1_out = VAGMD1.simulation(gen = generation, storage = 0)
    # VAGMD2_out = VAGMD1.simulation(gen = generation, storage = 6)
    VAGMD1_cost = VAGMD_cost(fuel_usage=VAGMD1_out[7]['Value'],Prod =VAGMD1_out[4]['Value'], sam_coh = lcoh, coh = 0.01, storage_cap = 0)
    # VAGMD2_cost = VAGMD_cost(fuel_usage=VAGMD2_out[7]['Value'],Prod =VAGMD2_out[4]['Value'], sam_coh = lcoh, coh = 0.01, storage_cap = VAGMD2_out[2]['Value'])    
    cost1 = VAGMD1_cost.lcow()
    # cost2 = VAGMD2_cost.lcow()
    
    # VAGMD2 = VAGMD_PSA(Fossil_f = 1)
    # VAGMD2.design()
    # VAGMD3_out = VAGMD2.simulation(gen = generation, storage = 6)
    # VAGMD3_cost = VAGMD_cost(fuel_usage=VAGMD3_out[7]['Value'],Prod =VAGMD3_out[4]['Value'],  sam_coh = lcoh, coh = 0.01, storage_cap = VAGMD3_out[2]['Value'])
    # cost3 = VAGMD3_cost.lcow()    
    csv_writer1.writerow(location_info + [lcoh, CF/1.96, CF, VAGMD1_out[7]['Value'], VAGMD1_out[4]['Value'], cost1[5]['Value'], cost1[2]['Value'], cost1[0]['Value'], cost1[1]['Value']])
    # csv_writer2.writerow(location_info + [lcoh, CF/1.96, CF, VAGMD2_out[7]['Value'], VAGMD2_out[4]['Value'], cost2[5]['Value'], cost2[2]['Value'], cost2[0]['Value'], cost2[1]['Value']])
    # csv_writer3.writerow(location_info + [lcoh, CF/1.96, CF, VAGMD3_out[7]['Value'], VAGMD3_out[4]['Value'], cost3[5]['Value'], cost3[2]['Value'], cost3[0]['Value'], cost3[1]['Value']])

    progress += 1
    if progress%5 == 0:
        print('Progress: ', round(progress/len(files)*100,1), '%', 'Processing time: ', round((time.time()-start_time)/60,1), 'min')
        
data_file1.close()   
# data_file2.close()   
# data_file3.close() 
#%% Run VAGMD for the map
## IPH-parabolic trough
from VAGMD_PSA import VAGMD_PSA
from VAGMD_cost import VAGMD_cost
import os
import time
US_solar_directory = 'D:/PhD/DOE/Sensitivity/US_solar_data/'
files = os.listdir(US_solar_directory)

# csv_outfile1 = 'D:/PhD/DOE/Sensitivity/11US_PT_VAGMD(SM=1.59).csv'
# csv_outfile2 = 'D:/PhD/DOE/Sensitivity/US_PT_VAGMD(SM=1.59,10hr).csv'
csv_outfile3 = 'D:/PhD/DOE/Sensitivity/US_PT_VAGMD(SM=1.59,10hr,fossil).csv'
# data_file1 = open(csv_outfile1, 'w', newline='')
# data_file2 = open(csv_outfile2, 'w', newline='') 
data_file3 = open(csv_outfile3, 'w', newline='')
# csv_writer1 = csv.writer(data_file1)
# csv_writer2 = csv.writer(data_file2)
csv_writer3 = csv.writer(data_file3)
# csv_writer1.writerow(["City", "State", "Country", "Latitude", "Longitude", "LCOH from solar field", "Capacity Factor", "% of solar energy", "% of external energy", "Water production", "Cost of heat per unit", "LCOW", "CAPEX", "OPEX"])
# csv_writer2.writerow(["City", "State", "Country", "Latitude", "Longitude", "LCOH from solar field", "Capacity Factor", "% of solar energy", "% of external energy", "Water production", "Cost of heat per unit", "LCOW", "CAPEX", "OPEX"])
csv_writer3.writerow(["City", "State", "Country", "Latitude", "Longitude", "LCOH from solar field", "Capacity Factor", "% of solar energy", "% of external energy", "Water production", "Cost of heat per unit", "LCOW", "CAPEX", "OPEX"])
start_time = time.time()
progress = 0
for path in files:
    weatherfile_path = US_solar_directory + path
    location_info, ave_info, seasonal_info = weather_info(weatherfile_path)     
    generation, lcoh, CF = IPH_parabolic(weatherfile_path)

    # VAGMD1 = VAGMD_PSA(Fossil_f = 0)
    # VAGMD1.design()
    # try:
    #     VAGMD1_out = VAGMD1.simulation(gen = generation, storage = 0)
    #     VAGMD1_cost = VAGMD_cost(fuel_usage=VAGMD1_out[7]['Value'],Prod =VAGMD1_out[4]['Value'], sam_coh = lcoh, coh = 0.01, storage_cap = VAGMD1_out[2]['Value'])
    #     cost1 = VAGMD1_cost.lcow()
    #     csv_writer1.writerow(location_info + [lcoh, CF/1.59, CF, VAGMD1_out[7]['Value'], VAGMD1_out[4]['Value'], cost1[5]['Value'], cost1[2]['Value'], cost1[0]['Value'], cost1[1]['Value']])

    # except:
    #     csv_writer1.writerow(location_info + ['Nah', 'Nah', 'Nah', 'Nah', 'Nah'])
        
    # VAGMD2 = VAGMD_PSA(Fossil_f = 0)
    # VAGMD2.design()
    # try:
    #     VAGMD2_out = VAGMD2.simulation(gen = generation, storage = 0)
    #     VAGMD2_cost = VAGMD_cost(fuel_usage=VAGMD2_out[7]['Value'],Prod =VAGMD2_out[4]['Value'], sam_coh = lcoh, coh = 0.01, storage_cap = VAGMD2_out[2]['Value'])
    #     cost2 = VAGMD2_cost.lcow()
    #     csv_writer2.writerow(location_info + [lcoh, CF/1.59, CF, VAGMD2_out[7]['Value'], VAGMD2_out[4]['Value'], cost2[5]['Value'], cost2[2]['Value'], cost2[0]['Value'], cost2[1]['Value']])

    # except:
    #     csv_writer2.writerow(location_info + ['Nah', 'Nah', 'Nah', 'Nah', 'Nah'])

    VAGMD3 = VAGMD_PSA(Fossil_f = 1)
    VAGMD3.design()
    
    try:
        VAGMD3_out = VAGMD3.simulation(gen = generation, storage = 0)
        VAGMD3_cost = VAGMD_cost(fuel_usage=VAGMD3_out[7]['Value'],Prod =VAGMD3_out[4]['Value'],  sam_coh = lcoh, coh = 0.01, storage_cap = 0)
        cost3 = VAGMD3_cost.lcow()
        csv_writer3.writerow(location_info + [lcoh, CF/1.59, CF, VAGMD3_out[7]['Value'], VAGMD3_out[4]['Value'], cost3[5]['Value'], cost3[2]['Value'], cost3[0]['Value'], cost3[1]['Value']])
 
    except:
        csv_writer3.writerow(location_info + ['Nah', 'Nah', 'Nah', 'Nah', 'Nah'])

    progress += 1
    if progress%5 == 0:
        print('Progress: ', round(progress/len(files)*100,1), '%', 'Processing time: ', round((time.time()-start_time)/60,1), 'min')
    

# data_file1.close()   
# data_file2.close()   
data_file3.close()   


#%% IPH_LFDS (5MW, actual thermal output: 8.54MW, solar multiple: 1.77)
from PySSC import PySSC
def IPH_LFDS_2(weatherfile_path):
    if __name__ == "__main__":
    	ssc = PySSC()
    	# print ('Current folder = D:/PhD/DOE/Sensitivity')
    	# print ('SSC Version = ', ssc.version())
    	# print ('SSC Build Information = ', ssc.build_info().decode("utf - 8"))
    	data = ssc.data_create()
    	ssc.data_set_string( data, b'file_name',  b'' + weatherfile_path.encode("ascii", "backslashreplace"));
    	ssc.data_set_number( data, b'I_bn_des', 950 )
    	ssc.data_set_number( data, b'T_cold_ref', 100 )
    	ssc.data_set_number( data, b'P_turb_des', 20 )
    	ssc.data_set_number( data, b'T_hot', 393 )
    	ssc.data_set_number( data, b'x_b_des', 0.75 )
    	ssc.data_set_number( data, b'q_pb_des', 4.8200000000000003 )
    	ssc.data_set_number( data, b'fP_hdr_c', 0.01 )
    	ssc.data_set_number( data, b'fP_sf_boil', 0.074999999999999997 )
    	ssc.data_set_number( data, b'fP_hdr_h', 0.025000000000000001 )
    	ssc.data_set_number( data, b'nModBoil', 6 )
    	ssc.data_set_number( data, b'nLoops', 4 )
    	ssc.data_set_number( data, b'eta_pump', 0.84999999999999998 )
    	ssc.data_set_number( data, b'theta_stow', 10 )
    	ssc.data_set_number( data, b'theta_dep', 10 )
    	ssc.data_set_number( data, b'T_fp', 10 )
    	ssc.data_set_number( data, b'Pipe_hl_coef', 0.0035000000000000001 )
    	ssc.data_set_number( data, b'SCA_drives_elec', 0.20000000000000001 )
    	ssc.data_set_number( data, b'ColAz', 0 )
    	ssc.data_set_number( data, b'e_startup', 2.7000000000000002 )
    	ssc.data_set_number( data, b'T_amb_des_sf', 42 )
    	ssc.data_set_number( data, b'V_wind_max', 20 )
    	ssc.data_set_number( data, b'csp.lf.sf.water_per_wash', 0.02 )
    	ssc.data_set_number( data, b'csp.lf.sf.washes_per_year', 12 )
    	A_aperture = [[ 513.60000000000002 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'A_aperture', A_aperture );
    	L_col = [[ 44.799999999999997 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'L_col', L_col );
    	OptCharType = [[ 1 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'OptCharType', OptCharType );
    	IAM_T = [[ 0.98960000000000004,   0.043999999999999997,   -0.072099999999999997,   -0.23269999999999999,   0 ], [ 0,   0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'IAM_T', IAM_T );
    	IAM_L = [[ 1.0031000000000001,   -0.22589999999999999,   0.53680000000000005,   -1.6434,   0.72219999999999995 ], [ 0,   0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'IAM_L', IAM_L );
    	TrackingError = [[ 1 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'TrackingError', TrackingError );
    	GeomEffects = [[ 0.83999999999999997 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'GeomEffects', GeomEffects );
    	rho_mirror_clean = [[ 0.93500000000000005 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'rho_mirror_clean', rho_mirror_clean );
    	dirt_mirror = [[ 0.94999999999999996 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'dirt_mirror', dirt_mirror );
    	error = [[ 1 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'error', error );
    	HLCharType = [[ 1 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'HLCharType', HLCharType );
    	HL_dT = [[ 0,   0.67200000000000004,   0.0025560000000000001,   0,   0 ], [ 0,   0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'HL_dT', HL_dT );
    	HL_W = [[ 1,   0,   0,   0,   0 ], [ 0,   0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'HL_W', HL_W );
    	D_2 = [[ 0.066000000000000003 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'D_2', D_2 );
    	D_3 = [[ 0.070000000000000007 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'D_3', D_3 );
    	D_4 = [[ 0.115 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'D_4', D_4 );
    	D_5 = [[ 0.12 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'D_5', D_5 );
    	D_p = [[ 0 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'D_p', D_p );
    	Rough = [[ 4.5000000000000003e-05 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'Rough', Rough );
    	Flow_type = [[ 1 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'Flow_type', Flow_type );
    	AbsorberMaterial = [[ 1 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'AbsorberMaterial', AbsorberMaterial );
    	HCE_FieldFrac = [[ 0.98499999999999999,   0.01,   0.0050000000000000001,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'HCE_FieldFrac', HCE_FieldFrac );
    	alpha_abs = [[ 0.95999999999999996,   0.95999999999999996,   0.80000000000000004,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'alpha_abs', alpha_abs );
    	b_eps_HCE1 = [[ 0 ], [ 0.1384 ]];
    	ssc.data_set_matrix( data, b'b_eps_HCE1', b_eps_HCE1 );
    	b_eps_HCE2 = [[ 0 ], [ 0.65000000000000002 ]];
    	ssc.data_set_matrix( data, b'b_eps_HCE2', b_eps_HCE2 );
    	b_eps_HCE3 = [[ 0 ], [ 0.65000000000000002 ]];
    	ssc.data_set_matrix( data, b'b_eps_HCE3', b_eps_HCE3 );
    	b_eps_HCE4 = [[ 0 ], [ 0.1384 ]];
    	ssc.data_set_matrix( data, b'b_eps_HCE4', b_eps_HCE4 );
    	sh_eps_HCE1 = [[ 0 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'sh_eps_HCE1', sh_eps_HCE1 );
    	sh_eps_HCE2 = [[ 0 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'sh_eps_HCE2', sh_eps_HCE2 );
    	sh_eps_HCE3 = [[ 0 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'sh_eps_HCE3', sh_eps_HCE3 );
    	sh_eps_HCE4 = [[ 0 ], [ 0 ]];
    	ssc.data_set_matrix( data, b'sh_eps_HCE4', sh_eps_HCE4 );
    	alpha_env = [[ 0.02,   0.02,   0,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'alpha_env', alpha_env );
    	EPSILON_4 = [[ 0.85999999999999999,   0.85999999999999999,   1,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'EPSILON_4', EPSILON_4 );
    	Tau_envelope = [[ 0.96299999999999997,   0.96299999999999997,   1,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'Tau_envelope', Tau_envelope );
    	GlazingIntactIn = [[ 1,   1,   0,   1 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'GlazingIntactIn', GlazingIntactIn );
    	AnnulusGas = [[ 1,   1,   1,   1 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'AnnulusGas', AnnulusGas );
    	P_a = [[ 0.0001,   750,   750,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'P_a', P_a );
    	Design_loss = [[ 150,   1100,   1500,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'Design_loss', Design_loss );
    	Shadowing = [[ 0.95999999999999996,   0.95999999999999996,   0.95999999999999996,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'Shadowing', Shadowing );
    	Dirt_HCE = [[ 0.97999999999999998,   0.97999999999999998,   1,   0 ], [ 0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'Dirt_HCE', Dirt_HCE );
    	b_OpticalTable = [[ -180,   -160,   -140,   -120,   -100,   -80,   -60,   -40,   -20,   0,   20,   40,   60,   80,   100,   120,   140,   160,   180,   -999.89999999999998 ], [ 0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1 ], [ 10,   0.97999999999999998,   0.97444500000000001,   0.97197599999999995,   0.97284700000000002,   0.97690999999999995,   0.97690999999999995,   0.97284700000000002,   0.97197599999999995,   0.97444500000000001,   0.97999999999999998,   0.97444500000000001,   0.97197599999999995,   0.97284700000000002,   0.97690999999999995,   0.97690999999999995,   0.97284700000000002,   0.97197599999999995,   0.97444500000000001,   0.97999999999999998 ], [ 20,   0.93000000000000005,   0.92297600000000002,   0.92893000000000003,   0.94600499999999998,   0.95401899999999995,   0.95401899999999995,   0.94600499999999998,   0.92893000000000003,   0.92297600000000002,   0.93000000000000005,   0.92297600000000002,   0.92893000000000003,   0.94600499999999998,   0.95401899999999995,   0.95401899999999995,   0.94600499999999998,   0.92893000000000003,   0.92297600000000002,   0.93000000000000005 ], [ 30,   0.83999999999999997,   0.83861799999999997,   0.87069099999999999,   0.91302099999999997,   0.94091100000000005,   0.94091100000000005,   0.91302099999999997,   0.87069099999999999,   0.83861799999999997,   0.83999999999999997,   0.83861799999999997,   0.87069099999999999,   0.91302099999999997,   0.94091100000000005,   0.94091100000000005,   0.91302099999999997,   0.87069099999999999,   0.83861799999999997,   0.83999999999999997 ], [ 40,   0.71999999999999997,   0.72994700000000001,   0.80368700000000004,   0.86696099999999998,   0.90003900000000003,   0.90003900000000003,   0.86696099999999998,   0.80368700000000004,   0.72994700000000001,   0.71999999999999997,   0.72994700000000001,   0.80368700000000004,   0.86696099999999998,   0.90003900000000003,   0.90003900000000003,   0.86696099999999998,   0.80368700000000004,   0.72994700000000001,   0.71999999999999997 ], [ 50,   0.55000000000000004,   0.59125499999999998,   0.70745400000000003,   0.79350900000000002,   0.83955999999999997,   0.83955999999999997,   0.79350900000000002,   0.70745400000000003,   0.59125499999999998,   0.55000000000000004,   0.59125499999999998,   0.70745400000000003,   0.79350900000000002,   0.83955999999999997,   0.83955999999999997,   0.79350900000000002,   0.70745400000000003,   0.59125499999999998,   0.55000000000000004 ], [ 60,   0.34000000000000002,   0.43217800000000001,   0.59747799999999995,   0.66400599999999999,   0.69351099999999999,   0.69351099999999999,   0.66400599999999999,   0.59747799999999995,   0.43217800000000001,   0.34000000000000002,   0.43217800000000001,   0.59747799999999995,   0.66400599999999999,   0.69351099999999999,   0.69351099999999999,   0.66400599999999999,   0.59747799999999995,   0.43217800000000001,   0.34000000000000002 ], [ 70,   0.13,   0.26525399999999999,   0.42558600000000002,   0.46449600000000002,   0.47710599999999997,   0.47710599999999997,   0.46449600000000002,   0.42558600000000002,   0.26525399999999999,   0.13,   0.26525399999999999,   0.42558600000000002,   0.46449600000000002,   0.47710599999999997,   0.47710599999999997,   0.46449600000000002,   0.42558600000000002,   0.26525399999999999,   0.13 ], [ 80,   0.01,   0.113694,   0.20891000000000001,   0.23325499999999999,   0.23882800000000001,   0.23882800000000001,   0.23325499999999999,   0.20891000000000001,   0.113694,   0.01,   0.113694,   0.20891000000000001,   0.23325499999999999,   0.23882800000000001,   0.23882800000000001,   0.23325499999999999,   0.20891000000000001,   0.113694,   0.01 ], [ 90,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0 ]];
    	ssc.data_set_matrix( data, b'b_OpticalTable', b_OpticalTable );
    	sh_OpticalTable = [[ 0,   0 ], [ 0,   0 ]];
    	ssc.data_set_matrix( data, b'sh_OpticalTable', sh_OpticalTable );
    	ssc.data_set_number( data, b'heat_sink_dP_frac', 0.01 )
    	ssc.data_set_number( data, b'adjust:constant', 4 )
    	module = ssc.module_create(b'linear_fresnel_dsg_iph')	
    	ssc.module_exec_set_print( 0 );
    	if ssc.module_exec(module, data) == 0:
    		print ('linear_fresnel_dsg_iph simulation error')
    		idx = 1
    		msg = ssc.module_log(module, 0)
    		while (msg != None):
    			print ('	: ' + msg.decode("utf - 8"))
    			msg = ssc.module_log(module, idx)
    			idx = idx + 1
    		SystemExit( "Simulation Error" );
    	ssc.module_free(module)
    	ssc.data_set_number( data, b'electricity_rate', 0.059999999999999998 )
    	ssc.data_set_number( data, b'fixed_operating_cost', 68251.1953125 )
    	module = ssc.module_create(b'iph_to_lcoefcr')	
    	ssc.module_exec_set_print( 0 );
    	if ssc.module_exec(module, data) == 0:
    		print ('iph_to_lcoefcr simulation error')
    		idx = 1
    		msg = ssc.module_log(module, 0)
    		while (msg != None):
    			print ('	: ' + msg.decode("utf - 8"))
    			msg = ssc.module_log(module, idx)
    			idx = idx + 1
    		SystemExit( "Simulation Error" );
    	ssc.module_free(module)
    	ssc.data_set_number( data, b'capital_cost', 4777583.5 )
    	ssc.data_set_number( data, b'variable_operating_cost', 0.0010000000474974513 )
    	ssc.data_set_number( data, b'fixed_charge_rate', 0.055353961884975433 )
    	module = ssc.module_create(b'lcoefcr')	
    	ssc.module_exec_set_print( 0 );
    	if ssc.module_exec(module, data) == 0:
    		print ('lcoefcr simulation error')
    		idx = 1
    		msg = ssc.module_log(module, 0)
    		while (msg != None):
    			print ('	: ' + msg.decode("utf - 8"))
    			msg = ssc.module_log(module, idx)
    			idx = idx + 1
    		SystemExit( "Simulation Error" );
    	ssc.module_free(module)
    	annual_energy = ssc.data_get_number(data, b'annual_energy');
    	annual_gross_energy = ssc.data_get_number(data, b'annual_gross_energy');
    	annual_thermal_consumption = ssc.data_get_number(data, b'annual_thermal_consumption');
    	capacity_factor = ssc.data_get_number(data, b'capacity_factor');
    	annual_electricity_consumption = ssc.data_get_number(data, b'annual_electricity_consumption');
    	lcoe_fcr = ssc.data_get_number(data, b'lcoe_fcr');
    	gen = ssc.data_get_array(data, b'gen')
    	ssc.data_free(data);
    	# print(type(gen))
    	return gen, lcoe_fcr, capacity_factor

#%% LFDS + LT_MED / MED-TVC
from LT_MED_General import lt_med_general
from LTMED_cost import LTMED_cost
import os
import time
import csv
US_solar_directory = 'D:/PhD/DOE/Sensitivity/US_solar_data/'
files = os.listdir(US_solar_directory)

csv_outfile1 = 'D:/PhD/DOE/Sensitivity/US_LFDS_LTMED(SM=1.77).csv'
csv_outfile2 = 'D:/PhD/DOE/Sensitivity/US_LFDS_LTMED(SM=1.77,6hr).csv'
csv_outfile3 = 'D:/PhD/DOE/Sensitivity/US_LFDS_LTMED(SM=1.77,6hr,fossil).csv'

data_file1 = open(csv_outfile1, 'w', newline='')
data_file2 = open(csv_outfile2, 'w', newline='') 
data_file3 = open(csv_outfile3, 'w', newline='') 

csv_writer1 = csv.writer(data_file1)
csv_writer2 = csv.writer(data_file2)
csv_writer3 = csv.writer(data_file3)

csv_writer1.writerow(["City", "State", "Country", "Latitude", "Longitude", "LCOH from solar field", "Capacity Factor", "% of solar energy", "% of external energy", "Water production", "Cost of heat per unit", "LCOW", "CAPEX", "OPEX"])
csv_writer2.writerow(["City", "State", "Country", "Latitude", "Longitude", "LCOH from solar field", "Capacity Factor", "% of solar energy", "% of external energy", "Water production", "Cost of heat per unit", "LCOW", "CAPEX", "OPEX"])
csv_writer3.writerow(["City", "State", "Country", "Latitude", "Longitude", "LCOH from solar field", "Capacity Factor", "% of solar energy", "% of external energy", "Water production", "Cost of heat per unit", "LCOW", "CAPEX", "OPEX"])

start_time = time.time()
progress = 0
for path in files:
    weatherfile_path = US_solar_directory + path
    location_info, ave_info, seasonal_info = weather_info(weatherfile_path)     
    generation, lcoh, CF = IPH_LFDS_2(weatherfile_path)
    LTMED1 = lt_med_general(Fossil_f = 0)
    LTMED1.design()
    LTMED1_out = LTMED1.simulation(gen = generation, storage = 0)
    LTMED2_out = LTMED1.simulation(gen = generation, storage = 6)    
    LTMED1_cost = LTMED_cost(fuel_usage=LTMED1_out[7]['Value'],Prod =LTMED1_out[4]['Value'],  sam_coh = lcoh, coh = 0.01, storage_cap = 0)
    LTMED2_cost = LTMED_cost(fuel_usage=LTMED2_out[7]['Value'],Prod =LTMED2_out[4]['Value'],  sam_coh = lcoh, coh = 0.01, storage_cap = LTMED2_out[2]['Value'])
    cost1 = LTMED1_cost.lcow()
    cost2 = LTMED2_cost.lcow()
    
    LTMED2 = lt_med_general(Fossil_f = 1)
    LTMED2.design()
    LTMED3_out = LTMED2.simulation(gen = generation, storage = 6)
    LTMED3_cost = LTMED_cost(fuel_usage=LTMED3_out[7]['Value'],Prod =LTMED3_out[4]['Value'],  sam_coh = lcoh, coh = 0.01, storage_cap = LTMED3_out[2]['Value'])
   
    cost3 = LTMED3_cost.lcow()    
    
    csv_writer1.writerow(location_info + [lcoh, CF/1.77, CF,  LTMED1_out[7]['Value'], LTMED1_out[4]['Value'], cost1[5]['Value'], cost1[2]['Value'], cost1[0]['Value'], cost1[1]['Value']])
    csv_writer2.writerow(location_info + [lcoh, CF/1.77, CF,  LTMED2_out[7]['Value'], LTMED2_out[4]['Value'], cost2[5]['Value'], cost2[2]['Value'], cost2[0]['Value'], cost2[1]['Value']])
    csv_writer3.writerow(location_info + [lcoh, CF/1.77, CF,  LTMED3_out[7]['Value'], LTMED3_out[4]['Value'], cost3[5]['Value'], cost3[2]['Value'], cost3[0]['Value'], cost3[1]['Value']])

    progress += 1
    if progress%5 ==0:
        print('Progress: ', round(progress/len(files)*100,1), '%', 'Processing time: ', round((time.time()-start_time)/60,1), 'min')
        
data_file1.close()   
data_file2.close()   
data_file3.close()

#%% Run LTMED for the map
## IPH-parabolic trough
from LT_MED_General import lt_med_general
from LTMED_cost import LTMED_cost
import os
import time
import csv
US_solar_directory = 'D:/PhD/DOE/Sensitivity/US_solar_data/'
files = os.listdir(US_solar_directory)

# csv_outfile1 = 'D:/PhD/DOE/Sensitivity/US_PT_LTMED(SM=1.08).csv'
csv_outfile2 = 'D:/PhD/DOE/Sensitivity/US_PT_LTMED(SM=1.8,10hr).csv'
csv_outfile3 = 'D:/PhD/DOE/Sensitivity/US_PT_LTMED(SM=1.8,10hr,fossil).csv'
# data_file1 = open(csv_outfile1, 'w', newline='')
data_file2 = open(csv_outfile2, 'w', newline='') 
data_file3 = open(csv_outfile3, 'w', newline='')
# csv_writer1 = csv.writer(data_file1)
csv_writer2 = csv.writer(data_file2)
csv_writer3 = csv.writer(data_file3)
# csv_writer1.writerow(["City", "State", "Country", "Latitude", "Longitude", "LCOH from solar field", "Capacity Factor", "% of solar energy", "% of external energy",  "Water production", "Cost of heat per unit", "LCOW", "CAPEX", "OPEX"])
csv_writer2.writerow(["City", "State", "Country", "Latitude", "Longitude", "LCOH from solar field", "Capacity Factor", "% of solar energy", "% of external energy",  "Water production", "Cost of heat per unit", "LCOW", "CAPEX", "OPEX"])
csv_writer3.writerow(["City", "State", "Country", "Latitude", "Longitude", "LCOH from solar field", "Capacity Factor", "% of solar energy", "% of external energy",  "Water production", "Cost of heat per unit", "LCOW", "CAPEX", "OPEX"])
start_time = time.time()
progress = 0
for path in files:
    weatherfile_path = US_solar_directory + path
    location_info, ave_info, seasonal_info = weather_info(weatherfile_path)     
    generation, lcoh, CF = IPH_parabolic(weatherfile_path)

    # LTMED1 = lt_med_general(Fossil_f = 0)
    # LTMED1.design()
    # try:
    #     LTMED1_out = LTMED1.simulation(gen = generation, storage = 0)
    #     LTMED1_cost = LTMED_cost(fuel_usage=LTMED1_out[7]['Value'],Prod =LTMED1_out[4]['Value'], sam_coh = lcoh, coh = 0.01, storage_cap = LTMED1_out[2]['Value'])
    #     cost1 = LTMED1_cost.lcow()
    #     csv_writer1.writerow(location_info + [lcoh, CF/1.08, CF, LTMED1_out[7]['Value'], LTMED1_out[4]['Value'], cost1[5]['Value'], cost1[2]['Value'], cost1[0]['Value'], cost1[1]['Value']])

    # except:
    #     csv_writer1.writerow(location_info + ['Nah', 'Nah', 'Nah', 'Nah', 'Nah'])
        
    LTMED2 = lt_med_general(Fossil_f = 0)
    LTMED2.design()
    try:
        LTMED2_out = LTMED2.simulation(gen = generation, storage = 0)
        LTMED2_cost = LTMED_cost(fuel_usage=LTMED2_out[7]['Value'],Prod =LTMED2_out[4]['Value'], sam_coh = lcoh, coh = 0.01, storage_cap = LTMED2_out[2]['Value'])
        cost2 = LTMED2_cost.lcow()
        csv_writer2.writerow(location_info + [lcoh, CF/1.8, CF, LTMED2_out[7]['Value'], LTMED2_out[4]['Value'], cost2[5]['Value'], cost2[2]['Value'], cost2[0]['Value'], cost2[1]['Value']])

    except:
        csv_writer2.writerow(location_info + ['Nah', 'Nah', 'Nah', 'Nah', 'Nah'])
        
    LTMED3 = lt_med_general(Fossil_f = 1)
    LTMED3.design()
    try:
        LTMED3_out = LTMED3.simulation(gen = generation, storage = 0)
        LTMED3_cost = LTMED_cost(fuel_usage=LTMED3_out[7]['Value'],Prod =LTMED3_out[4]['Value'], sam_coh = lcoh, coh = 0.01, storage_cap = LTMED3_out[2]['Value'])
        cost3 = LTMED3_cost.lcow()
        csv_writer3.writerow(location_info + [lcoh, CF/1.8, CF, LTMED3_out[7]['Value'], LTMED3_out[4]['Value'], cost3[5]['Value'], cost3[2]['Value'], cost3[0]['Value'], cost3[1]['Value']])

    except:
        csv_writer3.writerow(location_info + ['Nah', 'Nah', 'Nah', 'Nah', 'Nah'])

    progress += 1
    if progress%5 == 0:
        print('Progress: ', round(progress/len(files)*100,1), '%', 'Processing time: ', round((time.time()-start_time)/60,1), 'min')
    

# data_file1.close()   
data_file2.close()   
data_file3.close()   