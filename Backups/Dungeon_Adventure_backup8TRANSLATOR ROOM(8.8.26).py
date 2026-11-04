import sys, time, textwrap, os, copy, random, json, glob

def typing(text):
    terminal_size = os.get_terminal_size().columns
    wrap_width = terminal_size - 4
    if wrap_width < 20:
        wrap_width = 20

    paragraphs = text.split("\n")

    for paragraph in paragraphs:
        if paragraph.strip() == "":
            sys.stdout.write("\n")
            continue
        wrapped_lines = textwrap.wrap(paragraph, width=wrap_width)

        for line in wrapped_lines:
            for character in line:
                sys.stdout.write(character)
                sys.stdout.flush()
                time.sleep(0.01005)
            sys.stdout.write("\n")

score = 0                                       #Scoring
secrets = 0
discoveries = []

def discover(discovery_points=0, secret=False, discovery_name=None):
    global score
    global secrets

    if discovery_name == None:
        score += discovery_points

    elif discovery_name != None:
        if discovery_name not in discoveries:
            discoveries.append(discovery_name)
            score += discovery_points
    if secret == True:
        secrets += 1

def loading_bar(message, total_time):
    window_size = os.get_terminal_size().columns
    header_text = message
    sys.stdout.write(header_text)
    sys.stdout.flush()
    time.sleep(0.1)
    bar_length = window_size - (len(header_text) -1) -1
    if bar_length < 10:
        bar_length = 10
    load_time = total_time
    bar_characters = load_time / bar_length
    for i in range(bar_length):
        sys.stdout.write("-")
        sys.stdout.flush()
        time.sleep(bar_characters)




devmode = False
god = False
safe = False
#variables                              variables
playing = True
instructions = True
current_room = "cell"
inventory = []
switch_active = True
lighter_lit = False
lighter_is_lit = False
ending = ""
pigeon_tame = False
previous_room = current_room
met_prisoners = False
rubble_in_room = 3
rubble_in_pile = 0
guard_in_room = False
guard_alert = 0
is_hidden = False
switch_used = False
guard_water_count = 0
whistle_blown = 0

danger_zone1_Backup = ["industrial_junction", "vent_room", "boiler_room", "water_room", "translator_room", "tight_corridor", "dull_room", "guard_office_1", "workshop"]
danger_zone2_Backup = ["security_hall", "max_security_west", "max_security", "max_security_east"]

danger_zone1 = ["industrial_junction", "vent_room", "boiler_room", "water_room", "translator_room", "tight_corridor", "dull_room", "guard_office_1", "workshop"]
danger_zone2 = ["security_hall", "max_security_west", "max_security", "max_security_east"]

#Ranks Dictionary + endings--------------------------Ranks Dictionary + endings----------------------
ranks = {
    "escape" : {
        "1" : {
            "min_score" : 0,
            "max_score" :50,           #INTEGER 1
            "name" : "HOPELESSLY LOST"
            },
        "2" : {
            "min_score" : 50,             #INTEGER 2
            "max_score" : 66,             #INTEGER 3
            "name" : "AVERAGE PRISONER"
            },
        "3" : {
            "min_score" : 66,#INTEGER 3,
            "max_score" : 66,#INTEGER 4,
            "name" : "NOVICE ESCAPIST"
            },
        "4" : {
            "min_score" : 66,#INTEGER 4,
            "max_score" : 66,#INTEGER 5,
            "name" : "DUNGEON EXPLORER"
                },
        "5" : {
            "min_score" : 66,#INTEGER 5,
            "max_score" : 66,#INTEGER 6,
            "name" : "SEASONED ADVENTURER"
            },
        "6" : {
            "min_score" : 66,#INTEGER 6,
            "max_score" : 66,#INTEGER 7,
            "name" : "MASTER ESCAPIST"
            },
        "7" : {
            "min_score" : 66,#INTEGER 7,
            "max_score" : 66,#INTEGER 8,
            "name" : "MASTER OF THE DUNGEON"
            },
        "8" : {
            "min_score" : 66,#HIGHEST INTEGER,
            "max_score" : 66,# 1 ABOVE HIGHEST INTEGER,
            "name" : "LEGEND OF BLACKSTONE"
            },
        },

    "defeat" : {
        "1" : {
            "min_score" : 0,
            "max_score" : 50,           #INTEGER 1,
            "name" : "HOPELESSLY LOST"
            },
        "2" : {
            "min_score" : 50,                  #INTEGER 2,
            "max_score" : 66,                  #INTEGER 3,
            "name" : "AVERAGE PRISONER"
            },
        "3" : {
            "min_score" : 66,#INTEGER 3,
            "max_score" : 66,#INTEGER 4,
            "name" : "TROUBLEMAKER"
            },
        "4" : {
            "min_score" : 66,#INTEGER 4,
            "max_score" : 66,#INTEGER 5,
            "name" : "DUNGEON EXPLORER"
                },
        "5" : {
            "min_score" : 66,#INTEGER 5,
            "max_score" : 66,#INTEGER 6,
            "name" : "SEASONED ADVENTURER"
            },
        "6" : {
            "min_score" : 66,#INTEGER 6,
            "max_score" : 66,#INTEGER 7,
            "name" : "MASTER EXPLORER"
            },
        "7" : {
            "min_score" : 66,#INTEGER 7,
            "max_score" : 66,#INTEGER 8,
            "name" : "MASTER OF THE DUNGEON"
            },
        "8" : {
            "min_score" : 66,#HIGHEST INTEGER,
            "max_score" : 66,#1 ABOVE HIGHEST INTEGER,
            "name" : "LEGEND OF BLACKSTONE"
            },
        },
    }

def end():                                              #endings
    global score
    global secrets
    global ranks
    if ending == "death" or ending == "capture":
        for rank_type in ranks["defeat"]:
            if ranks["defeat"][rank_type]["min_score"] <= score and ranks["defeat"][rank_type]["max_score"] > score:
                rank = ranks["defeat"][rank_type]["name"]
                continue
    if ending == "escape":
        for rank_type in ranks["escape"]:
            if ranks["escape"][rank_type]["min_score"] <= score and ranks["escape"][rank_type]["max_score"] > score:
                rank = ranks["escape"][rank_type]["name"]
                continue


    loading_bar("", 0.01005)
    typing("\n\nSCORE: " +str(score) + "\n\nSECRETS: [" + str(secrets) + "/undefined_number]" + "\n\nRANK: " + rank + "\n")
    loading_bar("", 0.01005)
    typing("\n\n\nTYPE 'DISCOVERIES' TO LIST THE SECRETS YOU HAVE FOUND OR PRESS ENTER TO END THE GAME.")

    while True:
        discoverylist = input("\n\n> ").lower().strip()

        if discoverylist == "":
            break
        elif discoverylist == "discoveries":
            typing("\n\nDISCOVERIES:")
            if len(discoveries) < 1:
                typing("\nYOU HAVEN'T MADE ANY NOTABLE DISCOVERIES!")
                loading_bar("", 0.01005)
                time.sleep(3)
                break
            else:
                for secret_discovery in discoveries:
                    typing("\n- " + secret_discovery)
                loading_bar("", 0.01005)
                time.sleep(3)
                break
        else:
            typing("EITHER PRESS ENTER OR TYPE 'DISCOVERIES'.")
            continue


#-------------------------------------------------------------------------------------------------

template = {
    "room_template" : {
        "name" : "",
        "desc" : "",
        "visited" : False,
        "exits" : {},
        "objects" : {},
        "items" : {},
        },

    "dark_room_template" : {
        "dark" : True,
        "name" : "",
        "desc" : "IT IS TOO DARK TO SEE ANYTHING.",
        "desc_lit" : "",
        "visited" : False,
        "exits" : {},
        "objects" : {},
        "items" : {},
        },
    }

#Items Dictionary                              Items Dictionary
master_items = {
    "hook" : {
        "name" : "AN IRON HOOK",
        "weight" : "heavy",
        "examine" : "IT'S A LARGE IRON HOOK WITH A RUSTED END.",
        },
    "lighter" : {
        "used" : False,
        "name" : "A BRASS LIGHTER",
        "weight" : "light",
        "examine" : "IT'S A DIRTY BRASS LIGHTER. IT HAS NO OIL IN IT.",
        "examine_used" : "IT'S A DIRTY BRASS LIGHTER. IT IS LIT AND FULL OF OIL.",
        "open" : "THE FLAME IS LIT INSIDE THE LIGHTER.",
        },
    "key" : {
        "name" : "A SHINING BRASS KEY",
        "weight" : "light",
        "examine" : "IT'S A SHINING BRASS KEY THAT UNLOCKS YOUR CELL DOOR.",
        },
    "pot" : {
        "name" : "A NASTY CHAMBER POT",
        "weight" : "heavy",
        "examine" : "IT IS A NASTY GREEN CERAMIC CHAMBER POT THAT LOOKS LIKE IT HAS BEEN USED MANY TIMES. I'M NOT SURE YOU'D REALLY WANT THIS.",
        },
    "ticket" : {
        "name" : "A SPARKLING CINEMA TICKET",
        "weight" : "light",
        "examine" : "IT'S A SPARKLING, GOLDEN CINEMA TICKET.",
        },
    "bottle" : {
        "name" : "A PLASTIC BOTTLE",
        "weight" : "light",
        "examine" : "IT'S A SMALL PLASTIC BOTTLE THAT CAN STORE SOME LIQUIDS.",
        },
    "oil" : {
        "name" : "A CAN OF OIL",
        "weight" : "light",
        "examine" : "IT'S A SMALL METAL CAN FULL OF LIGHTER OIL.",
        },
    "note" : {
        "name" : "A MYSTERIOUS NOTE",
        "weight" : "light",
        "examine" : "IT'S A NOTE WITH SCRIBBLES IN AN UNIDENTIFIED DIALECT ALL OVER IT. HOW MYSTERIOUS.",
        },
    "instructions" : {
        "name" : "AN INSTRUCTIONS SHEET",
        "weight" : "light",
        "examine" : "IT'S A NOTE THAT YOU PUT THROUGH THE TRANSLATOR. YOU CAN NOW READ IT IN PLAIN ENGLISH. IT IS INSTRUCTIONS ON HOW TO OPERATE SOME KIND OF TORTURE DEVICE.",
        },
    "hat" : {
        "name" : "A HARD HAT",
        "weight" : "light",
        "examine" : "IT IS A BRIGHT YELLOW HARD HAT THAT FITS YOU PERFECTLY.",
        },
    "vinyl" : {
        "name" : "A VINYL DISC",
        "weight" : "light",
        "examine" : "IT IS A SHINY VINYL DISC WITH A NAVY BLUE CENTRE.",
        },
    "chocolate" : {
        "name" : "A CHOCOLATE BAR",
        "weight" : "light",
        "examine" : "IT IS A MILK CHOCOLATE BAR IN RED PLASTIC WRAPPING.",
        },
    "pigeon" : {
        "name" : "A SMALL PIGEON",
        "weight" : "heavy",
        "examine" : "IT'S A SMALL GREY CARRIER PIGEON. THERE'S A LABEL ON IT'S LEG THAT IT WON'T LET YOU SEE.",
        "examine_taken" : "IT'S A SMALL GREY CARRIER PIGEON. THERE'S A LABEL ON IT'S LEG THAT READS '1358'."
        },
    "seeds" : {
        "name" : "A PACKET OF SEEDS",
        "weight" : "light",
        "examine" : "IT IS A SMALL PACKET OF 'QUALITY SUNFLOWER SEEDS'.",
        },
    "roll" : {
        "name" : "SOME TOILET ROLL",
        "weight" : "light",
        "examine" : "IT IS A ROLL OF DISGUSTING TOILET PAPER.",
        },
    "rubble" : {
        "name" : "A CHUNK OF HEAVY RUBBLE",
        "weight" : "heavy",
        "examine" : "IT'S A CHUNK OF DEBRIS CONSISTING OF ROCK, DIRT AND CERAMIC.",
        },
    "water" : {
        "name" : "A FULL BOTTLE OF WATER",
        "weight" : "light",
        "examine" : "IT'S A PLASTIC BOTTLE FULL OF WATER, I'M NOT SURE HOW FRESH IT IS...",
        },
    }





#Room Dictionary                              Room Dictionary

