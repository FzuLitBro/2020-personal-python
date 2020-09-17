import json
import os
import argparse
import threading
import datetime

begintime = datetime.datetime.now()
s1=threading.Semaphore(5)

def outputFile(file_address, num):
	s1.acquire()
	Users = {}
	Repos = {}
	UsersAndRepos = {}
	json_list = []
	x = open(file_address, 'r', encoding = 'utf-8').read()
	for line in x.split('\n'):
		if(len(line)>0):
			try:
				i = json.loads(line)
				EventType = i.get('type',0)
				EventUser = i.get('actor',0).get('login',0)
				EventRepo = i.get('repo',0).get('name',0)
				if(not Users.get(EventUser)):
					Users.update({EventUser: {}})
				if(not Users[EventUser].get(EventType)):
					Users[EventUser].update({EventType: 0})
				Users[EventUser][EventType] += 1

				if(not Repos.get(EventRepo)):
					Repos.update({EventRepo: {}})
				if(not Repos[EventRepo].get(EventType)):
					Repos[EventRepo].update({EventType: 0})
				Repos[EventRepo][EventType] += 1


				if(not UsersAndRepos.get(EventUser)):
					UsersAndRepos.update({EventUser: {}})
				if(not UsersAndRepos[EventUser].get(EventRepo)):
					UsersAndRepos[EventUser].update({EventRepo: {}})
				if(not UsersAndRepos[EventUser][EventRepo].get(EventType)):
					UsersAndRepos[EventUser][EventRepo].update({EventType: 0})
				UsersAndRepos[EventUser][EventRepo][EventType] += 1
			except:
				pass

	with open('.\\output\\' + 'Users_' + str(num) + '.json', 'w', encoding='utf-8') as f:
		json.dump(Users,f)
		f.close()

	with open('.\\output\\' + 'Repos_' + str(num) + '.json', 'w', encoding='utf-8') as f:
		json.dump(Repos,f)
		f.close()
	with open('.\\output\\' + 'UsersAndRepos_' + str(num) + '.json', 'w', encoding='utf-8') as f:
		json.dump(UsersAndRepos,f)
		f.close()

	Users = {}
	Repos = {}
	UsersAndRepos = {}
	overtime = datetime.datetime.now()
	print(overtime - begintime)
	s1.release()

def getEventsRepos(repo, event):
	file_address = '.\\output'
	num = 0
	for root, dic, files in os.walk(file_address):
		for file in files:
			if(file[0:6] == 'Repos_'):
				x = open(root + '\\' + file, 'r', encoding='utf-8').read()
				f = json.loads(x)
				if(not f.get(repo,0)):
					pass
				else:
					num += f[repo].get(event,0)
	print(num)

def getEventsUsers(user, event):
	file_address = '.\\output'
	num = 0
	for root, dic, files in os.walk(file_address):
		for file in files:
			if(file[0:6] == 'Users_'):
				x = open(root + '\\' + file, 'r', encoding='utf-8').read()
				f = json.loads(x)
				if(not f.get(user,0)):
					pass
				else:
					num += f[user].get(event,0)
	print(num)

def getEventsUsersAndRepos(user, repo, event):
	file_address = '.\\output'
	num = 0
	for root, dic, files in os.walk(file_address):
		for file in files:
			if(file[0:14] == 'UsersAndRepos_'):
				x = open(root + '\\' + file, 'r', encoding='utf-8').read()
				f = json.loads(x)
				if(not f.get(user,0)):
					print("0")
				elif(not f[user].get(repo)):
					print("0")
				else:
					num += f[user][repo].get(event,0)
	print(num)

class RunFirst:
	def __init__(self):
		self.num = 0
		self.parser = argparse.ArgumentParser()
		self.argInit()
		self.analyse()

	def argInit(self):
		self.parser.add_argument('-i', '--init')
		self.parser.add_argument('-u', '--user')
		self.parser.add_argument('-r', '--repo')
		self.parser.add_argument('-e', '--event')

	def analyse(self):
		if(self.parser.parse_args().init):
			for root, dic, files in os.walk(self.parser.parse_args().init):
				for file in files:
					if(file[-5:] == '.json'):
						print(root + '\\' + file)
						self.num += 1
						t = threading.Thread(target=outputFile, args=(root + '\\' + file, self.num))
						t.start()
			return 0
		else:
			if(self.parser.parse_args().event):
				if(self.parser.parse_args().user):
					if(self.parser.parse_args().repo):
						getEventsUsersAndRepos(
							self.parser.parse_args().user, self.parser.parse_args().repo, self.parser.parse_args().event)
					else:
						getEventsUsers(
							self.parser.parse_args().user, self.parser.parse_args().event)
				elif(self.parser.parse_args().repo):
					getEventsRepos(
						self.parser.parse_args().repo, self.parser.parse_args().event)
				else:
					raise RuntimeError('error: argument -l or -c are required')
					return 0
			else:
				raise RuntimeError('error: argument -e is required')
				return 0

if __name__ == '__main__':
	Run = RunFirst()
