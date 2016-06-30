import os
import sys


def get_variable_name(line):
	return line.split(" ")[-1].split(";")[0]

def get_variable_in_method_name(line, prefix):
	variable = line[(line.index(prefix) + len(prefix)):]
	variable = variable.split("(")[0]
	return variable[0].lower() + variable[1:]

def count_leading_spaces(line):
	return (len(line) - len(line.lstrip(' ')))

def insert_comments(lines):
	index = 0
	while index < len(lines):
		line = lines[index]
		comment = None
		
		if "private" in line:
			# Variables
			if "(" not in line and ")" not in line:
				variable = get_variable_name(line)
				indentation = count_leading_spaces(line)
				comment = "/** */"
		
		if "public" in line:
			# Getters
			if "get" in line:
				variable = get_variable_in_method_name(line, "get")
				indentation = count_leading_spaces(line)
				comment = "/** @return the " + variable + " */"
			
			# Setters
			elif "set" in line:
				variable = get_variable_in_method_name(line, "set")
				indentation = count_leading_spaces(line)
				comment = "/** @param " + variable + " the " + variable + " to set */"
		
		if comment is not None:
			while indentation > 0:
				comment = " " + comment
				indentation -= 1
			lines.insert(index, comment)
			index += 1

		index += 1
	return "\n".join(lines)

def main():
    usage = "Usage: " + sys.argv[0] + " [-o] file_to_comment\n" \
            "\n" \
            "       -o:     Redirect output to stdout"
    
    redirect_to_stdout = False
    
    if len(sys.argv) < 2:
        print("ERROR: No arguments provided\n")
        print(usage)
        exit(1)
    
    for arg in sys.argv:
        if arg == "-o":
            redirect_to_stdout = True
        elif arg == "-h" or arg == "--help":
            print(usage)
            exit(0)
    
    try:
        with open(sys.argv[-1], "r") as fo:
            lines = fo.read().splitlines()
        
        lines = insert_comments(lines)
        
        if redirect_to_stdout:
            sys.stdout.write(lines)
        else:
            with open(sys.argv[-1], "w") as fo:
                fo.writelines(lines)
    except FileNotFoundError:
        print("ERROR: \"" + sys.argv[-1] + "\" not found\n")
        print(usage)
        exit(1)

main()
