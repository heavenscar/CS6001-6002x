# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from ps3b import *

#
# PROBLEM 1
#        
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    
    # TODO
    viruses = [ResistantVirus(0.1,0.05,{'guttagonol':False},0.005)] * 100
    popA = []
    popB = []
    popC = []
    popD = []
   
    for i in range(numTrials):
        patientA = TreatedPatient(viruses[:], 1000)
        patientB = TreatedPatient(viruses[:], 1000)
        patientC = TreatedPatient(viruses[:], 1000)
        patientD = TreatedPatient(viruses[:], 1000)
       
       
        for j in range(75):
            patientB.update()
           
        for j in range(150):
            patientC.update()
           
        for j in range(300):
            patientD.update()
       
        patientA.addPrescription('guttagonol')
        patientB.addPrescription('guttagonol')
        patientC.addPrescription('guttagonol')
        patientD.addPrescription('guttagonol')
       
        for j in range(150):
            patientA.update()
            patientB.update()
            patientC.update()
            patientD.update()
       
        popA.append(patientA.getTotalPop())
        popB.append(patientB.getTotalPop())
        popC.append(patientC.getTotalPop())
        popD.append(patientD.getTotalPop())
        
    """for pop in popA:
        print pop, 
    print
    for pop in popB:
        print pop,  
    print
    for pop in popC:
        print pop,  
    print
    for pop in popD:
        print pop,  
    print"""
    
    pylab.figure(1)
    pylab.hist(popA)
    pylab.figure(2)
    pylab.hist(popB)
    pylab.figure(3)
    pylab.hist(popC)
    pylab.figure(4)
    pylab.hist(popD)
    
    pylab.show()





#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    # TODO
    viruses = [ResistantVirus(0.1,0.05,{'guttagonol':False, 'grimpex':False},0.005)] * 100
    popA = []
    popB = []
    popC = []
    popD = []
   
    for i in range(numTrials):
        patientA = TreatedPatient(viruses[:], 1000)
        patientB = TreatedPatient(viruses[:], 1000)
        patientC = TreatedPatient(viruses[:], 1000)
        patientD = TreatedPatient(viruses[:], 1000)
        
        for j in range(150):
            patientA.update()
            patientB.update()
            patientC.update()
            patientD.update()
        
        patientA.addPrescription('guttagonol')
        patientB.addPrescription('guttagonol')
        patientC.addPrescription('guttagonol')
        patientD.addPrescription('guttagonol')
       
       
        for j in range(75):
            patientB.update()
           
        for j in range(150):
            patientC.update()
           
        for j in range(300):
            patientD.update()
       
        patientA.addPrescription('grimpex')
        patientB.addPrescription('grimpex')
        patientC.addPrescription('grimpex')
        patientD.addPrescription('grimpex')
       
        for j in range(150):
            patientA.update()
            patientB.update()
            patientC.update()
            patientD.update()
       
        popA.append(patientA.getTotalPop())
        popB.append(patientB.getTotalPop())
        popC.append(patientC.getTotalPop())
        popD.append(patientD.getTotalPop())
        
    pylab.figure(1)
    pylab.hist(popA)
    pylab.figure(2)
    pylab.hist(popB)
    pylab.figure(3)
    pylab.hist(popC)
    pylab.figure(4)
    pylab.hist(popD)
    
    pylab.show()