#!/usr/bin/python
import sys,getopt #to handle arguments in python
def main(argv):# defining the main function, called later
   try:
      opts, args = getopt.getopt(argv,"un:",["file_number=","usage"])
      #getopt takes three args: a list (argv),short options, long options
      #short options that requires an argument are followed by :, long options requiring an argument are followed by =
   except getopt.GetoptError:
      print("something went wrong")
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-u': # If you call the option h, it doesn't work but only in lxplus. Elsewhere it does (Why?)        
         print('python Z_pt1_pt2_plotter.py -n <file_number>')
         print('or, if you prefer')
         print('python Z_pt1_pt2_plotter.py --file_number=<file_number>')
         sys.exit(0)
      elif opt in ("-n","--file_number"):
         global _N #defining a global variable _N                                                                                                       
         _N=arg

if __name__ == "__main__":
   #I don't get why this __name; anyway it works
   main(sys.argv[1:])
   #The first argument is the python script itself, so start parsing from the second one
