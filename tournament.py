import tinydb
import FINAL_VARS
from game import game
from course import course
from state_info import state_info
import db_obj
import random
import simulator as sim

class tournament:

    name = ''
    venue = ''
    date = ''

    weekday_games = []
    sat_games = []
    sun_games = []
    #
    state = state_info()
    global course

    #leaderboard = leaderboard()

    # init method or constructor
    def __init__(self, p_name='', p_venue=''):

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

            self.course = course(venue)

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
            self.course = course(self.venue)
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
        cut_line = self._get_cut_line()

        # sel from db_obj.leaderboard_db where score_to_par <= cut_line
        #db.obj.
        db_obj.leaderboard_db.update({'cut': 'y'}, db_obj.Leaderboard.score_to_par > cut_line)


    def _get_cut_line(self):
        '''cut is top 65. calculate and return as int'''
        # load leaderboard
        lb = db_obj.leaderboard_db.all()

        # sort by score
        lb.sort(key=lambda x: x['score_to_par'])

        # first cut is score of #65
        cut_line = lb[64].score_to_par
        return cut_line


    ''' Functions for progressing through a tournament, to be called by runner'''
    def step_weekday_rounds(self):
        for game in self.weekday_games:
            for golfer in game.golfers:
                for hole in range(18):
                    #TODO: SIM HOLES, fix this call once flushed out
                    _play_hole()

        # increment Day
        self.state.increment_day()

    def step_weekend_rounds(self):
        # determine the correct game list based on day
        game_list = self.sat_games if self.state.day == 2 else self.sun_games
        games_on_course = []

        for game in game_list:
            # total_steps is (total_pairings + 17?)
            total_steps = len(game_list) + 17

            # for step in total_steps:
            for step in range(total_steps):

                # add new game if needed
                if (step < len(game_list)):
                    # still adding, games_on_course.add(game_list[step])
                    games_on_course.append(game_list[step])

                # sim one hole for everybody on the course
                for game in games_on_course:
                    for golfer in game.golfers:
                        # play one hole TODO: update this call? who owns sim logic
                        sim.simulate_one_hole(golfer, self.course.handicaps[golfer.thru])

                    # print info? leaderboard

                    # wait for keyboard input to continue TODO add user score input
                    input("Press Enter to continue")

                # remove finished game if needed
                if (step >= 18):
                    games_on_course.pop(0)




    def adm_before_weekend_rounds(self, b_make_cuts):
        '''make cuts (if parameter is true) and reorder pairings for weekend'''
        if b_make_cuts:
            self.make_cuts()

        self._setup_weekend_pairings()


    def finish_tournament(self):
        # rename leaderboard json using name/date/venue
        print('placeholder')
