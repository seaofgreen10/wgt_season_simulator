import tinydb
import FINAL_VARS
from course import course
from golfer import golfer
from tournament import tournament
import db_obj
import random




#course_db = tinydb.TinyDB(FINAL_VARS.COURSES_FILE_NAME)
#Course = tinydb.Query()

#debug seed data, #todo debug, remove
#t1 = course_db.insert({'name': 'Pebble Beach', 'handicaps': '[1,3,5,7,9,11,13,15,17,2,4,6,8,10,12,14,16,18]'})
#t2 = course_db.insert({'name': 'Chambers Bay', 'handicaps': '[1,3,5,7,9,11,13,15,17,2,4,6,8,10,12,14,16,18]'})
#{'name': 'Chambers Bay', 'handicaps': '[1,3,5,7,9,11,13,15,17,2,4,6,8,10,12,14,16,18]'})
#{'name': 'Chambers Bay', 'handicaps': '[1, 3, 5, 7, 9, 11, 13, 15, 17, 2, 4, 6, 8, 10, 12, 14, 16, 18]'}
#t3 = db.search(tinydb.where('name')=='Pebble Beach')
#t4 = course_db.get(Course.name == 'Chambers Bay2')




def get_course(p_course_name):
    course_info = course_db.get(Course.name == p_course_name)

    if course_info is not None:
        return course(course_info['name'], course_info['handicaps'])
    else:
        print("Error: Course {} not found in json".format(p_course_name))


#def add_course(p_course_name, p_handicaps):
    #insert_statement = '{\'name\': {}, \'handicaps\': {}}'.format(p_course_name, p_handicaps)
    #course_db.insert(insert_statement)

######COURSE INFO
#cour = get_course('Pebble Beach')
#print("course: {}".format(cour.name))
#hc = [1,3,5,7,9,11,13,15,17,2,4,6,8,10,12,14,16,18]
#p = [4,4,4,3,5,3,4,5,4,4,3,4,4,5,3,5,4,4]
#c = course('gvr', hc, p)
#print("name {}, hc {}".format(c.name, c.handicaps))
#c.export_course()
#add_course('test', hc)

#####GOLFER
# DEBUG: golfer object
# DEBUG: add golfer
#g = golfer('dustin johnson', True, 96)

# # DEBUG: update stats
#golfer.update_owgr('tiger woods', 1)
#golfer.update_finishes('tiger woods', 25)

#####TOURNEY
#t = tournament('co open', 'gvr')
#t.start_new_tournament()


#####LEADERBOARD
#db_obj.leaderboard_db.update_multiple([
#                            (tinydb.operations.increment('thru'), db_obj.Leaderboard.id == 488472945319),
#                            ({'score_to_par' : 2}, db_obj.Leaderboard.id == 488472945319)
#                            ])

#db_obj.leaderboard_db.update(increment('thru'), db_obj.Leaderboard.id == 488472945319)




#####ROSTER
#2/22/21: iterating thru roster to update IDs
#roster_list = db_obj.roster_db.all()
#for g in roster_list:
#    print(g['name'])
#    id = random.randint(0, 999999999999)
#    db_obj.roster_db.update({'id': id}, db_obj.Roster.name == g['name'])
