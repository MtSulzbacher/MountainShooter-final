import sys
from datetime import datetime

import pygame
from pygame import Surface, Rect, KEYDOWN, K_RETURN, K_BACKSPACE, K_ESCAPE
from pygame.font import Font

from code.Const import C_YELLOW, SCORE_POS, MENU_OPTION, C_WHITE
from code.DBProxy import DBProxy

class Score:
    def __init__(self, window: Surface):
        self.window = window
        self.surf = pygame.image.load('./asset/ScoreBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def save(self, game_mode: str, player_score: list[int]):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy('DBScore')
        name1 = ''
        name2 = ''
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.score_text(48, 'YOU WIN!!', C_YELLOW, SCORE_POS['Title'])

            if game_mode == MENU_OPTION[0]:  # Single player
                score = player_score[0]
                text = 'Enter Player 1 name (4 characters):'
                self.score_text(20, text, C_WHITE, SCORE_POS['EnterName'])

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_RETURN and len(name1) == 4:
                            db_proxy.save({'name': name1, 'score': score, 'date': get_formatted_date()})
                            self.show()
                            return
                        elif event.key == K_BACKSPACE:
                            name1 = name1[:-1]
                        else:
                            if len(name1) < 4:
                                name1 += event.unicode

                self.score_text(20, name1, C_WHITE, SCORE_POS['Name'])

            elif game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:  # Cooperative or Competitive
                if not name1:
                    score = player_score[0]
                    text = 'Enter Player 1 name (4 characters):'
                    self.score_text(20, text, C_WHITE, SCORE_POS['EnterName'])

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == KEYDOWN:
                            if event.key == K_RETURN and len(name1) == 4:
                                continue  # Move to Player 2 name input
                            elif event.key == K_BACKSPACE:
                                name1 = name1[:-1]
                            else:
                                if len(name1) < 4:
                                    name1 += event.unicode

                    self.score_text(20, name1, C_WHITE, SCORE_POS['Name'])
                
                else:  # Enter Player 2 name
                    score = player_score[1]
                    text = 'Enter Player 2 name (4 characters):'
                    self.score_text(20, text, C_WHITE, SCORE_POS['EnterName'])

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == KEYDOWN:
                            if event.key == K_RETURN and len(name2) == 4:
                                db_proxy.save({'name': name1, 'score': player_score[0], 'date': get_formatted_date()})
                                db_proxy.save({'name': name2, 'score': player_score[1], 'date': get_formatted_date()})
                                self.show()
                                return
                            elif event.key == K_BACKSPACE:
                                name2 = name2[:-1]
                            else:
                                if len(name2) < 4:
                                    name2 += event.unicode

                    self.score_text(20, name2, C_WHITE, SCORE_POS['Name'])

            pygame.display.flip()

    def show(self):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.play(-1)
        self.window.blit(source=self.surf, dest=self.rect)
        self.score_text(48, 'TOP 10 SCORE', C_YELLOW, SCORE_POS['Title'])
        self.score_text(20, 'NAME     SCORE           DATE      ', C_YELLOW, SCORE_POS['Label'])
        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for player_score in list_score:
            id_, name, score, date = player_score
            self.score_text(20, f'{name}     {int(score):05d}     {date}', C_YELLOW,
                            SCORE_POS[list_score.index(player_score)])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            pygame.display.flip()

    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

def get_formatted_date():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M")
    current_date = current_datetime.strftime("%d/%m/%y")
    return f"{current_time} - {current_date}"
