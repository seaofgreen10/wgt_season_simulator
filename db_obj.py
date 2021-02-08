import tinydb
import FINAL_VARS

leaderboard_db = tinydb.TinyDB(FINAL_VARS.LEADERBOARD_FILE_NAME)
Leaderboard = tinydb.Query()

tournament_db = tinydb.TinyDB(FINAL_VARS.TOURNAMENT_FILE_NAME)
Tournament = tinydb.Query()

roster_db = tinydb.TinyDB(FINAL_VARS.ROSTER_FILE_NAME)
Roster = tinydb.Query()
