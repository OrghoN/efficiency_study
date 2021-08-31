###############################################################################
# Author: Thomas McDowell
# Date: August 31, 2021
# DescripTion: A generator-level monte carlo simulation to study K0sK0s ->
# pi+pi-pi+pi- events
#
###############################################################################

# libraries
import sys
import numpy as np
import math
from matplotlib import pyplot as plt

# PIDs used within the simulaiton
K0s_ID = 310
PI_POS_ID = 211
PI_NEG_ID = -211
PROTON_ID = 2212
group_number = 1

# set config options
cfg = open( "Makefile.inc" )
lib = "../lib"
for line in cfg:
        if line.startswith( "PREFIX_LIB=" ): lib = line[11:-1]; break
sys.path.insert(0, lib)

# create files to store particle data
# csv file for event efficiency and error on event efficiency
event_eff_err = open( "event_eff_err.csv", "w" )
# csv file for min event pT, max event pT, max absolute value of eta in event
min_max_cut1 = open( "min_max_cut1.csv", "w" )
min_max_cut2 = open( "min_max_cut2.csv", "w" )
min_max_cut3 = open( "min_max_cut3.csv", "w" )
pion_pT_eta = open( "pion_pT_eta.csv", "w" )
proton_p_vals = open( "proton_p_vals.csv", "w" )

# SIMULATION INITIALIZATION
import pythia8
pythia = pythia8.Pythia()
pythia.readFile( "mymain04.cmnd" )
pythia.init()

