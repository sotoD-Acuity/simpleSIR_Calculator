from tkinter import *
from scipy.integrate import odeint
import ttkbootstrap as tkboot

import numpy as np
import matplotlib.pyplot as plt

# Functions
def setCrewSize():
    crewSize = crewSizeEntry.get()
    crewSize = float(crewSize)
    crewSizeDisplay.configure(text=f"{crewSize} = N")
    return crewSize
def setScenarioDuration():
    scenarioDuration = scenarioDurationEntry.get()
    scenarioDuration = float(scenarioDuration)
    scenarioDuration = int(np.ceil(scenarioDuration))
    scenarioDurationDisplay.configure(text=f"{scenarioDuration} days")
    return scenarioDuration
def setBeta():
    contacts = contactRateContactsEntry.get()
    days = contactRateDaysEntry.get()
    if contacts == "" or days == "":
        beta = 0.0
        return beta
    else:
        contacts = float(contacts)
        days = float(days)
    beta = contacts/days
    betaDisplay.configure(text=f"beta = {beta}")
    return beta
def setGamma():
    gamma = recoverTimeEntry.get()
    if gamma == "":
        gamma = 0.0
        gammaDisplay.configure(text=f"Days Missing")
        return gamma
    else:
        gamma = 1.0 / float(gamma)
        gammaDisplay.configure(text=f"gamma = {gamma}")
    return gamma
def setInitInf():
    iInf = initialInfectedPopulationEntry.get()
    iInf = float(iInf)
    iInfDisplay.configure(text=f"Infected(0): {iInf}")
    return iInf
def setInitSus():
    if setInitRec() != 0 and setCrewSize() != 0 and setCrewSize() > setInitRec() and setCrewSize() > setInitInf() and setInitInf() != 0:
        iSus = setCrewSize() - setInitRec() - setInitInf()
        iSusDisplay.configure(text=f"Susceptible(0): {iSus}")
        return iSus
    elif setInitInf() != 0 and setCrewSize() != 0 and setCrewSize() > setInitInf():
        iSus = setCrewSize() - setInitInf()
        iSusDisplay.configure(text=f"Susceptible(0): {iSus}")
        return iSus
    elif setCrewSize < setInitInf():
        iSus = 0
        iSusDisplay.configure(text=f"Susceptible(0): {iSus}  Crew Size must be greater than Initial Infected Population")
        return iSus
    else:
        iSus = 0
        iSusDisplay.configure(text=f"Susceptible(0): {iSus}  Initial Infected Population must be greater than 0")
        return iSus
def setInitRec():
    if iRecEntry.get() == "":
        iRec = 0.0
        iRecDisplay.configure(text=f"Recovered(0): {iRec}", wraplength=495)
        return iRec
    else:
        iRec = iRecEntry.get()
        iRec = float(iRec)
        iRecDisplay.configure(text=f"Recovered(0): {iRec}", wraplength=495)
        return iRec
def recButtonLogic():
    if setInitRec() != 0 and setCrewSize() != 0 and setCrewSize() > setInitRec() and setCrewSize() > setInitInf() and setInitInf() != 0:
        setInitSus()
        setInitRec()
    elif setInitRec() == 0 and setCrewSize() != 0 and setCrewSize() > setInitInf() and setInitInf() != 0:
        setInitSus()
        setInitRec()
    else:
       iRecDisplay.configure(text=f"Recovered(0): {iRec}  Crew Size must be greater than any initial condition", wraplength=495)

root = tkboot.Window(themename="flatly")
root.title("Simulating Days to Mission Failure")
root.geometry("505x1000")

windowTitle = tkboot.Label(root,text= "Hypothetical Communicable Disease Outbreaks in Long Duration Spaceflight: SIR Models",font=("Century Gothic", 16, "italic"),wraplength=500)
windowTitle.pack(side="top", anchor="nw", pady=5,padx=5)

parameterFrame = tkboot.Frame(root, bootstyle = "dark", width=500, height=950)
parameterFrame.pack(side="left", anchor="nw", pady=5,padx=5)

parameterFrameTitleA = tkboot.Label(parameterFrame, text="Mission Profile", font=("Century Gothic", 14, "bold"))
parameterFrameTitleA.place(x=5, y=5, anchor="nw")

# Create a label for the mission duration entry box
scenarioDurationLabel = tkboot.Label(parameterFrame, text="Scenario Duration (Full days)", font=("Century Gothic", 12))
scenarioDurationLabel.place(x=5, y = 35, anchor="nw")

