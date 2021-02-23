import tinydb
import db_obj


"""Simulates one hole for one golfer

Args:
    golfer (golfer): the golfer playing the hole
    handicap (int): the handicap of the current hole
    par (int): the par of the current hole

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



"""Algorithm to calculate score on a hole

Args:
    rating (int): the golfer's rating
    handicap (int): the handicap of the current hole
    par (int): the par of the current hole

Returns:
    the calculated score for this hole
"""
def _algorithm(p_rating, p_hc, p_par):
    # math

    return score
