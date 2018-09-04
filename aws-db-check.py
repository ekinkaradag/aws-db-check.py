#/bin/python
#Created and developed by Ekin Karadag

import sys,os
import curses
import subprocess
import datetime

#For Cassandra Databases
cassandra_user="user"
cassandra_pass="password"
cassandra_port="" #9042 for default
cassandra_cqlversion=""

#For Oracle Databases
oracle_user="user"
oracle_pass="password"
oracle_port="" #1521 for default
oracle_role=""
oracle_servicename=""

#For MSSQL Databases
mssql_user="user"
mssql_pass="password"
mssql_port="" #1433 for default

#For MySQL Databases
mysql_user="user"
mysql_pass="password"
mysql_port="" #3306 for default




def draw_menu(stdscr):
	cursor_x = 0
	cursor_y = 0

	# Clear and refresh the screen for a blank canvas
	stdscr.clear()
	stdscr.refresh()

	# Start colors in curses
	curses.start_color()
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

	# Initialization of the titles
	height, width = stdscr.getmaxyx()
	stdscr.addstr(0, 0, "IP ADDRESS", curses.color_pair(1)) #Print IP address
	stdscr.addstr(0, 20, "MACHINE NAME", curses.color_pair(1)) #Print the machines name
	stdscr.addstr(0, 40, "DATE", curses.color_pair(1)) #Print date
	stdscr.addstr(0, 50, "PORT", curses.color_pair(1)) #Print checked port
	stdscr.addstr(0, 60, "USERNAME", curses.color_pair(1)) #Print username
	stdscr.addstr(0, 75, "PASSWORD", curses.color_pair(1)) #Print password
	stdscr.addstr(0, 90, "ROLE", curses.color_pair(1)) #Print role
	stdscr.addstr(0, 100, "SERVICE", curses.color_pair(1)) #Print service name
	stdscr.addstr(0, 110, "VERSION", curses.color_pair(1)) #Print version

	while True:
		ipAddrs=[]
		names=[]
		# List out every device to be checked
		p = subprocess.Popen(["aws", "ec2", "describe-instances", "--filter", "Name=tag:Type,Values=Database", "--query", "Reservations[*].Instances[*].{Name:(Tags[?Key==`Name`].Value)[0],IPAddress:PrivateIpAddress}"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		out, err = p.communicate()
		out = str(out)
		for line in out.splitlines():
			wordz=line.split()
			ipAddrs.append(wordz[0])
			names.append(wordz[1])
	
		for i, ip in enumerate(ipAddrs):
			stdscr.addstr(2+i, 0, ip, curses.color_pair(4)) #Print the current IP
			stdscr.addstr(2+i, 40, str(datetime.datetime.now().time())[:8], curses.color_pair(1)) #Print date
			if "Cassandra" in names[i]:
				p = subprocess.Popen(["cqlsh", ip, cassandra_port , "--username=" + cassandra_user, "--password=" + cassandra_pass, "--cqlversion=" + cassandra_cqlversion],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				p.communicate("exit")
				if p.returncode != 0:
					stdscr.addstr(2+i, 20, names[i][-9:], curses.color_pair(2)) #Print the machines name in RED
				else:
					stdscr.addstr(2+i, 20, names[i][-9:], curses.color_pair(3)) #Print the machines name in GREEN
					stdscr.addstr(2+i, 50, str(cassandra_port), curses.color_pair(1)) #Print checked port
					stdscr.addstr(2+i, 60, str(cassandra_user), curses.color_pair(1)) #Print username
					stdscr.addstr(2+i, 75, str(cassandra_pass), curses.color_pair(1)) #Print password
					stdscr.addstr(2+i, 110, str(cassandra_cqlversion), curses.color_pair(1)) #Print version
			elif "Oracle" in names[i]:
				p = subprocess.Popen(["sqlplus", oracle_user + "/" + oracle_pass + "@" + ip + ":" +oracle_port + "/" + oracle_servicename , "as", oracle_role],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				p.communicate("exit")
				if p.returncode != 0:
					stdscr.addstr(2+i, 20, names[i][-9:], curses.color_pair(2)) #Print the machines name in RED
				else:
					stdscr.addstr(2+i, 20, names[i][-9:], curses.color_pair(3)) #Print the machines name in GREEN
					stdscr.addstr(2+i, 50, str(oracle_port), curses.color_pair(1)) #Print checked port
					stdscr.addstr(2+i, 60, str(oracle_user), curses.color_pair(1)) #Print username
					stdscr.addstr(2+i, 75, str(oracle_pass), curses.color_pair(1)) #Print password
					stdscr.addstr(2+i, 90, str(oracle_role), curses.color_pair(1)) #Print role
					stdscr.addstr(2+i, 100, str(oracle_servicename), curses.color_pair(1)) #Print service name
					stdscr.addstr(2+i, 110, "11g", curses.color_pair(1)) #Print version
			elif "MSSQL" in names[i]:
				p = subprocess.Popen(["sqlcmd", "-S", ip + "," + mssql_port, "-U", mssql_user, "-P", mssql_pass],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				p.communicate("exit")
				if p.returncode != 0:
					stdscr.addstr(2+i, 20, names[i][-5:], curses.color_pair(2)) #Print the machines name in RED
				else:
					stdscr.addstr(2+i, 20, names[i][-5:], curses.color_pair(3)) #Print the machines name in GREEN
					stdscr.addstr(2+i, 50, str(mssql_port), curses.color_pair(1)) #Print checked port
					stdscr.addstr(2+i, 60, str(mssql_user), curses.color_pair(1)) #Print username
					stdscr.addstr(2+i, 75, str(mssql_pass), curses.color_pair(1)) #Print password
			elif "MySQL" in names[i]:
				p = subprocess.Popen(["mysql", "-u", mysql_user, "-h", ip, "-P", mysql_port, "--password=" + mysql_pass],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				p.communicate("exit")
				if p.returncode != 0:
					stdscr.addstr(2+i, 20, names[i][-5:], curses.color_pair(2)) #Print the machines name in RED
				else:
					stdscr.addstr(2+i, 20, names[i][-5:], curses.color_pair(3)) #Print the machines name in GREEN
					stdscr.addstr(2+i, 50, str(mysql_port), curses.color_pair(1)) #Print checked port
					stdscr.addstr(2+i, 60, str(mysql_user), curses.color_pair(1)) #Print username
					stdscr.addstr(2+i, 75, str(mysql_pass), curses.color_pair(1)) #Print password
			stdscr.refresh()

	
def main():
	curses.wrapper(draw_menu)

if __name__ == "__main__":
	main()
