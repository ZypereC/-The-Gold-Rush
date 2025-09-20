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

def typer(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # For a new line after the text

def random_event():
    """Generate random events that can happen at trading posts"""
    events = [
        {
            'type': 'good',
            'description': "A friendly merchant offers you a great deal on supplies!",
            'effect': 'discount',
            'value': 0.5  # 50% discount on next purchase
        },
        {
            'type': 'bad',
            'description': "Bandits try to rob you! You lose some money but escape safely.",
            'effect': 'lose_money',
            'value': random.randint(5, 15)
        },
        {
            'type': 'good',
            'description': "You find a small pouch of gold coins on the ground!",
            'effect': 'gain_money',
            'value': random.randint(8, 20)
        },
        {
            'type': 'bad',
            'description': "Your supplies spoil in the heat. You lose some food and water.",
            'effect': 'lose_supplies',
            'value': {'food': random.randint(10, 25), 'water': random.randint(5, 15)}
        },
        {
            'type': 'neutral',
            'description': "You meet fellow travelers heading to California. They share stories of the gold rush.",
            'effect': 'morale_boost',
            'value': 10
        },
        {
            'type': 'good',
            'description': "A local doctor tends to your ailments for free. You feel refreshed!",
            'effect': 'restore_stamina',
            'value': 30
        },
        {
            'type': 'bad',
            'description': "Your horse/wagon needs repairs. You must pay for maintenance.",
            'effect': 'repair_cost',
            'value': random.randint(8, 18)
        },
        {
            'type': 'good',
            'description': "A generous farmer gives you fresh supplies!",
            'effect': 'free_supplies',
            'value': {'food': random.randint(15, 30), 'water': random.randint(10, 20)}
        },
        {
            'type': 'bad',
            'description': "You get sick from bad water and need to rest an extra day.",
            'effect': 'lose_day',
            'value': 1
        },
        {
            'type': 'good',
            'description': "You help a stranded traveler and they reward you with mining tools!",
            'effect': 'mining_bonus',
            'value': 1.2  # 20% bonus to future gold mining
        }
    ]
    return random.choice(events)

def handle_random_event(event, account, food, water, stamina, days):
    """Handle the effects of random events"""
    typer(f"\n🎲 RANDOM EVENT: {event['description']}", 0.03)
    
    if event['effect'] == 'discount':
        return {'discount': event['value']}, food, water, stamina, days
    elif event['effect'] == 'lose_money':
        if account.balance >= event['value']:
            account.withdraw(event['value'])
            typer(f"You lost ${event['value']:.2f}!", 0.03)
        else:
            lost = account.balance
            account.balance = 0
            account.record_history(f"Lost remaining ${lost:.2f} to bandits")
            typer(f"You lost all your remaining money (${lost:.2f})!", 0.03)
    elif event['effect'] == 'gain_money':
        account.deposit(event['value'])
        typer(f"You gained ${event['value']:.2f}!", 0.03)
    elif event['effect'] == 'lose_supplies':
        food = max(0, food - event['value']['food'])
        water = max(0, water - event['value']['water'])
        typer(f"You lost {event['value']['food']} food and {event['value']['water']} water!", 0.03)
    elif event['effect'] == 'restore_stamina':
        stamina = min(100, stamina + event['value'])
        typer(f"Your stamina increased by {event['value']}!", 0.03)
    elif event['effect'] == 'repair_cost':
        if account.balance >= event['value']:
            account.withdraw(event['value'])
            typer(f"Repairs cost you ${event['value']:.2f}!", 0.03)
        else:
            typer("You don't have enough money for repairs, but a kind mechanic helps for free!", 0.03)
    elif event['effect'] == 'free_supplies':
        food += event['value']['food']
        water += event['value']['water']
        typer(f"You gained {event['value']['food']} food and {event['value']['water']} water!", 0.03)
    elif event['effect'] == 'lose_day':
        days += event['value']
        typer(f"You lost {event['value']} day(s) due to illness!", 0.03)
    elif event['effect'] == 'mining_bonus':
        typer("You received mining tools that will help you find more gold!", 0.03)
        return {'mining_bonus': event['value']}, food, water, stamina, days
    
    return {}, food, water, stamina, days

def trading_post_encounter(post_name, account, inventory_slots, food, water, stamina, days, special_modifiers=None):
    """Handle trading post encounters with random events"""
    typer(f"\n🏪 You arrive at {post_name}!", 0.03)
    
    # Random event chance (70% chance)
    if random.random() < 0.7:
        event = random_event()
        event_result, food, water, stamina, days = handle_random_event(event, account, food, water, stamina, days)
        if special_modifiers is None:
            special_modifiers = {}
        special_modifiers.update(event_result)
    
    # Trading options
    discount_multiplier = 1.0
    if special_modifiers and 'discount' in special_modifiers:
        discount_multiplier = special_modifiers['discount']
        typer("🎉 You have a discount available for this trading post!", 0.03)
    
    options = {
        '1': f'Buy food for ${10 * discount_multiplier:.2f}',
        '2': f'Buy water for ${5 * discount_multiplier:.2f}',
        '3': f'Buy medicine (restore stamina) for ${12 * discount_multiplier:.2f}',
        '4': f'Buy extra supplies bundle for ${25 * discount_multiplier:.2f}',
        '5': 'Rest for the day (restore stamina, but lose a day)',
        '6': 'Continue journey'
    }
    
    while True:
        print(f"\n💰 Current balance: ${account.balance:.2f}")
        print(f"🎒 Inventory slots: {inventory_slots}")
        print(f"🍖 Food: {food} | 💧 Water: {water} | ⚡ Stamina: {stamina}")
        print(f"📅 Days traveled: {days}")
        print("\nTrading Post Options:")
        for k, v in options.items():
            print(f"{k}: {v}")

        choice = input("Choose an option (1-6): ").strip()
        
        if choice == '1':
            cost = 10 * discount_multiplier
            if account.balance >= cost:
                account.withdraw(cost)
                food += 30
                print(f"You bought food! Food increased to {food}.")
            else:
                print(f"You don't have enough money (${cost:.2f}).")
                
        elif choice == '2':
            cost = 5 * discount_multiplier
            if account.balance >= cost:
                account.withdraw(cost)
                water += 25
                print(f"You bought water! Water increased to {water}.")
            else:
                print(f"You don't have enough money (${cost:.2f}).")
                
        elif choice == '3':
            cost = 12 * discount_multiplier
            if account.balance >= cost:
                account.withdraw(cost)
                stamina = min(100, stamina + 40)
                print(f"You bought medicine! Stamina restored to {stamina}.")
            else:
                print(f"You don't have enough money (${cost:.2f}).")
                
        elif choice == '4':
            cost = 25 * discount_multiplier
            if account.balance >= cost:
                account.withdraw(cost)
                food += 50
                water += 35
                stamina = min(100, stamina + 20)
                print(f"You bought the supply bundle! Food: {food}, Water: {water}, Stamina: {stamina}")
            else:
                print(f"You don't have enough money (${cost:.2f}).")
                
        elif choice == '5':
            stamina = min(100, stamina + 50)
            days += 1
            print(f"You rested for the day. Stamina restored to {stamina}, but you lost a day.")
            
        elif choice == '6':
            typer("You continue your journey westward!", 0.03)
            break
            
        else:
            print("Invalid option. Please choose 1-6.")
            
        if choice in ['1', '2', '3', '4', '5']:
            continue_shopping = input("\nContinue at trading post? (yes/no): ").strip().lower()
            if continue_shopping != 'yes':
                break
    
    return food, water, stamina, days, special_modifiers

def mine_for_gold(account, special_modifiers=None):
    """Gold mining mini-game in California"""
    typer("\n⛏️  WELCOME TO CALIFORNIA! Time to mine for gold! ⛏️", 0.03)
    
    mining_bonus = 1.0
    if special_modifiers and 'mining_bonus' in special_modifiers:
        mining_bonus = special_modifiers['mining_bonus']
        typer("🔧 Your special mining tools give you an advantage!", 0.03)
    
    total_gold_value = 0
    mining_days = 0
    max_mining_days = 30
    
    while mining_days < max_mining_days:
        print(f"\n📅 Mining Day {mining_days + 1}/{max_mining_days}")
        print(f"💰 Total gold value so far: ${total_gold_value:.2f}")
        
        choice = input("Do you want to mine today? (yes/no/quit): ").strip().lower()
        
        if choice == 'quit':
            break
        elif choice == 'yes':
            mining_days += 1
            
            # Random mining results
            luck = random.random()
            if luck < 0.1:  # 10% chance - big strike!
                gold_found = random.randint(50, 150) * mining_bonus
                typer(f"🌟 EUREKA! You struck it rich and found ${gold_found:.2f} worth of gold!", 0.03)
            elif luck < 0.3:  # 20% chance - good day
                gold_found = random.randint(20, 50) * mining_bonus
                typer(f"✨ Good day! You found ${gold_found:.2f} worth of gold!", 0.03)
            elif luck < 0.6:  # 30% chance - average day
                gold_found = random.randint(5, 20) * mining_bonus
                typer(f"⚒️  Decent day. You found ${gold_found:.2f} worth of gold.", 0.03)
            elif luck < 0.8:  # 20% chance - poor day
                gold_found = random.randint(1, 5) * mining_bonus
                typer(f"😓 Tough day. Only found ${gold_found:.2f} worth of gold.", 0.03)
            else:  # 20% chance - nothing
                gold_found = 0
                typer("💔 No luck today. You found no gold.", 0.03)
            
            total_gold_value += gold_found
            account.deposit(gold_found)
            
        elif choice == 'no':
            mining_days += 1
            typer("You rested for the day.", 0.03)
        else:
            print("Please enter yes, no, or quit.")
            continue
    
    return total_gold_value

if __name__ == "__main__":
    print_gold_nugget()
    print()
    ascii_gold_text()

    Goal_distance = 2000  # miles to california
    Distance = 0  # starting distance
    Days = 0  # starting day
    InventorySlots = 5  # starting inventory slots
    TravelSpeed = 0  # miles per day
    Food = 100
    Stamina = 100
    Water = 100
    special_modifiers = {}

    typer("Welcome to the Gold rush!\n", 0.04)

    print('''You hear that there are Gold nuggets on the coast of california if you get there early enough and set out to upgrade your tools and get there on time you might just become the richest person
           in your families heritage for the next few generations as the Newspapers in New york city say\n''')

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
        InventorySlots += 3  # Increase inventory slots for wagon
        print(f"With the wagon, you now have {InventorySlots} inventory slots.")

    elif StartingGear.lower() == 'foot':
        TravelSpeed = 5  # miles per day
        typer("You chose to travel on foot. Your speed is 5 miles per day.", 0.03)
        print(f"you have {InventorySlots} inventory slots.")

    else:
        typer("Invalid choice. You will travel on foot by default. Your speed is 5 miles per day.", 0.03)
        TravelSpeed = 5  # miles per day
        print(f"you have {InventorySlots} inventory slots.")

    print("Your journey to California begins now!\n")

    # Trading posts along the way
    trading_posts = [
        (400, "Frontier Trading Post, Ohio"),
        (800, "Prairie Outpost, Missouri"),
        (1200, "Mountain Supply Station, Colorado"),
        (1600, "Desert Oasis Trading, Nevada"),
    ]

    current_post_index = 0

    while Distance < Goal_distance:
        Days += 1
        Distance += TravelSpeed
        
        # Resource consumption
        if Days % 5 == 0:  # Every 5 days (slower consumption)
            Food = max(0, Food - random.randint(5, 10))
            Water = max(0, Water - random.randint(3, 8))
            Stamina = max(0, Stamina - random.randint(3, 8))
        
        # Check for game over conditions
        if Food <= 0:
            typer("\n💀 GAME OVER: You ran out of food and starved on the trail!", 0.03)
            typer("Your journey to California ends here...", 0.03)
            print(f"\n📊 FINAL STATS:")
            print(f"📅 Days survived: {Days}")
            print(f"📍 Distance traveled: {Distance}/{Goal_distance} miles")
            print(f"💰 Final balance: ${account.balance:.2f}")
            account.Build_graph()
            exit()
        
        if Water <= 0:
            typer("\n💀 GAME OVER: You died of thirst on the trail!", 0.03)
            typer("Your journey to California ends here...", 0.03)
            print(f"\n📊 FINAL STATS:")
            print(f"📅 Days survived: {Days}")
            print(f"📍 Distance traveled: {Distance}/{Goal_distance} miles")
            print(f"💰 Final balance: ${account.balance:.2f}")
            account.Build_graph()
            exit()
        
        if Stamina <= 0:
            typer("\n💀 GAME OVER: You collapsed from exhaustion on the trail!", 0.03)
            typer("Your journey to California ends here...", 0.03)
            print(f"\n📊 FINAL STATS:")
            print(f"📅 Days survived: {Days}")
            print(f"📍 Distance traveled: {Distance}/{Goal_distance} miles")
            print(f"💰 Final balance: ${account.balance:.2f}")
            account.Build_graph()
            exit()
        
        if Distance > Goal_distance:
            Distance = Goal_distance
        
        # Check for trading posts
        if current_post_index < len(trading_posts):
            post_distance, post_name = trading_posts[current_post_index]
            if Distance >= post_distance:
                Food, Water, Stamina, Days, special_modifiers = trading_post_encounter(
                    post_name, account, InventorySlots, Food, Water, Stamina, Days, special_modifiers
                )
                current_post_index += 1
        
        # Display progress periodically
        if Days % 5 == 0 or Distance >= Goal_distance:
            print(f"\n📍 Day {Days}: You have traveled {Distance} miles out of {Goal_distance} miles to California.")
            print(f"🍖 Food: {Food} | 💧 Water: {Water} | ⚡ Stamina: {Stamina}")

    # Arrived in California!
    typer("\n🌟 CONGRATULATIONS! You've reached California! 🌟", 0.03)
    typer("The gold fields stretch before you, sparkling in the sunlight!", 0.03)
    
    print(f"\n📊 JOURNEY SUMMARY:")
    print(f"📅 Days traveled: {Days}")
    print(f"💰 Money remaining: ${account.balance:.2f}")
    print(f"🍖 Food remaining: {Food}")
    print(f"💧 Water remaining: {Water}")
    print(f"⚡ Stamina remaining: {Stamina}")
    
    # Gold mining phase
    total_gold = mine_for_gold(account, special_modifiers)
    
    # Final results
    typer(f"\n🏆 FINAL RESULTS 🏆", 0.03)
    typer(f"Total gold mined: ${total_gold:.2f}", 0.03)
    typer(f"Final balance: ${account.balance:.2f}", 0.03)
    
    if account.balance > 500:
        typer("🎉 You struck it rich! You're now wealthy beyond your wildest dreams!", 0.03)
    elif account.balance > 200:
        typer("💰 Great success! You found enough gold to live comfortably!", 0.03)
    elif account.balance > 100:
        typer("⭐ Good job! You found enough gold to make the journey worthwhile!", 0.03)
    else:
        typer("😅 The gold rush was tough, but you survived the adventure!", 0.03)
    
    # Show transaction history
    print("\n📜 Your complete financial history:")
    account.Build_graph()
    
    typer("\nThank you for playing the Gold Rush Adventure! 🌟", 0.03)
                
