import sys, time, textwrap, os

def typing(text):                   #Typing effect on text
    for character in text:
      sys.stdout.write(character)
      sys.stdout.flush()
      time.sleep(0.01)


#variables                              variables
playing = True
instructions = True
current_room = "cell"
inventory = []

#Items Dictionary                              Items Dictionary

master_items = {
    "hook" : {
        "name" : "AN IRON HOOK",
        "weight" : "heavy",
        },
    "lighter" : {
        "name" : "A BRASS LIGHTER",
        "weight" : "light",
        },
    "key" : {
        "name" : "A SHINING BRASS KEY",
        "weight" : "light",
        },

    }




#Room Dictionary                              Room Dictionary

dungeon = {
    "cell" : {
        "name" : "THE CELL.",
        "desc" : "A DARK AND GLOOMY CELL. THERE IS MOULD AND ALGAE GROWING ON THE CEILING AND PAINT IS PEELING OFF THE WALLS. THERE IS A LOCKED DOOR OF STEEL BARS NORTH OF YOU. THERE IS A MANKY BED IN THE ROOM AS WELL AS A MAHOGANY CHEST OF DRAWERS WITH BRASS HANDLES. A DISTINCT SMELL OF ROTTING LINGERS IN THE ROOM.",
        "visited" : False,
        "exits" : {},

        "objects" : {
            "bed" : {
                "examine" : "YOU SEE AN INCREDIBLY MANKY BED WITH MOULD GROWING ON THE MATTRESS. THE BEDSHEETS ARE TORN AT THE CORNERS. YOU PEER UNDERNEATH AND SPOT AN IRON HOOK WITH A RUSTED END!",
                "examine_taken" : "YOU SEE AN INCREDIBLY MANKY BED WITH MOULD GROWING ON THE MATTRESS. THE BEDSHEETS ARE TORN AT THE CORNERS. THERE IS NOTHING UNDERNEATH.",
                "has_item" : True,
                },
            "drawers" : {
                "examine" : "IT IS A MAHOGANY CHEST OF DRAWERS WITH SCRATCHES ETCHED ACROSS THE FRONT AND BRASS HANDLES IN NEED OF A POLISH. THE BOTTOM TWO DRAWERS ARE SCREWED SHUT BUT THE TOP ONE OPENS AND YOU SEE A BRASS LIGHTER FILLED WITH FRESH OIL! INSIDE!",
                "examine_taken" : "IT IS A MAHOGANY CHEST OF DRAWERS WITH SCRATCHES ETCHED ACROSS THE FRONT AND BRASS HANDLES IN NEED OF A POLISH. THE BOTTOM TWO DRAWERS ARE SCREWED SHUT. THE TOP DRAWER IS EMPTY.",
                "has_item" : True,
                },

            "door" : {
                "name" : "THE CELL DOOR",
                "examine" : "IT IS A HEAVY DOOR MADE OF THICK STEEL BARS. IT IS LOCKED. THROUGH THE BARS YOU CAN SEE INTO A DIM CORRIDOR AND ON THE FLOOR YOU SPOT A SHINING BRASS KEY JUST OUT OF REACH. IF ONLY YOU HAD A WAY TO GET IT.",
                "examine_taken" : "IT IS A HEAVY DOOR MADE OF THICK STEEL BARS.",
                "open_locked" : "THE DOOR IS LOCKED.",
                "open_unlocked" : "YOU INSERT THE KEY AND IT FITS PERFECTLY. WITH A STRUGGLE, YOU UNLOCK THE DOOR AND SHOVE IT OPEN.",

                "locked" : True,
                "unlocker" : "key",

                "unlock_direction" : "n",
                "unlock_room" : "corridor",
                },
            },
        "items" : {
            "hook" : {
                "name" : "AN IRON HOOK",
                "hidden_in" : "bed",
                },
            "lighter" : {
                "name" : "A BRASS LIGHTER",
                "hidden_in" : "drawers",
                },
            "key" : {
                "name" : "A SHINING BRASS KEY",
                "hidden_in" : "door"
                }

            },
       },
    "corridor" : {
        "name" : "THE CORRIDOR.",
        "desc" : "A DIMLY LIT, FOUL SMELLING EAST, WEST CORRIDOR. YOU HAVE AN EXIT SOUTH AND NORTH OF YOU BOTH LEADING INTO DARK CELLS. THE CORRIDOR APPEARS TO BE DESERTED.",
        "visited" : False,
        "exits" : {"s" : "cell"},
        "objects" : {},
        "items" : {},
        },
    }


                                                #Help command
