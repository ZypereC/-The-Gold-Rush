import time
from Finances import Graphing
import math
import random

print("This is the beginning of the game that runs in our terminal")

def print_gold_nugget():
    nugget = r"""
            @@@%%%%####***++==--..                
        @@@@%%%%%%######****++==--:::....        
     @@@%%%%%%%########****+++==---:::.....      
   @@@%%%%%%%#########*****+++==---:::.....      
  @@%%%%%%%#########******+++==---:::......      
 @@%%%%%%%#########******++++==---:::......      
 @@%%%%%%%########******++++==---::::......      
 @@%%%%%%%########******++++==---::::......      
  @@%%%%%%%########******+++==---:::......        
   @@%%%%%%%########*****+++==---:::.....        
    @@@%%%%%%%######****+++==---:::.....          
      @@@%%%%%%%####***++==---:::.....            
        @@@%%%%%%###***++==--:::....              
            @@%%%%##***++==--::....              
    """
    print(nugget)

def ascii_gold_text():
    art = r"""
       ____       ____                   __  
      /  ___|    /    \        | |      |   \
     | |  _     |  /\  |       | |      | |\ \
     | |_| |    | |  | |       | |___   | |/ /
      \____|    \______/       |_____|  |___/
    """
    print(art)

def print_gold():
    G = [
        " /███\\",
        "/     \\",
        "| /███ ",
        "| |    ",
        " \\___/"
    ]
   
    O = [
        " /███\\",
        "/     \\",
        "|     |",
        "|     |",
        " \\___/"
    ]
   
    L = [
        "/      ",
        "|      ",
        "|      ",
        "|      ",
        "|______"
    ]
   
    D = [
        "/███\\ ",
        "|    \\",
        "|    |",
        "|    /",
        "\\___/ "
    ]
   
    for i in range(5):
        print(G[i] + "  " + O[i] + "  " + L[i] + "  " + D[i])

if __name__ == "__main__":
    print_gold_nugget()
    print()  # Add some spacing
    ascii_gold_text()

Goal_distance = 2000  # miles to california
Distance = 0  # starting distance
Days = 0  # starting day
InventorySlots = 5  # starting inventory slots
TravelSpeed = 0  # miles per day, will be set based on travel method
Food = 100
Stamina = 100
Water = 100

