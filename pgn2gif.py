#!/usr/bin/env python3

# Plot a PGN game using python-chess and ImageMagick

import os
import sys
import getopt
import chess.pgn
import chess.svg

def generate_png(board, i):
	lm = board.peek()
	a = [(lm.from_square, lm.to_square)]
	s = chess.svg.board(board, arrows = a)

	f1 = "g_%04u.svg" % i
	f2 = "g_%04u.png" % i

	with open(f1, 'w') as f:
		f.write(s)
	os.system("convert -density 400 %s %s" % (f1, f2))
	os.system("rm %s" % f1)

def get_path_from_args(arguments):
	help_message = '-----\nUSAGE\n-----\nchess_analysis.py [-h] [--help] [-p <pgn-path>] [--pgn <pgn-path>]'
	try:
		opts, args = getopt.getopt(arguments,'hp:',['help','pgn='])
	except getopt.GetoptError:
		print(help_message)
		sys.exit(2)

	for opt, arg in opts:
		if opt in ('-h', '--help'):
			print(help_message)
			sys.exit(2)
		elif opt in ("-p", "--pgn"):
			return arg
	
	single_arg = ''
	if args:
		single_arg = args[0]
	if single_arg and not single_arg.isspace():
		return single_arg

	print("No valid arguments could be found")
	print(help_message)
	sys.exit(2)

def main(argv):
	pgn_path = get_path_from_args(argv)
	print("Generating GIF for PGN - " + pgn_path)

	pgn = open(pgn_path)
	game = chess.pgn.read_game(pgn)
	board = game.board()
	i = 1

	for m in game.mainline_moves():
		board.push(m)
		generate_png(board, i)
		if i > 1:
			break
		i += 1

	# duplicate last frame 3 more times for pause animation at the end:
	#for j in range(3):
		#generate_png(i)
		#i += 1

	# convert pgns to gif
	os.system("convert -delay 150 g_*.png -loop 0 g.gif")
	os.system("rm -f g_*.png")
	print("GIF has been generated successfully")

if __name__ == "__main__":
	main(sys.argv[1:])