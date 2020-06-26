import operator
import random

### Here we make a global variable which is accessible anywhere in the file ###
DIRECTIONS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
DIRECTIONS2 = {"up": 1, "down": 2, "left": 3, "right": 4}

### Here we make a class so that when we make create a simulation, we can use all of these functions within our class ###
### Otherwise known as attributes or methods ###
class GameSim:

    ### player ###
    # Contains -> [x_pos, y_pos, type]
    # Example -> [0, 1]

    ### items ###
    # Contains -> [x_pos, y_pos, Active]
    # Example -> [2, 2, True]

    ### We initialize the class with the following variables ###
    def __init__(self):
        ### map ###
        self.map = [
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0],
                    ]

        ### All the possible coordinates within the map ###
        self.available_coordinates = [
                                 (0, 0), (1, 0), (2, 0), (3, 0), 
                                 (0, 1), (1, 1), (2, 1), (3, 1), 
                                 (0, 2), (1, 2), (2, 2), (3, 2), 
                                 (0, 3), (1, 3), (2, 3), (3, 3),
                            ]

        ### Here we pick two coordinates at random from the available coordinates above ###
        item_coordinates, player_coordinates = random.sample(self.available_coordinates, 2)

        ### We get our map size automatically ###
        self.mapSize = {"x": len(self.map[0]), "y": len(self.map)}
        
        ### We create a previous action that is empty at first so we can tell the AI what it did for its last move ###
        self.previous_action = []

        ### Here we create a list that looks like the list of 0's above us, but the location of the AI ###
        ### is a 1! It looks like this 
                   # [
                   # [0,0,0,0],
                   # [0,1,0,0],
                   # [0,0,0,0],
                   # [0,0,0,0],
                    #]
                    
        ### Now the AI can look at the map and know where it is ###

        ### Player State ###
        self.player_location = [x[:] for x in [[0] * 4] * 4]
        self.player_location[player_coordinates[1]][player_coordinates[0]] = 1

        
        ### Here we do the same thing but the 1 is the location of the item ###
        ### It looks like this  ###
                   # [
                   # [0,0,0,0],
                   # [0,1,0,0],
                   # [0,0,0,0],
                   # [0,0,0,0],
                    #]
                    
        ### Item State ###
        self.item_location = [x[:] for x in [[0] * 4] * 4]
        self.item_location[item_coordinates[1]][item_coordinates[0]] = 1


        ### Here we tell the AI where it is using (x,y) coordinates ###
        ### Player Location ###
        self.player = [
                        player_coordinates[0],
                        player_coordinates[1],
                    ]

        ### We also tell it where the item is in (x,y) coordinates ###
        ### Item Location ###
        self.items = [
                     item_coordinates[0],
                     item_coordinates[1],
                     True,
                ]
    
    ### This is our first attribute below! All of the following functions get ran in the custom_env file ###
    ### To use any of these functions we create an instance of the GameSim class, thus creating an object ###
    ### To do that all we type is:
                         ###  simulation = GameSim() ###
    ### and thats it. We now have a simulation object called simulation! To use this reset() function ###
    ### you only need to type this:
                        ###    simulation.reset() ###
        
    def reset(self):
        ### This function basically just resets the item and AI location within the simulation ###
        ### Reusing code from the above initialization function ###
        item_coordinates, player_coordinates = random.sample(self.available_coordinates, 2)

        self.mapSize = {"x": len(self.map[0]), "y": len(self.map)}

        ### Player State ###
        self.player_location = [x[:] for x in [[0] * 4] * 4]
        self.player_location[player_coordinates[1]][player_coordinates[0]] = 1


        ### Item State ###
        self.item_location = [x[:] for x in [[0] * 4] * 4]
        self.item_location[item_coordinates[1]][item_coordinates[0]] = 1


        ### Player Location ###
        self.player = [
                        player_coordinates[0],
                        player_coordinates[1],
                    ]

        ### Item Location ###
        self.items = [
                        item_coordinates[0],
                        item_coordinates[1],
                        True,
        ]

        ### Here is where we tell the AI what the world looks like around it ###
        ### These are the things the AI will use to make its decisions and learn ###
    def get_state(self):
        ### Here we start an empty list which we will then fill up with information to give to it ###
        state = []

        ### Here we put the map in that list ###
        for row in self.map:
            state.extend(list(map(float, row)))
        ### Here we put the item location in the list ###
        for row in self.item_location:
            state.extend(list(map(float, row)))
        ### Here we put the player location in the list ###
        for row in self.player_location:
            state.extend(list(map(float, row)))
        ### Here we put the previous action the AI made in the list ###
        if self.previous_action != []:
            state.extend(list(map(float, self.previous_action)))
        ### We also check to make sure to just put in 0 if it is its first move of the game so our code ###
        ### doesn't get confused and not know what to do ###
        else:
            state.extend(list(map(float, [0])))
        ### Finally we tell this function what to return to the other code that told it to run in the first place ###
        return state
    
    ### Here is where we tell the AI whether its move was successful or not, this function is called ###
    ### like this (remember to use these functions we have to use the "object we created in the code above) ###
    ### simulation.reward((0,3)) here we see we called the function but we also gave it a set of (x,y) coordinates ###
    ### this allows us to use that information to tell the AI if the move was good or not ###
    def reward(self, new_pos):
        ### Here is where we create a new variable and then call another function within this same class ###
        ### We call item_update((0,3)) and give it the new_pos (new position) that we have ###
        ### item_update will tell return True or False if the AI reached the item. If it did then on_item becomes ###
        ### True, and if it didn't on_item becomes False.
        on_item = self.item_update(new_pos)
        # If on_item is True then we give the AI a reward of 35 points! ###
        if on_item:
            return 35, True
        ### If not, then we take 1 point away from it ###
        else:
            return -1, False
            
    ### Here we just check the item list to find out if its 2nd index is True or False. Remember ###
    ### True means the item is still active, False means the item is not active and the AI won ###
    def gameOver(self):
        return not self.items[2]
    
    ### Here is where we decide if the AI's move is actually inside of the map we gave it! ###
    ### Here we are given the "destination" which is the (x,y) coordinate that it wants to move to ###
    def inBounds(self, destination):
        ### Here we make a variable called valid that we set to True and use to decide if it is in bounds ###
        valid = True
        ### If its y coordinate is less than 0 valid is False ###
        valid = destination[0] >= 0
        ### If its x coordinate is less than 0 valid is False ###
        valid = valid and destination[1] >= 0
        ### If its y coordinate is more than 3 valid is False ###
        valid = valid and destination[1] <= (self.mapSize['x'] - 1)
        ### If its x coordinate is more than 3 valid is False ###
        valid = valid and destination[0] <= (self.mapSize['y'] - 1)
        ### Now if valid has survived all the checks and is still True, then the AI's move is valid! ###
        ### We then return the state of valid (True or False) to the function that called this attribute ###
        if not valid:
            return False
        return valid
    
    ### Here is where we actually update where the AI is in the simulation ###
    ### This function is given the decision of the AI, which is up, down, left, or right. ###
    def movePlayer(self, movement):
        ### Here we make the make the player variable refer to the player thats in this class ###
        player = self.player

        ### gets largest value in the dictionary given to the function, ###
        ### which will correlate with the chosen movement ###
        max_value = max(movement.items(), key=operator.itemgetter(1))[1]

        ### This is some wacky code that we use in the SMALL chance two of the decisions have the same ###
        ### number, making sure the function knows what to do if that does happen. ###
        # get all directions with that number 
        direction_possibilities = []
        for item in movement.items():
            if item[1] == max_value:
                direction_possibilities.append(item[0])
        
        ### We randomly choose one of the actions if they're the same ###    
        direction = random.choice(direction_possibilities)
        step = DIRECTIONS[direction]
        
        ### We make player_pos the players (x,y) coordinates ###
        player_pos = (player[0], player[1])
        
        ### We then use the global variable from the top to translate up, down, left, right to what those moves ###
        ### look like in the (x,y) coordinate grid ###
        destination = tuple(map(operator.add, player_pos, step))

        ### Here we use the inBounds() function and give it the AI's requested destination ###
        ### If it comes back False then we do not move the AI and it has to try again ###
        if self.inBounds(destination):
            player[0] = destination[0]
            player[1] = destination[1]
            self.player = player
        ### We then change destination to an (x,y) coordinate form and return it to the function that called this one ###
        ### so it has the new position ###
        destination = (player[0], player[1])
 
        return destination
    
    ### Here we update the second index of the item list so that if the AI gets the item we can double check ###
    ### that the game is over with that index. We also pass the new position to this function as pos in (x,y) form ###
    ### Remember indexes are just positions in a list. In this case it looks like the following ###
    
    ### looks like this:                 0               1               2                  ###
    ###             self.items = [x coordinate=2, y coordinate=3, Active?=True or False] ###
    
    ### So you can do stuff with its active information by using self.items[2] ###
    def item_update(self, pos):
        ### We make a variable to determine if the item was collected ###
        ret = False
        ### Make an if statement to see if the items (x,y) coordinates match the (x,y) coordinates passed ###
        ### to this function ###
        if (int(self.items[0]), int(self.items[1])) == pos:
            print("Gathered Item")
            ret = True
        ### If they are then we set ret to True and then update whether the item is active or not in self.items ###
        self.items[2] = False
        ### We then return ret which is True or False depending on whether the item was collected or not ###
        return ret

    ### Checks to see if the move the AI made was valid or not, without actually making any changes to where ###
    ### the AI is in the simulation ###
    def move_check(self, movement):
        ### Operates almost identically to move_player() but does not actually move them, just checks if its valid ###
        player = self.player

        # gets largest value in dictionary, which will correlate with the chosen movement
        max_value = max(movement.items(), key=operator.itemgetter(1))[1]

        # get all directions with that probability
        direction_possibilities = []
        for item in movement.items():
            if item[1] == max_value:
                direction_possibilities.append(item[0])

        direction = random.choice(direction_possibilities)
        state_direction = DIRECTIONS2[direction]
        self.previous_action.clear()
        self.previous_action.append(state_direction)
        step = DIRECTIONS[direction]

        player_pos = (player[0], player[1])

        destination = tuple(map(operator.add, player_pos, step))
        old_position = player[0], player[1]
        
        ### Major difference is that it uses the same logic to get its destination and check it in the ###
        ### inBounds() function, returning True or False ###
        if self.inBounds(destination):
            return True
        else:
            return False
