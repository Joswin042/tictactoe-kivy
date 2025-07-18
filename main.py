from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import random

Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)

        layout.add_widget(Label(text="Tic Tac Toe", font_size='40sp', bold=True, color=(1, 1, 1, 1), size_hint=(1, 0.3)))

        pvp_btn = Button(text="Player vs Player", size_hint=(1, 0.2), background_color=(0.2, 0.2, 0.2, 1))
        pvp_btn.bind(on_press=self.start_pvp)
        layout.add_widget(pvp_btn)

        ai_btn = Button(text="Player vs AI", size_hint=(1, 0.2), background_color=(0.2, 0.2, 0.2, 1))
        ai_btn.bind(on_press=self.select_difficulty)
        layout.add_widget(ai_btn)

        self.add_widget(layout)

    def start_pvp(self, instance):
        self.manager.get_screen('game').game_mode = 'PVP'
        self.manager.get_screen('game').reset_board()
        self.manager.current = 'game'

    def select_difficulty(self, instance):
        self.manager.current = 'difficulty'


class DifficultyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)

        layout.add_widget(Label(text="Select Difficulty", font_size='30sp', color=(1, 1, 1, 1), size_hint=(1, 0.3)))

        for level in ['Easy', 'Medium', 'Hard']:
            btn = Button(text=level, size_hint=(1, 0.2), background_color=(0.3, 0.3, 0.3, 1))
            btn.bind(on_press=self.set_difficulty)
            layout.add_widget(btn)

        self.add_widget(layout)

    def set_difficulty(self, instance):
        self.manager.get_screen('game').game_mode = 'AI'
        self.manager.get_screen('game').difficulty = instance.text
        self.manager.get_screen('game').reset_board()
        self.manager.current = 'game'


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_mode = 'AI'
        self.difficulty = 'Easy'
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = []
        self.user1_wins = 0
        self.user2_wins = 0
        self.draws = 0

        self.root_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.status_label = Label(text="", font_size='20sp', color=(1, 1, 1, 1), size_hint=(1, 0.2))
        self.root_layout.add_widget(self.status_label)

        self.grid = GridLayout(cols=3, spacing=5, size_hint=(1, 0.7))
        for i in range(3):
            row = []
            for j in range(3):
                btn = Button(font_size='40sp', background_color=(0.15, 0.15, 0.15, 1))
                btn.bind(on_press=self.make_move)
                row.append(btn)
                self.grid.add_widget(btn)
            self.buttons.append(row)

        self.root_layout.add_widget(self.grid)

        self.result_label = Label(text="", font_size='18sp', color=(0.8, 0.8, 0.8, 1), size_hint=(1, 0.1))
        self.root_layout.add_widget(self.result_label)

        restart_btn = Button(text="Main Menu", size_hint=(1, 0.1), background_color=(0.3, 0.3, 0.3, 1))
        restart_btn.bind(on_press=self.return_to_menu)
        self.root_layout.add_widget(restart_btn)

        self.add_widget(self.root_layout)

    def reset_board(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.status_label.text = f"{self.current_player}'s Turn"
        self.result_label.text = ""
        for row in self.buttons:
            for btn in row:
                btn.text = ""
                btn.disabled = False
        if self.game_mode == 'AI' and self.current_player == 'O':
            self.ai_move()

    def make_move(self, instance):
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j] == instance and self.board[i][j] == '':
                    self.board[i][j] = self.current_player
                    self.buttons[i][j].text = self.current_player
                    if self.check_winner(self.current_player):
                        self.result_label.text = f"{self.current_player} wins!"
                        self.update_score(self.current_player)
                        self.disable_all()
                    elif self.is_draw():
                        self.result_label.text = "It's a draw!"
                        self.draws += 1
                        self.disable_all()
                    else:
                        self.current_player = 'O' if self.current_player == 'X' else 'X'
                        self.status_label.text = f"{self.current_player}'s Turn"
                        if self.game_mode == 'AI' and self.current_player == 'O':
                            self.ai_move()
                    return

    def ai_move(self):
        if self.difficulty == 'Easy':
            empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']
            i, j = random.choice(empty)
        elif self.difficulty == 'Medium':
            for sym in ['O', 'X']:
                for i in range(3):
                    for j in range(3):
                        if self.board[i][j] == '':
                            self.board[i][j] = sym
                            if self.check_winner(sym):
                                self.board[i][j] = ''
                                return self.make_move(self.buttons[i][j])
                            self.board[i][j] = ''
            empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']
            i, j = random.choice(empty)
        else:
            _, move = self.minimax(True)
            i, j = move

        self.board[i][j] = 'O'
        self.buttons[i][j].text = 'O'
        if self.check_winner('O'):
            self.result_label.text = "O wins!"
            self.update_score('O')
            self.disable_all()
        elif self.is_draw():
            self.result_label.text = "It's a draw!"
            self.draws += 1
            self.disable_all()
        else:
            self.current_player = 'X'
            self.status_label.text = "X's Turn"

    def minimax(self, is_ai):
        winner = self.get_winner()
        if winner == 'O':
            return 1, None
        elif winner == 'X':
            return -1, None
        elif self.is_draw():
            return 0, None

        best = (-2, None) if is_ai else (2, None)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = 'O' if is_ai else 'X'
                    score, _ = self.minimax(not is_ai)
                    self.board[i][j] = ''
                    score = -score
                    if (is_ai and score > best[0]) or (not is_ai and score < best[0]):
                        best = (score, (i, j))
        return best

    def get_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        return None

    def is_draw(self):
        return all(self.board[i][j] != '' for i in range(3) for j in range(3))

    def disable_all(self):
        for row in self.buttons:
            for btn in row:
                btn.disabled = True

    def update_score(self, winner):
        if winner == 'X':
            self.user1_wins += 1
        else:
            self.user2_wins += 1

    def return_to_menu(self, instance):
        self.manager.current = 'menu'


class TicTacToeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(DifficultyScreen(name='difficulty'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    TicTacToeApp().run()
