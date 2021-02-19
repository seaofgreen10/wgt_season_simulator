import tinydb
import db_obj


"""
Args:
    golfer: the golfer playing the hole
    handicap: the handicap of the current hole
    par: the par of the current hole

Returns:
    None
"""
def simulate_one_hole(p_golfer, p_hc, p_par):
    # sim logic?
    # needed as param or collected:
    #   golfer rating
    #   golfer current score to par
    #   current hole par
    #   current hole handicap

    #TODO can prob combine these once algo is flsuhed out
    hole_score = _algorith(p_golfer.rating, p_hc, p_par)

    # outputs:
    #   update score to par with sim score
    #   update thru
    # update golfer object in memory
    golfer.thru += 1
    golfer.score_to_par  += hole_score

    # update leaderboard
    db_obj.leaderboard_db.update_multiple([
                                (tinydb.operations.increment('thru'), db_obj.Leaderboard.id == golfer.id),
                                ({'score_to_par' : golfer.score_to_par}, db_obj.Leaderboard.id == golfer.id)
                                ])



"""
Args:
    rating: the golfer's rating
    handicap: the handicap of the current hole
    par: the par of the current hole

Returns:
    the calculated score for this hole
"""
def _algorithm(p_rating, p_hc, p_par):
    # math

    return score
