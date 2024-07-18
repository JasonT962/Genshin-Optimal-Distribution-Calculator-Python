# This Genshin Artifact Optimal Distribution Calculator is used to find the best combination of main stats and sub stats to maximize average damage

# Character Stats:
# Add as percentage. E.g. Gladiator set bonus gives 18% attack so put 18 in AttackUp
# Do not include artifact main stats or substats. That's what this maximizer is for

BaseHP = 0
HPUp = 0
FlatHP = 0

BaseAttack = 0
AttackUp = 0
FlatAttack = 0

# Ignore if your unit does not scale off of defence
BaseDefence = 0
DefenceUp = 0
FlatDefence = 0

CritRate = 5
CritDamage = 50

# All forms of damage bonus is additive so elemental skill dmg bonus 50% + pyro damage bonus 30% = 80% total
DamageBonus = 0
ElementalMastery = 0
EnergyRecharge = 0

SkillDamage = 0


# Extra ---------------------------------------------

# Assumes damage scales off attack, otherwise assumes defence
AttackScaling = True

# Assumes damage is elemental damage, otherwise assumes physical damage
ElementalDamage = True

CharacterLevel = 90

EnemyLevel = 90

EnemyResistance = 10

ResistanceShred = 0

# E.g. For Klee C2, Razor C4
DefenceShred = 0

# E.g. For Raiden C2 (ignores 60% of enemy's defence). Put 60
DefenceIgnore = 0

# Leave 0 if not using reactions. Pyro hitting Cryo / Hydro hitting Pyro = 2, Cryo hitting Pyro / Pyro hitting Hydro = 1.5
ReactionDamage = 0


# Ignore rest of code unless you know what you're doing
#------------------------------------------------------------------------------------------------------------------------------------------

class Artifact:
    # MainStat can be HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,ElementalMastery,EnergyRecharge,EleDamageBonus,PhysDamageBonus,CritRate,CritDamage
    MainStat = ""
    # Substats can be HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,FlatDefence,ElementalMastery,EnergyRecharge,CritRate,CritDamage
    Sub1 = ""
    Sub2 = ""
    Sub3 = ""
    Sub4 = ""

    def __init__(self,MainStat,Sub1,Sub2,Sub3,Sub4):
        self.MainStat = MainStat
        self.Sub1 = Sub1
        self.Sub2 = Sub2
        self.Sub3 = Sub3
        self.Sub4 = Sub4

# Damage Functions to calculate damage, crit damage and average damage from a set of stats
def Damage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage):
    TotalHP = (BaseHP * ((HPUp/100)+1)) + FlatHP
    TotalAttack = (BaseAttack * ((AttackUp/100)+1)) + FlatAttack
    TotalDefence = (BaseDefence * ((DefenceUp/100)+1)) + FlatDefence
    SkillDamage = SkillDamage/100
    DamageBonus = (DamageBonus/100)+1
    DefDamageReduction = (CharacterLevel+100) / ((1-(DefenceShred/100))*(1-(DefenceIgnore/100))*(EnemyLevel+100)+CharacterLevel+100)

    # Calculations for Resistance
    ResDamageReduction = (EnemyResistance - ResistanceShred) / 100
    if ResDamageReduction < 0:
        ResDamageReduction = 1 - (ResDamageReduction/2)
    elif ResDamageReduction >= 0 and ResDamageReduction < 0.75:
        ResDamageReduction = 1 - (ResDamageReduction)
    elif ResDamageReduction >= 0.75:
        ResDamageReduction = 1 / (4*ResDamageReduction+1)
    else:
        ResDamageReduction = 1
    
    # Calculations for Reaction Damage
    if ReactionDamage <= 1:
        ReactionDamage = 1
    else:
        ReactionDamage = ReactionDamage * (1 + ((278 * (ElementalMastery / (ElementalMastery + 1400))) / 100))
    
    if AttackScaling == True:
        return TotalAttack * SkillDamage * DamageBonus * DefDamageReduction * ResDamageReduction * ReactionDamage
    elif AttackScaling == False:
        return TotalDefence * SkillDamage * DamageBonus * DefDamageReduction * ResDamageReduction * ReactionDamage
    else:
        print("Error, please check whether AttackScaling is set to True or False")

def critDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage):
    CritDamage = ((CritDamage/100)+1)
    return CritDamage * Damage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage)

def averageDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage):
    if CritRate >= 100:
        CritRate = 1
    else:
        CritRate = CritRate/100
    CritDamage = ((CritDamage/100)+1)
    return ((CritRate*CritDamage)+(1-CritRate)) * Damage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage)


# Artifact Damage Maximizer Functions
def SetMainStats(): # Compares all possible main stat combinations with and returns the set with the highest average damage
    Flower = Artifact("FlatHP","","","","")
    Feather = Artifact("FlatAttack","","","","")
    Sands = Artifact("","","","","") # Empty main stats for sands, goblet and circlet as flower and feather main stats are always the same
    Goblet = Artifact("","","","","")
    Circlet = Artifact("","","","","")
    
    SandsList = ["HPUp","AttackUp","DefenceUp","ElementalMastery","EnergyRecharge"] # List of all possible sands

    if ElementalDamage == True: # List of all possible goblets
        GobletList = ["HPUp","AttackUp","DefenceUp","ElementalMastery","EleDamageBonus"]
    else:
        GobletList = ["HPUp","AttackUp","DefenceUp","ElementalMastery","PhysDamageBonus"]

    CircletList = ["HPUp","AttackUp","DefenceUp","ElementalMastery","CritRate","CritDamage"] # List of all possible circlets

    # Optimization - Removes any main stats that do not provide any damage
    DefaultSet = [Flower,Feather,Sands,Goblet,Circlet] # Set with no added sands, goblet or circlet
    DefaultDamage = Maximize(DefaultSet,False,HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,FlatDefence,DamageBonus,CritRate,CritDamage,ElementalMastery,EnergyRecharge)

    # Sands
    ToKeep = []
    for i in range(len(SandsList)): # Loops through the list of sands and keeps the one's that add any amount of damage
        Sands = Artifact(SandsList[i],"","","","")
        TestSet = [Flower,Feather,Sands,Goblet,Circlet]
        if Maximize(TestSet,False,HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,FlatDefence,DamageBonus,CritRate,CritDamage,ElementalMastery,EnergyRecharge) > DefaultDamage:
            ToKeep.append(SandsList[i])
    SandsList = ToKeep
    Sands = Artifact("","","","","")

    # Goblet
    ToKeep = []
    for i in range(len(GobletList)): # Loops through the list of sands and keeps the one's that add any amount of damage
        Goblet = Artifact(GobletList[i],"","","","")
        TestSet = [Flower,Feather,Sands,Goblet,Circlet]
        if Maximize(TestSet,False,HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,FlatDefence,DamageBonus,CritRate,CritDamage,ElementalMastery,EnergyRecharge) > DefaultDamage:
            ToKeep.append(GobletList[i])
    GobletList = ToKeep
    Goblet = Artifact("","","","","")

    # Circlet
    ToKeep = []
    for i in range(len(CircletList)): # Loops through the list of sands and keeps the one's that add any amount of damage
        Circlet = Artifact(CircletList[i],"","","","")
        TestSet = [Flower,Feather,Sands,Goblet,Circlet]
        if Maximize(TestSet,False,HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,FlatDefence,DamageBonus,CritRate,CritDamage,ElementalMastery,EnergyRecharge) > DefaultDamage:
            ToKeep.append(CircletList[i])
    CircletList = ToKeep
    Circlet = Artifact("","","","","")

    HighestDamage = 0
    TestSet = [Flower,Feather,Sands,Goblet,Circlet] # The set we're going to change and compare to the current highest damage
    Final = [Flower,Feather,Sands,Goblet,Circlet] # The set which contains the current highest damage

    for i in range(len(SandsList)): # This loops through and compares all possible combinations of sands, goblets and circlets to find the best one with the highest average damage
        for j in range(len(GobletList)):
            for k in range(len(CircletList)):
                Sands = Artifact(SandsList[i],"","","","")
                Goblet = Artifact(GobletList[j],"","","","")
                Circlet = Artifact(CircletList[k],"","","","")

                TestSet = [Flower,Feather,Sands,Goblet,Circlet]
                damage1 = Maximize(SetSubStats(TestSet),False,HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,FlatDefence,DamageBonus,CritRate,CritDamage,ElementalMastery,EnergyRecharge)
                
                if damage1 > HighestDamage:
                    HighestDamage = damage1
                    Final = [Flower,Feather,Sands,Goblet,Circlet]
    
    return Final

