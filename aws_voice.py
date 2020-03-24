import speech_recognition as sr
from gtts import gTTS
import playsound
import boto3
import os
import json
import time

with open('cred.json') as cred:
	keys = json.load(cred)
	aws_access_key_id=keys['aws_access_key_id']
	aws_secret_access_key=keys['aws_secret_access_key']
	region_name=keys['region_name']

language = 'en'
r = sr.Recognizer()
client = boto3.client('ec2',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name=region_name)
ec2 = boto3.resource('ec2',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name=region_name)

image_id = None
instance_type='t2.micro'
minCount=1
maxCount=1
audioCount = 1

def check_keypair():
	keys_list = []
	allkeys = client.describe_key_pairs()
	count  = 0
	for temp in allkeys['KeyPairs']:
		count+=1
		print(str(count)+". "+temp['KeyName'])
		keys_list.append(temp['KeyName'])
	print(str(count+1)+". Create New Key Pair")
	while True:
		try:
			res = int(get_input("key_pair"))
			if res==count+1:
				name = get_input("new_key_pair")
				key = ec2.create_key_pair(KeyName = name)
				file=open("generated_keys/"+name+".pem", "w")
				file.write(key.key_material)
				file.close()
				#print(key.key_material)
			else:
				name = keys_list[res-1]
			break
		except Exception as e:
			play_audio("wrong_input")
	play_audio(name+" Selected")
	return name

def play_audio(data):
	if data=="intro":
		print("Welcome to voice automated AWS EC2 Management Console made by Riya Soni and Rhythm Bhiwani")
		playsound.playsound('intro.mp3', True)
	elif data=="exit":
		print("Thank you! Hoping to see you again.")
		playsound.playsound('exit.mp3', True)
	elif data=="please_try_again":
		print("Please try again!")
		playsound.playsound('please_try_again.mp3', True)
	elif data=="select_os":
		print("Which Operating System you want to install, windows or linux?")
		playsound.playsound('select_os.mp3', True)
	elif data=="choice":
		print("What task you want me to perform on AWS Cloud?")
		playsound.playsound('choice.mp3', True)
	elif data=="wrong_input":
		print("Wrong Input")
		playsound.playsound('wrong_input.mp3', True)
	elif data=="key_pair":
		print("Which key pair you want to use? You can say the number 1, 2 and so on")
		playsound.playsound('key_pair.mp3', True)
	elif data=="instance_num_terminate":
		print("Which instance you want to terminate, you can say the number 1, 2 and so on")
		playsound.playsound('instance_num_terminate.mp3', True)
	elif data=="instance_num_start":
		print("Which instance you want to start, you can say the number 1, 2 and so on")
		playsound.playsound("instance_num_start.mp3", True)
	elif data=="start_ins_audio":
		print("No instance to start, creating new instance")
		playsound.playsound('start_ins_audio.mp3', True)
	elif data=="instance_started":
		print("Instance Started")
		playsound.playsound('instance_started.mp3', True)
	elif data=="instance_num_stop":
		print("Which instance you want to stop, you can say the number 1, 2 and so on")
		playsound.playsound('instance_num_stop.mp3', True)
	elif data=="instance_num_reboot":
		print("Which instance you want to reboot, you can say the number 1, 2 and so on")
		playsound.playsound('instance_num_reboot.mp3', True)
	elif data=="no_instance_running":
		print("No instance running!")
		playsound.playsound("no_instance_running.mp3", True)
	elif data=="instance_stopped":
		print("Instance Stopped!")
		playsound.playsound('instance_stopped.mp3', True)
	elif data=="instance_terminated":
		print("Instance Terminated!")
		playsound.playsound('instance_terminated.mp3', True)
	elif data=="instance_rebooted":
		print("Instance Rebooted!")
		playsound.playsound('instance_rebooted.mp3', True)
	elif data=="no_instance_to_terminate":
		print("No Instance to Terminate!")
		playsound.playsound('no_instance_to_terminate.mp3', True)
	elif data=="new_key_pair":
		print("Enter Name of New Key Pair")
		playsound.playsound('new_key_pair.mp3', True)
	elif data=="connect":
		print("Do you want to connect to the instance now? (Yes or No)")
		playsound.playsound('connect.mp3', True)
	else:
		print(data)
		global audioCount
		myobj = gTTS(text=data, lang=language, slow=False)
		myobj.save("audio"+str(audioCount)+".mp3")
		playsound.playsound("audio"+str(audioCount)+".mp3", True)
		os.remove("audio"+str(audioCount)+".mp3")
		audioCount+=1

