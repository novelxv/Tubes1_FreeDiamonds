from typing import Tuple, Optional
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, position_equals
import random

class FreeDiamonds(BaseLogic):
    def __init__(self):
        # Inisisalisasi atribut yang diperlukan
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def distance(self, bot_position: Position, goal: Position):
        """ Menghitung jarak antara bot dan goal position """
        distance = abs(goal.x - bot_position.x) + abs(goal.y - bot_position.y)
        return distance # tipe data int
    
    def teleport(self, bot_position: Position, board: Board, goal_position: Position):
        """ Mencari jarak terpendek dari bot ke goal position dengan mempertimbangkan teleporter """
        list_teleporter = [i for i in board.game_objects if i.type == "TeleportGameObject"]
        # Membandingkan jarak tanpa melewati teleporter
        distance = self.distance(bot_position, goal_position)
        # Membandingkan jarak jika melewati teleporter 1 dan 2
        # Dari teleporter 1 ke teleporter 2
        in_teleporter1 = self.distance(bot_position, list_teleporter[0].position)
        out_teleporter1 = self.distance(list_teleporter[1].position, goal_position)
        distance1 = in_teleporter1 + out_teleporter1
        # Dari teleporter 2 ke teleporter 1
        in_teleporter2 = self.distance(bot_position, list_teleporter[1].position)
        out_teleporter2 = self.distance(list_teleporter[0].position, goal_position)
        distance2 = in_teleporter2 + out_teleporter2
        
        choosen = min(distance, distance1, distance2) 
        if (choosen == distance1):
            # Masuk ke teleporter 1
            return list_teleporter[0].position
        elif (choosen == distance2):
            # Masuk ke teleporter 2
            return list_teleporter[1].position
        else: # Tidak melewati teleporter
            return goal_position # tipe data Position

    def highest_density(self, bot_position: Position, list_diamonds: list):
        """ Mencari diamond dengan density tertinggi """
        highest_density = 0
        highest_density_position = None

        for diamond in list_diamonds:
            distance = self.distance(bot_position, diamond.position)
            point = diamond.properties.points
            density = point / distance
            if density > highest_density:
                highest_density = density
                highest_density_position = diamond.position
        return highest_density_position # tipe data Position
    
    def is_tackle(self, board_bot: GameObject, bot_position: Position, board: Board):
        """ Mengecek apakah ada musuh yang bisa di-tackle """
        enemy = [i for i in board.bots if (i.position != bot_position)]
        move = [-99, -99]
        for target in enemy:
            if ((target.properties.diamonds > 0) and (board_bot.properties.diamonds < board_bot.properties.inventory_size) and (board_bot.properties.milliseconds_left < target.properties.milliseconds_left)):
                # Jika musuh memiliki diamond, bot belum penuh, dan waktu bot lebih sedikit
                if (bot_position.x == target.position.x) and (abs(bot_position.y - target.position.y) == 1):
                    # Jika musuh ada di atas atau bawah bot
                    move = [0, target.position.y - bot_position.y]
                elif (bot_position.y == target.position.y) and (abs(bot_position.x - target.position.x) == 1):
                    # Jika musuh ada di kiri atau kanan bot
                    move = [target.position.x - bot_position.x, 0]
        return move # tipe data tuple
    
    def push_red_button(self, bot_position:Position, highest_density_position:Position, board: Board):
        """ Memilih antara red button atau diamond dengan density tertinggi berdasarkan jarak terdekat """
        list_red_button = [i for i in board.game_objects if i.type == "DiamondButtonGameObject"]
        print(list_red_button) # debug
        diamond_distance = self.distance(bot_position, highest_density_position)
        for button in list_red_button:
            button_distance = self.distance(bot_position, button.position)
            if (button_distance < diamond_distance):
                print("go to red button") # debug
                return button.position # tipe data Position
            else:
                print("go to diamond") # debug
                return highest_density_position # tipe data Position 

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        inventory_size = board_bot.properties.inventory_size if board_bot.properties.inventory_size else 5 # default 5
        bot_position = board_bot.position
        list_diamonds = board.diamonds
        collected = board_bot.properties.diamonds
        tackle_check = self.is_tackle(board_bot, bot_position, board)
        base_position = board_bot.properties.base
        milliseconds_left = board_bot.properties.milliseconds_left if board_bot.properties.milliseconds_left else 0
        seconds_left = milliseconds_left / 1000

        list_teleporter = self.teleport(bot_position, board, base_position)
        print("TELEPORTERS: ", list_teleporter) # debug

        distance_to_base = self.distance(bot_position, base_position)

        if (collected == inventory_size):
            # Jika inventory penuh, kembali ke base
            self.goal_position = base_position
            print("FULL, AYO KE BASE") # debug
        elif (tackle_check[0] != -99):
            # Jika ada musuh yang bisa di-tackle, lakukan tackle
            delta_x = tackle_check[0]
            delta_y = tackle_check[1]
            print("TACKLE: ", delta_x, delta_y) # debug
        else:
            highest_density_position = self.highest_density(bot_position, list_diamonds)
            if (seconds_left - 2 <= distance_to_base and collected > 0):
                # Jika waktu tersisa dalam detik kurang lebih sama dengan jarak ke base, kembali ke base
                if (not position_equals(bot_position, base_position) and not position_equals(bot_position, list_teleporter)):  
                    self.goal_position = base_position
            elif (len(list_diamonds) <= 7):
                # Jika diamond kurang dari 7, pilih antara red button atau diamond dengan density tertinggi
                self.goal_position = self.push_red_button(bot_position, highest_density_position, board)
            # elif (collected == 4 and highest_density_position.properties.points == 2):
            #     self.goal_position = base_position # delete
            else:
                # Ke diamond dengan density tertinggi
                self.goal_position = highest_density_position
        
        if self.goal_position:
            # Jika ada goal position, cek apakah teleporter perlu digunakan
            self.goal_position = self.teleport(bot_position, board, self.goal_position)
            delta_x, delta_y = get_direction(
                bot_position.x,
                bot_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            # Jika tidak ada goal position, gerakan random
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )

        if (delta_x == delta_y):
            # Menghindari invalid move
            delta_x = 0
            delta_y = 1

        return delta_x, delta_y