# K0sK0sFilter is a class to filter out unwanted events and store events
# of interest
class K0sK0sFilter:
    # constructor
    def __init__( self ):
        self.min_pT = 0.05 # GeV
        self.max_pT = 2.50 # GeV
        self.max_abs_eta = 2.50
        self.event_count = 0
        self.event_set = set([])
        self.proton_set = set([])
        self.K0s_set = set([])
        self.K0s_pairs = []
        self.event_pions = []
    
    # filterEvent filters out events without K0sK0s -> pi+pi-pi+pi- decay
    def filterEvent( self, event ):
        global K0s_ID

        if self.isK0sK0sEvent( event ):
            self.event_set.add( event )

    # isK0sK0sEvent inspects an event an determines if it contains a
    # K0sK0s -> pi+pi-pi+pi- decay pattern. Does the heavy lifting for
    # event selection
    def isK0sK0sEvent( self, event ):
        global K0s_ID
        global PI_POS_ID
        global PROTON_ID
        global group_number

        for prt in event:
            # set check ensures no double counting
            if ( prt.id() == K0s_ID ) and ( prt not in self.K0s_set ):
                valid_K0s = []
                for mother in prt.motherList():
                    cur_mother = pythia.event[mother]
                    for K0s in cur_mother.daughterList():
                        cur_K0s = pythia.event[K0s]
                        if ( cur_K0s.id() == K0s_ID ) and ( self.checkPionDecay( cur_K0s ) )\
                          and ( cur_K0s not in valid_K0s ):
                            valid_K0s.append( cur_K0s )

                # make sure event has two K0s
                if ( len( valid_K0s ) == 2 ):
                    pion_group = []
                    for K0s in valid_K0s:
                        for pion in K0s.daughterList():
                            cur_pion = pythia.event[pion]
                            # check pion decay. if decay is valid, add pions to list of pion groups
                            if ( cur_pion.idAbs() == PI_POS_ID ) and ( self.checkThresholds( cur_pion ) ):
                                pion_group.append( cur_pion )

                    if ( len( pion_group ) == 4 ):
                       # UNCOMMENT FOR DEBUGGING PURPOSES
                       # print( "Pion group " + str( group_number ) + " :" )
                       # for i in range( len( pion_group ) ):
                       #     print( "pion " + str( i ) + ':' )
                       #     print( "| pT: " + str( pion_group[i].pT() )\
                       #                 + " | eta: " + str( pion_group[i].eta() ) + " |" )
                        
                        # if event is valid, append particles to lists
                        self.K0s_pairs.append( valid_K0s )
                        self.K0s_set.add( valid_K0s[0] )
                        self.K0s_set.add( valid_K0s[1] )
                        self.recordPionData( pion_group )
                        group_number += 1

                        # search valid K0sK0s -> pi+pi-pi+pi- event for diffractively and
                        # elastically scattered protons
                        for proton in event:
                            if ( ( proton.id() == PROTON_ID ) and ( ( proton.status() == 14 ) or ( proton.status() == 15 ) ) ):
                                self.proton_set.add( proton )
                        return True
        return False

    # recordData records particle data after event generation and filtering
    def recordPionData( self, pion_group ):
        global event_eff_err
        global min_max_cut1
        global min_max_cut2
        global min_max_cut3
        global pi_pT_eta

        event_prt_efficiencies = [ 0, 0, 0, 0 ]
        event_efficiency_errors = [ 0, 0, 0, 0 ]
        event_momentum_list = [ 0, 0, 0, 0 ]
        event_energy_list = [ 0, 0, 0, 0 ]
        event_prt_inv_masses = [ 0, 0, 0, 0 ]
        event_err = 0
        event_fract_err = 0

        # set efficiency and error for each pi+ and pi- ( or each track ) to
        # values corresponding to those in the analysis note
        for i in range( len( pion_group ) ):

            if pion_group[i].pT() >= 0.05 and pion_group[i].pT() < 0.10:
                event_prt_efficiencies[i] = 0.40
                event_efficiency_errors[i] = 0.05

            if pion_group[i].pT() >= 0.10 and pion_group[i].pT() < 0.15:
                event_prt_efficiencies[i] = 0.66
                event_efficiency_errors[i] = 0.06

            if pion_group[i].pT() >= 0.15 and pion_group[i].pT() < 0.20:
                event_prt_efficiencies[i] = 0.79
                event_efficiency_errors[i] = 0.05

            if pion_group[i].pT() >= 0.20 and pion_group[i].pT() < 0.25:
                event_prt_efficiencies[i] = 0.88
                event_efficiency_errors[i] = 0.02

            if pion_group[i].pT() >= 0.25 and pion_group[i].pT() < 0.30:
                event_prt_efficiencies[i] = 0.89
                event_efficiency_errors[i] = 0.01

            if pion_group[i].pT() >= 0.30 and pion_group[i].pT() < 0.35:
                event_prt_efficiencies[i] = 0.88
                event_efficiency_errors[i] = 0.01

            if pion_group[i].pT() >= 0.35 and pion_group[i].pT() < 0.40:
                event_prt_efficiencies[i] = 0.89
                event_efficiency_errors[i] = 0.01

            if pion_group[i].pT() >= 0.40 and pion_group[i].pT() < 0.50:
                event_prt_efficiencies[i] = 0.92
                event_efficiency_errors[i] = 0.005

            if pion_group[i].pT() >= 0.50 and pion_group[i].pT() < 0.55:
                event_prt_efficiencies[i] = 0.94
                event_efficiency_errors[i] = 0.005

            if pion_group[i].pT() >= 0.55 and pion_group[i].pT() < 0.70:
                event_prt_efficiencies[i] = 0.95
                event_efficiency_errors[i] = 0.005

            if pion_group[i].pT() >= 0.70 and pion_group[i].pT() < 0.85:
                event_prt_efficiencies[i] = 0.96
                event_efficiency_errors[i] = 0.005

            if pion_group[i].pT() >= 0.85 and pion_group[i].pT() < 1.00:
                event_prt_efficiencies[i] = 0.97
                event_efficiency_errors[i] = 0.005

            if pion_group[i].pT() >= 1.00 and pion_group[i].pT() < 1.35:
                event_prt_efficiencies[i] = 0.96
                event_efficiency_errors[i] = 0.005

            if pion_group[i].pT() >= 1.35 and pion_group[i].pT() < 1.40:
                event_prt_efficiencies[i] = 0.99
                event_efficiency_errors[i] = 0.005

            if pion_group[i].pT() >= 1.40 and pion_group[i].pT() < 1.50:
                event_prt_efficiencies[i] = 0.97
                event_efficiency_errors[i] = 0.01

            if pion_group[i].pT() >= 1.50 and pion_group[i].pT() < 1.55:
                event_prt_efficiencies[i] = 0.96
                event_efficiency_errors[i] = 0.02

            if pion_group[i].pT() >= 1.55 and pion_group[i].pT() < 1.60:
                event_prt_efficiencies[i] = 0.91
                event_efficiency_errors[i] = 0.04

            if pion_group[i].pT() >= 1.60 and pion_group[i].pT() < 1.70:
                event_prt_efficiencies[i] = 0.95
                event_efficiency_errors[i] = 0.04

            if pion_group[i].pT() >= 1.70 and pion_group[i].pT() < 1.75:
                event_prt_efficiencies[i] = 1.00
                event_efficiency_errors[i] = 0

            if pion_group[i].pT() >= 1.75 and pion_group[i].pT() < 1.80:
                event_prt_efficiencies[i] = 0.97
                event_efficiency_errors[i] = 0.04

            if pion_group[i].pT() >= 1.80:
                event_prt_efficiencies[i] = 1.00
                event_efficiency_errors[i] = 0

            event_momentum_list[i] = math.sqrt( pion_group[i].px()**2 + pion_group[i].py()**2 + pion_group[i].pz()**2 )
            event_energy_list[i] = pion_group[i].e()
            pion_pT_eta.write( str( pion_group[i].pT() ) + ',' )
            pion_pT_eta.write( str( pion_group[i].eta() ) + '\n' )

        if 0 not in event_prt_efficiencies:
            # multiply event_contribution by particle efficiencies for event efficiency
            event_efficiency = 1
            for i in range( len( event_prt_efficiencies ) ):
                event_efficiency *= event_prt_efficiencies[i]
                event_fract_err += ( event_efficiency_errors[i] / event_prt_efficiencies[i] )**2

            # add contribution of this K0sK0s event to K0sK0s event count
            self.event_count += event_efficiency

            # write some data to sim_values.txt
            event_eff_err.write( str( event_efficiency ) + ',' )
            event_eff_err.write( str( event_fract_err ) + '\n' )

            # find min pT, max pT, and max abs eta of current pion group
            min_pT = pion_group[0].pT()
            max_pT = pion_group[0].pT()
            max_abs_eta = abs( pion_group[0].eta() )

            for i in range( 1, len( pion_group ) ):
                if pion_group[i].pT() < min_pT:
                    min_pT = pion_group[i].pT()

                if pion_group[i].pT() > max_pT:
                    max_pT = pion_group[i].pT()

                if abs(pion_group[i].eta()) > max_abs_eta:
                    max_abs_eta = abs( pion_group[i].eta() )

            # add values to csv files if they pass the pT and eta cuts
            # max abs eta check is probably redundant
            if ( min_pT >= self.min_pT ) and ( max_abs_eta <= self.max_pT ):
                min_max_cut1.write( str( min_pT ) + ',' )
                min_max_cut1.write( str( max_pT ) + ',' )
                min_max_cut1.write( str( max_abs_eta ) + '\n' )

            if ( min_pT >= self.min_pT ) and ( max_abs_eta <= self.max_pT ):
                min_max_cut2.write( str( min_pT ) + ',' )
                min_max_cut2.write( str( max_pT ) + ',' )
                min_max_cut2.write( str( max_abs_eta ) + '\n' )

            if ( min_pT >= self.min_pT ) and ( max_abs_eta <= self.max_pT ):
                min_max_cut3.write( str( min_pT ) + ',' )
                min_max_cut3.write( str( max_pT ) + ',' )
                min_max_cut3.write( str( max_abs_eta ) + '\n' )

        else:
            self.test_count += 1
            print( "error group efficiencies: " + str( event_prt_efficiencies ) )
            for j in range( len( pion_group ) ):
                if ( event_prt_efficiencies[j] == 0 ):
                    print( "error: pion " + str( j ) + ':' )
                    print( "| pT: " + str( pion_group[j].pT() )\
                            + " | eta: " + str( pion_group[j].eta() ) + " |" )
            self.event_pions.remove( pion_group )


    def recordProtonData( self ):
        global PROTON_ID

        for proton in self.proton_set:
            proton_p_vals.write( str( proton.px() ) + ',' )
            proton_p_vals.write( str( proton.py() ) + ',' )
            proton_p_vals.write( str( proton.pz() ) + '\n' )


    # checkpiondecay checks a K0s for valid pi+pi- decay
    def checkPionDecay( self, K0s ):
        global PI_POS_ID
        global PI_NEG_ID

        pi_plus = 0
        pi_minus = 0
        for daughter in K0s.daughterList():
            prt = pythia.event[daughter]
            if ( prt.id() == PI_POS_ID ) and ( self.checkThresholds( prt ) ):
                pi_plus += 1
            if ( prt.id() == PI_NEG_ID ) and ( self.checkThresholds( prt ) ):
                pi_minus += 1
        if ( pi_plus == 1 ) and ( pi_minus == 1 ):
            return True
        else:
            return False

    # checkThresholds verifies that a particle meets threshold requirements
    def checkThresholds( self, prt ):
        if ( prt.pT() >= self.min_pT ) and ( prt.pT() <= self.max_pT ) and ( abs( prt.eta() ) <= self.max_abs_eta ):
            return True
        else:
            return False


# MAIN LOOP, EVENT GENERATION
nEvent = pythia.mode( "Main:numberOfEvents" )
ef = K0sK0sFilter()
for iEvent in range( 0, nEvent ):
        if not pythia.next(): continue
        ef.filterEvent( pythia.event )
ef.recordProtonData()

# end of loop statistics
pythia.stat()
sigma_info = pythia.info.sigmaGen();
weightSum = pythia.info.weightSum();

print( "Number of valid K0sK0s -> pi+pi-pi+pi- events: " + str( len( ef.event_set ) ) )
print( "Number of events ( with efficiency factor ): " + str( ef.event_count ) )
print( "Number of valid protons: " + str( len( ef.proton_set ) ) )