dungeon = {
    "cell" : {
        "name" : "THE CELL.",
        "desc" : "YOU ARE IN A DARK AND GLOOMY CELL. THERE IS MOULD AND ALGAE GROWING ON THE CEILING AND PAINT IS PEELING OFF THE WALLS. THERE IS A LOCKED DOOR OF STEEL BARS NORTH OF YOU. THERE IS A MANKY BED IN THE ROOM AS WELL AS A MAHOGANY CHEST OF DRAWERS WITH BRASS HANDLES. A DISTINCT SMELL OF ROTTING LINGERS IN THE ROOM.",
        "visited" : False,
        "exits" : {},
        "blocked_exits" : {
            "n" : "THE DOOR IS LOCKED. THERE MUST BE A KEY AROUND SOMEWHERE."
            },

        "objects" : {
            "bed" : {
                "examine" : "YOU SEE AN INCREDIBLY MANKY BED WITH MOULD GROWING ON THE MATTRESS. THE BED SHEETS ARE TORN AT THE CORNERS. YOU PEER UNDERNEATH AND SPOT AN IRON HOOK WITH A RUSTED END!",
                "examine_taken" : "YOU SEE AN INCREDIBLY MANKY BED WITH MOULD GROWING ON THE MATTRESS. THE BED SHEETS ARE TORN AT THE CORNERS. THERE IS NOTHING UNDERNEATH.",
                "has_item" : True,
                },
            "drawers" : {
                "examine" : "IT IS A MAHOGANY CHEST OF DRAWERS WITH SCRATCHES ETCHED ACROSS THE FRONT AND BRASS HANDLES IN NEED OF A POLISH. THE BOTTOM TWO DRAWERS ARE SCREWED SHUT BUT THE TOP ONE OPENS AND YOU SEE A BRASS LIGHTER INSIDE!",
                "examine_taken" : "IT IS A MAHOGANY CHEST OF DRAWERS WITH SCRATCHES ETCHED ACROSS THE FRONT AND BRASS HANDLES IN NEED OF A POLISH. THE BOTTOM TWO DRAWERS ARE SCREWED SHUT. THE TOP DRAWER IS EMPTY.",
                "has_item" : True,
                },

            "cell_door" : {
                "name" : "THE CELL DOOR",
                "examine" : "IT IS A HEAVY DOOR MADE OF THICK STEEL BARS. IT IS LOCKED. THROUGH THE BARS YOU CAN SEE INTO A DIM CORRIDOR AND ON THE FLOOR YOU SPOT A SHINING BRASS KEY JUST OUT OF REACH. IF ONLY YOU HAD A WAY TO GET IT.",
                "examine_taken" : "IT IS A HEAVY DOOR MADE OF THICK STEEL BARS.",
                "open_locked" : "THE DOOR IS LOCKED.",
                "open" : "YOU INSERT THE KEY AND IT FITS PERFECTLY. WITH A STRUGGLE, YOU UNLOCK THE DOOR AND SHOVE IT OPEN.",
                "examine_opened" : "IT IS A HEAVY DOOR MADE OF THICK STEEL BARS. IT IS WIDE OPEN INTO THE CORRIDOR.",
                "id_type" : "door",
                "unlocker" : "key",
                "object_open" : False,
                "locked" : True,
                "unlock_direction" : "n",
                "unlock_room" : "cell_corridor",
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
                "hidden_in" : "cell_door",
                },

            },
       },

    "cell_corridor" : {
        "name" : "THE CELL CORRIDOR.",
        "desc" : "YOU ARE IN A DIMLY LIT, FOUL SMELLING EAST, WEST CORRIDOR. YOU HAVE AN EXIT SOUTH AND NORTH OF YOU BOTH LEADING INTO DARK CELLS. THE CORRIDOR APPEARS TO BE DESERTED.",
        "visited" : False,
        "exits" : {"s" : "cell",
                   "e" : "east_cell_corridor",
                   "w" : "west_cell_corridor",
                   "n" : "dark_cell",
                       },
        "objects" : {},
        "items" : {},
        },

    "dark_cell" : {
        "dark" : True,
        "name" : "THE DARK CELL",
        "desc" : "YOU ARE IN A VERY DARK CELL. THE FLOOR IS LITTERED WITH SCRAPS OF PLASTIC. THERE MAY BE SOMETHING USEFUL IN HERE BUT YOU CAN'T TELL WITH THE LACK OF LIGHT.",
        "desc_lit" : "YOU ARE IN A LARGE, DIRTY CELL WITH PLASTIC AND GLASS SHARDS LITTERING THE FLOOR. AMONGST THE DEBRIS, YOU FOUND A PLASTIC BOTTLE.",
        "visited" : False,
        "exits" : {"s" : "cell_corridor"},
        "objects" : {},
        "items" : {"bottle" : {"name" : "A PLASTIC BOTTLE",
                               "hidden_in" : "dark"
                                },
                   },
        },

     "east_cell_corridor" : {
         "name" : "THE EAST END OF THE CELL CORRIDOR.",
         "desc" : "YOU ARE AT THE EAST END OF THE CORRIDOR. THERE ARE CELLS TO THE NORTH AND SOUTH OF YOU, THE SOUTHERN CELL'S DOOR IS AJAR AND THE NORTHERN CELL'S DOOR IS LOCKED. AHEAD OF YOU TO THE EAST IS A HEAVY DUTY IRON DOOR. THERE IS A MYSTERIOUS SWITCH ON THE WALL.",
         "visited" : False,
         "exits" : {"s" : "grim_cell",
                    "w" : "cell_corridor",
                        },
         "blocked_exits" : {
             "n" : "DID YOU NOT READ? I SAID THE NORTHERN DOOR WAS LOCKED."
             },
         "objects" : {
             "switch" : {
                 "examine" : "THE PLASTIC SWITCH IS LOOSELY SCREWED ONTO THE GRIMY WALLS. DO YOU WANT TO FLICK THE SWITCH? Y OR N.",
                 "scoring" : {
                     "score" : 10,
                     "secret" : False,
                     "discovery" : "WHAT DOES THIS DO?  -  FIND THE HIDDEN SWITCH",
                     "scored" : False
                        },
                     },
                 },
         "items" : {},
             },

    "grim_cell" : {
        "name" : "THE GRIM CELL.",
        "desc" : "YOU WALK INTO A TRULY GRIM CELL. THERE ARE OILY MARKS AND STAINS COVERING THE WALLS AND FLOORS. THERE IS A RIPPED UP MATTRESS IN THE CORNER OF THE ROOM NEXT TO A SLIMY CHAMBER POT. THERE IS A RANCID POSTER ON THE SOUTHERN WALL, SO FADED THE DETAILS CANNOT BE SEEN. A PUTRID SMELL LINGERS IN THE AIR.",
        "visited" : False,
        "exits" : {"n" : "east_cell_corridor",
                   "s" : "poster_room",
            },
        "objects" : {},
        "items" : {"pot" : {
            "name" : "A NASTY CHAMBER POT",
            "hidden_in" : None,
                },

            },
        },

    "poster_room" : {
        "name" : "THE POSTER ROOM.",
        "desc" : "YOU SOMEHOW THINK TO WALK THROUGH THE POSTER AND FIND YOURSELF IN A SMALL, BRIGHTLY LIT ROOM WITH CONCRETE WALLS AND A CARPETED FLOOR. THERE IS A JUKEBOX IN THE CORNER BLASTING FREE JAZZ THAT YOU WOULD HAVE THOUGHT YOU COULD HEAR FROM THE CELL JUST OUTSIDE. THE POSTER SEEMS TO HAVE GOOD SOUNDPROOFING! SURROUNDING YOU THERE ARE SOFAS AGAINST EACH WALL, POTS WITH PALM TREES IN AND CHESS SETS. YOU HAVE PROBABLY FOUND THE NICEST ROOM IN THE WHOLE DUNGEON. CONGRATULATIONS!",
        "visited" : False,
        "exits" : {"n" : "grim_cell"},
        "objects" : {
            "jukebox" : {
                "examine" : "IT IS A 1970'S RAINBOW JUKEBOX BLASTING FREE JAZZ MUSIC, YOU HAVE NO IDEA WHAT TIME SIGNITURE THE MUSIC'S IN.",
                },
            },
        "items" : {
            "ticket" : {"name" : "A SPARKLING CINEMA TICKET",
                        "hidden_in" : None,
                    },
            },

        },
    "west_cell_corridor" : {
        "name" : "THE WEST END OF THE CELL CORRIDOR.",
        "desc" : "YOU ARE AT THE WEST END OF THE CORRRIDOR NOW. THERE ARE CELLS NORTH AND SOUTH OF YOU. ONE IS LOCKED AND ONE IS UNLOCKED. THE CELL TO THE NORTH HAS A SHADOWY FIGURE INSIDE RESTING AGAINST THE WALL. THE CORRIDOR CONTINUES TO THE WEST ROUND A BEND.",
        "visited" : False,
        "exits" : {"s" : "decent_cell",
                   "e" : "cell_corridor",
                   "w" : "detention_junction",
            },
        "blocked_exits" : {
            "n" : "THE DOOR TO THE OCCUPIED CELL IS LOCKED. YOU CANNOT GET THROUGH."
            },
        "objects" : {
            "figure" : {
                "examine" : "YOU LOOK INTO THE OCCUPIED CELL. IF THE FIGURE HAS NOTICED YOU, THEY CLEARLY DO NOT CARE. NO MATTER WHAT YOU, DO THEY SHOW NO INTEREST WHATSOEVER."
                },
            },
        "items" : {},
        },
    "decent_cell" : {
        "name" : "THE DECENT CELL.",
        "desc" : "YOU ARE IN A DECENTLY CLEAN AND TIDY CELL IN CONTRAST TO YOUR OWN. THE BED IS WELL MADE AND THE ROOM IS BRIGHTLY LIT. ON THE FLOOR THERE IS A PAPER NOTE WITH UNIDENTIFIED SCRIBBLES ALL OVER IT.",
        "visited" : False,
        "exits" : {"n" : "west_cell_corridor"},
        "objects" : {},
        "items" : {
            "note" : {
                "name" : "A MYSTERIOUS NOTE",
                "hidden_in" : None,
                },
            },

        },
    "detention_junction" : {
        "name" : "THE DETENTION BLOCK JUNCTION.",
        "desc" : "YOU ARE AT A JUNCTION WITH PASSAGES IN FOUR DIRECTIONS. THE WESTERN PASSAGE IS BLOCKED BY A HIGH TECH DOOR UNLOCKED WITH A KEYCARD.",
        "visited" : False,
        "exits" : {"s" : "west_cell_corridor",
                   "e" : "torture_room",
                   "n" : "common_ns_corridor"
                   },
        "blocked_exits" : {
            "w" : "YOUR PATH IS BARRED BY THE LOCKED DOOR."
            },
        "objects" : {
            "detention_door" : {
                "examine" : "IT IS A HIGH TECH STEEL DOOR WITH A SMALL PIN PAD ON IT.",
                "open_locked" : "THE DOOR IS LOCKED.",
                "open" : "YOU ENTER THE CORRECT CODE, THERE IS A LOUD BEEP AND THE DOOR SLOWLY GRINDS OPEN.",
                "examine_opened" : "IT IS A HIGH TECH STEEL DOOR WITH A SMALL PIN PAD ON IT. THE DOOR IS OPEN.",
                "unlocker" : "pincode",
                "id_type" : "door",
                "locked" : True,
                "object_open" : False,

                "unlock_direction" : "w",
                "unlock_room" : "max_security_east"
                }
            },
        "items" : {},
        },
    "torture_room" : {
        "name" : "THE TORTURE ROOM.",
        "desc" : "YOU ARE IN A DIMLY LIT LARGE ROOM WITH STONE WALLS. THERE ARE VARIOUS TORTURE INSTRUMENTS AND DEVICES AROUND THE CHAMBER. IT'S PROBABLY BEST NOT TO LINGER.",
        "visited" : False,
        "exits" : {"w" : "detention_junction"},
        "objects" : {"device" : {
            "has_item" : True,
            "examine" : "IT IS AN UNIDENTIFIED BUT DANGEROUS LOOKING MEDIEVAL TORTURE DEVICE. BETTER STAY AWAY FROM IT.",
            "open_locked" : "YOU HAVE ABSOLUTELY NO CLUE HOW TO OPEN IT. I'M NOT SURE YOU EVEN SHOULD.",
            "open" : "YOU CHECK THE INSTRUCTIONS ON THE NOTE CAREFULLY BEFORE OPENING IT. YOU CORRECTLY SPOT A TINY HIDDEN LEVER ROUND THE BACK OF THE DEVICE AND ONCE YOU CRANK IT, YOU CAN SLOWLY PRY IT OPEN. INSIDE IT THERE IS A HARD HAT! I WONDER HOW THAT GOT IN THERE.",
            "examine_taken" : "IT IS AN UNIDENTIFIED BUT DANGEROUS LOOKING MEDIEVAL TORTURE DEVICE. IT IS WIDE OPEN AND THERE IS AN EMPTY CHAMBER INSIDE.",
            "examine_opened" : "IT IS AN UNIDENTIFIED BUT DANGEROUS LOOKING MEDIEVAL TORTURE DEVICE. IT IS WIDE OPEN AND THERE IS AN EMPTY CHAMBER INSIDE.",
            "locked" : True,
            "unlocker" : "instructions",
            "object_open" : False,
            "contains" : "hat",
            },
                     },
        "items" : {
            "hat" : {
                "name" :"A YELLOW HARD HAT",
                "hidden_in" : "indevice",
                },
            },
        },
    "common_ns_corridor" : {
        "name" : "THE N/S CORRIDOR.",
        "desc" : "YOU ARE IN A SLOPING N/S CORRIDOR. THE DESIGN OF THE DUNGEON SEEMS TO BE GETTING OLDER.",
        "visited" : False,
        "exits" : {"s" : "detention_junction",
                   "n" : "canteen",
                   "u" : "canteen",
                   "d" : "detention_junction"},
        "objects" : {},
        "items" : {},
        },

    "canteen" : {
        "name" : "THE CANTEEN.",
        "desc" : "YOU ARE IN A VERY LARGE ROOM THAT I ASSUME IS A CANTEEN, HOWEVER IT LOOKS AS THOUGH IT HASN'T BEEN USED IN A LONG TIME. THERE ARE ROTTING WOODEN TABLES AND BENCHES EVERYWHERE.",
        "visited" : False,
        "exits" : {"s" : "common_ns_corridor",
                   "e" : "common_room",
                   "n" : "common_ew_corridor"},
        "objects" : {"table" : {
                "examine" : "IT'S A ROTTING WOODEN TABLE. WHAT DID YOU EXPECT?",
                    },
                },
        "items" : {
            "chocolate" : {
                "name" : "A CHOCOLATE BAR",
                "hidden_in" : None
                },
            },

        },
    "common_room" : {
        "name" : "THE COMMON ROOM.",
        "desc" : "YOU ARE IN A VERY LARGE ROOM NOW WITH STONE BRICK WALLS AND A TILED FLOOR. IT APPEARS TO BE A COMMON ROOM AS THERE ARE MULTIPLE ANCIENT SOFAS DOTTED AROUND AND A VERY OLD VINYL PLAYER SITS UPON A LONG WOODEN DESK. THERE ARE EXITS TO THE EAST AND WEST.",
        "visited" : False,
        "exits" : {"w" : "canteen",
                   "e" : "pigeon_room"},
        "objects" : {
            "player" : {
                "examine" : "IT IS AN INCREDIBLY OLD VINYL PLAYER THAT LOOKS AS IF ITS BEEN HERE A LONG TIME.",
                },
            },
        "items" : {},
        },

    "pigeon_room" : {
        "name" : "THE PIGEON ROOM.",
        "desc" : "YOU ARE IN A VERY TALL BUT NARROW ROOM WITH A SMALL GRATE IN THE CEILING LETTING A TINY AMOUNT OF SUNLIGHT IN. IT'S BEEN AGES SINCE YOU'VE SEEN NATURAL LIGHT. THE ONLY OTHER NOTABLE THING IN THE ROOM IS A METAL POLE ON WHICH A SMALL PIGEON SITS.",
        "visited" : False,
        "exits" : {"w" : "common_room"},
        "objects" : {"grate" : {"examine" : "IT IS A SMALL METAL GRATE THROUGH WHICH YOU CAN SEE SUNLIGHT POURING IN. YOU HAVEN'T SEEN SUNLIGHT IN DAYS."},},
        "items" : {"pigeon" : {
            "name" : "A SMALL PIGEON",
            "hidden_in" : None
                                   },
                },
        },
    "common_ew_corridor" : {
        "name" : "THE E/W CORRIDOR.",
        "desc" : "YOU ARE IN A BRIGHTLY LIT E/W CORRIDOR WITH TORCHES ALONG EACH WALL.",
        "visited" : False,
        "exits" : {"s" : "canteen",
                   "e" : "common_junction",
                   "w" : "common_hole_room",},
        "objects" : {},
        "items" : {},
        },

    "common_junction" : {
        "name" : "THE TORCHLIT JUNCTION.",
        "desc" : "YOU ARE AT A THREE WAY JUNCTION, BRIGHTLY LIT WITH TORCHES ON EACH WALL. THE SMELL OF THE DUNGEON BECOMES MORE BEARABLE HERE.",
        "visited" : False,
        "exits" : {"w" : "common_ew_corridor",
                   "e" : "common_small_room",
                   "n" : "wide_hall"},
        "objects" : {},
        "items" : {},

        },

    "common_small_room" : {
        "name" : "THE CRAMPED ROOM.",
        "desc" : "YOU ARE IN A SMALL, CRAMPED ROOM WITH STONE BRICK WALLS.",
        "visited" : False,
        "exits" : {"w" : "common_junction"},
        "objects" : {},
        "items" : {},
        },

    "common_hole_room" : {
        "name" : "THE HOLE ROOM.",
        "desc" : "YOU ARE AT THE EAST END OF THE CORRIDOR. THERE IS A SMALL, METRE WIDE PIT IN THE FLOOR LEADING DOWN INTO THE DARKNESS BELOW. YOU CAN GO DOWN, BUT YOU PROBABLY CAN'T GET BACK UP. THERE IS A LIGHT COMING FROM THE EAST.",
        "visited" : False,
        "exits" : {"e" : "common_ew_corridor",
                   "d" : "common_pit"},
        "objects" : {},
        "items" : {},
        },

    "common_pit" : {
        "name" : "THE DEEP PIT.",
        "desc" : "YOU ARE IN A DEEP PIT. ABOVE YOU IS A DIMLY LIT CHAMBER AND THERE ARE MULTIPLE EXITS ON GROUND LEVEL. IT LOOKS AS THOUGH THIS HOLE WAS DUG IN A HURRY AS THE SIDES ARE JUST MADE OF ROCK AND MUD.",
        "visited" : False,
        "exits" : {"n" : "grotty_tunnel_south",
                   "s" : "bath_tunnel"},
        "objects" : {},
        "items" : {},
        "blocked_exits" : {
            "u" : "YOU CAN'T GET BACK UP INTO THE CHAMBER ABOVE.",
            },
        },

    "grotty_tunnel_south" : {
        "dark" : True,
        "name" : "THE SOUTH END OF THE GROTTY TUNNEL.",
        "desc" : "IT IS NOW TOO DARK TO SEE WHERE YOU ARE GOING.",
        "desc_lit" : "YOU ARE AT THE SOUTH END OF A DARK, GROTTY TUNNEL. THE TUNNEL CONTINUES NORTH.",
        "visited" : False,
        "exits" : {"n" : "grotty_tunnel_north",
                   "s" : "common_pit"},
        "objects" : {},
        "items" : {},
        },

    "grotty_tunnel_north" : {
        "dark" : True,
        "name" : "THE NORTH END OF THE GROTTY TUNNEL.",
        "desc" : "IT IS TOO DARK TO SEE ANYTHING.",
        "desc_lit" : "YOU ARE AT THE NORTH END OF THE DARK TUNNEL. IT IS VERY NARROW HERE, ONLY ABOUT 2 FEET WIDE.",
        "visited" : False,
        "exits" : {"n" : "meeting_room",
                   "s" : "grotty_tunnel_south"},
        "objects" : {},
        "items" : {},
        },

    "meeting_room" : {
        "dark" : True,
        "name" : "THE SECRET MEETING ROOM.",
        "desc" : "IT IS TOO DARK TO SEE ANYTHING.",
        "desc_lit" : "YOU ARE IN A CRAMPED, LOW HOLLOWED OUT CHAMBER WITH STONE BENCHES CARVED OUT OF THE ROCK ITSELF. ALL BENCHES ARE FACING TOWARDS THE SMOKING REMNANTS OF A FIRE IN THE CENTRE OF THE ROOM. IT LOOKS LIKE SOME SORT OF MEETING WAS HELD HERE.",
        "visited" : False,
        "exits" : {"s" : "grotty_tunnel_north"},
        "objects" : {"fire" : {
            "examine" : "IT IS THE REMNANTS OF AN RECENT CAMPFIRE. THE ROOM IS STILL WARM AND SMELLS OF SMOKE.",},
            },
        "items" : {},
        },

    "meeting_secret_passage" : {
        "name" : "THE SECRET PASSAGE.",
        "desc" : "A LOW, BUT WIDE PASSAGE THAT CONTINUES NORTH BUT AHEAD OF YOU MAKES A SHARP RIGHT HAND BEND. THERE IS LIGHT COMING FROM THE END OF THE PASSAGE.",
        "visited" : False,
        "exits" : {"s" : "meeting_room",
                   "n" : "thug_room",
                   "e" : "thug_room"},
        "objects" : {},
        "items" : {},
        },
    "thug_room" : {
        "name" : "THE HIDEOUT.",
        "desc" : "YOU ARE IN THE SECRET HIDEOUT. THERE ARE FIVE MUSCULAR THUGS LOUNGING AROUND AND PLAYING POKER. THEY ACKNOWLEDGE YOU ONCE AND THEN RETURN TO THEIR GAME.",
        "visited" : False,
        "exits" : {"w" : "meeting_secret_passage"},
        "objects" : {},
        "items" : {},
        },

    "bath_tunnel" : {
        "name" : "THE DIRTY TUNNEL.",
        "desc" : "YOU ARE IN A GLOOMY, TIGHT TUNNEL DUG INTO THE DIRT, THERE IS A FAINT LIGHT COMING FROM THE EAST.",
        "visited" : False,
        "exits" : {"n" : "common_pit",
                   "e" : "bathroom_broken"},
        "objects" : {},
        "items" : {},
        },

    "bathroom_broken" : {
        "name" : "THE BROKEN BATHROOM.",
        "desc" : "YOU ARE IN WHAT USED TO BE A FUNCTIONING BATHROOM WITH WHITE MARBLE TILES ON THE WALLS AND FLOOR BEFORE IT WAS COMPLETELY WRECKED IN SOME KIND OF FRENZY INVOLVING SHOVELS, PICKAXES, POSSIBLY DYNAMYTE AND LOTS OF DIRT, MUD AND ROCK.",
        "visited" : False,
        "exits" : {"w" : "bath_tunnel",
                   "e" : "bathroom",
                   "s" : "cubicle"},
        "objects" : {},
        "items" : {"rubble" : {
            "name" : "SOME RUBBLE",
            "hidden_in" : None
            },
        },
        "blocked_exits" : {"n" : "WHAT LOOKS LIKE THE MAIN ENTRANCE TO THE BATHROOM HAS TOTALLY COLLAPSED. THERE'S NO WAY YOU'RE GETTING THROUGH THAT."},
        },

    "cubicle" : {
        "name" : "THE TOILET CUBICLE.",
        "desc" : "YOU ARE IN A SMALL AND UNCOMFORTABLE TOILET CUBICLE. THE LOCK ON THE DOOR DOESN'T WORK ANYMORE.",
        "visited" : False,
        "exits" : {"n" : "bathroom_broken"},
        "objects" : {"toilet" : {
            "examine" : "IT'S A REVOLTING TOILET. PLEASE DON'T MAKE ME DESCRIBE IT FURTHER."},
        },
        "items" : {"roll" : {
        "name" : "SOME TOILET ROLL",
        "hidden_in" : None
                },
            },
        },

    "bathroom" : {
        "name" : "THE UNDAMAGED BATHROOM.",
        "desc" : "YOU ARE IN THE OTHER HALF OF THE BATHROOM WHICH IS RELATIVLEY UNHARMED. VERY HIGH UP ON ONE WALL THERE IS A VENTILATION SHAFT AND ON THE FLOOR THERE IS A METAL GRATE WITH ONLY DARKNESS UNDERNEATH.",
        "visited" : False,
        "exits" : {"w" : "bathroom_broken",
                   "d" : "sewer_east"},
        "objects" : {},
        "items" : {},
        "blocked_exits" : {
            "u" : "YOU CANNOT REACH THE VENTILATION SHAFT."
            },

        },
    "vent_shaft" : {
        "name" : "A VENT SHAFT WITH TIGHT AIRDUCTS IN ALL DIRECTIONS!",
        "desc" : "YOU CLIMB UP INTO A METAL VENT SHAFT WITH TIGHT AIRDUCTS IN ALL DIRECTIONS!",
        "visited" : False,
        "exits" : {},
        "objects" : {},
        "items" : {},
        },

    "wide_hall" : {
        "name" : "THE WIDE HALL.",
        "desc" : "YOU ARE IN A VERY WIDE HALLWAY WITH A LARGE DOOR TO THE SOUTH AND A SMALL SIDE DOOR TO THE EAST. THE HALLWAY CONTINUES NORTH.",
        "visited" : False,
        "exits" : {"s" : "common_junction",
                   "n" : "wide_door_room",
                   "e" : "maintenance_room"},
        "objects" : {},
        "items" : {},
        },

    "wide_door_room" : {
        "name" : "THE WIDE DOORWAY.",
        "desc" : "YOU ARE AT A VERY LARGE DOOR AT THE END OF THE WIDE HALL. TEN METRES HIGH, IT TOWERS OVER YOU.",
        "visited" : False,
        "exits" : {"s" : "wide_hall"},
        "objects" : {"big_door" : {
            "name" : "THE BIG DOOR",
            "examine" : "IT IS A HUGE WOODEN DOOR THAT IS AS HIGH AS THE CEILING, TEN METRES HIGH.",
            "open" : "WITH A BIG STRUGGLE, YOU MANAGE TO HEAVE THE DOOR OPEN JUST ENOUGH FOR YOU TO SLIP THROUGH.",
            "examine_opened" : "IT IS A HUGE WOODEN DOOR THAT IS AS HIGH AS THE CEILING, TEN METRES HIGH. IT IS OPEN JUST A CRACK.",
            "id_type" : "door",
            "object_open" : False,
            "unlock_direction" : "n",
            "unlock_room" : "huge_room",
                },
            },
        "blocked_exits" : {"n" : "THE DOOR IS IN THE WAY!"},
        "items" : {},
        },
    "huge_room" : {
        "name" : "THE HUGE ROOM.",
        "desc" : "YOU WALK INTO AN ABSOLUTELY HUGE AND CAVERNOUS CHAMBER, SO LARGE THAT THE MANY CHANDELIERS AND TORCHES FAIL TO LIGHT UP THE ENTIRE SPACE. THERE ARE EXITS IN ALL DIRECTIONS AND IN THE CENTRE OF THE ROOM THERE IS A LARGE BOARD WITH WRITING ALL OVER IT.",
        "visited" : False,
        "exits" : {"n" : "industrial_junction",
                   "s" : "wide_door_room",
                   "e" : "tight_corridor",
                   "w" : "kitchen"},
        "objects" : {"board" : {
        "examine" : "\n-----GUARD DUTY ROTA-----\n\nZONE A : LEVEL 1 GENERAL SURVEILLANCE\n\nZONE B : LEVEL 1 GENERAL SURVEILLANCE\n\nZONE C : LEVEL 0 PATROL SUSPENDED DUE TO STAFF SHORTAGE\n\nZONE D : LEVEL 2 REGULAR PATROLS\n\nZONE E : LEVEL 0 PATROL SUSPENDED DUE TO STAFF SHORTAGE\n\nZONE F : LEVEL 3 HIGH ALERT DUE TO INCREASED ACTIVITY IN SECTOR\n\n\n-----ZONES-----\n\n-ZONE A : INDUSTRIAL SECTOR\n\n-ZONE B : WORKSHOPS AND STORAGE\n\n-ZONE C : CELL BLOCK ALPHA AND DETENTION CORRIDOR\n\n-ZONE D : MAX SECURITY CELL CORRIDOR\n\n-ZONE E : COMMON AREA AND CANTEEN\n\n-ZONE F : SECURITY DEPARTMENT AND STAFF QUARTERS"
            },
        },
        "items" : {},
        },

    "maintenance_room" : {
        "name" : "THE MAINTENANCE ROOM.",
        "desc" : "YOU ARE IN A CLUTTERED, TINY ROOM WITH MAINTENANCE EQUIPMENT EVERYWHERE. THERE IS AN EMPTY DESK AGAINST THE BACK WALL.",
        "visited" : False,
        "exits" : {"w" : "wide_hall"},
        "objects" : {"desk" : {
            "examine" : "IT'S A WOODEN DESK."
            },
        },
        "items" : {},
        },

    "kitchen" : {
        "name" : "THE KITCHEN.\n\nIT SMELLS LOVELY!",
        "desc" : "YOU ARE IN A VERY HOT KITCHEN WITH MANY LIT FIRES AND COOKING EQUIPMENT. THERE IS NOBODY HERE AT THE MOMENT BUT THE FIRES CAN'T BE UNOCCUPIED FOR LONG. A LOVELY SMELL LINGERS IN THE ROOM.",
        "visited" : False,
        "exits" : {"e" : "huge_room",
                   "n" : "pantry"},
        "objects" : {},
        "items" : {},
        },

    "pantry" : {
        "dark" : True,
        "name" : "THE PANTRY.",
        "desc" : "YOU WALK INTO A VERY NARROW ROOM BUT IT'S TOO DARK TO SEE ANYTHING.",
        "desc_lit" : "YOU ARE IN A PANTRY. THE ROOM IS INCREDIBLY LONG YET VERY NARROW. THERE ARE SHELVES AND SHELVES OF FOOD, INGREDIENTS, PRESERVATIVES AND DRINKS ALONG BOTH WALLS. I'M NOT GOING TO LET YOU TAKE ANYTHING!",
        "visited" : False,
        "exits" : {"s" : "kitchen"},
        "objects" : {},
        "items" : {},
        },

    "tight_corridor" : {
        "name" : "THE TIGHT CORRIDOR.",
        "desc" : "YOU ARE IN A VERY TIGHT EAST/WEST CORRIDOR WITH ROUGH WALLS OF STONE. THE PASSAGE IS JUST BIG ENOUGH FOR YOU TO SQUEEZE THROUGH.",
        "visited" : False,
        "exits" : {"w" : "huge_room",
                   "e" : "dull_room"},
        "objects" : {},
        "items" : {},
        },

    "dull_room" : {
        "name" : "THE DULL ROOM.",
        "desc" : "YOU WALK INTO THE MOST EMPTY AND DULL ROOM YOU'VE EVER SEEN. THE ONLY THING TO NOTE IN THE ROOM ARE THE EXITS TO THE WEST, SOUTH AND EAST.",
        "visited" : False,
        "exits" : {"w" : "tight_corridor",
                   "s" : "workshop",
                   "e" : "guard_office_1"},
        "objects" : {},
        "items" : {},
        },

    "workshop" : {
        "name" : "THE WORKSHOP.",
        "desc" : "YOU ARE IN A WARM, WELL USED WORKSHOP WITH WORKBENCHES, ANVILS AND FORGES ALL OVER THE ROOM. AMONGST ALL THE EQUIPMENT AND CLUTTER, YOU CAN SEE A PIT AT THE END OF THE ROOM WITH A ROPE LADDER DESENDING IN.",
        "visited" : False,
        "exits" : {"n": "dull_room",
                   "d" : "storage_pit"},
        "objects" : {"workbench" : {
            "examine" : "IT'S A WOODEN WORKBENCH WITH HAMMERS AND CHISELS ON IT. THERE ARE ALSO IRON ANVILS AND FORGES WITH UNIDENTIFIED TOOLS ON. THERE IS A "},
                     },
        "items" : {},
        },

    "storage_pit" : {
        "name" : "THE STORAGE PIT.",
        "desc" : "YOU ARE AT THE BOTTOM OF A FAIRLY DEEP PIT WITH STUFF EVERYWHERE. I COULDN'T NAME ALL THE ITEMS AND OBJECTS HERE. HOWEVER AMONG THE JUNK, I HAVE SPOTTED A FRESH CAN OF OIL. THERE IS A DECREPIT ROPE LADDER LEADING BACK UP THE PIT.",
        "visited" : False,
        "exits" : {"u" : "workshop"},
        "objects" : {"stuff" : {"examine" : "YOU LOOK AROUND AND JUST SEE PILES AND PILES OF TOTALLY RANDOM ITEMS. IT MUST BE THE STORAGE FOR THE WHOLE DUNGEON."},
                     },
        "items" : {"oil" : {
                "name" : "A CAN OF OIL",
                "hidden_in" : None},
            },
        },

    "guard_office_1" : {
        "name" : "THE SMALL GUARD OFFICE.",
        "desc" : "YOU ARE IN A SMALL OFFICE WITH A STURDY STONE DESK AND AN UNCOMFORTABLE LOOKING CHAIR BEHIND IT. THE DESK IS COVERED IN PIECES OF PAPER AND NOTES. THERE ARE A FEW BAND POSTERS ON THE WALLS.",
        "visited" : False,
        "exits" : {"w" : "dull_room"},
        "objects" : {"desk" : {"examine" : "IT'S INCREDIBLY CLUTTERED. ON THE EDGE OF THE DESK THERE IS A SMALL STICKY NOTE THAT READS: 'TO WHOEVER IS COVERING THE SHIFT BEFORE ME, PLEASE CAN YOU DROP OFF SOME WATER, I GET THIRSTY DOWN HERE!'"},
                     "posters" : {"examine" : "THE POSTERS ALL HAVE NAMES AND ARTWORK OF FAMOUS BANDS AND MUSIC GROUPS."}
                     },
        "items" : {},
        },
    "industrial_junction" : {
        "name" : "THE INDUSTRIAL JUNCTION.",
        "desc" : "YOU ARE IN A THREE WAY JUNCTION THAT SMELLS OF COAL AND STEAM. THERE ARE COPPER AND BRASS PIPES COVERING EACH WALL. MOST SEEM TO BE HEADING EAST.",
        "visited" : False,
        "exits" : {"s" : "huge_room",
                   "n" : "vent_room",
                   "e" : "boiler_room"},
        "objects" : {"pipes" : {"examine" : "THE PIPES ARE HOT TO THE TOUCH."},},
        "items" : {},
        },
    "vent_room" : {
        "name" : "THE VENTILATION ROOM.",
        "desc" : "YOU ARE IN A VERY TALL ROOM WITH CONCRETE WALLS AND A LOW DRONING RATTLE. THE ROOM IS FULL OF HUGE SQUARE, STEEL DUCTS VANISHING INTO WALLS AND CEILING, THERE ARE CATWALKS BRANCHING OUT TO LITTLE MAINTENANCE PLATFORMS AROUND THE FANS AND MACHINERY. IN THE CENTRE OF THE CHAMBER SITS A GIANT STEEL FRAME, FIVE METRES HIGH. UNDERNEATH SITS A LARGE MOTOR, SPINNING SLOWLY BUT OCCASIONALLY STUTTERING TO A HALT AND JERKING BACK TO LIFE AGAIN A FEW SECONDS LATER. MOUNTED ONTO THE CENTRAL COLUMN IS AN ENORMOUS FAN HIDDEN BEHIND A STEEL GRILLE. IT'S EASILY TWICE THE SIZE OF YOU AND SQUEAKS EVERY HALF TURN. OFF TO ONE SIDE IS A CONTROL PANEL. THERE ARE MULTIPLE WARNING LIGHTS BLINKING LAZILY AND MANY GAUGES SIT STUBBORNLY AT 0. DESPITE THE FAINT BREEZE CIRCULATING THE ROOM, THE AIR FEELS STALE AND DUSTY.",
        "visited" : False,
        "exits" : {"s" : "industrial_junction"},
        "objects" : {"panel" : {"examine" : "THERE ARE LOTS OF COMPLEX BUTTONS, LEVERS AND LIGHTS. WARNING LIGHTS ARE BLINKING AND THERE ARE A NUMBER OF GAUGES. THE SMALL NUMBER THAT AREN'T AT 0 ARE UNSTABLY THROTTLING BACK AND FORTH. A SMALL SCREEN DISPLAYS THE MESSAGE: 'EMERGENCY POWER ONLY'."},},
        "items" : {},
        },
    "boiler_room" : {
        "name" : "THE BOILER ROOM.",
        "desc" : "YOU ARE IN A SCOLDINGLY HOT, CRAMPED ROOM WITH A CONSTANT HISSING NOISE. THERE ARE BRASS AND OXIDISED COPPER PIPES OF ALL THICKNESSES SNAKING AROUND ALL CORNERS OF THE ROOM MEANING YOU HAVE TO DUCK TO GET AROUND THE ROOM. ALL OF THE PIPES CONVERGE INTO A LARGE, CENTRAL BOILER TANK CONNECTED BY COMPLEX VALVES. THE LARGEST PIPE CONTINUES NORTH FROM THE TANK. THERE IS A SMALL, METAL DOOR TO THE EAST.",
        "visited" : False,
        "exits" : {"w" : "industrial_junction",
                   "n" : "water_room",
                   "e" : "translator_room"},
        "objects" : {"tank" : {"examine" : "IT'S A VERY BIG, COPPER TANK, RADIATING IMMENSE HEAT. IT'S COVERED IN VALVES AND GAUGES. THERE IS A SMALL WHISLE ON ONE SIDE."},},
        "items" : {},
        },
    "water_room" : {
        "name" : "THE WATER ROOM.",
        "desc" : "YOU ARE IN A ROOM ADJACENT TO THE BOILER ROOM BUT MUCH COOLER. THERE IS A HUGE POOL OF WATER IN THE MIDDLE OF THE CHAMBER AND A TALL TANK COMING UP FROM THE CENTRE OF THE POOL. THE CALMING SOUND OF TRICKLING WATER FILLS THE SPACE. THERE ARE TWO PIPES IN THE ROOM. ONE FEEDS THE POOL, AND THE OTHER IS COMING FROM THE TANK AND BRINGING IT THROUGH THE SOUTHERN WALL.",
        "visited" : False,
        "exits" : {"s" : "boiler_room",
                   "d" : "sewer_west"},
        "objects" : {},
        "items" : {},
        },
    "sewer_west" : {
        "dark" : True,
        "name" : "THE WEST END OF THE SEWERS.",
        "desc" : "IT IS TOO DARK TO SEE ANYTHING. THE AIR SMELLS PUTRID.",
        "desc_lit" : "YOU ARE AT THE WEST END OF A TIGHT, ROUND TUNNEL WITH A CHANNEL OF MURKY BROWN, VISCOUS LIQUID RUNNING ALONG THE FLOOR. THERE ARE LITTLE PASSAGES IN DIFFERENT DIRECTIONS GUARDED BY METAL GRATES. A METAL LADDER DISAPPEARS UP A TINY SHAFT.",
        "visited" : False,
        "exits" : {"e" : "sewer",
                   "u" : "water_room"},
        "blocked_exits" : {
            "n" : "THERE IS A METAL GRATE IN THE WAY.",
            "s" : "THERE IS A METAL GRATE IN THE WAY.",
            "w" : "THERE IS A METAL GRATE IN THE WAY.",
            "d" : "NO WAY ARE YOU GOING IN THAT WATER!",
            },
        "objects" : {},
        "items" : {},
        },
    "sewer" : {
        "dark" : True,
        "name" : "THE SEWER.",
        "desc" : "IT IS TOO DARK TO SEE ANYTHING. THE AIR SMELLS PUTRID.",
        "desc_lit" : "YOU ARE IN THE MIDDLE OF THE SEWERS, RIGHT AT THE EPICENTRE OF THE STENCH, THE NEXUS OF THE WASTEWATER, THE HEART OF THE FILTH, THE ROOT OF THE REPUGNANCE, YOU GET THE POINT. ONE OF THE SIDE PASSAGES IS UNLOCKED.",
        "visited" : False,
        "exits" : {"w" : "sewer_west",
                   "e" : "sewer_east",
                   "s" : "wet_hole"},
        "blocked_exits" : {
            "n" : "THERE IS A METAL GRATE IN THE WAY.",
            "u" : "THERE IS A METAL GRATE IN THE WAY.",
            "d" : "NO WAY ARE YOU GOING IN THAT WATER!",
            },
        "objects" : {},
        "items" : {},
        },
    "wet_hole" : {
        "dark" : True,
        "name" : "THE WET HOLE.",
        "desc" : "IT IS TOO DARK TO SEE ANYTHING.",
        "desc_lit" : "YOU ARE IN A WET HOLE.\nDAMP AND DEEP, FILLED WITH WORMS BIG ENOUGH TO MAKE YOU WEEP.\nWATER DRIPS DOWN THE DEAD PLANT THAT STILL GRIPS TO THE TALL WALLS IN THIS WET HOLE.\nTHIS PLACE HAS THE SMELL OF HELL IF YOU LINGER YOU SHALL NO LONGER BE WELL.\nSO I WOULD FLEE FROM THIS PLACE, WITH MUCH GRACE.\nBUT YOU,\nYOU WILL TAKE A STROLL,\nDEEP, IN THIS COLD WET HOLE.",
        "visited" : False,
        "exits" : {"n" : "sewer",
                   "u" : "sewer"},
        "objects" : {
            "journal" : {
                "examine" : "IT'S A JOURNAL WITH MOST PAGES RIPPED OUT. THE FIRST ONE YOU SEE ONLY HAS ONE SENTENCE WRITTEN IN:\n\n 'IN A HOLE IN THE GROUND, THERE LIVED A PRISONER. NOT A NASTY, DIRTY, WET HOLE - OH WAIT IT TOTALLY IS.'",
                "scoring" : {
                    "score" : 0,
                    "secret" : True,
                    "discovery" : None,
                    "scored" : False
                    },
                },
            "pool" : {
                "examine" : "YOU SWEAR YOU COULD HAVE SEEN SOMETHING MOVING IN THERE..."
                },
            },
        "items" : {},
        },
    "sewer_east" : {
        "dark" : True,
        "name" : "THE EAST END OF THE SEWERS.",
        "desc" : "IT IS TOO DARK TO SEE ANYTHING. THE AIR SMELLS PUTRID.",
        "desc_lit" : "YOU ARE AT THE WEST END OF A TIGHT, ROUND TUNNEL WITH A CHANNEL OF MURKY BROWN, VISCOUS LIQUID RUNNING ALONG THE FLOOR. A METAL LADDER DISAPPEARS UP A TINY SHAFT AND THERE ARE LITTLE PASSAGES ALL DIRECTIONS, GUARDED BY METAL GRATES.",
        "visited" : False,
        "exits" : {"w" : "sewer",
                   "u" : "bathroom"},
        "blocked_exits" : {
            "n" : "THERE IS A METAL GRATE IN THE WAY.",
            "s" : "THERE IS A METAL GRATE IN THE WAY.",
            "e" : "THERE IS A METAL GRATE IN THE WAY.",
            "d" : "NO WAY ARE YOU GOING IN THAT WATER!",},
        "objects" : {},
        "items" : {},
        },
    "translator_room" : {
        "name" : "THE TRANSLATOR ROOM.",
        "desc" : "YOU ARE IN A DIMLY LIT STONE CHAMBER WITH NO FURNITURE IN AT ALL EXCEPT A LARGE MACHINE IN THE CENTRE, TAKING UP MOST OF THE SPACE. IT RESEMBLES A LARGE PHOTOCOPIER OR PRINTER BUT YOU CANNOT TELL FROM WHERE YOU ARE. THERE ARE TWO SMALL EXIT DOORS IN THE ROOM.",
        "visited" : False,
        "exits" : {"w" : "boiler_room",
                   "s" : "dull_room"},
        "objects" : {"machine" : {"examine" : "THE MACHINE APPEARS TO BE A TRANSLATOR! IT IS UNCLEAR WHAT LANGUAGES IT TRANSLATES AND THERE DOESN'T SEEM TO BE A CONTROL PANEL. THERE IS AN INPUT AND AN OUTPUT HOWEVER. THE INSIDE IS COVERED IN COBWEBS AND DUST. I DOUBT IT STILL WORKS."},},
        "items" : {},
        },

    }


                                                #Help command
