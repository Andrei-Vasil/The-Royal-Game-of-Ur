
from src.domain.validators import MetaException
from src.services.tools import Color


class BoardException(MetaException):
    pass


class Board:
    def __init__(self, pieces):
        """
        :param pieces: pieces repository that is also assigned to game_controller
        """
        self.__pieces = pieces

    @property
    def max_index(self) -> int:
        """
        :return: the maximum index any piece has (most usually 7, in the case of the classic game)
        """
        max_index = 0
        for piece in self.__pieces.get_all():
            max_index = max(max_index, piece.index)
        return max_index

    def get_offset_for_piece(self, piece_id) -> (int, int):
        """
        This helps the gui place each piece where it is supposed to be placed.
        E.g.: (0, 0) - on top of the first row, first column (spawn of the first piece of the first player)
              (3, 2) - the safe spot
              (8, 3) - end location of the first piece of the second player
        :param piece_id: The piece id for which you want to get the offset.
        :return: A tuple (imaginary number, one might say) of two integers: (column, row).
        """
        piece = self.__pieces.find_by_id(piece_id)
        piece_location = piece.location
        index = piece.index
        player = piece.owner

        return Board.get_offset(piece_location, index, player)

    @staticmethod
    def get_offset(piece_location, index, player) -> (int, int):
        """
        This helps the gui place each piece / piece selector where it is supposed to be placed.
        E.g.: (0, 0) - on top of the first row, first column (spawn of the first piece of the first player)
              (3, 2) - the safe spot
              (8, 3) - end location of the first piece of the second player
        :param piece_location: the location of the piece you want to get the offset for
        :param index: the index of the piece (ranging from 1 to max_index)
        :param player: can either be "player1" or "player2"
        :return: A tuple (imaginary number, one might say) of two integers: (column, row).
        """
        if piece_location == 0:
            row = 0
            if player == "player2":
                row = 4
            offset = (index - 1, row)
        elif piece_location == 15:
            row = 1
            if player == "player2":
                row = 3
            offset = (7 + index, row)
        elif 1 <= piece_location <= 4 or 13 <= piece_location <= 14:
            if 1 <= piece_location <= 4:
                column = 4 - piece_location
            else:
                column = 20 - piece_location
            row = 1
            if player == "player2":
                row = 3
            offset = (column, row)
        elif 5 <= piece_location <= 12:
            offset = (piece_location - 5, 2)
        else:
            raise BoardException("Invalid piece location given!")
        return offset

    def __build_the_board(self) -> None:
        """
            This method build the entire board in a string format, for the console to use later.
        """
        self.__the_board_string_format = ""
        self.__the_board_string_format += self.__get_spawn_pieces_for_player(2) + "\n"
        for sector in range(3):
            for i in range(3):
                if i % 2 == 0:
                    group = "--- "
                else:
                    group = "| | "
                if sector == 0 or sector == 2:
                    self.__build_gap_row(group, sector)
                else:
                    self.__build_full_row(group, sector)
        self.__the_board_string_format += self.__get_spawn_pieces_for_player(1) + "\n"

    def __build_gap_row(self, group, sector) -> None:
        """
        Gap row is either first row or third row.
        :param group: either "--- " or "| | ", indicating it is either a border, or a spot where a piece might stand.
        :param sector: the row
        """
        for i in range(4):
            aux = group
            if self.__there_should_be_a_piece_here(group, sector, 4 - i):
                group = self.__put_a_piece_here()
            if i == 0:
                self.__the_board_string_format += Color.YELLOW + group + Color.END + Color.BOLD
            else:
                self.__the_board_string_format += group
            group = aux

        for _ in range(2):
            self.__the_board_string_format += "    "

        for i in range(2):
            aux = group
            if self.__there_should_be_a_piece_here(group, sector, 2 - i + 12):
                group = self.__put_a_piece_here()
            if i == 0:
                self.__the_board_string_format += Color.YELLOW + group + Color.END + Color.BOLD
            else:
                self.__the_board_string_format += group
            group = aux
        if sector == 0 and group == "| | ":
            self.__the_board_string_format += self.__get_end_pieces_for_player(2)
        elif sector == 2 and group == "| | ":
            self.__the_board_string_format += self.__get_end_pieces_for_player(1)
        self.__the_board_string_format += "\n"

    def __build_full_row(self, group, sector) -> None:
        """
        Full row is either second row.
        :param group: either "--- " or "| | ", indicating it is either a border, or a spot where a piece might stand.
        :param sector: the row
        """
        for i in range(8):
            aux = group
            if self.__there_should_be_a_piece_here(group, sector, i + 5):
                group = self.__put_a_piece_here()
            if i == 3:
                self.__the_board_string_format += Color.YELLOW + group + Color.END + Color.BOLD
            else:
                self.__the_board_string_format += group
            group = aux
        self.__the_board_string_format += "\n"

    def __there_should_be_a_piece_here(self, group, sector, index) -> bool:
        """
        Should there be a piece on that sector, in that group, on that index?
        :param group: either "--- " or "| | ", indicating it is either a border, or a spot where a piece might stand.
        :param sector: the row
        :param index: index of the square. Ranges between 0 and 15
        :return: True if there should be a piece here, False otherwise
        """
        if not group == "| | ":
            return False
        if sector == 0:  # safezone for player 2
            return self.__check_if_player2_has_pieces_here(index)
        elif sector == 2:  # safezone for player 1
            return self.__check_if_player1_has_pieces_here(index)
        else:  # warzone
            return self.__check_if_player1_has_pieces_here(index) or self.__check_if_player2_has_pieces_here(index)

    def __check_if_player1_has_pieces_here(self, index) -> bool:
        """
        :param index: index of the square. Ranges between 0 and 15
        :return: True if player1 has pieces here, False otherwise
        """
        for piece in self.__pieces.get_all():
            if piece.location == index and piece.owner == "player1":
                self.__player_who_has_a_piece_here = "player1"
                self.__piece_index = piece.id.split("_")[1]
                return True
        return False

    def __check_if_player2_has_pieces_here(self, index) -> bool:
        """
        :param index: index of the square. Ranges between 0 and 15
        :return: True if player1 has pieces here, False otherwise
        """
        for piece in self.__pieces.get_all():
            if piece.location == index and piece.owner == "player2":
                self.__player_who_has_a_piece_here = "player2"
                self.__piece_index = piece.id.split("_")[1]
                return True
        return False

    def __put_a_piece_here(self) -> str:
        """
        :return: an index (red or blue) between two bars. E.g.: "|1| "
        """
        piece = ""
        if self.__player_who_has_a_piece_here == "player1":
            piece = Color.BLUE + str(self.__piece_index) + Color.END + Color.BOLD
        elif self.__player_who_has_a_piece_here == "player2":
            piece = Color.RED + str(self.__piece_index) + Color.END + Color.BOLD
        return "|" + piece + "| "

    def __get_spawn_pieces_for_player(self, player_number) -> str:
        """
        :param player_number: 1 or 2
        :return: the pieces (string: "1 2 3 ...") that are still on spawn squares
        """
        spawn_pieces = " "
        piece_color = Color.BLUE
        if player_number == 2:
            piece_color = Color.RED
        for piece in self.__pieces.get_all():
            if piece.state == "spawn" and piece.id.split("_")[0] == "player" + str(player_number):
                spawn_pieces += Color.END + Color.BOLD + piece_color + " " + str(piece.index) + " " + Color.END + \
                                Color.BOLD
        return spawn_pieces

    def __get_end_pieces_for_player(self, player_number) -> str:
        """
        :param player_number: 1 or 2
        :return: the pieces (string: "1 2 3 ...") that are still on end squares
        """
        end_pieces = " "
        piece_color = Color.BLUE
        if player_number == 2:
            piece_color = Color.RED
        for piece in self.__pieces.get_all():
            if piece.state == "finish" and piece.id.split("_")[0] == "player" + str(player_number):
                end_pieces += Color.END + Color.BOLD + piece_color + " " + str(piece.index) + " " + Color.END + \
                              Color.BOLD
        return end_pieces

    def __str__(self):
        """
        :return: string format of the board, used by the console to print it out.
        """
        self.__build_the_board()
        return self.__the_board_string_format
