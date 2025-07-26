import random
import math

class Career:

    def __init__(self,name,speed,stamina,power,guts,wit,skillpts,speedGrwth,staminaGrwth,powerGrwth,gutsGrwth,witGrwth,raceSchedule = None):
        """
        Initialize Uma object initial state
        """
        self.Uma = name
        self.speed = speed
        self.stamina = stamina
        self.power = power
        self.guts = guts
        self.wit = wit
        self.skillpts = skillpts

        self.speedGrwth = speedGrwth
        self.staminaGrwth = staminaGrwth
        self.powerGrwth = powerGrwth
        self.gutsGrwth = gutsGrwth
        self.witGrwth = witGrwth

        self.speedTraincount = 0
        self.staminaTraincount = 0
        self.powerTraincount = 0
        self.gutsTraincount = 0
        self.witTraincount = 0

        self.Energy = 100
        self.Mood = 3     #Scale from 1-5
        self.fans = 0

        self.TurnCount = 1

        self.raceSchedule = raceSchedule if raceSchedule is not None else {}
    def __str__(self):
        return (f"\nUma: {self.Uma}\n"
                f"Speed: {self.speed}, Stamina: {self.stamina}, "
                f"Power: {self.power}, Guts: {self.guts}, Wit: {self.wit}, Skill Points: {self.skillpts}, "
                f"Energy: {self.Energy}, Mood: {self.moodStatus()} \n")
    
    def turnCount(self):
        self.TurnCount += 1
        
        if self.TurnCount in self.raceSchedule:
            raceInfo = self.raceSchedule[self.TurnCount]
            self.raceSim(raceInfo)
            self.TurnCount += 1


    def checkRaceDay(self):
        if self.TurnCount in self.raceSchedule:
            return True
        return False
        
    def raceSim(self, raceInfo):
        race_name = raceInfo["name"]
        difficulty = raceInfo["difficulty"]
        runners = raceInfo["runners"]
        fanReward = raceInfo["fanReward"]
        print(f"\n--- Turn {self.TurnCount} ---")
        print(f"\n{race_name} begins! Let's see how you place...")

        score = .4*self.speed +.2*self.stamina + .2*self.power + .1*self.guts * .1*self.wit

        opponents = [random.randint(round(difficulty /1.5), round(difficulty * 1.5)) for _ in range(runners - 1)]            
        scores = opponents + [score]
        sorted_scores = sorted(scores, reverse=True)
        placement = sorted_scores.index(score) + 1

        print(f"You placed {placement}{self.ordinalSuffix(placement)} out of {runners} runners!")

        if placement == 1:
            print(f"You won the {race_name}! Gained {fanReward} fans!")
            self.fans += fanReward
            self.speed += 3
            self.stamina += 3
            self.power += 3
            self.guts += 3
            self.wit += 3
            print(f"You feel inspired!")
            print(f"Speed up by 3, Stamina up by 3, Power up by 3, Guts up by 3, Wit up by 3!")
            
        elif placement <= 3:
            print(f"Top 3! Solid performance. Gained {int(fanReward *.7)} fans!")
            self.fans += int(fanReward * 0.7)
            self.speed += 2
            self.stamina += 2
            self.power += 2
            self.guts += 2
            self.wit += 2
            print(f"You feel good!")
            print(f"Speed up by 2, Stamina up by 2, Power up by 2, Guts up by 2, Wit up by 2!")

        elif placement <= 5:
            print(f"Mid-pack finish. Gained {int(fanReward *.4)} fans!")
            self.fans += int(fanReward * 0.4)
            self.speed += 1
            self.stamina += 1
            self.power += 1
            self.guts += 1
            self.wit += 1
            print(f"You feel hopeful.")
            print(f"Speed up by 1, Stamina up by 1, Power up by 1, Guts up by 1, Wit up by 1")
        else:
            print(f"You finished near the back. Gained {int(fanReward *.2)} fans!")
            self.fans += int(fanReward * 0.2)
            
    def ordinalSuffix(self, n):
        if 11 <= n % 100 <= 13:
            return "th"
        return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    
    def moodStatus(self):
        mood_map = {
        1: "Awful",
        2: "Bad",
        3: "Normal",
        4: "Good",
        5: "Great"
    }
        mood_clamped = max(1, min(5, self.Mood))
        return mood_map[mood_clamped]
        
    
    def speedTrain(self):
        
        if self.checkRaceDay(): # If there is a race, skip action
            return
        
        failcheck = self.failTrain(self.Energy)
        if failcheck:
            print('\nTraining Failed')
            self.Mood += -1
            print(f'Mood Down by 1')
            print(f'Mood: {self.moodStatus()}')
            
        else: 
            self.Energy += -20
            if self.Energy <= 0:
                self.Energy = 0
            
            level = self.speedTraincount // 4 + 1
            speedGain = (1 + self.speedGrwth) * (level + 9)
            powerGain = (1 + self.powerGrwth) * (level + 4)
            skillGain = 2

            self.speed += speedGain
            self.power += powerGain
            self.skillpts += skillGain
            self.speedTraincount += 1

            print(f"[Speed Training Lv{level}] +{speedGain} Speed, +{powerGain} Power, +{skillGain} SkillPts")
            newLevel = self.speedTraincount // 4 + 1
            if newLevel > level:
                print(f"Speed Training leveled up! Lv{newLevel}")

            self.turnCount()
            
    def staminaTrain(self):

        if self.checkRaceDay(): # If there is a race, skip action
            return
        
        failcheck = self.failTrain(self.Energy)
        if failcheck:
            print('Training Failed')
            self.Mood += -1

        else:
            self.Energy += -15
            if self.Energy <= 0:
                self.Energy = 0
            
            level = self.staminaTraincount //4 + 1
            staminaGain = (1 + self.staminaGrwth) * (level + 9)
            gutsGain = (1 + self.gutsGrwth) * (level + 4)
            skillGain = 2

            self.stamina += staminaGain
            self.guts += gutsGain
            self.skillpts += skillGain
            self.staminaTraincount += 1

            print(f"[Stamina Training Lv{level}] +{staminaGain} Stamina, +{gutsGain} Guts, +{skillGain} SkillPts")
            newLevel = self.staminaTraincount // 4 + 1
            if newLevel > level:
                print(f"Stamina Training leveled up! Lv{newLevel}")

            self.turnCount()
            
    def powerTrain(self):

        if self.checkRaceDay(): # If there is a race, skip action
            return
        
        failcheck = self.failTrain(self.Energy)
        if failcheck:
            print('Training Failed')
            self.Mood += -1
            
        else: 
            self.Energy += -15
            if self.Energy <= 0:
                self.Energy = 0
            
            level = self.powerTraincount //4 + 1
            powerGain = (1 + self.powerGrwth) * (level + 9)
            staminaGain = (1 + self.staminaGrwth) * (level + 4)
            skillGain = 2

            self.stamina += staminaGain
            self.power += powerGain
            self.skillpts += skillGain
            self.powerTraincount += 1

            print(f"[Power Training Lv{level}] +{staminaGain} Stamina, +{powerGain} Power, +{skillGain} SkillPts")
            newLevel = self.powerTraincount // 4 + 1
            if newLevel > level:
                print(f"Power Training leveled up! Lv{newLevel}")

            self.turnCount()
            
    def gutsTrain(self):
        
        if self.checkRaceDay(): # If there is a race, skip action
            return
        
        failcheck = self.failTrain(self.Energy)
        if failcheck:
            print('Training Failed')
            self.Mood += -1
        else: 
            self.Energy += -20
            if self.Energy <= 0:
                self.Energy = 0
            
            level = self.gutsTraincount //4 + 1
            gutsGain = (1 + self.gutsGrwth) * (level + 9)
            speedGain = (1 + self.speedGrwth) * (level + 4)
            powerGain = (1 + self.powerGrwth) * (level + 4)
            skillGain = 2

            self.guts += gutsGain
            self.speed += speedGain
            self.power += powerGain
            self.skillpts += skillGain
            self.gutsTraincount += 1

            print(f"[Guts Training Lv{level}] "
              f"+{int(gutsGain)} Guts, +{int(speedGain)} Speed, "
              f"+{int(powerGain)} Power, +{int(skillGain)} SkillPts")
            newLevel = self.gutsTraincount // 4 + 1
            if newLevel > level:
                print(f"Speed Training leveled up! Lv{newLevel}")

            self.turnCount()
            
    def witTrain(self):

        if self.checkRaceDay(): # If there is a race, skip action
            return
        
        failcheck = self.failTrain(self.Energy)
        if failcheck:
            print('Training Failed')
            self.Mood += -1
            
        else:
            self.Energy += 5
            if self.Energy > 100:
                self.Energy = 100
            
            level = self.witTraincount //4 + 1
            witGain = (1 + self.witGrwth) * (level + 9)
            speedGain = ( 1 + self.speedGrwth) * (level + 1)
            skillGain = 4 + level

            self.wit += witGain
            self.speed += speedGain
            self.skillpts += skillGain

            print(f"[Wit Training Lv{level}] +{witGain} Wit, +{speedGain} Speed, +{skillGain} SkillPts")
            newLevel = self.witTraincount // 4 + 1
            if newLevel > level:
                print(f"Speed Training leveled up! Lv{newLevel}")

            self.turnCount()
            
    def failureRate(self,energy):
        if (energy/100) >= 0.5:
            return 0.0
        else:
            k = 6
            n = 1.6
            deficit = (0.5 - (energy/100)) ** n
            return 0.99 * (1 - math.exp(-k * deficit))   
            
    def failTrain(self,energy):
        """
        Returns True if training fails, False otherwise.
        """
        fail_prob = self.failureRate(energy)
        roll = random.random()  # Uniform [0.0, 1.0)
        return roll < fail_prob

    def rest(self):
        self.turnCount()

        if self.checkRaceDay(): # If there is a race, skip action
            return
        
        roll = random.random()  # Value between 0.0 and 1.0

        if roll < 0.25:
            self.Energy += 70
            print('Well Rested! Energy restored by 70 Pts')
        elif roll < 0.75:
            self.Energy += 50
            print('Energy restored by 50 Pts')
        else:
            self.Energy += 30
            print('Sleep Deprived. Energy restored by 30 Pts')

        # Cap to max energy
        if self.Energy > 100:
            self.Energy = 100

    def recreation(self):

        if self.checkRaceDay(): # If there is a race, skip action
            return
        
        roll = random.random()
        if self.Mood <= 3:
            if roll < .25:
                self.Mood += 2
                print('Karaoke Outing! +2 Mood.')
            elif roll < .75:
                self.Mood += 1
                self.Energy += 15
                #Cure Negative Effect
                print('Shrine Outing! +1 Mood, +15 Energy.')
            else:
                score = self.clawMachine()
                if score == 1:
                    self.Energy += 10
                    self.Mood += 1
                    #Add Hint 30% Chance
                    print(f'You got {score} plushy! +1 Mood, +10 Energy')
                if score == 2:
                    self.Energy += 20
                    self.Mood += 1
                    print(f'You got {score} plushies! +1 Mood, +20 Energy')
                if score == 3:
                    self.Energy += 30
                    self.Mood += 2
                    print(f'Amazing! You got {score} plushies! +2 Mood, +30 Energy')
        else:
            self.Mood += 1
            self.Energy += 20
            print(f'Park Outing! +1 Mood, +20 Energy')

        self.turnCount()
        
    def clawMachine(self):
        attempt = 3
        score = 0
        print("Welcome to the Arcade! Let's play the Claw Machine.")
        print("To play, choose where to drop the claw: Left, Right, or Center. You get 3 attempts!")
        while attempt > 0:
            plushyPos = random.choice(["Left", "Right", "Center"])
            print(f'\nAttempt {4-attempt}. Ready? ')
            clawPos = input('Left, Right or Center? ').strip().capitalize()
            if clawPos == plushyPos:
                attempt += -1
                score += 1
                print(f'Congratulations! You won a prize! Score +1! Current Score: {score}. {attempt} attempts left.')
                
            else:
                attempt += -1
                print(f'Awww! Nice try, better luck next time! Current Score {score}. {attempt} attempt lefts.')

        print(f"\nGame Over! Final Score: {score}")     
        return score

