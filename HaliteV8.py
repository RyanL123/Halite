#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("deFus3")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """
ships_dict = {}
last_position = (0,0)
	
while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
	game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
	me = game.me
	game_map = game.game_map

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
	command_queue = []
	
	# Checks every cell around the shipyard for ships
	ship_yard_cell1 = not game_map[me.shipyard.position.get_surrounding_cardinals()[0]].is_occupied
	ship_yard_cell2 = not game_map[me.shipyard.position.get_surrounding_cardinals()[1]].is_occupied
	ship_yard_cell3 = not game_map[me.shipyard.position.get_surrounding_cardinals()[2]].is_occupied
	ship_yard_cell4 = not game_map[me.shipyard.position.get_surrounding_cardinals()[3]].is_occupied
	safe_to_spawn = False
	
	# If no cell is occupied, it is safe to spawn ships
	if ship_yard_cell1 and ship_yard_cell2 and ship_yard_cell3 and ship_yard_cell4:
		safe_to_spawn = True
		
    # spawns a ship if the turn number is below 300 and the shipyard and all ceels around it are not occupied
	if game.turn_number <= 250 and me.halite_amount >= 1000 and not game_map[me.shipyard].is_occupied and safe_to_spawn: 
		command_queue.append(me.shipyard.spawn())
	for ship in me.get_ships():
	
		game_map[ship.position].mark_unsafe(ship)
		
		if game_map.height == 32:
			if game.turn_number == 360:
				ships_dict[ship.id] = "returning"
		elif game_map.height == 40:
			if game.turn_number == 370:
				ships_dict[ship.id] = "returning"
		elif game_map.height == 48:
			if game.turn_number == 390:
				ships_dict[ship.id] = "returning"
		elif game_map.height == 56:
			if game.turn_number == 400:
				ships_dict[ship.id] = "returning"
		elif game_map.height == 64:
			if game.turn_number == 430:
				ships_dict[ship.id] = "returning"
		

			
		
		# if the ship is not in the dictionary, add it with the status of searching
		if ship.id not in ships_dict:
			ships_dict[ship.id] = "searching"
			
		
		# if the ship is full and not at shipyard, change status to returning
		elif ship.position != me.shipyard.position and ship.is_full:
			# Marks the position the ship was at before returning
			if ships_dict[ship.id] != "returning":
				last_position = game_map[ship.position]
				ships_dict[ship.id] = "returning"

		# returns the ship to the last marked position, then changes status to searching
#		if ships_dict[ship.id] == "returning_to_last_position":
#			if ship.position != last_position:
#				command_queue.append(game_map.naive_navigate(ship, last_position))
#			elif ship.position == last_position:
#				ships_dict[ship.id] = "searching"
		
		# if the status is searching, look for the square with the highest halite amount, and move to it, then change status to collecting
		if ships_dict[ship.id] == "searching":
			highest_halite = 0
			highest_halite_position = 0
			surrounding_cardinals = ship.position.get_surrounding_cardinals()
			for i in range(0,4):
				# if the square is bigger than the highest halite amount and is not occupied
				if game_map[surrounding_cardinals[i]].halite_amount >= highest_halite and not game_map[surrounding_cardinals[i]].is_occupied:
					# updates the highest halite amount variable
					highest_halite = game_map[surrounding_cardinals[i]].halite_amount
					# records the index of the direction with the highest halite amount
					highest_halite_position = i
				# go to the square with the highest halite amount
			command_queue.append(ship.move(game_map.naive_navigate(ship, surrounding_cardinals[highest_halite_position])))
			ships_dict[ship.id] = "collecting"
			
			
		# if the status is colecting, stay still and change status to searching
		elif ships_dict[ship.id] == "collecting":
			command_queue.append(ship.stay_still())
			ships_dict[ship.id] = "searching"
			
			
		# if the ship just finished depositing, then return the ship to the last marked position
		elif not ship.is_full and ships_dict[ship.id] == "returning" and ship.position == me.shipyard.position:
#			ships_dict[ship.id] = "returning_to_last_position"
			ships_dict[ship.id] = "searching"
			
			
		# if the status is returning, return to base
		elif ships_dict[ship.id] == "returning":
			command_queue.append(ship.move(game_map.naive_navigate(ship, me.shipyard.position)))
		
       	
	
       		
		            

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.

#	if game.turn_number <= 32 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
#		command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
	game.end_turn(command_queue)

