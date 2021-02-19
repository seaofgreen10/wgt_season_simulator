import tinydb
import FINAL_VARS
import db_obj

class course:

    name = ''
    handicaps = []
    pars = []


    """Build a course obj based on course name and optional hc
    leave hc blank to lookup from existing course in json
    include hc for adding new courses

    Args:
        p_name(str): golf course name
        p_handicaps(int[18]): list of handicaps for each hole
        p_pars(int[18]): list of pars for each hole

    Returns:
        None
    """
    def __init__(self, p_name, p_handicaps='', p_pars=''):
        self.name = p_name
        if(p_handicaps == ''):
            # if not passed in, try to look it up
            _set_course_scorecard_info()
        else:
            self.handicaps = p_handicaps
            self.pars = p_pars

    """Searches for a course in the database and extracts
    the course info into memory

    Attributes:
        course_info: database object for storing the course info

    Returns:
        None
    """
    def _set_course_scorecard_info(self):
        course_info = db_obj.course_db.get(db_obj.Course.name == self.name)

        if course_info is not None:
            # valid course - set handicaps (int[18]) and pars (int[18])
            self.handicaps = course_info['handicaps']
            self.pars = course_info['pars']
        else:
            print("Error:course _set_course_scorecard_info: Course {} not found in json".format(self.name))

    """Saves this course to the database courses.json

    Attributes:
        insert_dict: database object for saving the course info

    Returns:
        None
    """
    def export_course(self):
        insert_dict = {'name': self.name, 'handicaps': self.handicaps, 'pars': self.pars}
        print("Adding course: " + str(insert_dict))
        db_obj.course_db.insert(insert_dict)