# Create an Entry Widget by calling the Entry() method
scenarioDurationEntry = tkboot.Entry(parameterFrame, bootstyle = "light", font=("Century Gothic", 12), width=10)
scenarioDurationEntry.place(x=5, y = 65, anchor="nw")
scenarioDuration = 0.0
scenarioDurationDisplay = tkboot.Label(parameterFrame, text=f"{scenarioDuration} days", font=("Consolas", 10))
scenarioDurationDisplay.place(x=70, y = 110, anchor="nw")
durationButton = tkboot.Button(parameterFrame, text="Set", width=5, command=setScenarioDuration)
durationButton.place(x=5, y = 105, anchor="nw")

# Create a label for the Crew Size entry box
crewSizeLabel = tkboot.Label(parameterFrame, text="Crew Size", font=("Century Gothic", 12))
crewSizeLabel.place(x=490, y = 35, anchor="ne")

# Create an Entry Widget by calling the Entry() method
crewSizeEntry = tkboot.Entry(parameterFrame, bootstyle = "light", font=("Century Gothic", 12), width=10)
crewSizeEntry.place(x=490, y = 65, anchor="ne")

crewSize = 0.0
crewButton = tkboot.Button(parameterFrame, text="Set", width=5, command=setCrewSize)
crewButton.place(x=490, y = 105, anchor="ne")
crewSizeDisplay = tkboot.Label(parameterFrame, text=f"{crewSize} = N", font=("Consolas", 10))
crewSizeDisplay.place(x=420, y = 110, anchor="ne")

# Create a label with extra y padding to separate mission profile from pathogen profile
parameterFrameTitleB = tkboot.Label(parameterFrame, text="Pathogen Profile", font=("Century Gothic", 14, "bold"))
parameterFrameTitleB.place(x=5, y=140, anchor="nw")

# Create a label for effective contact rate (beta = 1/tau = 1/[contacts/day])
pathogenContactRateLabel = tkboot.Label(parameterFrame, text="Contact Rate (Beta)", font=("Century Gothic", 12), wraplength=400)
pathogenContactRateLabel.place(x=5, y = 170, anchor="nw")
betaExplanationLabel = tkboot.Label(parameterFrame, text="We'll simplify beta to be the number of effective contacts (sneeze, cough, etc) per unit day(s). This will determine how the fractions susceptible and infected change assuming a closed population where everyone is randomly mixing and giving health reports day-to-day", font=("Century Gothic", 10), wraplength=493)
betaExplanationLabel.place(x=5, y = 200, anchor="nw")

# Create an entry box for the number of contacts that resulted in infection
contactRateContactsEntry = tkboot.Entry(parameterFrame, bootstyle = "light", font=("Century Gothic", 12), width=10)
contactRateContactsEntry.place(x=5, y = 280, anchor="nw")

# This is just a visual to show that the entered element is a fraction
divisorLabel = tkboot.Label(parameterFrame, text="/" , font=("Century Gothic", 12))
divisorLabel.place(x=125, y = 285, anchor="nw")

# Create an entry box for the number of days over which the contacts took place\
contactRateDaysEntry = tkboot.Entry(parameterFrame, bootstyle = "light", font=("Century Gothic", 12), width=10)
contactRateDaysEntry.place(x=150, y = 280, anchor="nw")

# Create a button to set the beta value
beta = 0.0
betaDisplay = tkboot.Label(parameterFrame, text=f"beta = {beta}", font=("Consolas", 10))
betaSetButton = tkboot.Button(parameterFrame, text="Set", width=5, command=setBeta)
betaSetButton.place(x=5, y = 320, anchor="nw")
betaDisplay.place(x=275, y = 290, anchor="nw")

# Create a label for how many days it takes for an infected person to recover
recoveryTimeLabel = tkboot.Label(parameterFrame, text="Avg. Infection Duration (days)", font=("Century Gothic", 12))
recoveryTimeLabel.place(x=5, y = 355, anchor="nw")
recoverTimeEntry = tkboot.Entry(parameterFrame, bootstyle = "light", font=("Century Gothic", 12), width=10)
recoverTimeEntry.place(x=5, y = 385, anchor="nw")

# Create a button to set the recovery time
gamma = 0.0
gammaDisplay = tkboot.Label(parameterFrame, text=f"gamma = {gamma}", font=("Consolas", 10))
gammaDisplay.place(x=275, y = 390, anchor="nw")
gammaSetButton = tkboot.Button(parameterFrame, text="Set", width=5, command=setGamma)
gammaSetButton.place(x=5, y = 425, anchor="nw")