Help = "IN THIS GAME YOU MUST ESCAPE THE DUNGEON. USE ONE OR TWO WORD COMMANDS TO NAVIGATE THE GAME. YOU CAN MOVE IN FOUR DIRECTIONS: NORTH, EAST, SOUTH AND WEST. USE THE FIRST LETTER OF THESE WORDS AS SHOWN IN THE LIST OF VALID COMMANDS BELOW. IF YOU FORGET THESE COMMANDS, TYPE HELP TO BRING UP THIS TEXT ONCE MORE.\n\nVALID COMMANDS:\n\n>N\n>S\n>E\n>W\n>GET\n>DROP\n>EXAMINE\n>INVENTORY\n>HEALTH\n>HELP\n>QUIT\n>LOOK\n>OPEN\n>OBJECTS\n>ITEMS\n\nFOLLOW COMMANDS SUCH AS GET, DROP, EXAMINE, AND OPEN WITH A NOUN OR ITEM YOU WISH TO USE. USE Y AND N AS YES AND NO. IF YOU WISH TO KNOW WHICH OBJECTS IN A ROOM ARE INTERACTABLE, USE OBJECTS. IF YOU WISH TO KNOW WHICH ITEMS YOU CAN PICK UP IN A ROOM, USE ITEMS.\n"








#Introduction:                          Introduction:

typing("-----ESCAPE THE DUNGEON----- \n")
time.sleep(1)


while instructions == True:
    typing("WOULD YOU LIKE INSTRUCTIONS? Y/N")
    inst = input("\n> ").lower().strip()
    if inst == "y":
        typing(Help)
        instructions = False
        time.sleep(1)
        typing("\nPRESS ENTER TO START.")
        start_game = input("")
        if start_game == "":
            continue
    elif inst == "n":
        typing("ALRIGHT\n")
        instructions = False
    else:
        typing("PLEASE ANSWER THE QUESTION\n")
        time.sleep(1)

#Game Start:---------------------------------------- Game Start:-----------------------

