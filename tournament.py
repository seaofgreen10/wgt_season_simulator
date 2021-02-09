import tinydb
import FINAL_VARS
from game import game
from course import course
import leaderboard
from state_info import state_info
import db_obj
import random

class tournament:

    name = ''
    venue = ''
    date = ''

    weekday_games = []
    sat_games = []
    sun_games = []
    #
    state = state_info()

    #leaderboard = leaderboard()

    # init method or constructor
    def __init__(self, p_name='', p_venue=''):
        ## DEBUG: remove
        self.get_cut_line()
        return

        if p_name == '':
            # load any in-progress tournament
            self._get_existing_tournament_from_db()
        else:
            # new tournament
            self.name = p_name
            self.venue = p_venue

    def start_new_tournament(self):
        self.save_tournament_info()
        self._setup_entries()
        self._setup_leaderboard()

    def save_tournament_info(self):
        ''' save off name, venue if first time
            update curr state, weekend states, day '''
        if self.state.curr_state == 0:
            # haven't started yet, create new entry
            insert_dict = { 'name': self.name,
                            'venue': self.venue,
                            'date': self.date,
                            'day': self.state.day,
                            'curr_state' : self.state.curr_state,
                            'weekend_states' : self.state.weekend_states}

            print("Creating new tournament: " + str(insert_dict))
            db_obj.tournament_db.insert(insert_dict)


    ''' helper methods for setting up pairings'''
    def _setup_entries(self):
        ''' load entry list and split into games. for now this will just be roster db
            possiblie enhancement for roster size > tournament size, but future work '''
        roster_list = db_obj.roster_db.all()
        random.shuffle(roster_list)

        self._split_list_to_pairings(roster_list, self.weekday_games)

        self._print_game_list(0) #0 for thurs


    '''functions to set up pairings for weekday and weekend'''
    def _split_list_to_pairings(self, p_list, p_game_list):
        '''p_list: full list to split up
           p_game_list: output list of pairings
           func: split full list into pairings'''
        golfers = []
        for g in p_list:
            if (len(golfers) % 2) == 0:
                # clear out previous golfers
                golfers.clear()
                # add first golfer to game
                golfers.append(g)

            else:
                # add second golfer
                golfers.append(g)
                # add game to tournament list
                p_game_list.append(game(list(golfers)))

    def _setup_weekend_pairings(self, p_day):
        '''use only golfers who made the cut to setup pairings, output in the given day'''
        # get leaderboard where made cut
        made_cut = db_obj.leaderboard_db.search(db_obj.Leaderboard.cut == "n")
        print(made_cut)

        # sort
        made_cut.sort(key=lambda x: x['score_to_par'])

        print(made_cut)

        # split into pairings
        if p_day == 2:
            self._split_list_to_pairings(made_cut, self.sat_games)
            print(*self.sat_games, sep='\n')
        else:
            self._split_list_to_pairings(made_cut, self.sun_games)
            print(*self.sun_games, sep='\n')







    def _print_game_list(self, p_day):
        '''info function, prints out list of games.
            # TODO: change to print to file or display'''
        if(p_day < 2):
            self._print_game_list_helper(self.weekday_games)
        elif(p_day == 2):
            self._print_game_list_helper(self.sat_games)
        else:
            self._print_game_list_helper(self.sun_games)


    def _print_game_list_helper(self, p_game_list):
        ''' helper for above function'''
        for g in p_game_list:
            print("Game {}: {}, {}".format(p_game_list.index(g),
                g.golfers[0]['name'], g.golfers[1]['name']))





    def _get_existing_tournament_from_db(self):
        ''' called if we are in the middle of a tournament. get meta data for it'''
        tournament_info = db_obj.tournament_db.all()[0]
        if tournament_info is not None:
            self.name = tournament_info['name']
            self.venue = tournament_info['venue']
            self.date = tournament_info['date']
            self.state.day = tournament_info['day']
            self.state.curr_state = tournament_info['curr_state']
            self.state.weekend_states = tournament_info['weekend_states']
        else:
            print("""Error:tournament _get_existing_tournament_from_db:
                Tournament {} not found in tournament json""".format(self.name))





    '''leaderboard functions'''

    def _setup_leaderboard(self):
        ''' initial step to copy games to full leaderboard list '''
        # from wd game list, add entries for all
        for game in self.weekday_games:
            for golfer in game.golfers:
                insert_dict = { 'name': golfer['name'],
                                'id': golfer['id'],
                                'score_to_par': 0,
                                'thru': 0,
                                'cut': 'n'}
                db_obj.leaderboard_db.insert(insert_dict)









    def make_cuts(self):
        ''' calls helper function to calculate cut line, then uses tinydb to update
        made_cut field in db. will reference this when setting up pairings, so
        no need to return anything '''
        cut_line = self.get_cut_line()

        # sel from db_obj.leaderboard_db where score_to_par <= cut_line
        #db.obj.
        db_obj.leaderboard_db.update({'cut': 'y'}, db_obj.Leaderboard.score_to_par > cut_line)


    def get_cut_line(self):
        '''cut is top 65 and anyone within 10 leader. calculate and return as int'''
        # load leaderboard
        lb = db_obj.leaderboard_db.all()

        # sort by score
        lb.sort(key=lambda x: x['score_to_par'])

        # first cut is score of #65
        cut_line = lb[64].score_to_par
        return cut_line



    def finish_tournament(self):
        # rename leaderboard json using name/date/venue
        print('placeholder')