initialInfectedPopulation = tkboot.Label(parameterFrame, text="Initial Infected Population, I(0) ", font=("Century Gothic", 12))
initialInfectedPopulation.place(x=5, y = 460, anchor="nw")
infectPopulationExplanationLabel = tkboot.Label(parameterFrame, text="# of infected that are capable of spreading the disease from the start of day 0", font=("Century Gothic", 10), wraplength=495)
infectPopulationExplanationLabel.place(x=5, y = 490, anchor="nw")
initialInfectedPopulationEntry = tkboot.Entry(parameterFrame, bootstyle = "light", font=("Century Gothic", 12), width=10)
initialInfectedPopulationEntry.place(x=5, y = 535, anchor="nw")
iInf = 0.0
iInfDisplay = tkboot.Label(parameterFrame, text=f"Infected(0): {iInf}", font=("Consolas", 10))
iInfDisplay.place(x=275, y = 540, anchor="nw")
iInfButton = tkboot.Button(parameterFrame, text="Set", width=5, command=setInitInf)
iInfButton.place(x=125, y = 540, anchor="nw")


initialSusceptiblePopulation = tkboot.Label(parameterFrame, text="Initial Susceptible Population, S(0) ", font=("Century Gothic", 12))
initialSusceptiblePopulation.place(x=5, y = 580, anchor="nw")
iSPexplanationLabel = tkboot.Label(parameterFrame, text="# of people that can catch the disease from the start of day 0\n N - Infected(0) - Recovered(0)", font=("Century Gothic", 10), wraplength=495)
iSPexplanationLabel.place(x=5, y = 610, anchor="nw")
iSus = 0.0
iSusDisplay = tkboot.Label(parameterFrame, text=f"Susceptible(0): {iSus}", font=("Consolas", 10))
iSusDisplay.place(x=275, y = 660, anchor="nw")
iSusButton = tkboot.Button(parameterFrame, text="Set", width=5, command=setInitSus)
iSusButton.place(x=125, y = 660, anchor="nw")

initialRecoveredPopulation = tkboot.Label(parameterFrame, text="Initial Recovered Population, R(0) ", font=("Century Gothic", 12))
initialRecoveredPopulation.place(x=5, y = 700, anchor="nw")
iRPexplanationLabel = tkboot.Label(parameterFrame, text="# of people that have recovered or are immune from the disease from the start of day 0     *will automatically adjust S(0)", font=("Century Gothic", 10), wraplength=495)
iRPexplanationLabel.place(x=5, y = 730, anchor="nw")
iRec = 0.0
iRecDisplay = tkboot.Label(parameterFrame, text=f"Recovered(0): {iRec}", font=("Consolas", 10))
iRecDisplay.place(x=275, y = 780, anchor="nw")
iRecEntry = tkboot.Entry(parameterFrame, bootstyle = "light", font=("Century Gothic", 12), width=10)
iRecEntry.place(x=5, y = 780, anchor="nw")
iRecButton = tkboot.Button(parameterFrame, text="Set", width=5, command=recButtonLogic)
iRecButton.place(x=125, y = 780, anchor="nw")

# Checkbutton. We'll use this if we want to modify the contact rate or recovery time over time
betaBoostScenario = IntVar()
betaReduceScenario = IntVar()
gammaBoostScenario = IntVar()
gammaReduceScenario = IntVar()

def betaBoost():
    if betaBoostScenario.get() == 1:
        beta = setBeta() * 1.5
        betaDisplay.configure(text=f"beta = {beta}")
        return beta
    else:
        beta = setBeta()
        betaDisplay.configure(text=f"beta = {beta}")
        return beta
def betaReduce():
    if betaReduceScenario.get() == 1:
        beta = setBeta() * 0.5
        betaDisplay.configure(text=f"beta = {beta}")
        return beta
    else:
        beta = setBeta()
        betaDisplay.configure(text=f"beta = {beta}")
        return beta
def gammaBoost():
    if gammaBoostScenario.get() == 1 and setGamma() != 0:
        gamma = setGamma() * 1.5
        gammaDisplay.configure(text=f"gamma = {gamma}")
        return gamma
    else:
        gamma = setGamma()
        gammaDisplay.configure(text=f"gamma = {gamma}")
        return gamma
def gammaReduce():
    if gammaReduceScenario.get() == 1 and setGamma() != 0:
        gamma = setGamma() * 0.5
        gammaDisplay.configure(text=f"gamma = {gamma}")
        return gamma
    else:
        gamma = setGamma()
        gammaDisplay.configure(text=f"gamma = {gamma}")
        return gamma
    
