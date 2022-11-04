###############################################################################
# sim_hists.py is a script to histogram data that is stored in text files 
# and generated by mymain02.py
#
# Author: Thomas McDowell
# Date: 31/08/2021
# Status: In progress
###############################################################################

# Libraries used
import numpy as np
import math
from matplotlib import pyplot as plt
import csv

pi_max_pT_vals_cut1 = []
pi_max_pT_vals_cut2 = []
pi_max_pT_vals_cut3 = []

pi_min_pT_vals_cut1 = []
pi_min_pT_vals_cut2 = []
pi_min_pT_vals_cut3 = []

pi_max_abs_eta_cut1 = []
pi_max_abs_eta_cut2 = []
pi_max_abs_eta_cut3 = []

pi_pTs  = []
pi_etas = []

K0s_px = []
K0s_py = []
p_total = 0

total_eff_err = 0
average_eff   = 0

with open( 'event_eff_err.csv' ) as eff_file:
    readCSV = csv.reader( eff_file, delimiter = ',' )
    for row in eff_file:
        row_list = row.split(',')
        average_eff += float( row_list[0] )
        total_eff_err += ( float( row_list[1] )**2 )

with open( 'min_max_cut1.csv' ) as cut1_file:
    readCSV = csv.reader( cut1_file, delimiter = ',' )
    for row in cut1_file:
        row_list = row.split( ',' )
        pi_min_pT_vals_cut1.append( float( row_list[0] ) )
        pi_max_pT_vals_cut1.append( float( row_list[1] ) )
        pi_max_abs_eta_cut1.append( float( row_list[2] ) )

with open( 'min_max_cut2.csv' ) as cut2_file:
    readCSV = csv.reader( cut2_file, delimiter = ',' )
    for row in cut2_file:
        row_list = row.split( ',' )
        pi_min_pT_vals_cut2.append( float( row_list[0] ) )
        pi_max_pT_vals_cut2.append( float( row_list[1] ) )
        pi_max_abs_eta_cut2.append( float( row_list[2] ) )

with open( 'min_max_cut3.csv' ) as cut3_file:
    readCSV = csv.reader( cut3_file, delimiter = ',' )
    for row in cut3_file:
        row_list = row.split( ',' )
        pi_min_pT_vals_cut3.append( float( row_list[0] ) )
        pi_max_pT_vals_cut3.append( float( row_list[1] ) )
        pi_max_abs_eta_cut3.append( float( row_list[2] ) )

with open( 'pion_pT_eta.csv' ) as pT_eta_file:
    readCSV = csv.reader( pT_eta_file, delimiter = ',' )
    for row in pT_eta_file:
        row_list = row.split( ',' )
        pi_pTs.append( float( row_list[0] ) )
        pi_etas.append( abs( float( row_list[1] ) ) )

# pyplot histograms
plt.figure(0)

histbins = [ 0.00, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50,
             0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00,
             1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45, 1.50,
             1.55, 1.60, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00 ]

total_eff_err = math.sqrt( total_eff_err )
#average_eff /= NUMBER OF VALID EVENTS GENERATED (WITHOUT EFFICIENCY FACTOR)
average_eff = 0
print("Total Efficiency Error = " + str( total_eff_err ) )
print("average efficiency = " + str( average_eff ) )


plt.figure(0)
plt.figure(0).patch.set_facecolor('white')
plt.xlim( 0, 3 )
plt.hist(pi_max_pT_vals_cut1, bins = histbins)
plt.figtext( 0.6, 0.75, ( "No. Entries = " + str( len( pi_max_pT_vals_cut1 ) ) ) )
plt.title("Max pT of pi+ and pi- in K0K0s Daughter Groups (0.1 GeV cut)")
plt.xlabel("pT (GeV)")
plt.ylabel("Number of pi+ and pi-")

plt.show()

plt.figure(1)
plt.figure(1).patch.set_facecolor('white')
plt.xlim( 0, 3 )
plt.hist(pi_min_pT_vals_cut1, bins = histbins)
plt.figtext( 0.6, 0.75, ( "No. Entries = " + str( len( pi_min_pT_vals_cut1 ) ) ) )
plt.title("Min pT of pi+ and pi- in K0sK0s Daughter Groups (0.1 GeV cut)")
plt.xlabel("pT (GeV)")
plt.ylabel("Number of pi+ and pi-")

plt.show()