Help = "IN THIS GAME YOU MUST ESCAPE THE DUNGEON. USE ONE OR TWO WORD COMMANDS TO NAVIGATE THE GAME. YOU CAN MOVE IN FOUR DIRECTIONS: NORTH, EAST, SOUTH AND WEST. USE THE FIRST LETTER OF THESE WORDS AS SHOWN IN THE LIST OF VALID COMMANDS BELOW. IF YOU FORGET THESE COMMANDS, TYPE HELP TO BRING UP THIS TEXT ONCE MORE.\n\nVALID COMMANDS:\n\n>N\n>S\n>E\n>W\n>U\n>D\n\n>GET\n>DROP\n>EXAMINE\n>INVENTORY\n>HELP\n>QUIT\n>LOOK\n>LIGHT\n>OPEN\n>OBJECTS\n>ITEMS\n>SAVE\n>LOAD\n>HIDE\n\nFOLLOW COMMANDS SUCH AS GET, DROP, EXAMINE, AND OPEN WITH A NOUN OR ITEM YOU WISH TO USE. USE Y AND N AS YES AND NO. IF YOU WISH TO KNOW WHICH OBJECTS IN A ROOM ARE INTERACTABLE, USE OBJECTS. IF YOU WISH TO KNOW WHICH ITEMS YOU CAN PICK UP IN A ROOM, USE ITEMS. DROP CAN ALSO BE USED IF YOU WANT TO USE AN ITEM WITH AN OBJECT IN THE ROOM. USE SAVE AND LOAD ALONG WITH A FILE NAME TO MANAGE SAVE GAMES. 'LIST SAVE' CAN BE USED TO LIST ALL SAVE GAMES.\n\nNOT EVERYTHING IN THE DUNGEON IS AS IT FIRST SEEMS,\nYOU MUST THINK CAREFULLY IF YOU WISH TO ESCAPE."