def playTurn(uma):
    while True:
        print(f"\n--- Turn {uma.TurnCount} ---")
        print(uma)
        print("💪 What would you like to do?")
        print("1. Speed Train")
        print("2. Stamina Train")
        print("3. Power Train")
        print("4. Guts Train")
        print("5. Wit Train")
        print("6. Rest")
        print("7. Recreation")
        print("8. View Skills")
        print("9. End Turn")

        choice = input("Enter your choice (1–9): ").strip()

        if choice == "1":
            uma.speedTrain()
        elif choice == "2":
            uma.staminaTrain()
        elif choice == "3":
            uma.powerTrain()
        elif choice == "4":
            uma.gutsTrain()
        elif choice == "5":
            uma.witTrain()
        elif choice == "6":
            uma.rest()
        elif choice == "7":
            uma.recreation()
        elif choice == "8":
            print(uma)
        else:
            print("❌ Invalid choice. Try again.")
            
def umaRoster():
    #Creates Uma's wih associated stats along with their schedules
    special_week_schedule = {
    5: {"name": "Debut Race", "difficulty": 200, "runners": 5,"fanReward": 800},
    12: {"name": "Junior Finals", "difficulty": 280, "runners": 8, "fanReward": 1200},
    24: {"name": "Classic Finals", "difficulty": 340, "runners": 12,"fanReward": 1600},
    36: {"name": "Senior Finals", "difficulty": 400, "runners": 16,"fanReward": 2500}
}

    gold_ship_schedule = {
    5: {"name": "Debut Race", "difficulty": 200, "runners": 5,"fanReward": 800},
    12: {"name": "Junior Finals", "difficulty": 280, "runners": 8, "fanReward": 1200},
    24: {"name": "Classic Finals", "difficulty": 340, "runners": 12,"fanReward": 1600},
    36: {"name": "Senior Finals", "difficulty": 400, "runners": 16,"fanReward": 2500}
}

    special_week = Career(
    name="Special Week",
    speed=100,
    stamina=100,
    power=100,
    guts=100,
    wit=100,
    skillpts=140,
    speedGrwth=0,
    staminaGrwth=.2,
    powerGrwth=0,
    gutsGrwth=0,
    witGrwth=.1,
    raceSchedule = special_week_schedule
    )

    gold_ship = Career(
    name="Gold Ship",
    speed=82,
    stamina=96,
    power=100,
    guts=77,
    wit=70,
    skillpts=140,
    speedGrwth=0,
    staminaGrwth=.2,
    powerGrwth=.1,
    gutsGrwth=0,
    witGrwth=0,
    raceSchedule = gold_ship_schedule
    )
    
    return{"1": special_week,
           "2": gold_ship
           }
def umaSelect():
    roster = umaRoster()

    print("Select your Umamusume!")
    for key, uma in roster.items():
        print(f"{key}.{uma.Uma}")

    choice = input("Enter the number of your choice: ").strip()
    while choice not in roster:
        print("Invalid choice. Try again.")
        choice = input("Enter a valid number: ").strip()

    selected = roster[choice]
    print(f"\nYou selected: {selected.Uma}!\n")
    return selected

def main():   

    uma = umaSelect()
    lastTurn = max(uma.raceSchedule.keys())
    while uma.TurnCount <= lastTurn:
        playTurn(uma)
    
    
    
    
    
if __name__ == "__main__":
    main()



