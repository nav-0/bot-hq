#!/usr/bin/env/python3
import argparse
import logging
import sys
import uuid

commands = {'health': 'uptime', }
location_set = ".locations"
error_event = {1: 'Scout down.'} # Flesh

FORMAT = '%(asctime)s %(levelname)s %(name)s:%(lineno)s - %(message)s'
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'default': {
	  'format': FORMAT, 
	},
  },
  'handlers': {
    'console': 'logging.StreamHandler',
	'formatter': 'default',
  },
  'loggers': {
    'bot-scout': {'level': 'DEBUG'},
  },
  'root': {
    'level': 'DEBUG', 
	'handlers': ['console'],
  },
}
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

class Scout():
"""
  Defines a bot object. 
"""
  def __init__(self, host, user, password):
    self.id = uuid.uuid4()
    self.host = host
    self.user = user
    self.password = password
	self.status = False
	
  def send_command(self, command):
    if self.status:
	  try:
        ssh.connect(self.hostname, self.username, self.password)
        stdin, stderr, stdout = ssh.exec_command(command)
		return [True, stdout.channel.recv(4096).decode(encoding='UTF-8')]
	  except Exception exc:
	    logger.error('Unable to connect to %s.' % self.host)
	    if(self.update_status()):
		    logger.debug('Status OK. Command issue: %s' % exc)
		    return [False, exc]
	logger.debug('Scout %s is down.' % self.host)
	return [False, error_event[1]]
	
	def update_status():
	  try:
      ssh.connect(self.hostname, self.username, self.password)
      stdin, stderr, stdout = ssh.exec_command(commands['health'])
		  self.status = True 
	  except Exception exc:
	    logger.debug('Scout is down.')
		  self.status = False
	  return self.status
  
def scout_report(self, scouts, options=False):
"""
  Get a round of updates from the bots in your network.
  TODO: specify options to retrieve additional stats. 
"""
  report = {}
  for scout in scouts:
    hostname, username, password = scout.host, scout.username, scout.password
    try:
      logger.debug('Checking in on %s' % hostname)
  	  response = scout.send_command(commands['health'])
	  if response[0]:
        report[hostname] = response[1]
	  else:
	    logger.error('Error: %s' % str(response[1]))
		  report[hostname] = str(response[1])
    except Exception as exc:
      logger.error('SSH connection failed for %s: %s' % hostname, exc)
      report[hostname] = exc
  return report
	
def canvass(locations=location_set):
"""
  Get a list of hosts and their credentials from location set. 
  Location set content line format host:username@password.
  TODO: validation.
"""
  hosts = scouts = new list()
  with open(locations) as loc:
    hosts += [[line.split(':')[0]] + line.split(':')[1].split('@') for line in loc.readlines()]
  for host in hosts:
    hname, uname, pass = host[i] for i in range(2)
    scouts += [new Scout(hname, uname, pass)]
  return scouts
	
def broadcast_command(scouts, command):
  result = {'errors': {},}
  for scout in scouts:
    response = scout.send_command(command)
	if response[0]:
	  result[scout.host] = response[1]
	else:
   	  result['errors'][scout.host] = response[1]
  return result
    
def scout_session(scouts):
  session = True
  while session:
    control = input("[scout-hq] ")
    if control == "close":
      session = False
	elif control == "health":
	  outputHandler(scout_report(scouts))
	else:
    outputHandler(broadcast_command(scouts, control))
  
def outputHandler(output, use_stdout=True):
  if not output:
    logger.error('Output failed.')
	return 1
  logger.info('Output successful: %s' % str(output))
  if use_stdout:
    print(output)
	return 0
  with open('scout.out', 'w') as outhandle:
    outhandle.write(output)
  return 0
  
def scout_hq(argv=None):
  if argv is None:
    argv = sys.argv[1:]
  parser = argparse.ArgumentParser()
  parser.add_argument('--session', help='Start control session')
  parser.add_argument('--health', help='Do a health check on bots')
  parser.add_argument('--hosts', help='Specify hosts file')
  args = parser.parse_args(argv)
  hostfile = location_set
  if args.hosts:
  # filename validation would be nice
    hostfile = args.hosts
  if args.health:
    outputHandler(scout_report(canvass(hostfile)))
  if args.session:
    scouts = canvass(hostfile)
	  scout_session(scouts)
    
if __name__ == "__main__":
  sys.exit(scout_hq())
	
 
