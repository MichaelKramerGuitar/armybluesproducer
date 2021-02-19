"""
1. instantiate Person's for every member of The Blues
2. instantiate Person's for every member of the tech crew
3. instantiate Person's for every member of the transportation team
"""


from armybluesproducer_CLI.person import Person

# Blues
Chief = Person("james", "landrum", "10", "oic", "male")
Ken = Person("kenneth", "mcgee", "9", "group leader, lead trumpet", "male")
Graham = Person("graham", "breedlove", "9", "section leader, trumpet", "male")
Josh = Person("joshua", "kauffman", "6", "lead trumpet", "male")
Alec = Person("alec", "aldred", "6", "trumpet", "male")
Chris = Person("chris", "burbank", "6", "trumpet", "male")
Luke = Person("luke", "brimhall", "7", "section leader, trombone", "male")
Aaron = Person("aaron", "eckert", "6", "trombone", "male")
Javier = Person("javier", "nero", "6", "lead trombone", "male")
Jake = Person("jake", "kraft", "6", "trombone, assistant librarian", "male")
Antonio = Person("antonio", "orta", "8", "section leader, lead alto saxophone", "male")
Dan = Person("dan", "andrews", "6", "alto saxophone", "male")
Xavier = Person("xavier", "perez", "6", "musical director, tenor saxophone", "male")
Clay = Person("clay", "pritchard", "6", "musical director, tenor saxophone", "male")
Dustin = Person("dustin", "mollick", "6", "baritone saxophone", "male")
Regan = Person("regan", "brough", "8", "bass, section leader", "male")
James = Person("james", "collins", "6", "piano, librarian, assistant producer", "male")
Eric_blues = Person("eric", "tapper, pers", "6", "drums", "male")
Michael = Person("michael", "kramer", "7", "producer, guitar", "male")

# group various Person's together via job in Blues
blues_roster = [Chief, Ken, Graham, Josh, Alec, Chris,
                Luke, Aaron, Javier, Jake,
                Antonio, Dan, Xavier, Clay, Dustin,
                Regan, James, Eric_blues, Michael]

rhythm_section = [Regan, Eric_blues, James, Michael]

saxophone_section = [Antonio, Dan, Xavier, Clay, Dustin]

trumpet_section = [Ken, Graham, Josh, Alec, Chris]

trombone_section = [Luke, Aaron, Javier, Jake]

# Crew
Jon = Person("jonathan", "seipp", "7", "crew member, crew leader", "male")
Mike = Person("mike", "willis", "6", "crew member", "male")
Brian = Person("brian", "knox", "7", "crew member, crew leader", "male")
May = Person("may", "duarte", "6", "crew member", "female")
Jeff = Person("jeff", "keller", "7", "crew member", "male")
Alex = Person("alex", "righter", "6", "crew member", "male")
Matt = Person("mattius", "bleicken", "6", "crew member", "male")
AJ = Person("aj", "maynard", "6", "crew member", "male")
Eric_crew = Person("eric", "messick", "6", "crew member", "male")

# group crew Person objects together
crew = [Jon, Mike, Brian, May, Jeff, Alex, Matt, AJ, Eric_crew]


# Transportation Team
Jay = Person("jay", "fuller", "9", "driver", "male")
Nick = Person("nick", "nickens", "9", "driver", "male")

# Group driver Person objects
drivers = [Jay, Nick]

full_team = [Chief, Ken, Graham, Josh, Alec, Chris,
                Luke, Aaron, Javier, Jake,
                Antonio, Dan, Xavier, Clay, Dustin,
                Regan, James, Eric_blues, Michael,
                Jon, Mike, Brian, May, Jeff, Alex, Matt,
                AJ, Eric_crew, Jay, Nick]