def SetSubStats(Set): # Takes a set of artifacts, replaces each substat with the one that gives the highest damage and returns the set
    # Resets substats for all artifacts
    for i in range(5):
        Set[i].Sub1 = ""
        Set[i].Sub2 = ""
        Set[i].Sub3 = ""
        Set[i].Sub4 = ""

    for i in range(len(Set)): # Loops through each artifact in the set
        SubStatList = ["HPUp","FlatHP","AttackUp","FlatAttack","DefenceUp","FlatDefence","ElementalMastery","EnergyRecharge","CritRate","CritDamage"]

        for j in range(len(SubStatList)): # Removes the sub stat from list that is the same as the main stat
            if Set[i].MainStat == SubStatList[j]:
                SubStatList.pop(j)
                break

        HighestDamage = 0
        BestSubStat = SubStatList[len(SubStatList)-1] # Set default best substat to last one in list (EnergyRecharge)
        
        # SubStat 1
        for j in range(len(SubStatList)): # Goes through all substats in list, picks the one that gives the highest damage and removes it from list
            Set[i].Sub1 = SubStatList[j]
            CurrentDamage = Maximize(Set,False,HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,FlatDefence,DamageBonus,CritRate,CritDamage,ElementalMastery,EnergyRecharge)

            if CurrentDamage > HighestDamage:
                HighestDamage = CurrentDamage
                BestSubStat = SubStatList[j]
        Set[i].Sub1 = BestSubStat
        SubStatList.remove(BestSubStat)
        BestSubStat = SubStatList[len(SubStatList)-1]

        # SubStat 2
        for j in range(len(SubStatList)):
            Set[i].Sub2 = SubStatList[j]
            CurrentDamage = Maximize(Set,False,HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,FlatDefence,DamageBonus,CritRate,CritDamage,ElementalMastery,EnergyRecharge)

            if CurrentDamage > HighestDamage:
                HighestDamage = CurrentDamage
                BestSubStat = SubStatList[j]
        Set[i].Sub2 = BestSubStat
        SubStatList.remove(BestSubStat)
        BestSubStat = SubStatList[len(SubStatList)-1]

        # SubStat 3
        for j in range(len(SubStatList)):
            Set[i].Sub3 = SubStatList[j]
            CurrentDamage = Maximize(Set,False,HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,FlatDefence,DamageBonus,CritRate,CritDamage,ElementalMastery,EnergyRecharge)

            if CurrentDamage > HighestDamage:
                HighestDamage = CurrentDamage
                BestSubStat = SubStatList[j]
        Set[i].Sub3 = BestSubStat
        SubStatList.remove(BestSubStat)
        BestSubStat = SubStatList[len(SubStatList)-1]

        # SubStat 4
        for j in range(len(SubStatList)):
            Set[i].Sub4 = SubStatList[j]
            CurrentDamage = Maximize(Set,False,HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,FlatDefence,DamageBonus,CritRate,CritDamage,ElementalMastery,EnergyRecharge)

            if CurrentDamage > HighestDamage:
                HighestDamage = CurrentDamage
                BestSubStat = SubStatList[j]
        Set[i].Sub4 = BestSubStat
        SubStatList.remove(BestSubStat)
        BestSubStat = SubStatList[len(SubStatList)-1]

    return Set
            