while playing == True:

    if dungeon[current_room]["visited"] == False:
        typing("\n\nYOU ARE IN " + dungeon[current_room]["desc"])
        dungeon[current_room]["visited"] = True
    else:
        typing("\n\nYOU ARE IN " + dungeon[current_room]["name"])

    for item_name in dungeon[current_room]["items"]:
        if dungeon[current_room]["items"][item_name]["hidden_in"] == None:
            typing("\n\nTHERE IS " + dungeon[current_room]["items"][item_name]["name"] + " HERE!")



    command = input("\n\n> ").lower().strip()          #Input Command

    words = command.split(" ")              #Sentence Splitter

    action = words[0]
    if len(words) > 1:
        target = words[1]
    else:
        target = ""


    if command == "quit":                                             #Quit Command
        typing("ARE YOU SURE YOU WISH TO QUIT? Y/N")
        quitconfirm = input("\n> ").lower().strip()
        if quitconfirm == "y":
            typing("OK.\n")
            break
        elif quitconfirm == "n":
            typing("OK")
            continue
        else:
            typing("I WILL TAKE THAT AS A NO.")
            continue

    elif command == "":                                              #Empty Command
        typing("YOU HAVEN'T DONE ANYTHING!\nPLEASE ENTER A COMMAND.")

    elif command == "look":                                          #Look Command
        typing("YOU ARE IN " + dungeon[current_room]["desc"])

    #Movement--------------------------------------------------------#Movement-------

    elif action == "n":
        if "n" in dungeon[current_room]["exits"]:                   #north
            current_room = dungeon[current_room]["exits"]["n"]
        else:
            typing("YOU CANNOT MOVE IN THAT DIRECTION!")

    elif action == "s":
        if "s" in dungeon[current_room]["exits"]:                   #south
            current_room = dungeon[current_room]["exits"]["s"]
        else:
            typing("YOU CANNOT MOVE IN THAT DIRECTION!")

    elif action == "e":
        if "e" in dungeon[current_room]["exits"]:                   #east
            current_room = dungeon[current_room]["exits"]["e"]
        else:
            typing("YOU CANNOT MOVE IN THAT DIRECTION!")

    elif action == "w":
        if "w" in dungeon[current_room]["exits"]:                   #west
            current_room = dungeon[current_room]["exits"]["w"]
        else:
            typing("YOU CANNOT MOVE IN THAT DIRECTION!")

    #----------------------------------------------------------------------------------

    elif command == "help":                                        #Help Command
        typing(Help)

    elif command == "inventory":                                   #Inventory Command
        if len(inventory) == 0:
            typing("YOU ARE CARRYING NOTHING.")
        else:
            typing("YOU ARE CARRYING:")
            for item in inventory:
                if master_items[item]["weight"] == "heavy":
                    typing("\n\nBIG ITEMS:\n")
                    typing("\n- " + item.upper())
                elif master_items[item]["weight"] == "light":
                    typing("\n\nSMALL ITEMS:\n")
                    typing("\n- " + item.upper())




    elif action == "examine":                                   #Examine command
        if target in dungeon[current_room]["objects"]:

              #door exeption ------------------------------door exeption
            if target == "door":
                if "hook" in inventory:
                    if "key" in dungeon["cell"]["items"]:
                        typing("IT IS A HEAVY DOOR MADE OF THICK STEEL BARS. IT IS LOCKED. THROUGH THE BARS YOU CAN SEE INTO A DIM CORRIDOR AND ON THE FLOOR YOU SPOT A SHINING BRASS KEY JUST OUT OF REACH. YOU DECIDE TO USE THE HOOK YOU FOUND AND PULL THE KEY INTO THE CELL. HOW CLEVER OF YOU!")
                        dungeon["cell"]["items"]["key"]["hidden_in"] = None
                        continue
                    else:
                        typing(dungeon["cell"]["objects"]["door"]["examine_taken"])
                        continue
                else:
                    typing(dungeon["cell"]["objects"]["door"]["examine"])
                    continue
            #door exeption ------------------------------door exeption
            for item_name in dungeon[current_room]["items"]:
                item_details = dungeon[current_room]["items"][item_name]

                if item_details["hidden_in"] == target:
                    item_details["hidden_in"] = None

            obj_data = dungeon[current_room]["objects"][target]
            if "has_item" in obj_data and obj_data["has_item"] == True:
                typing(obj_data["examine"])
                dungeon[current_room]["objects"][target]["has_item"] = False
            elif "examine_taken" in obj_data:
                typing(obj_data["examine_taken"])
            continue
        elif target == "":
            typing("WHAT DO YOU WISH TO EXAMINE?")
            continue
        else:
            typing("I SEE NO " + target.upper() + " HERE.")



    elif command == "objects":                                    #Objects Command
        if len(dungeon[current_room]["objects"]) == 0:
            typing("THERE ARE NO INTERACTABLE OBJECTS HERE.")
            continue
        else:
            typing("THE INTERACTABLE OBJECTS IN THIS ROOM ARE:")
            for object_name in dungeon[current_room]["objects"]:
                typing("\n- " + object_name.upper())

    elif command == "items":                                    #Items Command
        if len(dungeon[current_room]["items"]) == 0:
            typing("THERE ARE NO ITEMS YOU CAN PICK UP RIGHT NOW.")
            continue
        else:
            typing("THE ITEMS YOU CAN PICK UP RIGHT NOW ARE:")
            for itemdectector_name in dungeon[current_room]["items"]:
                if dungeon[current_room]["items"][itemdectector_name]["hidden_in"] == None:
                    typing("\n- " + itemdectector_name.upper())

    elif action == "get":                                         #Get Command
        if target == "":
            typing("WHAT DO YOU WANT TO GET?")
            continue
        elif target in dungeon[current_room]["items"]:
            if dungeon[current_room]["items"][target]["hidden_in"] == None:

                heavy_count = 0
                light_count = 0
                for pocket_item in inventory:
                    if master_items[pocket_item]["weight"] == "heavy":
                        heavy_count = heavy_count + 1
                    elif master_items[pocket_item]["weight"] == "light":
                        light_count = light_count + 1


                item_weight = master_items[target]["weight"]
                if item_weight == "heavy" and heavy_count >= 1:
                    typing("YOUR HANDS ARE FULL. DROP A BIG ITEM TO PICK THIS ONE UP.")
                elif item_weight == "light" and light_count >= 4:
                    typing("YOUR POCKETS ARE FULL. DROP A SMALL ITEM TO PICK THIS ONE UP.")
                else:
                    inventory.append(target)
                    del dungeon[current_room]["items"][target]

                    typing("OK.")
                    continue
            else:
                typing("I SEE NO " + target.upper() + " HERE.")
                continue
        else:
            typing("I SEE NO " + target.upper() + " HERE.")




                                                                #Open Command
    elif action == "open":
        if target == "":
            typing("WHAT DO YOU WANT TO OPEN?")
            continue
        elif target in dungeon[current_room]["objects"]:
            obj_data = dungeon[current_room]["objects"][target]
            if "locked" in obj_data:
                if obj_data["locked"] == True:
                    if obj_data["unlocker"] in inventory:
                        typing(dungeon[current_room]["objects"][target]["open_unlocked"])
                        obj_data["locked"] = False
                        if "unlock_direction" in obj_data:
                            new_dir = obj_data["unlock_direction"]
                            new_room = obj_data["unlock_room"]
                            dungeon[current_room]["exits"][new_dir] = new_room
                            continue
                    else:
                        typing(dungeon[current_room]["objects"][target]["open_locked"])
                        continue
                elif "open" in obj_data:
                    typing(obj_data["open"])
                else:
                    typing("IT CANNOT BE OPENED.")
        else:
            typing("I SEE NO " + target.upper() + " HERE!")











    else:                                                    #END OF COMMANDS!!!!
        typing("I DON'T UNDERSTAND THAT. TYPE HELP FOR A LIST OF VALID COMMANDS.")





