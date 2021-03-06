# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        
        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        
        
    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        # TODO
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        # TODO
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        # TODO
        return random.random() <= self.clearProb
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        # TODO
        prob = self.maxBirthProb * (1 - popDensity)
        if random.random() <= prob:
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException()


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        # TODO
        self.viruses = viruses
        self.maxPop = maxPop
        
    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        # TODO
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        # TODO
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        # TODO        
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        virusesCopy = []
        for virus in self.viruses:
            if not virus.doesClear():
                virusesCopy.append(virus)
        self.virus = virusesCopy
        popDensity = self.getTotalPop() / float(self.maxPop)
        for virus in self.viruses:
            try:
                if self.getTotalPop() <= self.maxPop:
                    self.viruses.append(virus.reproduce(popDensity))
            except NoChildException:
                continue
        return self.getTotalPop()


#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    # TODO
    VirusPop = [0.0]*300
    viruses = [SimpleVirus(maxBirthProb, clearProb)] * numViruses
    for j in range(numTrials):
        patient = Patient(viruses[:], maxPop)
        for i in range(300):
            patient.update()
            VirusPop[i] += patient.getTotalPop()
    for pop in VirusPop:
        pop /= float(numTrials)
    
    pylab.title('Simulation without Drugs')
    pylab.xlabel('Time Step')
    pylab.ylabel('Virus Population')
    pylab.legend('Pop vs Time Step')
    pylab.plot(range(300), VirusPop)
    pylab.show()
            
            


#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        # TODO
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        # TODO
        return self.resistances
        
    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        # TODO
        return self.mutProb
        
    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        
        # TODO
        try:
            return self.resistances[drug]
        except KeyError:
            return

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.
        """

        # TODO
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                break
        else:
            prob = self.maxBirthProb * (1 - popDensity)
            if random.random() <= prob:
                mutProb = self.getMutProb()
                ResistList = {}
                ResistList.update(self.getResistances())
                for Drug in ResistList:
                    if ResistList[Drug] and random.random() <= mutProb:
                        ResistList[Drug] = False
                    elif (not ResistList[Drug]) and random.random() <= mutProb:
                        ResistList[Drug] = True
                return ResistantVirus(self.maxBirthProb, self.clearProb, ResistList, mutProb)
            else:
                raise NoChildException()
        raise NoChildException()
                
class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        # TODO
        Patient.__init__(self, viruses, maxPop)
        self.drugs = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        # TODO
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        # TODO
        return self.drugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        # TODO
        pop = 0
        for virus in self.viruses:
            Resisted = True
            for drug in drugResist:
                try:
                    if not virus.getResistances()[drug]:
                        Resisted = False
                except KeyError:
                    Resisted = False
            if Resisted:
                pop += 1
        return pop

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        virusesCopy = []
        for virus in self.viruses:
            if not virus.doesClear():
                virusesCopy.append(virus)
        self.viruses = virusesCopy
        popDensity = self.getTotalPop() / float(self.maxPop)
        for virus in self.viruses:
            try:
                if self.getTotalPop() <= self.maxPop:
                    virusesCopy.append(virus.reproduce(popDensity, self.getPrescriptions()))
            except NoChildException:
                continue
        self.viruses = virusesCopy
        return self.getTotalPop()

#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """

    # TODO
    VirusPop = [0.0]*300
    ResistVirusPop = [0.0]*300
    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)] * numViruses
    for j in range(numTrials):
        patient = TreatedPatient(viruses[:], maxPop)
        for i in range(150):
            patient.update()
            VirusPop[i] += patient.getTotalPop()
            ResistVirusPop[i] += patient.getResistPop(['guttagonol'])
        patient.addPrescription('guttagonol')
        for i in range(150):
            patient.update()
            VirusPop[i+150] += patient.getTotalPop()
            ResistVirusPop[i+150] += patient.getResistPop(['guttagonol'])
    vp = [pop/float(numTrials) for pop in VirusPop]
    rvp = [pop/float(numTrials) for pop in ResistVirusPop]
    
    pylab.title('Simulation with Drugs')
    pylab.xlabel('Time Step')
    pylab.ylabel('Virus Population')
    
    pylab.plot(range(300), vp, 'b', label='VirusPop vs Time Step')
    pylab.plot(range(300), rvp, 'r', label='ResistVirusPop vs Time Step')
    pylab.legend(('VirusPop vs Time Step', 'ResistVirusPop vs Time Step'))
    pylab.show()