import math

class state_info:

    day = 0 #th=0, fri=1, sat=2, sun=3
    weekend_states = 0
    curr_state = 0

    def calculate_states(self, p_num_made_cut):
        # 18 + (x/2-1) where x=golfers made cut
        self.weekend_states = 18 + math.ceil(p_num_made_cut/2) - 1

    