def get_input(data):
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		play_audio(data)
		try:
			audio = r.listen(source, timeout=10, phrase_time_limit=10)
		except Exception as e:
			play_audio("please_try_again")

		try:
			text = r.recognize_google(audio)
			print("Your Input : ",text)
			if 'tu' in text.lower():
				return "2"
			return text
		except:
			return "None"

def create_ins():
	global image_id
	while image_id==None:
		res = get_input("select_os")
		if 'linux' in res.lower():
			image_id='ami-0520e698dd500b1d1'
		elif 'window' in res.lower() or 'windows' in res.lower():
			image_id='ami-0ce84304ef5b08a22'
		else:
			play_audio("please_try_again")
	keyName = check_keypair()
	result = client.run_instances(ImageId=image_id,
			InstanceType=instance_type,
			MinCount=minCount,
			MaxCount=maxCount,
			KeyName=keyName)
	out = "New instance created with number : "+result['Instances'][0]['InstanceId']
	play_audio(out)
	time.sleep(2)
	# result = client.describe_instances(InstanceIds=[result['Instances'][0]['InstanceId']])
	# print(result['Reservations'][0]['Instances'][0]['PublicDnsName'])
	# res = get_input("connect").lower()
	# if 'yes' in res:
	# 	os.system('ssh -i "generated_keys/'+keyName+'.pem" ec2-user@'+result['Reservations'][0]['Instances'][0]['PublicDnsName'])

def start_ins():
	instance_list = []
	instances = ec2.instances.filter(
		Filters = [{'Name': 'instance-state-name', 'Values': ['stopped','stopping']}]
		)
	count  = 0
	for instance in instances:
		count+=1
		print(str(count)+". "+instance.id)
		instance_list.append(instance.id)
	if count==0:
		play_audio("start_ins_audio")
		create_ins()
	else:
		while True:
			try:
				id_num = get_input("instance_num_start")
				temp = instance_list[int(id_num)-1]
				break
			except Exception as e:
				play_audio("wrong_input")
		client.start_instances(InstanceIds=[temp])
		play_audio("instance_started")

def stop_ins():
	instance_list = []
	instances = ec2.instances.filter(
		Filters = [{'Name': 'instance-state-name', 'Values': ['running','pending']}]
		)
	count  = 0
	for instance in instances:
		count+=1
		print(str(count)+". "+instance.id)
		instance_list.append(instance.id)
	if count==0:
		play_audio("no_instance_running")
	else:
		while True:
			try:
				id_num = get_input("instance_num_stop")
				temp = instance_list[int(id_num)-1]
				break
			except Exception as e:
				play_audio("wrong_input")
		client.stop_instances(InstanceIds=[temp])
		play_audio("instance_stopped")

def reboot_ins():
	instance_list = []
	instances = ec2.instances.filter(
		Filters = [{'Name': 'instance-state-name', 'Values': ['running','pending']}]
		)
	count  = 0
	for instance in instances:
		count+=1
		print(str(count)+". "+instance.id)
		instance_list.append(instance.id)
	if count==0:
		play_audio("no_instance_running")
	else:
		while True:
			try:
				id_num = get_input("instance_num_reboot")
				temp = instance_list[int(id_num)-1]
				break
			except Exception as e:
				play_audio("wrong_input")
		client.reboot_instances(InstanceIds=[temp])
		play_audio("instance_rebooted")

def terminate_ins():
	instance_list = []
	instances = ec2.instances.filter(
		Filters = [{'Name': 'instance-state-name', 'Values': ['running','stopped','pending','shutting-down','stopping']}]
		)
	count  = 0
	for instance in instances:
		count+=1
		print(str(count)+". "+instance.id)
		instance_list.append(instance.id)
	if count==0:
		play_audio("no_instance_to_terminate")
	else:
		while True:
			try:
				id_num = get_input("instance_num_terminate")
				temp = instance_list[int(id_num)-1]
				break
			except Exception as e:
				play_audio("wrong_input")
		client.terminate_instances(InstanceIds=[temp])
		play_audio("instance_terminated")

#Program starts from here
play_audio("intro")
while True:
	image_id = None
	res = get_input("choice").lower()
	if 'linux' in res or 'redhat' in res:
		image_id='ami-0520e698dd500b1d1'

	if 'window' in res or 'windows' in res:
		image_id='ami-0ce84304ef5b08a22'

	if 'create' in res or 'launch' in res:
		create_ins()

	if 'start' in res:
		start_ins()

	if 'stop' in res:
		stop_ins()

	if 'restart' in res or 'reboot' in res:
		reboot_ins()

	if 'terminate' in res or 'delete' in res or 'remove' in res:
		terminate_ins()

	if 'exit' in res or 'quit' in res or 'close' in res:
		play_audio("exit")
		exit()
	print()
	time.sleep(2)
