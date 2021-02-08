import tinydb
import FINAL_VARS
import random
import db_obj


class golfer:
    #indexing id
    player_id = random.randint(0, 999999999999)
    #skill rating for sim
    rating = 0

    #todo not sure if we need raw totals
    scores = []
    score_to_par = 0
    thru = 0

    owgr_points = 0
    finishes = []

    def __init__(self, p_name, p_create=False, p_rating=0):
        '''lookup or create a new golfer
           p_name: golfers name 'first last'
           p_create: true=create new, false=lookup existing
           p_rating: if creating new, set rating to this'''
        self.name = p_name
        if p_create:
            self.rating = p_rating
            self._export_new_golfer()
        else:
            self._lookup_golfer()


    def _export_new_golfer(self):
        '''save off this golfer and relevant data to db'''
        insert_dict = {'name': self.name, 'rating': self.rating, 'owgr_points': 0, 'finishes': [], 'id': self.player_id }
        print("Adding golfer: " + str(insert_dict))
        db_obj.roster_db.insert(insert_dict)


    def _lookup_golfer(self):
        '''look up golfer from db and populate this object with correct info '''
        golfer_info_r = db_obj.roster_db.get(db_obj.Roster.name == self.name)



        if golfer_info_r is not None:
            self.rating = golfer_info_r['rating']
            self.owgr_points = golfer_info_r['owgr_points']
            self.finishes = golfer_info_r['finishes']
            self.player_id = golfer_info_r['id']

            golfer_info_l = db_obj.leaderboard_db.get(db_obj.Leaderboard.id == self.player_id)
            if golfer_info_l is not None:
                self.score_to_par = golfer_info_l['score_to_par']
                self.thru = golfer_info_l['thru']
            else:
                print("Warning(Error if during tourney):golfer _lookup_golfer: Golfer {} not found in leaderboard json".format(self.name))

        else:
            print("Error:golfer _lookup_golfer: Golfer {} not found in roster json".format(self.name))


    def update_owgr(p_name, p_points):
        db_obj.roster_db.update({'owgr_points': p_points}, db_obj.Roster.name == p_name)

    def update_finishes(p_name, p_finish):
        item = db_obj.roster_db.get(db_obj.Roster.name == p_name)
        item['finishes'].append(p_finish)
        db_obj.roster_db.update({'finishes': item['finishes']}, db_obj.Roster.name == p_name)