# Pass in True to Print parameter to print stats, otherwise, set to False to return average damage
def Maximize(Set,Print,HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,FlatDefence,DamageBonus,CritRate,CritDamage,ElementalMastery,EnergyRecharge): # Maximizes the damage from a set of artifacts
    # Average Artifact Roll Values
    RollHP = 4.95
    RollFlatHP = 254
    RollAttack = 4.95
    RollFlatAttack = 16.5
    RollDefence = 6.2
    RollFlatDefence = 19.5
    RollCR = 3.3
    RollCD = 6.6
    RollEM = 19.5
    RollER = 5.5

    # Roll Limits for each substat
    HPUpLimit = 0
    FlatHPLimit = 0
    AttackUpLimit = 0
    FlatAttackLimit = 0
    DefenceUpLimit = 0
    FlatDefenceLimit = 0
    CRLimit = 0
    CDLimit = 0
    EMLimit = 0
    ERLimit = 0

    # Set to 5 if you want artifacts to start with 4 substats, set to 4 if you want artifacts to start with 3 substats
    AddRolls = 5

    # Loops through all artifacts in the set and adds artifact main stats and sub stats
    for i in range(5):
        # Checks the artifact's main stat and adds the appropriate stat to the character stats
        # Main Stat - HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,ElementalMastery,EnergyRecharge,EleDamageBonus,PhysDamageBonus,CritRate,CritDamage
        MainStat = Set[i].MainStat
        if MainStat == "HPUp":
            HPUp += 46.6
        elif MainStat == "FlatHP":
            FlatHP += 4780
        elif MainStat == "AttackUp":
            AttackUp += 46.6
        elif MainStat == "FlatAttack":
            FlatAttack += 311
        elif MainStat == "DefenceUp":
            DefenceUp += 58.3
        elif MainStat == "ElementalMastery":
            ElementalMastery += 187
        elif MainStat == "EnergyRecharge":
            EnergyRecharge += 51.8
        elif MainStat == "EleDamageBonus":
            DamageBonus += 46.6
        elif MainStat == "PhysDamageBonus":
            DamageBonus += 58.3
        elif MainStat == "CritRate":
            CritRate += 31.1
        elif MainStat == "CritDamage":
            CritDamage += 62.2

        # Checks each substat, adds it to the character stats and increases the roll limit for the substat
        # Substats - HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,FlatDefence,ElementalMastery,EnergyRecharge,CritRate,CritDamage
        Sub1 = Set[i].Sub1
        if Sub1 == "HPUp":
            HPUp += RollHP
            HPUpLimit += AddRolls
        elif Sub1 == "FlatHP":
            FlatHP += RollFlatHP
            FlatHPLimit += AddRolls
        elif Sub1 == "AttackUp":
            AttackUp += RollAttack
            AttackUpLimit += AddRolls
        elif Sub1 == "FlatAttack":
            FlatAttack += RollFlatAttack
            FlatAttackLimit += AddRolls
        elif Sub1 == "DefenceUp":
            DefenceUp += RollDefence
            DefenceUpLimit += AddRolls
        elif Sub1 == "FlatDefence":
            FlatDefence += RollFlatDefence
            FlatDefenceLimit += AddRolls
        elif Sub1 == "ElementalMastery":
            ElementalMastery += RollEM
            EMLimit += AddRolls
        elif Sub1 == "EnergyRecharge":
            EnergyRecharge += RollER
            ERLimit += AddRolls
        elif Sub1 == "CritRate":
            CritRate += RollCR
            CRLimit += AddRolls
        elif Sub1 == "CritDamage":
            CritDamage += RollCD
            CDLimit += AddRolls
        
        Sub2 = Set[i].Sub2
        if Sub2 == "HPUp":
            HPUp += RollHP
            HPUpLimit += AddRolls
        elif Sub2 == "FlatHP":
            FlatHP += RollFlatHP
            FlatHPLimit += AddRolls
        elif Sub2 == "AttackUp":
            AttackUp += RollAttack
            AttackUpLimit += AddRolls
        elif Sub2 == "FlatAttack":
            FlatAttack += RollFlatAttack
            FlatAttackLimit += AddRolls
        elif Sub2 == "DefenceUp":
            DefenceUp += RollDefence
            DefenceUpLimit += AddRolls
        elif Sub2 == "FlatDefence":
            FlatDefence += RollFlatDefence
            FlatDefenceLimit += AddRolls
        elif Sub2 == "ElementalMastery":
            ElementalMastery += RollEM
            EMLimit += AddRolls
        elif Sub2 == "EnergyRecharge":
            EnergyRecharge += RollER
            ERLimit += AddRolls
        elif Sub2 == "CritRate":
            CritRate += RollCR
            CRLimit += AddRolls
        elif Sub2 == "CritDamage":
            CritDamage += RollCD
            CDLimit += AddRolls
        
        Sub3 = Set[i].Sub3
        if Sub3 == "HPUp":
            HPUp += RollHP
            HPUpLimit += AddRolls
        elif Sub3 == "FlatHP":
            FlatHP += RollFlatHP
            FlatHPLimit += AddRolls
        elif Sub3 == "AttackUp":
            AttackUp += RollAttack
            AttackUpLimit += AddRolls
        elif Sub3 == "FlatAttack":
            FlatAttack += RollFlatAttack
            FlatAttackLimit += AddRolls
        elif Sub3 == "DefenceUp":
            DefenceUp += RollDefence
            DefenceUpLimit += AddRolls
        elif Sub3 == "FlatDefence":
            FlatDefence += RollFlatDefence
            FlatDefenceLimit += AddRolls
        elif Sub3 == "ElementalMastery":
            ElementalMastery += RollEM
            EMLimit += AddRolls
        elif Sub3 == "EnergyRecharge":
            EnergyRecharge += RollER
            ERLimit += AddRolls
        elif Sub3 == "CritRate":
            CritRate += RollCR
            CRLimit += AddRolls
        elif Sub3 == "CritDamage":
            CritDamage += RollCD
            CDLimit += AddRolls

        Sub4 = Set[i].Sub4
        if Sub4 == "HPUp":
            HPUp += RollHP
            HPUpLimit += AddRolls
        elif Sub4 == "FlatHP":
            FlatHP += RollFlatHP
            FlatHPLimit += AddRolls
        elif Sub4 == "AttackUp":
            AttackUp += RollAttack
            AttackUpLimit += AddRolls
        elif Sub4 == "FlatAttack":
            FlatAttack += RollFlatAttack
            FlatAttackLimit += AddRolls
        elif Sub4 == "DefenceUp":
            DefenceUp += RollDefence
            DefenceUpLimit += AddRolls
        elif Sub4 == "FlatDefence":
            FlatDefence += RollFlatDefence
            FlatDefenceLimit += AddRolls
        elif Sub4 == "ElementalMastery":
            ElementalMastery += RollEM
            EMLimit += AddRolls
        elif Sub4 == "EnergyRecharge":
            EnergyRecharge += RollER
            ERLimit += AddRolls
        elif Sub4 == "CritRate":
            CritRate += RollCR
            CRLimit += AddRolls
        elif Sub4 == "CritDamage":
            CritDamage += RollCD
            CDLimit += AddRolls

    # This section checks adding which substat will add the highest average damage, then add it to the stats
    for i in range(25):
        # HP% Roll
        HPUp += RollHP
        Damage1 = averageDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage)
        HPUp -= RollHP
        # FlatHP Roll
        FlatHP += RollFlatHP
        Damage2 = averageDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage)
        FlatHP -= RollFlatHP
        # Attack% Roll
        AttackUp += RollAttack
        Damage3 = averageDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage)
        AttackUp -= RollAttack
        # FlatAttack Roll
        FlatAttack += RollFlatAttack
        Damage4 = averageDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage)
        FlatAttack -= RollFlatAttack
        # Defence% Roll
        DefenceUp += RollDefence
        Damage5 = averageDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage)
        DefenceUp -= RollDefence
        # Flat Defence Roll
        FlatDefence += RollFlatDefence
        Damage6 = averageDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage)
        FlatDefence -= RollFlatDefence
        # CritRate Roll
        CritRate += RollCR
        Damage7 = averageDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage)
        CritRate -= RollCR
        # CritDamage Roll
        CritDamage += RollCD
        Damage8 = averageDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage)
        CritDamage -= RollCD
        # Elemental Mastery Roll
        ElementalMastery += RollEM
        Damage9 = averageDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage)
        ElementalMastery -= RollEM
        # EnergyRecharge Roll
        EnergyRecharge += RollER
        Damage10 = averageDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage)
        EnergyRecharge -= RollER

        # Check roll limits, if the substat has no rolls left then the damage for that roll will be voided.
        if HPUpLimit == 0:
            Damage1 = 0
        if FlatHPLimit == 0:
            Damage2 = 0
        if AttackUpLimit == 0:
            Damage3 = 0
        if FlatAttackLimit == 0:
            Damage4 = 0
        if DefenceUpLimit == 0:
            Damage5 = 0
        if FlatDefenceLimit == 0:
            Damage6 = 0
        if CRLimit == 0:
            Damage7 = 0
        if CDLimit == 0:
            Damage8 = 0
        if EMLimit == 0:
            Damage9 = 0
        if ERLimit == 0:
            Damage10 = 0
        
        # Compare Damages and adds the substat that gives the highest damage
        if Damage1 >= max(Damage2,Damage3,Damage4,Damage5,Damage6,Damage7,Damage8,Damage9,Damage10):
            HPUp += RollHP
            HPUpLimit -= 1
        elif Damage2 >= max(Damage1,Damage3,Damage4,Damage5,Damage6,Damage7,Damage8,Damage9,Damage10):
            FlatHP += RollFlatHP
            FlatHPLimit -= 1
        elif Damage3 >= max(Damage1,Damage2,Damage4,Damage5,Damage6,Damage7,Damage8,Damage9,Damage10):
            AttackUp += RollAttack
            AttackUpLimit -= 1
        elif Damage4 >= max(Damage1,Damage2,Damage3,Damage5,Damage6,Damage7,Damage8,Damage9,Damage10):
            FlatAttack += RollFlatAttack
            FlatAttackLimit -= 1
        elif Damage5 >= max(Damage1,Damage2,Damage3,Damage4,Damage6,Damage7,Damage8,Damage9,Damage10):
            DefenceUp += RollDefence
            DefenceUpLimit -= 1
        elif Damage6 >= max(Damage1,Damage2,Damage3,Damage4,Damage5,Damage7,Damage8,Damage9,Damage10):
            FlatDefence += RollFlatDefence
            FlatDefenceLimit -= 1
        elif Damage7 >= max(Damage1,Damage2,Damage3,Damage4,Damage5,Damage6,Damage8,Damage9,Damage10):
            CritRate += RollCR
            CRLimit -= 1
        elif Damage8 >= max(Damage1,Damage2,Damage3,Damage4,Damage5,Damage6,Damage7,Damage9,Damage10):
            CritDamage += RollCD
            CDLimit -= 1
        elif Damage9 >= max(Damage1,Damage2,Damage3,Damage4,Damage5,Damage6,Damage7,Damage8,Damage10):
            ElementalMastery += RollEM
            EMLimit -= 1
        elif Damage10 >= max(Damage1,Damage2,Damage3,Damage4,Damage5,Damage6,Damage7,Damage8,Damage9):
            EnergyRecharge += RollER
            ERLimit -= 1
        else:
            print("Error: Problem with checking next best substat roll")
    
    if Print == True:
        TotalHP = (BaseHP * ((HPUp/100)+1)) + FlatHP
        TotalAttack = (BaseAttack * ((AttackUp/100)+1)) + FlatAttack
        TotalDefence = (BaseDefence * ((DefenceUp/100)+1)) + FlatDefence
        print("HP:",TotalHP)
        print("Attack:",TotalAttack)
        print("Defence:",TotalDefence)
        print("Crit Rate:",CritRate)
        print("Crit Damage:",CritDamage)
        print("Damage Bonus:",DamageBonus)
        print("Elemental Mastery:",ElementalMastery)
        print("Energy Recharge:",EnergyRecharge)
        print()
        print("Damage(on crit):",critDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage))
        print("Damage(no crit):",Damage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage))
        print("Average damage:",averageDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage))
        print()
        print("Sands:",Set[2].MainStat)
        print("Goblet:",Set[3].MainStat)
        print("Circlet:",Set[4].MainStat)
    else:
        return averageDamage(BaseHP,HPUp,FlatHP,BaseAttack,AttackUp,FlatAttack,BaseDefence,DefenceUp,FlatDefence,CritRate,CritDamage,DamageBonus,ElementalMastery,EnergyRecharge,SkillDamage,AttackScaling,CharacterLevel,EnemyLevel,EnemyResistance,ResistanceShred,DefenceShred,DefenceIgnore,ReactionDamage)


def Main():
    ArtifactSet = SetSubStats(SetMainStats())
    Maximize(ArtifactSet,True,HPUp,FlatHP,AttackUp,FlatAttack,DefenceUp,FlatDefence,DamageBonus,CritRate,CritDamage,ElementalMastery,EnergyRecharge)
    return

Main()