betaBoostButton = tkboot.Checkbutton(root,
                                  bootstyle="danger, round-toggle",
                                  text="Simulate Increased Infectiousness (beta+50%))",
                                  variable=betaBoostScenario,
                                  onvalue=1,
                                  offvalue=0,
                                  command=betaBoost)
betaBoostButton.place(x=250, y = 920-5, anchor="n")
betaReduceButton = tkboot.Checkbutton(root,
                                  bootstyle="success, round-toggle",
                                  text="Simulate Social Distancing and PPE from day 0 (beta-50%)",
                                  variable=betaReduceScenario,
                                  onvalue=1,
                                  offvalue=0,
                                  command=betaReduce)
betaReduceButton.place(x=250, y = 940-5, anchor="n")
gammaReduceButton = tkboot.Checkbutton(root,
                                    bootstyle="danger, round-toggle",
                                    text="Simulate Weakened Immune System (double infection duration)",
                                    variable=gammaReduceScenario,
                                    onvalue=1,
                                    offvalue=0,
                                    command=gammaReduce)
gammaReduceButton.place(x=250, y = 960-5, anchor="n")
gammaBoostButton = tkboot.Checkbutton(root,
                                    bootstyle="success, round-toggle",
                                    text="Simulate physician on board (half infection duration)",
                                    variable=gammaBoostScenario,
                                    onvalue=1,
                                    offvalue=0,
                                    command=gammaBoost)
gammaBoostButton.place(x=250, y = 980-5, anchor="n")

# Create a button to run the simulation
def runSimulation():
    # Set the initial conditions
    N = setCrewSize()
    I0 = setInitInf()
    S0 = setInitSus()
    R0 = setInitRec()
    beta = setBeta()
    gamma = setGamma()
    if betaBoostScenario.get() == 1:
        if betaReduceScenario.get() == 1:
            beta = setBeta()
        else :
            beta = betaBoost()
    elif betaReduceScenario.get() == 1:
        beta = betaReduce()
    
    if gammaBoostScenario.get() == 1:
        if gammaReduceScenario.get() == 1:
            gamma = setGamma()
        else :
            gamma = gammaBoost()
    elif gammaReduceScenario.get() == 1:
        gamma = gammaReduce()
        
    timeFrame = int(setScenarioDuration())
    # Create a time array
    t = np.linspace(0, timeFrame, timeFrame)
    # Create the SIR model differential equations
    def deriv(y, t, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt
    # Initial conditions vector
    y0 = S0, I0, R0
    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T
    # Plot the data on three separate curves for S(t), I(t) and R(t)
    try:
        fig = plt.figure(facecolor='w')
        ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
        # infoWindow = tkboot.Window(themename="flatly")
        # infoWindow.geometry("600x600")
        # 
        # infoWindowTitle = tkboot.Label(infoWindow,text= "Simulation Results",font=("Century Gothic", 16, "italic"),wraplength=500)
        # infoWindowTitle.pack(side="top", anchor="nw", pady=5,padx=5)
        # 
        # infoWindowParameterFrame = tkboot.Frame(infoWindow, bootstyle = "dark", width=500, height=950)
        # infoWindowParameterFrame.pack(side="left", anchor="nw", pady=5,padx=5)
        # resultsLabel = tkboot.Label(infoWindowParameterFrame, text=f"Scenario Duration: {timeFrame} days\nCrew Size: {N} people\nInitial Infected Population: {I0} people\nInitial Recovered Population: {R0} people\nInitial Susceptible Population: {S0} people\nContact Rate: {beta} contacts/day\nRecovery Time: {1/gamma} days", font=("Consolas", 12), wraplength=495)
        # resultsLabel.place(x=5, y = 5, anchor="nw")
        ax.set_title(f"Forecasting {timeFrame} days ,Crew Size: {N} people\n Initial: Infected={I0} Recovered={R0} Susceptible={S0}\nContact Rate: {beta} contacts/day & Recovery Time: {1/gamma} days", fontdict={'fontsize': 10, 'fontweight': 'medium'})
        ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
        ax.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
        ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Number (1000s)')
        ax.set_ylim(0,N/1000)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)
        plt.show()
    except:
        print("Error in plot")
    return

runSimulationButton = tkboot.Button(parameterFrame, text="Run Simulation", width=15, command=runSimulation)
runSimulationButton.place(x=300, y = 5, anchor="n")

root.mainloop()