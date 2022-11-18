import numpy as np
from time import sleep
from sys import exit as sys_exit
from os import system

class OccupationError(Exception): ...
class CommandError(Exception): ...
class RestartError(Exception): ...

class Game():

    '''
    Console 3x3 tic-tac-toe game
    For detailed help type help
    '''

    def __init__(self):
        self.field = np.zeros((3, 3), dtype=str)

    def __repr__(self):
        return '\n'.join(str(x) for x in self.field)

    def _check_win(self) -> str:
        for symbol in ('O', 'X'):
            for _ in range(3):
                if (all((self.field == symbol)[_]) or
                    all(np.rot90((self.field == symbol))[_]) or
                    all(np.diag((self.field == symbol))) or
                    all(np.diag(np.rot90((self.field == symbol))))):
                    return f'{symbol} won!'
        if all(((self.field == 'O') | (self.field == 'X')).flatten()):
                return 'Draw'
        return ''

    def _cmd_input(self):
        try:
            match input().lower():
                case 'play':
                    system('cls')
                    return self.play_game()
                case 'restart':
                    return self.restart_game()
                case 'check':
                    return self.check_field()
                case 'help':
                    system('cls')
                    return self.get_help()
                case 'exit':
                    return self.exit()
                case _:
                    raise CommandError
        except CommandError:
            print('Unknown command')
            return self._cmd_input()
        except KeyboardInterrupt:
            system('cls')
            return self.open_menu()

    def play_game(self):
        if self._check_win():
            self.field = np.zeros((3, 3), dtype=str)
        turn = 1
        print(self)
        while 1:
            if result := self._check_win():
                print(result)
                sleep(2)
                system('cls')
                return self.open_menu()
            try:
                x, y = int(input('x = ')), int(input('y = '))
                if self.field[x-1][y-1] in ('O', 'X'):
                    raise OccupationError
                self.field[x-1][y-1] = 'O' if turn else 'X'
                turn = not turn
                system('cls')
                print(self)
            except IndexError:
                print('X and Y must be between [1, 3]')
            except ValueError:
                print('X and Y must be integers')
            except OccupationError:
                print('This cell is occupied')
            except KeyboardInterrupt:
                system('cls')
                return self.open_menu()

    def restart_game(self):
        try:
            if len(np.unique(self.field)) == 1:
                raise RestartError
            self.field = np.zeros((3, 3), dtype=str)
            print('Succesfully restarted')
        except RestartError:
            print('Already restarted')
        finally:
            return self._cmd_input()

    def check_field(self):
        print(self)
        return self._cmd_input()

    def get_help(self):
        print('''
    When game starts, field 3x3 will appear.
    At player's turn, player should enter (x, y) coordinates to place 'X' or 'O' in cell in (x, y), where
    X - row number;
    Y - column number.
    Player wins, when any row, column or diagonal is fulfilled by his specific symbol (X or O).
    Note: all commands are not case sensitive.
              ''')
        return self._cmd_input()

    def exit(self):
        sys_exit()

    def open_menu(self):
        print('''
    Type:
    1. 'Play' to play or continue playing the last game
    2. 'Restart' to restart the game 
    3. 'Check' to check the last game field
    4. 'Help' for detailed help
    5. 'Exit' to exit
    You can use the Ctrl + C combination to return to the menu at any moment. (Unfinished game will be saved)
              ''')
        return self._cmd_input()

if __name__ == "__main__":
    game = Game()
    game.open_menu()