def typer(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # For a new line after the text

typer("Welcome to the Gold rush!\n", 0.04)

print('''You hear that there are Gold nuggets on the coast of california if you get there early enough and set out to upgrade your tools and get there on time you might just become the richest person
       in your families heritage for the next few generations as the Newspapers in New york city say\n''',)

Starting = input(" would you like to set out to california in hopes to find gold? (yes or no)").strip()
    
if Starting.lower() == 'yes':
        typer("Great! Let's get started on your journey to California!\n", 0.03)
        account = Graphing()
        account.deposit(50)  # Starting money for the player
        print(f"You start your journey with a balance of ${account.balance:.2f}.\n")
else:
        typer("Maybe next time! Goodbye!", 0.03)
        exit()

StartingGear = input(f'''You have several options for starting travel gear:
1. Horse ($20) - Faster travel speed, moderate inventory space.
2. Wagon ($30) - Slower travel speed, larger inventory space.
3. Foot ($0) - Slowest travel speed, limited inventory space.
Choose your starting gear (horse, wagon, foot):''')

if StartingGear.lower() == 'horse':
        account.withdraw(20)
        TravelSpeed = 15  # miles per day
        typer("You chose to travel with a horse. Your speed is 15 miles per day.\n", 0.03)
        print(f"Your remaining balance is ${account.balance:.2f}.\n")
        print(f"you have {InventorySlots} inventory slots.")

elif StartingGear.lower() == 'wagon':
    account.withdraw(30)
    TravelSpeed = 10  # miles per day
    typer("You chose to travel with a wagon. Your speed is 10 miles per day.\n", 0.03)
    print(f"Your remaining balance is ${account.balance:.2f}.\n")
    print(f"you have {InventorySlots} inventory slots.")
    InventorySlots += 3  # Increase inventory slots for wagon
    print(f"With the wagon, you now have {InventorySlots} inventory slots.")

elif StartingGear.lower() == 'foot':
    TravelSpeed = 5  # miles per day
    typer("You chose to travel on foot. Your speed is 5 miles per day.", 0.03)

else:
    typer("Invalid choice. You will travel on foot by default. Your speed is 5 miles per day.", 0.03)
    TravelSpeed = 5  # miles per day
    print(f"you have {InventorySlots} inventory slots.")

print("Your journey to California begins now!\n")

while Distance < Goal_distance:
    Days += 1
    Distance += TravelSpeed
    if Distance > Goal_distance:
        Distance = Goal_distance  # Prevent overshooting the goal
    
    # Only display progress every 5 days
    if Days % 5 == 0 or Distance >= Goal_distance:
        print(f"Day {Days}: You have traveled {Distance} miles out of {Goal_distance} miles to California.")

    if Days == 10:
        typer("You found a trading post outside a small town, on the edge of Pennsylvania. You can trade some of your money for better gear or supplies.\n", 0.03)
        Options1 = {
            '1': 'buy a wagon for $30',
            '2': "buy a shovel for $5",
            '3': 'buy food for $10',
            '4': 'buy water for $5',
            '5': 'continue on your journey for gold',
        }
        
        while True:
            print(f"\nCurrent balance: ${account.balance:.2f}")
            print(f"Current inventory slots: {InventorySlots}")
            print(f"Food: {Food}, Water: {Water}, Stamina: {Stamina}")
            print("\nOptions:")
            for k, v in Options1.items():
                print(f"{k}: {v}")

            User_input = input("Choose an option (1-5): ").strip()
            
            if User_input == '1':
                if account.balance >= 30:
                    if InventorySlots >= 8:
                        print("You already have a wagon or enough inventory space.")
                    elif StartingGear.lower() == 'wagon':
                        print("You already have a wagon!")
                    else:
                        account.withdraw(30)
                        InventorySlots += 3
                        TravelSpeed = 10  # Upgrade to wagon speed if on foot
                        if StartingGear.lower() == 'foot':
                            StartingGear = 'wagon'
                        print(f"You bought a wagon! Your inventory slots increased to {InventorySlots}.")
                        if TravelSpeed == 5:  # Was on foot
                            TravelSpeed = 10
                            print("Your travel speed increased to 10 miles per day!")
                else:
                    print("You don't have enough money for a wagon ($30).")
                    
            elif User_input == '2':
                if account.balance >= 5:
                    account.withdraw(5)
                    print("You bought a shovel! This will help you mine gold more efficiently when you reach California.")
                    # You could add a shovel variable here to track if player has one
                else:
                    print("You don't have enough money for a shovel ($5).")
                    
            elif User_input == '3':
                if account.balance >= 10:
                    account.withdraw(10)
                    Food += 50
                    print(f"You bought food! Your food increased to {Food}.")
                else:
                    print("You don't have enough money for food ($10).")
                    
            elif User_input == '4':
                if account.balance >= 5:
                    account.withdraw(5)
                    Water += 30
                    print(f"You bought water! Your water increased to {Water}.")
                else:
                    print("You don't have enough money for water ($5).")
                    
            elif User_input == '5':
                typer("You decide to continue on your journey without making any purchases.\n", 0.03)
                break
                
            else:
                print("Invalid option. Please choose 1-5.")
                
            # Ask if they want to continue shopping or move on
            if User_input in ['1', '2', '3', '4']:
                continue_shopping = input("\nWould you like to buy something else? (yes/no): ").strip().lower()
                if continue_shopping != 'yes':
                    typer("You finish your business at the trading post and continue your journey.\n", 0.03)
                    break
                