initial_dungeon = copy.deepcopy(dungeon)






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
        typing("ALRIGHT.")
        print("BUT REMEMBER... \n\nNOT EVERYTHING IN THE DUNGEON IS AS IT FIRST SEEMS,\nYOU MUST THINK CAREFULLY IF YOU WISH TO ESCAPE.\n")
        loading_bar("", 0)
        time.sleep(0.4)
        instructions = False
    else:
        typing("PLEASE ANSWER THE QUESTION\n")
        time.sleep(1)

#Game Start:---------------------------------------- Game Start:-----------------------
while True:
    while playing == True:

        if is_hidden != current_room:
            is_hidden = False

        if "water" not in dungeon["guard_office_1"]["items"]:
            guard_water_count = 0

        if current_room not in ["guard_office_1", "dull_room"] and guard_water_count > 0:
            guard_water_count -= 1
        if guard_water_count ==1 and current_room == "guard_office_1":
            typing("YOU WALK INTO THE OFFICE. THE WATER BOTTLE IS GONE AND NOW THERE IS A VINYL DISC ON THE DESK ALONG WITH ANOTHER STICKY NOTE.")
            dungeon["guard_office_1"]["items"]["vinyl"] = {
                "name" : "A VINYL DISC",
                "hidden_in" : None
                }
            del dungeon[current_room]["items"]["water"]
            guard_water_count = 0

        if "pincode" in inventory:
            inventory.remove("pincode")

        if current_room == "thug_room" and met_prisoners == False:
            typing("AS YOU TURN THE CORNER, YOU WALK INTO A HIDEOUT WITH FIVE FIGURES IN TORN, DIRTY CLOTHES LOUNGING AROUND. THEY ALL JUMP UP IN ALERT. THE TALLEST ONE DRAWS HIS SWORD AND CHALLENGES YOU TO A DUEL!")
            time.sleep(1)
            duel_challenge = input("\nDO YOU ACCEPT? Y/N\n\n>").lower().strip()
            if duel_challenge == "y":
                typing("YOU BRAVELY DRAW YOUR... FISTS? THE THUG LAUGHS AND STRIKES YOU DOWN BEFORE YOU COULD EVEN SWING A PUNCH AT HIM. THAT WAS UNWISE.")
                time.sleep(0.5)
                ending = "death"
                playing = False
                break
            elif duel_challenge == "n":
                typing("'AW OK.' THE FIGURES LOOK MILDLY UPSET BUT THEY DON'T CHALLENGE YOU FURTHER.\n\n")
                discover(50, False, "ABSOLUTELY NOT.  -  DENY THE DUEL")
                time.sleep(1)
                typing("'WELL, SEEING AS YOU FOUND OUR SECRET HIDEOUT, WE'LL GIVE YOU THESE SEEDS AS A REWARD. GO... PLANT IT OR SOMETHING.' WITH A SIGH, THEY ALL SIT BACK DOWN.")
                met_prisoners = True
                dungeon["thug_room"]["visited"] = True
                dungeon["thug_room"]["items"]["seeds"] = {
                "name" : "A PACKET OF SEEDS",
                "hidden_in" : None
                }
            else:
                typing("THE FIGURES LOOK AT YOU, CONFUSED BY YOUR ACCENT. YOU TAKE THIS OPPORTUNITY TO LEAVE THE ROOM SWIFTLY.\n\n(MAYBE NEXT TIME TYPE EITHER Y OR N.)")
                current_room = "meeting_secret_passage"
                continue
        if lighter_is_lit == True and "lighter" in inventory:
            lighter_lit = True
        elif lighter_is_lit == True and "lighter" not in inventory:
            lighter_lit = False
            if "dark" in dungeon[current_room] and dungeon[current_room]["dark"] == True:
                for dark_item in dungeon[current_room]["items"]:
                    dungeon[current_room]["items"][dark_item]["hidden_in"] = "dark"
                for dark_object in dungeon[current_room]["objects"]:
                    dungeon[current_room]["objects"][dark_object]["hidden_in"] = "dark"
        else:
            lighter_lit = False
            if "dark" in dungeon[current_room] and dungeon[current_room]["dark"] == True:
                for dark_item in dungeon[current_room]["items"]:
                    dungeon[current_room]["items"][dark_item]["hidden_in"] = "dark"
                for dark_object in dungeon[current_room]["objects"]:
                    dungeon[current_room]["objects"][dark_object]["hidden_in"] = "dark"

        if lighter_lit == True:
            for dark_item in dungeon[current_room]["items"]:
                if dungeon[current_room]["items"][dark_item]["hidden_in"] == "dark":
                    dungeon[current_room]["items"][dark_item]["hidden_in"] = None

            for dark_object in dungeon[current_room]["objects"]:
                if "hidden_in" in dungeon[current_room]["objects"][dark_object]:
                    if dungeon[current_room]["objects"][dark_object]["hidden_in"] == "dark":
                        dungeon[current_room]["objects"][dark_object]["hidden_in"] = None

        if "dark" in dungeon[current_room] and dungeon[current_room]["dark"] == True:
            if lighter_lit == True:
                if dungeon[current_room]["visited"] == False:
                    typing("\n\n" + dungeon[current_room]["desc_lit"])
                    dungeon[current_room]["visited"] = True
                else:
                    typing("\n\nYOU ARE IN " + dungeon[current_room]["name"])
            else:
                typing("\n\n" + dungeon[current_room]["desc"])
        else:
            if dungeon[current_room]["visited"] == False:
                typing("\n\n" + dungeon[current_room]["desc"])
                dungeon[current_room]["visited"] = True
            else:
                typing("\n\nYOU ARE IN " + dungeon[current_room]["name"])
        #Prisoner exeption-------------------------------------------------------------
        if current_room == "thug_room" and met_prisoners == True:
            typing("THE PRISONERS NOD AT YOU CORDIALLY.")
        #------------------------------------------------------------------------------
        #Bathroom exeption-------------------------------------------------------------
        if current_room == "bathroom":
            if rubble_in_pile == 1:
                typing("THERE IS A SMALL PILE OF RUBBLE ON THE FLOOR.")
            if rubble_in_pile == 2:
                typing("THERE IS A PILE OF RUBBLE ON THE FLOOR.")
            if rubble_in_pile == 3:
                typing("THERE IS A TALL PILE OF RUBBLE ON THE FLOOR!")
        #------------------------------------------------------------------------------

        for item_name in dungeon[current_room]["items"]:
            if dungeon[current_room]["items"][item_name]["hidden_in"] == None:
                typing("\n\nTHERE IS " + dungeon[current_room]["items"][item_name]["name"] + " HERE!")

        if "dark" in dungeon[current_room] and lighter_lit == False:
            dungeon[current_room]["visited"] = False


        if guard_alert > 0:                                             #Danger zones
            guard_alert = guard_alert - 1
            if guard_alert == 0:
                guard_in_room = True

        if guard_in_room == False and guard_alert == 0:
            if current_room in danger_zone1:
                if guard_alert == 0:
                    if random.randint(1, 25) == 1:
                        if "hat" in inventory:
                            guard_in_room = True
                        else:
                            typing("\nYOU HEAR HEAVY FOOTSTEPS IN THE DISTANCE BEHIND YOU.")
                            guard_alert = 1
                            guard_in_room = False

            if current_room in danger_zone2:
                if guard_alert == 0:
                    if random.randint(1, 5) == 1:
                        if "hat" in inventory:
                            guard_in_room = True
                        else:
                            typing("\nYOU HEAR HEAVY FOOTSTEPS IN THE DISTANCE BEHIND YOU.")
                            guard_alert = 1
                            guard_in_room = False

        elif guard_in_room == True:
            if "hat" in inventory:
                typing("\nA GUARD IS IN THE ROOM WITH YOU. HE NODS HIS HEAD AT YOU AS HE WALKS PAST.")
                guard_alert = 0
                guard_in_room = False
            elif is_hidden == current_room:
                typing("\nA GUARD COMES INTO THE ROOM! HE DOESN'T SEEM TO NOTICE YOU AS YOU HIDE AND WALKS PAST. IT NOW SEEMS SAFE TO PROCEED.")
                is_hidden = False
                guard_alert = 0
                guard_in_room = False
            else:
                typing("\nYOU HEAR THUNDERING FOOTSTEPS BEHIND YOU AND A GUARD GRABS YOU BY THE COLLAR.")
                ending = "capture"
                playing = False
                guard_alert = 0
                guard_in_room = False
                break

        if is_hidden == current_room:
            typing("\nYOU ARE HIDDEN.")


    #-----------------------------------------------------------------Discovery Rooms---
        if current_room == "vent_shaft" and dungeon["vent_shaft"]["visited"] == False:
            discover(10, False, "I WONDER WHERE THIS COULD LEAD...  -  GET INSIDE THE VENT SHAFT")
        if current_room in ["sewer_east", "sewer_west"] and dungeon["sewer_east"]["visited"] == False and dungeon["sewer_west"]["visited"] == False:
            discover(10, False, "A HANDY SHORTCUT  -  DISCOVER THE SEWERS")
        if current_room == "wet_hole" and dungeon["wet_hole"]["visited"] == False:
            discover(5, True, None)
