import tournament
import roster
import course

def main():
	print('Hello World')



	# ask user input (stats or tourney)

	# if get stats, call get historical

	# if progress tourney, call tourney obj

		#if tournament in progress, get tournament
		tourney = get_current_tourney()

		#else new tournament
		i_course_str = #TODO get string input
		i_name = #TODO get name
		venue = get_course(i_course_str)
		tourney = new tournament(i_name, venue)

if __name__ = "__main__":
	main()
