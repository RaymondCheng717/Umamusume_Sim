import random
import math

class supportCard:

    def __init__(self, name, uma, typing, lvl, bonuses):
        self.name = name
        self.uma = uma
        self.typing = typing
        self.lvl = lvl
        self.all_bonuses = bonuses
        self.active_bonuses = self.filter_bonuses()
    

    def __str__(self):
        return f"{self.name} ({self.uma}) Lv{self.lvl} {self.typing}"
    
    def filter_bonuses(self):
        active = {}
        for level, bonus_dict in self.all_bonuses.items():
            if level <= self.lvl:
                for key, value in bonus_dict.items():
                    value = func(self.lvl) 
                    active[key] = active.get(key, 0) + value

        
        return active    
        
    def setLVL(self,new_lvl):
        if new_lvl > 45:
            self.lvl = 45
            print(f'Max level is 45')
            print(f'{self.name} set to level 45')
        elif new_lvl < 1:
            self.lvl = 1
            print(f'Minimum level is 1')
            print(f'{self.name} set to level 1')
            
        else:
            self.lvl = new_lvl
        
       
        
    def supportRoster():
        your_team_ace_Bonuses = {
            1: {'Friendship Bonus': 0.1},
            10: {'Specialty Priority': 0.3},
            15: {'Mood Effect': 0.2, 'Race Bonus': 0.2, 'Fan Bonus': 0.1},
            35: {'Guts Bonus': 0.2},
            40: {'Stamina Bonus': 0.2, 'Initial Stamina': 15},
            45: {'Hint Frequency': 0.1}
        }

        your_team_ace = supportCard(
            name='[Your Team Ace]',
            uma='Mejiro Mcqueen',
            typing = 'Stamina',
            lvl=1,
            bonuses=your_team_ace_Bonuses
    )
        fire_at_my_heels_Bonuses = {
            1: {
                'Friendship Bonus': lambda lvl: 0.1,
                'Initial Friendship': lambda lvl: 10 + max((lvl - 1) // 2, 0)  # +1 every 2 levels
            },
            10: {
                'Training Effectiveness': lambda lvl: 0.3,
                'Race Bonus': lambda lvl: 0.1,
                'Fan Bonus': lambda lvl: 0.1
            },
            15: {
                'Mood Effect': lambda lvl: 0.2,
                'Hint Levels': lambda lvl: 0.2,
                'Hint Frequency': lambda lvl: 0.1
            },
            35: {
                'Power Bonus': lambda lvl: 0.2
            },
            40: {
                'Training Effectiveness': lambda lvl: 0.05,
                'Training Frequency': lambda lvl: 20
            },
            45: {
                'Specialty Priority': lambda lvl: 0.1
            }
        }
        fire_at_my_heels = supportCard(
            name = '[Fire at my Heels]',
            uma = 'Kitasan Black',
            typing = 'Speed',
            lvl = 1,
            bonuses = fire_at_my_heels_Bonuses
            )

        return {"1": your_team_ace,
                "2": fire_at_my_heels}
                
def main():
    # Get the support roster dictionary
    roster = supportCard.supportRoster()

    # Pick the card object from the dictionary
    card = roster["1"]

    # Show the card details
    print(card)  # uses __str__

    # Show active bonuses
    print("Active Bonuses at Level 1:")
    print(card.active_bonuses)

    # Try changing the level
    card.setLVL(15)
    print("\nAfter setting to Level 15:")
    print(card)
    print("Active Bonuses:")
    print(card.filter_bonuses())

    # Try setting above cap
    card.setLVL(50)
    print("\nAfter attempting to set to Level 50:")
    print(card)
    print("Active Bonuses:")
    print(card.filter_bonuses())

    # Try setting below min
    card.setLVL(-2)
    print("\nAfter attempting to set to Level -2:")
    print(card)
    print("Active Bonuses:")
    print(card.filter_bonuses())

if __name__ == "__main__":
    main()
    
