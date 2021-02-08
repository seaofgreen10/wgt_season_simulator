import tinydb
import FINAL_VARS
import db_obj  

class course:

    name = ''
    handicaps = []


    def __init__(self, p_name, p_handicaps=''):
        '''build a course obj based on course name and optional hc
            leave hc blank to lookup from existing course in json
            include hc for adding new courses
        '''

        self.name = p_name
        if(p_handicaps == ''):
            # if not passed in, try to look it up
            self.handicaps = _lookup_course_handicap()
        else:
            self.handicaps = p_handicaps

    def _lookup_course_handicap(self):
        course_info = db_obj.course_db.get(db_obj.Course.name == self.name)

        if course_info is not None:
            #return course_info['handicaps']
            self.handicaps = course_info['handicaps']
        else:
            print("Error:course _lookup_course_handicap: Course {} not found in json".format(self.name))

    def export_course(self):
        insert_dict = {'name': self.name, 'handicaps': self.handicaps}
        print("Adding course: " + str(insert_dict))
        db_obj.course_db.insert(insert_dict)