#---------------------------------------------------------------------------------------





        command = input("\n> ").lower().strip()          #Input Command






        words = command.split(" ")              #Sentence Splitter

        action = words[0]
        if len(words) > 1:
            target = words[1]
        else:
            target = ""

        for obj_name in dungeon[current_room]["objects"]:
            obj_data = dungeon[current_room]["objects"][obj_name]
            if "id_type" in obj_data:
                if target == obj_data["id_type"]:
                    target = obj_name
                    break

                                                                        #Target redirector
        if target == "sign" and current_room == "huge_room" or target == "signpost" and current_room == "huge_room":
            target = "board"
        if target in ["workbenches", "forge", "forges", "anvil", "anvils", "equipment", "tools", "tool"] and current_room == "workshop":
            target = "workbench"
        if target == "drawer":
            target = "drawers"

        if action == "use":                                              #Use redirector
            if target in ["key", "keycard"]:
                action = "open"
                target = "detention_door"
            elif target == "instructions":
                action = "open"
                target = "device"
            elif target in ["lighter"]:
                action = "light"
                target = "lighter"
            elif target == "hook" and current_room == "cell":
                action = "examine"
                target = "cell_door"
            else:
                typing("YOU CANNOT USE THAT IN THIS CONTEXT.")

        if action == "open" and target == "drawers":
            action = "examine"




                                                                        #Uninteractable objects:
        if target in ["sheet", "bedsheet", "sheets", "bedsheets", "stains", "poster", "torch", "torches", "equipment"]:
            typing("YOU CANNOT INTERACT WITH THAT!")

        if target == "pipes" and current_room in ["water_room", "boiler_room"]:
            typing("THEY'RE PIPES.")

        if action == "blow" and target == "whistle" and current_room == "boiler_room":
            action = "examine"
            target = "tank"

        if command in ["sit", "rest", "sleep",]:
            typing("YOU TIRED? COME ON, YOU'VE GOT A DUNGEON TO ESCAPE!")

        if target == "door" and current_room == "boiler_room":
            typing("IT IS ALREADY OPEN!")


        if command == "quit":                                             #Quit Command
            typing("ARE YOU SURE YOU WISH TO QUIT? Y/N")
            quitconfirm = input("\n> ").lower().strip()
            if quitconfirm == "y":
                ending = "quit"
                typing("OK.")
                playing = False
                break
            elif quitconfirm == "n":
                typing("OK.")
                continue
            else:
                typing("I WILL TAKE THAT AS A NO.")
                continue

        elif command == "":                                              #Empty Command
            typing("YOU HAVEN'T DONE ANYTHING!\nPLEASE ENTER A COMMAND.")

        elif command == "look":                          #Look Command
            if "dark" in dungeon[current_room] and dungeon[current_room]["dark"] == True:
                if lighter_lit == True:
                    typing("\n\n" + dungeon[current_room]["desc_lit"])
                    continue
            else:
                typing(dungeon[current_room]["desc"])

        elif action == "fill":
            if target == "bottle" and "bottle" in inventory:
                if current_room == "water_room":
                    typing("YOU FILL THE BOTTLE WITH WATER.")
                    inventory.remove("bottle")
                    inventory.append("water")
                elif current_room in ["sewer","sewer_east","sewer_west","wet_hole"]:
                    typing("I DON'T THINK YOU SHOULD.")
                else:
                    typing("YOU CAN'T FILL IT.")
            elif target == "lighter":
                action == "light"
                target == "lighter"
            else:
                typing("YOU CAN'T FILL THAT.")

        elif action in ["drink", "consume", "chug", "swallow"]:
            if target in inventory or target in dungeon[current_room]["objects"] or target in dungeon[current_room]["items"]:
                if target == "water" and "water" in inventory or current_room == "water_room":
                    typing("YOU DRINK THE WATER. IT TASTES STALE.")
                    if "water" in inventory:
                        inventory.remove("water")
                        inventory.append("bottle")
                elif target == "oil":
                    typing("I'M SORRY, HAVE YOU GONE MAD?")
                elif target == "pigeon" and "pigeon" in inventory or "pigeon" in dungeon[current_room]["items"]:
                    typing("THE PIGEON DOES'T LOOK PARTICULARLY KEEN ON THAT IDEA.")
                else:
                    typing("I DON'T THINK THAT WOULD HELP.")
            else:
                typing("I SEE NO " + target.upper() + " HERE!")

        elif command == "wait":
            typing("YOU WAIT A FEW SECONDS.")
        #Movement--------------------------------------------------------#Movement-------

        if current_room == "vent_shaft" and action in ["n", "s", "e", "w", "north", "south"
, "east", "west"]:
                    vent_dir = random.randint(1, 4)
                    if vent_dir != 4:
                        typing("YOU CRAWL AROUND THROUGH TINY PASSAGES ALL ALIKE FOR A WHILE BUT END UP WHERE YOU STARTED.")
                        time.sleep(0.2)
                    else:
                        typing("YOU CRAWL AROUND THROUGH TINY PASSAGES ALL ALIKE FOR A WHILE AND EVENTUALLY EMERGE OUT OF THE SYSTEM INTO A ROOM.")
                        time.sleep(0.2)
                        if action == "n" or action == "north":
                            current_room = "common_small_room"
                        elif action == "s" or action == "south":
                            current_room = "grim_cell"
                        elif action == "w" or action == "west":
                            current_room = "pigeon_room"
                        elif action == "e" or action == "east":
                            current_room = "maintenance_room"
                        continue

        elif action == "n" or action == "north":                                #north
            if "n" in dungeon[current_room]["exits"]:
                if "dark" in dungeon[current_room] and dungeon[current_room]["dark"] == True and lighter_lit == False:
                    dest = dungeon[current_room]["exits"]["n"]
                    if dest != previous_room:
                        typing("YOU CANNOT SEE WHERE YOU ARE GOING!")
                        continue
                previous_room = current_room
                current_room = dungeon[current_room]["exits"]["n"]
            elif "blocked_exits" in dungeon[current_room] and "n" in dungeon[current_room]["blocked_exits"]:
                typing(dungeon[current_room]["blocked_exits"]["n"])
            else:
                typing("YOU CANNOT MOVE IN THAT DIRECTION!")


        elif action == "s" or action == "south":                                #south
            if "s" in dungeon[current_room]["exits"]:
                if "dark" in dungeon[current_room] and dungeon[current_room]["dark"] == True and lighter_lit == False:
                    dest = dungeon[current_room]["exits"]["s"]
                    if dest != previous_room:
                        typing("YOU CANNOT SEE WHERE YOU ARE GOING!")
                        continue
                previous_room = current_room
                current_room = dungeon[current_room]["exits"]["s"]
            elif "blocked_exits" in dungeon[current_room] and "s" in dungeon[current_room]["blocked_exits"]:
                typing(dungeon[current_room]["blocked_exits"]["s"])
            else:
                typing("YOU CANNOT MOVE IN THAT DIRECTION!")


        elif action == "e" or action == "east":                               #east
            #Tight corridor exeption---------------------------------------
            if current_room == "huge_room":
                heavy_count = 0

                for pocket_item in inventory:
                    if master_items[pocket_item]["weight"] == "heavy":
                        heavy_count = heavy_count + 1
                if heavy_count > 0:
                    typing("THE CORRIDOR IS TOO TIGHT FOR YOU TO FIT THROUGH. YOU MIGHT NEED TO DROP SOMETHING FIRST.")
                    continue
            #--------------------------------------------------------------
            if "e" in dungeon[current_room]["exits"]:
                if "dark" in dungeon[current_room] and dungeon[current_room]["dark"] == True and lighter_lit == False:
                    dest = dungeon[current_room]["exits"]["e"]
                    if dest != previous_room:
                        typing("YOU CANNOT SEE WHERE YOU ARE GOING!")
                        continue
                previous_room = current_room
                current_room = dungeon[current_room]["exits"]["e"]
            elif "blocked_exits" in dungeon[current_room] and "e" in dungeon[current_room]["blocked_exits"]:
                typing(dungeon[current_room]["blocked_exits"]["e"])
            else:
                typing("YOU CANNOT MOVE IN THAT DIRECTION!")


        elif action == "w" or action == "west":                              #west
            #Tight corridor exeption---------------------------------------
            if current_room == "dull_room":
                heavy_count = 0

                for pocket_item in inventory:
                    if master_items[pocket_item]["weight"] == "heavy":
                        heavy_count = heavy_count + 1
                if heavy_count > 0:
                    typing("THE CORRIDOR IS TOO TIGHT FOR YOU TO FIT THROUGH. YOU MIGHT NEED TO DROP SOMETHING FIRST.")
                    continue
            #--------------------------------------------------------------
            if "w" in dungeon[current_room]["exits"]:
                if "dark" in dungeon[current_room] and dungeon[current_room]["dark"] == True and lighter_lit == False:
                    dest = dungeon[current_room]["exits"]["w"]
                    if dest != previous_room:
                        typing("YOU CANNOT SEE WHERE YOU ARE GOING!")
                        continue
                previous_room = current_room
                current_room = dungeon[current_room]["exits"]["w"]
            elif "blocked_exits" in dungeon[current_room] and "w" in dungeon[current_room]["blocked_exits"]:
                typing(dungeon[current_room]["blocked_exits"]["w"])
            else:
                typing("YOU CANNOT MOVE IN THAT DIRECTION!")

        elif action == "u" or action == "up":                              #up
            if "u" in dungeon[current_room]["exits"]:
                if "dark" in dungeon[current_room] and dungeon[current_room]["dark"] == True and lighter_lit == False:
                    dest = dungeon[current_room]["exits"]["u"]
                    if dest != previous_room:
                        typing("YOU CANNOT SEE WHERE YOU ARE GOING!")
                        continue
                previous_room = current_room
                current_room = dungeon[current_room]["exits"]["u"]
            elif "blocked_exits" in dungeon[current_room] and "u" in dungeon[current_room]["blocked_exits"]:
                typing(dungeon[current_room]["blocked_exits"]["u"])
            else:
                typing("YOU CANNOT MOVE IN THAT DIRECTION!")

        elif action == "d" or action == "down":                            #down
            if "d" in dungeon[current_room]["exits"]:
                if "dark" in dungeon[current_room] and dungeon[current_room]["dark"] == True and lighter_lit == False:
                    dest = dungeon[current_room]["exits"]["d"]
                    if dest != previous_room:
                        typing("YOU CANNOT SEE WHERE YOU ARE GOING!")
                        continue
                previous_room = current_room
                current_room = dungeon[current_room]["exits"]["d"]
            elif "blocked_exits" in dungeon[current_room] and "d" in dungeon[current_room]["blocked_exits"]:
                typing(dungeon[current_room]["blocked_exits"]["d"])
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

                typing("\n\nBIG ITEMS:\n")
                for item in inventory:
                    if master_items[item]["weight"] == "heavy":
                        typing("\n- " + item.upper())
                typing("\n\nSMALL ITEMS:\n")
                for item in inventory:
                    if master_items[item]["weight"] == "light":
                        typing("\n- " + item.upper())




        elif action in ["examine", "ex", "x", "inspect", "read", "check", "search"]: #Examine command
            if target in dungeon[current_room]["objects"]:              #objects

                #door exeption ------------------------------door exeption
                if target == "cell_door":
                    if current_room == "cell":
                        if "hook" in inventory:
                            if "key" in dungeon["cell"]["items"]:
                                typing("IT IS A HEAVY DOOR MADE OF THICK STEEL BARS. IT IS LOCKED. THROUGH THE BARS YOU CAN SEE INTO A DIM CORRIDOR AND ON THE FLOOR YOU SPOT A SHINING BRASS KEY JUST OUT OF REACH. YOU DECIDE TO USE THE HOOK YOU FOUND AND PULL THE KEY INTO THE CELL. HOW CLEVER OF YOU!")
                                dungeon["cell"]["items"]["key"]["hidden_in"] = None
                                continue
                            else:
                                typing(dungeon["cell"]["objects"]["cell_door"]["examine_taken"])
                                continue
                        else:
                            typing(dungeon["cell"]["objects"]["cell_door"]["examine"])
                            continue
                #-----------------------------------------------------------------
                #switch exeption ------------------------------switch exeption
                if target == "switch":
                    if current_room == "east_cell_corridor":
                        typing(dungeon["east_cell_corridor"]["objects"]["switch"]["examine"])
                        flick_mysterious_switch = input("\n> ").lower().strip()

                        if flick_mysterious_switch == "y":
                            if switch_active == True:
                                if switch_used == False:
                                    typing("YOU FLICK THE SWITCH AND HEAR A WHIRRING MOTOR START UP. YOU HEAR THE ECHO OF GEARS GRINDING IN THE DISTANCE. AS YOU LOOK TOWARDS THE HEAVY DUTY DOOR TO YOUR EAST, YOU SEE IT SLOWLY SWING OPEN. THROUGH THE DOORWAY YOU SEE INTO A BRIGHTLY LIT HALL.")
                                    dungeon["east_cell_corridor"]["exits"]["e"] = "security_hall"
                                    discover(40, False, "AH, THAT'S WHAT IT'S FOR!  -  SWITCH THE SWITCH WHEN IT'S ACTIVE")
                                    switch_used = True
                                    continue
                                if switch_used == True:
                                    typing("THE SWITCH IS IN ON. YOU CAN HEAR A FAINT WHIRRING IN THE DISTANCE.")
                            else:
                                typing("NOTHING HAPPENS.")
                                if dungeon[current_room]["objects"][target]["scoring"]["scored"] == False:
                                    discover(
                                        obj_data["scoring"]["score"],
                                        obj_data["scoring"]["secret"],
                                        obj_data["scoring"]["discovery"],
                                        )
                                    obj_data["scoring"]["scored"] = True
                                continue
                        elif flick_mysterious_switch == "n":
                            typing("OK.")
                            continue
                        else:
                            typing("THAT IS NOT A VALID OPTION.")
                            continue
                #-----------------------------------------------------------------
                #Steam Whistle exeption-------------------------------------------
                if target == "tank":
                    typing(dungeon[current_room]["objects"][target]["examine"])
                    typing("DO YOU WANT TO BLOW THE WHISTLE? Y/N")
                    blowdecision = input("\n>").strip().lower()
                    if blowdecision == "y":
                        if whistle_blown == 0:
                            typing("TOOT! TOOT!")
                            discover(0, True, None)
                            whistle_blown += 1
                            continue
                        if whistle_blown == 1:
                            typing("TOOOOOT!! \n\nSOMEWHERE IN THE DISTANCE A VOICE YELLS 'WOULD YOU STOP THAT?!'")
                            whistle_blown += 1
                            continue
                        if whistle_blown > 1:
                            typing("TOOT!\n\nYOU HEAR FAINT GRUMBLING IN THE DISTANCE.")
                            continue
                    else:
                        typing("YOU'RE NO FUN.")
                        continue
                #-----------------------------------------------------------------
                for item_name in dungeon[current_room]["items"]:
                    item_details = dungeon[current_room]["items"][item_name]

                    if "hidden_in" in item_details:
                        if item_details["hidden_in"] == target:
                            item_details["hidden_in"] = None

                obj_data = dungeon[current_room]["objects"][target]
                if "hidden_in" in obj_data and obj_data["hidden_in"] != None:
                    typing("YOU CANNOT SEE WHAT YOU ARE DOING.")
                    continue
                elif "has_item" in obj_data and obj_data["has_item"] == True:
                    typing(obj_data["examine"])
                    dungeon[current_room]["objects"][target]["has_item"] = False
                elif "examine_opened" in obj_data and obj_data["object_open"] == True:
                    typing(obj_data["examine_opened"])
                elif "examine_taken" in obj_data:
                    typing(obj_data["examine_taken"])
                else:
                    typing(obj_data["examine"])

                if "scoring" in obj_data and obj_data["scoring"]["scored"] == False:
                    discover(
                        obj_data["scoring"]["score"],
                        obj_data["scoring"]["secret"],
                        obj_data["scoring"]["discovery"],
                        )
                    obj_data["scoring"]["scored"] = True

            elif target in inventory or target in dungeon[current_room]["items"]: #items
                #Pigeon exeption------------------------------------------------
                if target == "pigeon":
                    if pigeon_tame == True:
                        typing(master_items["pigeon"]["examine_taken"])
                        continue
                    elif pigeon_tame == False:
                        typing(master_items["pigeon"]["examine"])
                        continue
                #-----------------------------------------------------------------
                if target in dungeon[current_room]["items"] and dungeon[current_room]["items"][target]["hidden_in"] != None:
                    typing("I SEE NO " + target.upper() + " HERE!")
                else:
                    typing(master_items[target]["examine"])
                continue

            elif target == "":
                typing("WHAT DO YOU WISH TO EXAMINE?")
                continue
            else:
                typing("I SEE NO " + target.upper() + " HERE!")



        elif command == "objects":                                    #Objects Command
            if len(dungeon[current_room]["objects"]) == 0:
                typing("THERE ARE NO INTERACTABLE OBJECTS HERE.")
                continue
            else:
                typing("THE INTERACTABLE OBJECTS IN THIS ROOM ARE:")
                for object_name in dungeon[current_room]["objects"]:
                    if "id_type" in dungeon[current_room]["objects"][object_name]:
                        typing("\n- " + dungeon[current_room]["objects"][object_name]["id_type"].upper())
                    else:
                        typing("\n- " + object_name.upper())

        elif command == "items":                                    #Items Command
            visible_count = 0
            for itemdectector_name in dungeon[current_room]["items"]:
                if dungeon[current_room]["items"][itemdectector_name]["hidden_in"] == None:
                    visible_count = visible_count + 1
            if visible_count == 0:
                typing("THERE ARE NO ITEMS YOU CAN PICK UP RIGHT NOW.")
                continue
            else:
                typing("THE ITEMS YOU CAN PICK UP RIGHT NOW ARE:")
                for itemdectector_name in dungeon[current_room]["items"]:
                    if dungeon[current_room]["items"][itemdectector_name]["hidden_in"] == None:
                        typing("\n- " + itemdectector_name.upper())


                                                                                    #Get Command
        elif action in ["get", "take", "pick", "pickup", "grab", "collect", "steal", "give", "g"]:
            #pantry exeption------------------
            if current_room == "pantry":
                typing("I'M NOT LETTING YOU TAKE ANYTHING! THEY'D NOTICE!")
                continue
            #--------------------------------
            #water room exeption----------------------
            if "bottle" in inventory or "bottle" in dungeon[current_room]["items"]:
                if current_room == "water_room" and target == "water":
                    typing("YOU FILL THE BOTTLE WITH WATER.")
                    inventory.remove("bottle")
                    inventory.append("water")
                    continue
            #-----------------------------------------
            if target == "":
                typing("WHAT DO YOU WANT TO GET?")
                continue
            elif target in dungeon[current_room]["items"]:
                if dungeon[current_room]["items"][target]["hidden_in"] == None:
            #Pigeon exeption-----------------------------------------------------------
                    if target == "pigeon":
                        if pigeon_tame == False:
                            if "seeds" in inventory:
                                typing("THE PIGEON MAKES A BIG FUSS AND WON'T LET YOU PICK IT UP. IT DOES HOWEVER LOOK, ENVIOUSLY AT THE SEEDS YOU ARE CARRYING.")
                                continue
                            else:
                                typing("THE PIGEON MAKES A BIG FUSS AND WON'T LET YOU PICK IT UP.")
                                continue
            #---------------------------------------------------------------------------

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
                        #Rubble exeption-----------------------------------------------------------
                        if target == "rubble" and current_room == "bathroom_broken":
                            if rubble_in_room <= 3 and rubble_in_room > 0:
                                rubble_in_room = rubble_in_room - 1
                                if rubble_in_room <= 0:
                                    inventory.append(target)
                                    del dungeon["bathroom_broken"]["items"]["rubble"]
                                    typing("OK.")
                                else:
                                    inventory.append(target)
                                    typing("OK.")
                                continue
                        #--------------------------------------------------------------------------
                        inventory.append(target)
                        del dungeon[current_room]["items"][target]

                        typing("OK.")

                    if "scoring" in master_items[target] and master_items[target]["scoring"]["scored"] == False:
                        discover(
                            master_items[target]["scoring"]["score"],
                            master_items[target]["scoring"]["secret"],
                            master_items[target]["scoring"]["discovery"],
                            )
                        master_items[target]["scoring"]["scored"] = True
                    continue
                else:
                    typing("I SEE NO " + target.upper() + " HERE!")
                    continue
            elif target in dungeon[current_room]["objects"]:
                typing("YOU CAN'T PICK THAT UP.")
            else:
                typing("I SEE NO " + target.upper() + " HERE!")


        elif action in ["drop", "discard", "leave", "place", "toss", "dump"]:   #Drop Command
            if target == "":
                typing("WHAT DO YOU WANT TO DROP?")
                continue
            elif target in inventory:
                #rubble exeption------------------------------------------------------
                if target == "rubble" and current_room == "bathroom":
                    inventory.remove("rubble")
                    rubble_in_pile = rubble_in_pile + 1
                    if rubble_in_pile == 1:
                        typing("YOU PLACE THE RUBBLE ON THE GROUND BUT IT IS BARELY ENOUGH TO LET YOU REACH THE VENT.")
                        dungeon["bathroom"]["objects"]["pile"] = {
                            "examine" : "IT'S A SMALL LUMP OF RUBBLE BARELY A FOOT HIGH."
                            }
                    elif rubble_in_pile == 2:
                        typing("YOU ADD SOME RUBBLE TO THE PILE.")
                        dungeon["bathroom"]["objects"]["pile"]["examine"] = "IT'S A MODERATE PILE OF RUBBLE ALMOST HIGH ENOUGH TO LET YOU REACH THE VENT SHAFT."
                    elif rubble_in_pile == 3:
                        typing("YOU ADD SOME RUBBLE TO THE PILE AND NOW IT IS HIGH ENOUGH FOR YOU TO STAND ON IT AND JUMP INTO THE VENT SHAFT.")
                        dungeon["bathroom"]["objects"]["pile"]["examine"] = "IT'S A LARGE PILE OF RUBBLE  HIGH ENOUGH TO LET YOU REACH THE VENT SHAFT."
                        dungeon["bathroom"]["exits"]["u"] = "vent_shaft"
                        if "blocked_exits" in dungeon["bathroom"] and "u" in dungeon["bathroom"]["blocked_exits"]:
                            del dungeon["bathroom"]["blocked_exits"]["u"]
                    else:
                        typing("THE PILE IS AS HIGH AS YOU NEED!")
                    continue
                #---------------------------------------------------------------------
                #seeds exeption-----------------------------------seeds exeption
                if target == "seeds" and current_room == "pigeon_room" and "pigeon" in dungeon[current_room]["items"]:
                    if pigeon_tame == False:
                        typing("THE PIGEON SWOOPS DOWN AND GRAPS THE PACKET OF SEEDS, IN A BIG MESS IT RIPS THE PACKET OPEN AND EATS ALL OF THE CONTENTS INSIDE. IT NOW SEEMS MORE PLACID AND TAME.")
                        pigeon_tame = True
                        discover(20, False, "MAN'S SECOND BEST FRIEND  -  TAME THE PIGEON")
                #-------------------------------------------------------------
                #choc-pigeon exeption-----------------------------------choc-pigeon exeption
                if target == "chocolate" and current_room == "pigeon_room" and "pigeon" in dungeon[current_room]["items"]:
                    typing("THE PIGEON LOOKS DISGUSTEDLY AT THE CHOCOLATE BAR YOU GAVE IT. IN FACT IT BECOMES FURIOUS AND DELIVERS A LETHAL PECK.")
                    ending = "death"
                    playing = False
                    break
                #-------------------------------------------------------------
                #water office exeption--------------------------------------------------
                if target == "water" and current_room == "guard_office_1":
                    typing("YOU PUT THE BOTTLE OF WATER ON THE DESK.")
                    inventory.remove(target)
                    dungeon[current_room]["items"][target] = { "name" : master_items[target]["name"],
                                                        "hidden_in" : None,
                                                        }
                    guard_water_count = 8
                    continue

                #---------------------------------------------------------------
                #water room exeption---------------------------------------------------
                if target == "bottle" and current_room == "water_room":
                    typing("YOU FILL UP THE BOTTLE WITH WATER.")
                    inventory.remove("bottle")
                    inventory.append("water")

                #--------------------------------------------------------------------

                dungeon[current_room]["items"][target] = { "name" : master_items[target]["name"],
                                                        "hidden_in" : None,
                                                        }
                inventory.remove(target)
                typing("OK.")
            else:
                typing("YOU AREN'T CARRYING THAT!")




                                                                    #Open Command
        elif action in ["open", "unlock","enter"]:
            if target == "":
                typing("WHAT DO YOU WANT TO OPEN?")
                continue
            elif target in dungeon[current_room]["objects"] and "object_open" in dungeon[current_room]["objects"][target] and dungeon[current_room]["objects"][target]["object_open"] == True:
                typing("IT IS ALREADY OPEN!")
                continue
            elif target in dungeon[current_room]["objects"]:
                obj_data = dungeon[current_room]["objects"][target]
                #code door exeption-----------------------------------------
                if target == "detention_door" and current_room == "detention_junction":
                    typing("ENTER THE PIN CODE.")
                    pin_code = input("\n>>")
                    if pin_code == "1358":
                        inventory.append("pincode")
                    else:
                        typing("\nINCORRECT.")
                        continue

                    #--------------------------------------------------------------

                if "locked" in obj_data and obj_data["locked"] == True:
                    if obj_data["unlocker"] in inventory:
                        obj_data["locked"] = False
                    else:
                        typing(obj_data["open_locked"])
                        continue
                if "locked" in obj_data and obj_data["locked"] == False or "object_open" in obj_data:
                    obj_data["object_open"] = True

                    if "open" in obj_data:
                        typing(obj_data["open"])
                    else:
                        typing("OK.")

                    if "unlock_direction" in obj_data and "unlock_room" in obj_data:
                        new_dir = obj_data["unlock_direction"]
                        new_room = obj_data["unlock_room"]

                        dungeon[current_room]["exits"][new_dir] = new_room

                        if "blocked_exits" in dungeon[current_room] and new_dir in dungeon[current_room]["blocked_exits"]:
                            del dungeon[current_room]["blocked_exits"][new_dir]

                    if "contains" in obj_data:
                        item_to_drop = obj_data["contains"]
                        dungeon[current_room]["items"][item_to_drop] = {
                            "name" : master_items[item_to_drop]["name"],
                            "hidden_in" : None
                            }
                        del obj_data["contains"]

                else:
                    typing("IT CANNOT BE OPENED.")

            elif target in inventory or target in dungeon[current_room]["items"]:
                if target in dungeon[current_room]["items"] and dungeon[current_room]["items"][target]["hidden_in"] != None:
                    typing("I SEE NO " + target.upper() + " HERE!")
                elif "open" in master_items[target]:
                    typing(master_items[target]["open"])
                    if "contains" in master_items[target] and master_items[target]["contains"] != None:
                        item_to_drop = master_items[target]["contains"]
                        dungeon[current_room]["items"][item_to_drop] = {
                            "name" : master_items[item_to_drop]["name"],
                            "hidden_in" : None
                        }
                        del master_items[target]["contains"]
                        continue
                else:
                    typing("IT CANNOT BE OPENED.")
            else:
                typing("I SEE NO " + target.upper() + " HERE!")



        elif action == "light":                                 #light Command
            if target == "":
                typing("WHAT DO YOU WANT TO LIGHT?")
                continue
            elif target == "lighter":
                if target in inventory:
                    if "oil" in inventory:
                        typing("YOU LIGHT THE LIGHTER USING THE OIL!")

                        inventory.remove("oil")
                        lighter_is_lit = True
                        master_items["lighter"]["used"] = True
                    else:
                        typing("YOU HAVE NOTHING TO LIGHT IT WITH.")
                else:
                    typing("YOU DON'T HAVE THE LIGHTER.")

            elif target == "fire":
                if current_room == "meeting_room":
                    if "lighter" in inventory and lighter_lit == True:
                        typing("YOU LIGHT THE SMOKING REMAINS WITH YOUR LIGHTER AND THE OLD FIREPIT BURSTS INTO FLAMES. YOU HEAR A LOW RUMBLING AND TO YOUR NORTH, A HUGE, VERTICAL SLAB OF ROCK SHIFTS ASIDE REVEALING A HIDDEN PASSAGE!")
                        dungeon["meeting_room"]["exits"]["n"] = "meeting_secret_passage"
                        dungeon["meeting_room"]["dark"] = False
                    else:
                        typing("YOU HAVE NOTHING TO LIGHT THE FIRE WITH.")
                else:
                    typing("I SEE NO FIRE HERE...")

            else:
                typing("YOU CAN'T LIGHT THAT!")

        elif command in ["hide", "conceal", "duck"]:                   #hide command
            if guard_alert > 0:
                is_hidden = current_room
                typing("YOU HIDE AWAY IN THE SHAD0WS.")
            else:
                typing("WHAT ARE YOU HIDING FROM? YOU DON'T NEED TO.")

        elif command == "devcheat1234":                                 #Devcommands

            typing("DEVELPOER MODE ACTIVE - USE WITH CAUTION. THIS WILL SPOIL THE GAME IF USED INCORRECTLY!")
            devmode = True

        elif action == "tp" and devmode == True:
            if target in dungeon:
                if target == current_room:
                    typing("YOU ARE ALREADY HERE!")
                    continue
                else:
                    current_room = target
                    typing("TELEPORTING TO " + target.upper() + "!")
                    continue
            else:
                typing("INVALID ROOM NAME!")
                continue
        elif action == "devgive" and devmode == True:
            if target in master_items:
                if target in inventory:
                    typing("YOU ALREADY HAVE THE ITEM!")
                else:
                    inventory.append(target)
                    typing("ITEM ADDED!")
                    continue
        elif command == "safe" and devmode == True:
            if safe == False:
                danger_zone1 = []
                danger_zone2 = []
                typing("GUARDS REMOVED!")
                safe = True
                continue
            else:
                typing("THE GUARDS ARE ALREADY GONE!")
                continue
        elif command == "unsafe" and devmode == True:
            if safe == True:
                danger_zone1 = danger_zone1_Backup
                danger_zone2 = danger_zone2_Backup
                typing("GUARDS ARE BACK!")
                safe = False
                continue
            else:
                typing("THE DUNGEON IS ALREADY UNSAFE!")
        elif command == "devinv" and devmode == True:
            for devitem in master_items:
                if devitem not in inventory:
                    inventory.append(devitem)
            loading_bar("-ADDING ITEMS-", 0.5)
            typing("ALL ITEMS ADDED TO INVENTORY!")
            continue
        elif action == "devmap" and devmode == True:
            if target == "":
                typing("TARGET REQUIRED! WHAT DO YOU WANT TO MAP?")
            elif target == "rooms":
                typing("MAPPING ROOMS:\n")
                for room in dungeon:
                    typing("-"+room)
                typing("\nROOMS MAPPED!")
                continue
            elif target == "objects":
                typing("MAPPING OBJECTS:\n")
                for room in dungeon:
                    if len(dungeon[room]["objects"]) > 0:
                        for obj in dungeon[room]["objects"]:
                            typing(obj + " IN " + room)
                typing("\nOBJECTS MAPPED!")
            elif target == "items":
                typing("MAPPING ITEMS:\n")
                for item in master_items:
                    typing("-"+item)
                typing("\nITEMS MAPPED!")
            elif target == "exits":
                typing("MAPPING EXITS:\n")
                if len(dungeon[current_room]["exits"]) == 0:
                    typing("DEVMAP ERROR - NO EXITS IN CURRENT ROOM!\nHAVE YOU OPENED ALL DOORS?")
                    continue
                else:
                    for exit in dungeon[current_room]["exits"]:
                        exit_dir = dungeon[current_room]["exits"][exit]
                        typing("-"+exit+" = "+exit_dir)

                    typing("\nEXITS MAPPED!")
            elif target == "help":
                typing("FOLLOW DEVMAP WITH ONE OF THE FOLLOWING:\n\n-rooms\n\n-objects\n\n-items\n\n-exits")
            else:
                typing("PLEASE USE A VALID TARGET.")



        elif command == "god" and devmode == True:
            if god == False:
                typing("GOD MODE ACTIVATED!")
                god = True
                continue
            elif god == True:
                typing("GOD MODE DEACTIVATED!")
                god = False
                continue

        elif action == "devopen" and devmode == True:
            if target == "":
                typing("WHAT DO YOU WANT TO FORCE OPEN?")
                continue
            devobject_found = False
            for room in dungeon:
                if target in dungeon[room]["objects"]:
                    devobject_found = True
                    devobject = dungeon[room]["objects"][target]
                    if "object_open" in devobject or "locked" in devobject:
                            devobject["object_open"] = True
                            devobject["locked"] = False

                            if "unlock_direction" in devobject:
                                new_dir = devobject["unlock_direction"]
                                new_room = devobject["unlock_room"]
                                dungeon[room]["exits"][new_dir] = new_room

                            if "blocked_exits" in dungeon[room] and new_dir in dungeon[room]["blocked_exits"]:
                                    del dungeon[room]["blocked_exits"][new_dir]

                            if "contains" in devobject and devobject["contains"] != None:
                                item_to_drop = devobject["contains"]
                                dungeon[room]["items"][item_to_drop] = {
                                    "name" : master_items[item_to_drop]["name"],
                                    "hidden_in" : None
                                        }
                                devobject["contains"] = None
                                typing("THE OBJECT HAS BE FORCED OPEN!")
                                continue
                            else:
                                typing("THE OBJECT HAS BEEN FORCED OPEN!")
                                continue
                    else:
                        typing("THE OBJECT CAN'T BE OPENED!")
            if devobject_found == False:
                typing("THE OBJECT CANNOT BE FOUND!")
                continue
        elif action == "devopenall" and devmode == True:
            for room in dungeon:
                for obj_to_open in dungeon[room]["objects"]:
                    devobject = dungeon[room]["objects"][obj_to_open]
                    if "object_open" in devobject or "locked" in devobject:
                        devobject["object_open"] = True
                        devobject["locked"] = False

                        if "unlock_direction" in devobject:
                            new_dir = devobject["unlock_direction"]
                            new_room = devobject["unlock_room"]
                            dungeon[room]["exits"][new_dir] = new_room

                        if "blocked_exits" in dungeon[room] and new_dir in dungeon[room]["blocked_exits"]:
                                del dungeon[room]["blocked_exits"][new_dir]

                        if "contains" in devobject and devobject["contains"] != None:
                            item_to_drop = devobject["contains"]
                            dungeon[room]["items"][item_to_drop] = {
                                "name" : master_items[item_to_drop]["name"],
                                "hidden_in" : None
                                        }
                            devobject["contains"] = None
                        typing("\n-OPENED " + obj_to_open)
            typing("\nOBJECTS OPENED!")


        elif action == "save":                                                 #Save
            if target == "":
                typing("PLEASE PROVIDE A SAVE NAME.")
                continue                             #ADD ALL VARIABLES
            save_packet = {
                "playing" : playing,
                "current_room" : current_room,
                "inventory" : inventory,
                "switch_active" : switch_active,
                "lighter_lit" : lighter_lit,
                "lighter_is_lit" : lighter_is_lit,
                "ending" : ending,
                "pigeon_tame" : pigeon_tame,
                "previous_room" : previous_room,
                "met_prisoners" : met_prisoners,
                "score" : score,
                "discoveries" : discoveries,
                "secrets" : secrets,
                #ADD ALL VARIABLES
                "dungeon_state" : dungeon
                }

            filename = "etdsave_" + target + ".json"
            with open(filename, "w") as file:
                json.dump(save_packet, file)
            typing("GAME SAVED AS: " + filename.upper() + "! YOU CAN REFER TO IT AS '" + target.upper() + "' WHEN LOADING.\n")

        elif action == "list" and target == "save":                          #list save
            save_files = glob.glob("etdsave_*.json")
            if len(save_files) == 0:
                typing("NO VALID SAVE FILES DETECTED.\n")
            else:
                typing("\nSAVE FILES LOCATED:\n")
                for file_path in save_files:
                    clean_name = file_path.replace("etdsave_", "").replace(".json", "")
                    typing("-" + clean_name.upper() + "\n")


        elif action == "load":                                                #load
            if target == "":
                typing("PLEASE PROVIDE THE SAVE NAME.")
                continue
            filename = "etdsave_" + target + ".json"
            if not os.path.exists(filename):
                typing("SAVE " + target.upper() + " NOT FOUND. ARE YOU SURE YOU TYPED THE CORRECT NAME?")
                continue
            with open(filename, "r") as file:
                save_packet = json.load(file)

            playing = save_packet["playing"]#ADD ALL VARIABLES
            current_room = save_packet["current_room"]
            inventory = save_packet["inventory"]
            switch_active = save_packet["switch_active"]
            lighter_lit = save_packet["lighter_lit"]
            lighter_is_lit = save_packet["lighter_is_lit"]
            ending = save_packet["ending"]
            pigeon_tame = save_packet["pigeon_tame"]
            previous_room = save_packet["previous_room"]
            score = save_packet["score"]
            discoveries = save_packet["discoveries"]
            secrets = save_packet["secrets"]
            met_prisoners = save_packet["met_prisoners"]
            #ADD ALL VARIABLES
            dungeon = save_packet["dungeon_state"]
            loading_bar("RESTORING SAVE", 2)
            typing("SAVE RESTORED.")
            continue







        else:                                                    #END OF COMMANDS!!!!
            typing("I DON'T UNDERSTAND THAT. TYPE HELP FOR A LIST OF VALID COMMANDS.")








    #ENDINGS-----------------------------------------------------------ENDINGS!!-----------------------------
    if god == True:
        if ending == "death":
            playing = True
            current_room = previous_room
            typing("-GOD MODE SAVED YOU FROM DYING! YOU HAVE BEEN PUT BACK IN THE PREVIOUS ROOM!-")
            continue
        elif ending == "capture":
            playing = True
            current_room = previous_room
            typing("-GOD MODE SAVED YOU FROM BEING CAPTURED! YOU HAVE BEEN PUT BACK IN THE PREVIOUS ROOM!-")
            continue
        elif ending == "quit":
            continue


    if ending == "death":
        time.sleep(0.5)
        typing("\n\nUNFORTUNATLEY YOU HAVE DIED. I'M AFRAID YOU WILL HAVE TO START OVER. WHAT A SHAME.")
        time.sleep(0.5)
        typing("\n\n-----GAME OVER-----")
        end()
        break

    elif ending == "quit":
        break

    elif ending == "capture":
        time.sleep(0.1)
        typing("\n\nYOU HAVE BEEN CAUGHT. YOU ARE CHUCKED RIGHT BACK IN YOUR CELL AND THE DOOR IS LOCKED AGAIN.")
        typing("\n\nWOULD YOU LIKE TO TRY AND ESCAPE AGAIN? Y/N.")
        restart = input("\n> ").lower().strip()
        if restart == "y":
            typing("\n\nOK.\n")
            time.sleep(0.7)
            window_size = os.get_terminal_size().columns
            header_text = "-RESETTING DUNGEON:"
            sys.stdout.write(header_text)
            sys.stdout.flush()
            time.sleep(0.3)
            bar_length = window_size - (len(header_text) -1) -1
            if bar_length < 10:
                bar_length = 10
            load_time = 4
            bar_characters = load_time / bar_length
            for i in range(bar_length):
                sys.stdout.write("-")
                sys.stdout.flush()
                time.sleep(bar_characters)

            typing("\n\nTHE DUNGEON HAS BEEN RESET!")
            dungeon = copy.deepcopy(initial_dungeon)
            time.sleep(1)
            #COPY VARIABLES HERE!!!!!!!!!!!!!



        elif restart == "n":
            typing("SO BE IT.")
            time.sleep(0.5)
            typing("\n\nYOU WERE CAPTURED AND DECIDED NOT TO TRY AND ESCAPE AGAIN.")
            time.sleep(0.6)
            typing("FOR NOW...")
            time.sleep(0.5)
            typing("\n\n-----GAME OVER-----")
            instructions = False
            end()
            break
        else:
            typing("PLEASE ANSWER THE QUESTION\n")
            time.sleep(1)

    elif ending == "escape":
        if "ticket" in inventory:
            discover(1, True, "LOOK WHAT I FOUND!  -  ESCAPE WITH THE CINEMA TICKET")
            break#ENDING HERE WITH TICKET
        else:
            typing("\n\n-----YOU ESCAPED!-----\n")
            time.sleep(2)
            end()
            break#ENDING HERE