plt.figure(2)
plt.figure(2).patch.set_facecolor('white')
plt.hist(pi_max_abs_eta_cut1, bins = 20)
plt.figtext( 0.2, 0.75, ( "No. Entries = " + str( len( pi_max_abs_eta_cut1 ) ) ) )
plt.title("Max Abs. Value of eta for pi+ pi- in K0sK0s Daughter Groups (0.1 GeV cut)")
plt.xlabel("eta")
plt.ylabel("Number of pi+ and pi-")

plt.show()

plt.figure(3)
plt.figure(3).patch.set_facecolor('white')
plt.xlim( 0, 3 )
plt.hist(pi_max_pT_vals_cut2, bins = histbins)
plt.figtext( 0.65, 0.75, ( "No. Entries = " + str( len( pi_max_pT_vals_cut2 ) ) ) )
plt.title("Max pT of pi+ and pi- in K0K0s Daughter Groups (0.5 GeV cut)")
plt.xlabel("pT (GeV)")
plt.ylabel("Number of pi+ and pi-")

plt.show()

plt.figure(4)
plt.figure(4).patch.set_facecolor('white')
plt.xlim( 0, 3 )
plt.hist(pi_min_pT_vals_cut2, bins = histbins)
plt.figtext( 0.6, 0.75, ( "No. Entries = " + str( len( pi_min_pT_vals_cut2 ) ) ) )
plt.title("Min pT of pi+ and pi- in K0sK0s Daughter Groups (0.5 GeV cut)")
plt.xlabel("pT (GeV)")
plt.ylabel("Number of pi+ and pi-")

plt.show()

plt.figure(5)
plt.figure(5).patch.set_facecolor('white')
plt.hist(pi_max_abs_eta_cut2, bins = 20)
plt.figtext( 0.6, 0.75, ( "No. Entries = " + str( len( pi_max_abs_eta_cut2 ) ) ) )
plt.title("Max Abs. Value of eta for pi+ pi- in K0sK0s Daughter Groups (0.5 GeV cut)")
plt.xlabel("eta")
plt.ylabel("Number of pi+ and pi-")

plt.show()

plt.figure(6)
plt.figure(6).patch.set_facecolor('white')
plt.xlim( 0, 3 )
plt.hist(pi_max_pT_vals_cut3, bins = histbins)
plt.figtext( 0.7, 0.75, ( "No. Entries = " + str( len( pi_max_pT_vals_cut3 ) ) ) )
plt.title("Max pT of pi+ and pi- in K0K0s Daughter Groups (1.0 GeV cut)")
plt.xlabel("pT (GeV)")
plt.ylabel("Number of pi+ and pi-")

plt.show()

plt.figure(7)
plt.figure(7).patch.set_facecolor('white')
plt.xlim( 0, 3 )
plt.hist(pi_min_pT_vals_cut3, bins = histbins)
plt.figtext( 0.6, 0.75, ( "No. Entries = " + str( len( pi_min_pT_vals_cut3 ) ) ) )
plt.title("Min pT of pi+ and pi- in K0sK0s Daughter Groups (1.0 GeV cut)")
plt.xlabel("pT (GeV)")
plt.ylabel("Number of pi+ and pi-")

plt.show()

plt.figure(8)
plt.figure(8).patch.set_facecolor('white')
plt.hist(pi_max_abs_eta_cut3, bins = 20)
plt.figtext( 0.7, 0.75, ( "No. Entries = " + str( len( pi_max_abs_eta_cut3 ) ) ) )
plt.title("Max Abs. Value of eta for pi+ pi- in K0sK0s Daughter Groups (1.0 GeV cut)")
plt.xlabel("eta")
plt.ylabel("Number of pi+ and pi-")

plt.show()

plt.figure(9)
plt.figure(9).patch.set_facecolor('white')
plt.hist(pi_pTs, bins = histbins)
plt.figtext( 0.6, 0.75, ( "No. Entries = " + str( len( pi_pTs ) ) ) )
plt.xlim( 0, 3 )
plt.title("pT of pi+ and pi- from K0sK0s Decay")
plt.xlabel("pT (GeV)")
plt.ylabel("Number of pi+ and pi-")

plt.show()

plt.figure(10)
plt.figure(10).patch.set_facecolor('white')
plt.hist(pi_etas, bins = 20)
plt.figtext( 0.6, 0.75, ( "No. Entries = " + str( len( pi_etas ) ) ) )
plt.xlim( 0, 3 )
plt.title("eta of pi+ and pi- from K0sK0s Decay")
plt.xlabel("eta")
plt.ylabel("Number of pi+ and pi-")

plt.show()
