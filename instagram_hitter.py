########################################################################################
# Welcome to Instagram Automator
#
#This program is about getting you seen by more people on instagram 
#it does the liking and following for you to hopefully increase the number of people who see your stuff.
#      - How do people get 1.5m followers on instagram? Is it done outside of instagram? 
#      - Is it where you put your photo and name? 
#
#
#Set Up a Set of Like Categories you want to interact with.
# (Future mod will suggest tags based on your tag list - Scrolls through your page and finds your most common hash tags and compares to API call)
#  -   Set the Like Limit
#  -   Set the Follow Limit
#  -   Set the Like time limit (Don't like anything newer than X minutes)
#  -   Unfollows after 1 Day (So that people can see the follow link in their app)
#  -   Only follows people who have a ratio of less than X:1 this is due to the fact people with high Ratio's have zero chance of following you.
#  -   Find photo's to comment on. (Create a user interface that makes it easy to do)
# 
# 
# 
# (Auto Create accounts
# 	- Grab some generic photos
# 	- do some random liking
# 	- Wait a month until mass spamming?
# 	- Sell Likes 
#
#
#
#
#  Build in Docker
#
#
#
#
#
#
########################################################################################
from selenium import webdriver
#from selenium import RemoteWebDriver
import time
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.action_chains import ActionChains
#import mysqlclient
import pymysql
import requests
from lxml import html


print('Version 0.1 - 11/06/2017')

HOST="instagram.lukerussell.com"     #The host you want to connect to.
USER="lukerussell"    # The database username. 
PASSWORD="Anna1234"    # The database password. 
DATABASE="lr_instagram"    # The database name.

db = pymysql.connect(HOST,USER,PASSWORD,DATABASE,autocommit=True)

cur = db.cursor(pymysql.cursors.DictCursor)
update = db.cursor(pymysql.cursors.DictCursor)
search_term = db.cursor(pymysql.cursors.DictCursor)

User_To_Run = '1'


global loop_limit
loop_limit = 1000

global continue_script
continue_script = 'Yes'
global user_to_unfollow 
user_to_unfollow = 0
	#print(users_following[0].text)
global users_to_unfollow 
users_to_unfollow = []
global users_unfollowed
users_unfollowed = 0 
global unfollow_capped 
unfollow_capped = 'false'
global debug
debug = 'false'

sql = 'SELECT * FROM lr_instagram.instagram_user WHERE User_ID = '+str(User_To_Run)
cur.execute(sql)

for row in cur:
    username = row['username']
    password = row['password']

#conn = mysqlclient.connect(host= "instagram.lukerussell.common",
 #                 user="lukerussell",
  #                passwd="Anna1234",
   #               db="lr_instagram")
#x = conn.cursor()

def ins_user_exists():
	sql = 'Select * from lr_instagram.instagram_user_record where Username = "'+ins_user_name+'"'
	#sql = 'SELECT * FROM lr_instagram.instagram_user_records WHERE Username = ' + photo_user
	#print(sql)
	cur.execute(sql)
	data=cur.fetchall()
	#print('User Exists?')
	global ins_user_exists_len
	ins_user_exists_len = len(data)
	#print(ins_user_exists_len)


def update_ins_user():

	sql = 'Select * from lr_instagram.instagram_user_record where Username = "'+ins_user_name+'"'
	#sql = 'SELECT * FROM lr_instagram.instagram_user_records WHERE Username = ' + photo_user
	#print(sql)
	cur.execute(sql)
	data=cur.fetchall()
	if len(data)==0:
		#print('There is no component named')
		sql = 'INSERT INTO lr_instagram.instagram_user_record (Username, Posts, Followers, Following, Date) VALUES ("'+ins_user_name+'", "'+str(user_posts)+'", "'+str(user_followers) + '", "'+ str(user_following)+'", "' + str(date.today()) + '")'
		#print(sql)
		cur.execute(sql)

	else:
		print('User Exists')
		


def unfollow():

	search_button = driver.find_element_by_class_name(instagram_search_button)
	search_button.click()

	print('Entering Search:',instagram_search_category)
	time.sleep(pause_amount)
	search_input = driver.find_element_by_class_name(instagram_search_input)
	search_input.send_keys(instagram_search_category)
	time.sleep(pause_amount)
	search_input.send_keys(u'\ue007')


def follow():
	sql = 'Select Distinct UserName from lr_instagram.instagram_user_follows Where User_ID = 1 and Username ="'+str(ins_user_name)+'"'
	#print(sql)
	cur.execute(sql)
	data=cur.fetchall()

	if len(data)==0:
		print('#####     Following and Updating Record')
		sql = 'INSERT INTO `lr_instagram`.`instagram_user_follows` (`User_ID`, `Username`, `Date_Followed`, `Ins_User_ID`) VALUES ("'+User_To_Run+'","' + ins_user_name +'","' + str(date.today()) + '", "1")'
		cur.execute(sql)
		#print(sql)

		for row in cur:
			print(row['Ins_User_ID'])

		button_exists_click(instagram_follow_button)
			#photo_like_button = driver.find_element_by_class_name(instagram_follow_button)
			#photo_like_button.click()


def button_exists_click(web_element):
	#print('Checking Button Exists:',web_element)
	global continue_script

	button_to_click = driver.find_elements_by_class_name(web_element)
	#print('Length:',len(button_to_click))
	loop_check = 0
	while len(button_to_click) < 1 and loop_check < loop_limit:
		#print('Looking for Element')
		button_to_click = driver.find_elements_by_class_name(web_element)
		loop_check = loop_check + 1

	if len(button_to_click) >= 1:
		button_to_click = driver.find_element_by_class_name(web_element)
		#print('Next:',button_to_click)
		button_to_click.click() 
		#global continue_script
		
		continue_script = 'Yes'
		print('Continue?',continue_script)
	else: 

		continue_script = 'No'
		print('Continue?',continue_script)

def element_exists(web_element_type,web_element,action,variable):
	if debug == 'true': print('Checking Button Exists:',web_element)
	global continue_script

	if web_element_type == 'class':

		if debug == 'true': print('Finding by Class')
		button_to_click = driver.find_elements_by_class_name(web_element)
		if debug == 'true': print('Length:',len(button_to_click))
		loop_check = 0
		while len(button_to_click) < 1 and loop_check < loop_limit:
			#print('Looking for Element')
			button_to_click = driver.find_elements_by_class_name(web_element)
			loop_check = loop_check + 1

		if debug == 'true': print('Found by Class')
		if len(button_to_click) >= 1:
			button_to_click = driver.find_element_by_class_name(web_element)
			#global continue_script
			if action == 'click':
				if debug == 'true': print('Clicking')
				button_to_click.click() 
			elif action == 'input':
				if debug == 'true': print('Inputting')
				button_to_click.send_keys(variable)

			continue_script = 'Yes'
			if debug == 'true':print('Continue?',continue_script)
		else: 

			continue_script = 'No'
			if debug == 'true': print('Continue?',continue_script)
	
	elif web_element_type == 'name':
		if debug == 'true': print('Finding by Name')
		button_to_click = driver.find_elements_by_name(web_element)
		if debug == 'true': print('Length:',len(button_to_click))
		loop_check = 0
		while len(button_to_click) < 1 and loop_check < loop_limit:
			#print('Looking for Element')
			button_to_click = driver.find_elements_by_name(web_element)
			loop_check = loop_check + 1

		if debug == 'true': print('Found by Name')
		if len(button_to_click) >= 1:
			button_to_click = driver.find_element_by_name(web_element)
			#global continue_script
			if action == 'click':
				if debug == 'true': print('Clicking')
				button_to_click.click()
			elif action == 'input':
				if debug == 'true': print('Inputting')
				button_to_click.send_keys(variable) 

			continue_script = 'Yes'
			if debug == 'true': print('Continue?',continue_script)
		else: 

			continue_script = 'No'
			if debug == 'true': print('Continue?',continue_script)

def pausing():
	print('Pause')
	time.sleep(pause_amount)

def unfollowing_all():

	print('Clicking User Settings')
	button_exists_click(instagram_user_account)

	time.sleep(5)

	print('Pressing Followers')

	button_to_click = driver.find_elements_by_partial_link_text('following')
	loop_check = 0
	while len(button_to_click) < 1 and loop_check < loop_limit:
		#print('Looking for Element')
		button_to_click = driver.find_elements_by_partial_link_text('following')
		loop_check = loop_check + 1

	print('Element Found')

	#if len(button_to_click) >= 1:
		#button_to_click = driver.find_element_by_partial_link_text('following')
		#print('Next:',button_to_click)
	button_to_click = driver.find_element_by_partial_link_text('following')
	button_to_click.click() 
	
	button_to_click = driver.find_elements_by_class_name('_mmgca')
	loop_check = 0
	while len(button_to_click) < 1 and loop_check < loop_limit:
		#print('Looking for Element')
		button_to_click = driver.find_elements_by_class_name('_mmgca')
		loop_check = loop_check + 1


	button_to_click = driver.find_element_by_class_name('_mmgca')
	button_to_click.click()
	


	for i in range(0,1000):
		ActionChains(driver).key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN).perform()
		#print(i)

# 	# while scroll_frame < scroll_frame_limit:	
# 	# 	#unfollow_frame.send_keys(u'\ue015')
# 	# 	#unfollow_frame.click()
# 	# 	#unfollow_frame.send_keys(Keys.PAGE_DOWN).perform()
# 	# 	#print('Scrolling',scroll_frame)
# 	# 	scroll_frame = scroll_frame + 1

	print('Listing Followers')

# 	print()

#    #//li[1]/div[1]

 
# # //li[2]/div/div[2]/span/button is follow button

	#button_text = driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/div[2]/ul/li/div/div[2]/span/button")
	#while len(button_text) < 1 and loop_check < loop_limit:
# 			#print('Looking for Element')
		#button_text = driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/div[2]/ul/li/div/div[2]/span/button")
# 	#		user_name_text = driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/div[2]/ul/li[1]/div/div[2]/span/button")
		#loop_check = loop_check + 1

	#print(len(button_text))

# 	#button_text = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[2]/ul/li[30]/div/div[2]/span/button")
# 	#print(len(button_text))
# 	#print('Testing Button Text:',button_text.text)

# #print()
# 	unfollow_times = 50
# 	unfollow_scrolls = 0

#	while unfollow_scrolls < unfollow_times:
	users_following = driver.find_elements_by_class_name(instagram_photo_username)
	loop_check = 0
# 		unfollow_buttons = driver.find_elements_by_class_name('_i46jh')
	while len(users_following) < 1 and loop_check < loop_limit:
# 			#print('Looking for Element')
		users_following = driver.find_elements_by_class_name(instagram_photo_username)
		#unfollow_buttons = driver.find_elements_by_class_name('_i46jh')
		loop_check = loop_check + 1

	print('Users:',len(users_following))
# 		#print(users_following)

	print('Screenshot')
	driver.get_screenshot_as_file('followers.png')

# 		unfollow_button = driver.find_elements_by_class_name('_ah57t')

# 		user_number = 0
# 		while user_number < len(users_following):
# 			user_to_unfollow = users_following[user_number].text
# 			unfollow_button =  unfollow_buttons[user_number]
# 			unfollow_button_text = unfollow_buttons[user_number].text
# 			print(user_number,'/',len(users_following),' ',users_following[user_number].text,':',unfollow_button_text)
# 			#print(users_following[user_number].text)
			
# 			sql = "Select * from lr_instagram.instagram_user_follows Where User_ID = 1 and Username = '" + str(user_to_unfollow) + "'" #and Date_Unfollowed is null' # and Date_Followed < curdate()'
# 			cur.execute(sql)

# 			for row in cur:
# 				if unfollow_buttons[user_number].text == 'Following':
# 					unfollow_button.click()
# 					time.sleep(3)
# 				#unfollowed = unfollowed + 1

# 			user_number = user_number + 1
# 		unfollow_scrolls = unfollow_scrolls + 1
# 		loop_check = 0

# 	#sql = ''
# 	unfollow_buttons = driver.find_elements_by_class_name('_i46j')
# 	unfollow_buttons.click()


	# Just lists all Followers in an array
	while user_to_unfollow < len(users_following):
		users_to_unfollow.append([user_to_unfollow,users_following[user_to_unfollow].text])
		#users_to_unfollow[user_to_unfollow] = users_following[user_to_unfollow].text
		#print()
		#print(user_to_unfollow,'/',len(users_following))
		user_to_unfollow =  user_to_unfollow + 1

	#print(users_to_unfollow[0][0])
	#print(users_to_unfollow[0][1])

	# Looping through Followers to unlike 
	user_to_unfollow = 0
	while user_to_unfollow < len(users_to_unfollow) and unfollow_capped != 'true':
	
		print(user_to_unfollow,'/',len(users_to_unfollow))
		#users_to_unfollow[0]
		#print(users_to_unfollow[user_to_unfollow].text)

		sql = "Select * from lr_instagram.instagram_user_follows Where User_ID = 1 and username = '" + str(users_to_unfollow[user_to_unfollow][1]) +"'"
		#print(sql)
		cur.execute(sql)

		for row in cur:

			check_again = 'false'
			check_count = 0
			while check_again == 'false' and check_count <= 5:

				print('Unfollowing:',row['Username'])
				Record_To_Unfollow = row['Record_Number']
			# 	#time.sleep(pause_amount)
			# 	#search_button = driver.find_element_by_class_name(instagram_search_button)
			# 	#search_button.click()

			# 	#print('Entering Search:',row['Username'])
			# 	#time.sleep(pause_amount)
			# 	#search_input = driver.find_element_by_class_name(instagram_search_input)
			# 	#search_input.send_keys(row['Username'])
			# 	#time.sleep(pause_amount)
			# 	#search_input.send_keys(u'\ue007')
			# 	#time.sleep(pause_amount)
				user_name = row['Username'] 
				user_url = 'https://www.instagram.com/'+str(user_name)

				driver.get(user_url)

				#button_exists_click(instagram_follow_button)
		        
			# 	#user_unfollow = driver.find_element_by_class_name(instagram_follow_button)
				button_to_click = driver.find_elements_by_class_name(instagram_follow_button)

				loop_check = 0
			# #print('Length:',len(button_to_click))
				while len(button_to_click) < 1 and loop_check < 100:
			# 	#print('Looking for Element')
					button_to_click = driver.find_elements_by_class_name(instagram_follow_button)
					loop_check = loop_check + 1

			# 	if len(button_to_click) >= 1:
				button_to_click = driver.find_element_by_class_name(instagram_follow_button)
			# 		#print('Currently:',button_to_click.text)
				if button_to_click.text == 'Following':
			# 	#print('Next:',button_to_click)
					#print('Unfollowing')
					#sql = "UPDATE lr_instagram.instagram_user_follows SET Date_Unfollowed=curdate() WHERE Record_Number="+str(Record_To_Unfollow)
					#update.execute(sql)	
					button_to_click.click()
					check_count = check_count + 1 
				else: 
					check_again = 'true'
					users_unfollowed = users_unfollowed + 1
					print('User Unfollowed:', users_unfollowed)

					#button_to_click = driver.find_element_by_class_name(instagram_follow_button)

					#loop_check = 0		
					#while button_to_click.text != "Follow" and loop_check < 100:
					#	loop_check = loop_check + 1

					#driver.implicitly_wait(5)
					#user_unfollow.click()

					#sql = "UPDATE lr_instagram.instagram_user_follows SET Date_Unfollowed=curdate() WHERE Record_Number="+str(Record_To_Unfollow)
					#print('SQL Updated',sql)

				if check_count == 5:
					print('Instagram Unfollow Capped')
					unfollow_capped = 'true'

	
		#time.sleep(1)
		#print(users_following)
		user_to_unfollow = user_to_unfollow + 1
		print('Next User')

pause_amount = 2

url = 'https://www.instagram.com/?hl=en'
#driver=webdriver.Chrome()
#driver=webdriver.Firefox()
#driver = webdriver.PhantomJS()
#driver = webdriver.Remote("http://192.168.99.100:32780/wd/hub", webdriver.DesiredCapabilities.CHROME.copy())
driver = webdriver.Remote("http://192.168.99.100:32780/wd/hub", webdriver.DesiredCapabilities.FIREFOX.copy())
#driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.CHROME.copy())
driver.get("http://www.google.com")
driver.get_screenshot_as_file('filename.png')


driver.get(url)
#time.sleep(pause_amount)



login_method = 'Username'
#username = 'luke.russell@hotmail.com'
#password = 'Anna1234'

facebook_username = 'email'
facebook_password = 'pass'
facebook_login_button = 'loginbutton'

username_login_button = '_ah57t' #_ah57t _84y62 _i46jh _rmr7s

instagram_search_button = '_9pxkq'   #_9pxkq _icv3j
instagram_search_input = '_9x5sw'   #_9x5sw _qy55y
instagram_search_ready = '_o1o4h'                 #_o1o4h
#instagram_search_category = 'instacake'
#
instagram_follow_button = '_ah57t' #_ah57t _84y62 _frcv2 _rmr7s
instagram_more_button = '_8imhp'    # _8imhp _glz1g
instagram_close_preview = '_3eajp'    #_3eajp

instagram_user_account = 'coreSpriteDesktopNavProfile'  #_soakw _vbtk2 coreSpriteDesktopNavProfile
instagram_user_following = '_bkw5z'   #_bkw5z
instagram_following_list = '_4zhc5 notranslate _j7lfh' #_4zhc5 notranslate _j7lfh
#Instagram - Minutes before like? Like a photo after 60 mins?
#
instagram_first_photo_link = '_t5r8b'   # _8mlbc _vbtk2 _t5r8b
instagram_search_term = '_totu9' #_totu9
instagram_photo_username = '_4zhc5'  #_4zhc5 notranslate _ook48
instagram_photo_no_likes = '_kkf84' # _kkf84 _oajsw
instagram_photo_likes = '_oajsw'  # _tf9x3   div-_iuf51 _oajsw  If Views Section - _tfkbw _d39wz   Div - _iuf51 _3sst1
instagram_photo_like_button = '_1tv0k'  #_ebwb5 _1tv0k
instagram_next_photo = 'coreSpriteRightPaginationArrow'   #_de018 coreSpriteRightPaginationArrow

inst_user_name = '_i572c' #_i572c 
inst_user_details = '_s53mj' #_s53mj _13vpi
global ins_user_exists_len
ins_user_exists_len = 0
instagram_follow_user_switch = 'false'

Keys_Control = '\ue009'
Keys_Enter = '\ue007'
Keys_Shift = '\ue008'
Keys_Down = '\ue015'

if login_method == 'Username':
	print('Logging In')
	time.sleep(pause_amount)
	element_exists('class','_fcn8k','click','') 
	#button_exists_click('_fcn8k')
	#login_button = driver.find_element_by_class_name('_fcn8k')
	#login_button.click()

	print('Entering Username:',username)
	element_exists('name','username','input',username)
	#time.sleep(pause_amount)
	#username_input = driver.find_element_by_name('username')
	#username_input.send_keys(username)

	print('Entering Password:',password)
	element_exists('name','password','input',password)
	time.sleep(pause_amount)
	#password_input = driver.find_element_by_name('password')
	#password_input.send_keys(password)

	print('Pressing Login')
	#time.sleep(pause_amount)
	button_exists_click(username_login_button)
	time.sleep(pause_amount)
	#login_button = driver.find_element_by_class_name(username_login_button)
	#login_button.click()

if login_method == 'facebook':

	# button class = _ah57t _84y62 _i46jh _rmr7s
	# span class = coreSpriteFacebookIconInverted _a0z3x

	print('Logging in with Facebook')
	login_button = driver.find_element_by_class_name('_a0z3x')
	login_button.click()

	print('Entering Username')
	username_input = driver.find_element_by_name(facebook_username)
	username_input.send_keys(username)

	print('Entering Password')
	password_input = driver.find_element_by_name(facebook_password)
	password_input.send_keys(password)

	print('Pressing Login')
	time.sleep(pause_amount)
	login_button = driver.find_element_by_id(facebook_login_button)
	login_button.click()

#time.sleep(10)
print('Unfollowing')
#unfollowing_all()


print('Unfollowed')


#sql = 'SELECT * FROM lr_instagram.instagram_tags_to_hit WHERE User_ID = '+str(User_To_Run)+' and Record_No = 3'
sql = 'SELECT * FROM lr_instagram.instagram_tags_to_hit WHERE User_ID = '+str(User_To_Run)
search_term.execute(sql)

for row in search_term:
	instagram_search_category = row['Tag']
	likes_to_hit = int(row['Likes_Per_Day'])
	follows_to_hit = int(row['Follows_Per_Day'])
	follow_ratio = int(row['Follow_Ratio'])
	print('Running')
	driver.get(url)
	
	print(username,': Hitting :',instagram_search_category,':',likes_to_hit)

	print('Screenshot')
	driver.get_screenshot_as_file('search.png')

	#time.sleep(pause_amount)
	print('Pressing Search')
	#driver.save_screenshot('screenshot.png')
	#search_input = driver.find_element(By.XPATH, '//span[text()="Search"]')
	button_exists_click(instagram_search_button)

	print('Entering Search:',instagram_search_category)
	#pausing()

	search_input = driver.find_elements_by_class_name(instagram_search_input)
	#print('Length:',len(search_input))
	while len(search_input) < 1:
		#pausing()
		#print('Looking for Element',instagram_search_input,end='')
		search_input = driver.find_elements_by_class_name(instagram_search_input)
		#print('Length:',len(photo_user))

	if len(search_input) >= 1:
		#print('Running')
		search_input = driver.find_element_by_class_name(instagram_search_input)

	search_input = driver.find_element_by_class_name(instagram_search_input)
	search_input.send_keys(instagram_search_category)


	search_ready = driver.find_elements_by_class_name(instagram_search_ready)
	#print('Length:',len(search_ready))
	while len(search_ready) < 1:
		#pausing()
		#print('Waiting For Search',instagram_search_ready,end='')
		search_ready = driver.find_elements_by_class_name(instagram_search_ready)
		#print('Length:',len(photo_user))

	if len(search_ready) >= 1:
		#print('Pressing Enter')
		search_ready = driver.find_element_by_class_name(instagram_search_ready)

	search_input.send_keys(u'\ue007')

	#button_exists_click(instagram_more_button)
	print('Is this a search Term?')

	element_exists('class',instagram_search_term,'next','') 

	#pausing()
	continue_script = 'No'
	while continue_script != 'Yes':
		print('Clicking First Image')
		#button_exists_click(instagram_first_photo_link)
		#time.sleep(pause_amount)
		element_exists('class',instagram_first_photo_link,'click','') 

		#first_photo = driver.find_element_by_class_name(instagram_first_photo_link)
		#first_photo.click()
		#print('Has Photo been clicked?')
		element_exists('class','_d20no','next','')   # _n3cp9 _d20no

		#print('Continue?:',continue_script)

	likes_hit = 0

	while likes_hit <= likes_to_hit:

		print('***********************',likes_hit,'/',likes_to_hit,'for',instagram_search_category,'****************************************')
		#time.sleep(pause_amount)
		print('Looking at Photo Details')

		#photo_present = driver.find_elements_by_class_name('_22yr2')          #_22yr2 _e0mru
		#element_exists('_22yr2')

		element_exists('class',instagram_photo_username,'next','')

		photo_user = driver.find_elements_by_class_name(instagram_photo_username)
		
		print('Checking User Exists:',instagram_photo_username)


############### Checking User Exists

		#photo_user = driver.find_elements_by_class_name(instagram_photo_username)
		#print('Length:',len(photo_user))
		
		while len(photo_user) < 1:
			#pausing()
			#print('Looking for Element',instagram_photo_username,end='')
			photo_user = driver.find_elements_by_class_name(instagram_photo_username)
			#print('Length:',len(photo_user))

		if len(photo_user) >= 1:
			photo_user = driver.find_element_by_class_name(instagram_photo_username)
			#print(photo_user.text)
			ins_user_name = photo_user.text


			#print('Next:',photo_user)
			#photo_user.click() 
		ins_user_exists()
		#print(ins_user_exists_len)
		#button_exists_click(instagram_photo_username)

		#print('User',photo_user.text)
		#photo_user.click()

		base = driver.window_handles
		focus = driver.current_window_handle
		#print(base,focus)

		#print('Opening User Page to Check Stats:')
		photo_user.send_keys(u'\ue009' + u'\ue007')
		#pausing()

		base = driver.window_handles
		focus = driver.current_window_handle
		#print(base,focus)

		print('User Windows Open:',len(base),'(This should be 2)')
		while len(base) < 2:
			base = driver.window_handles

		driver.switch_to.window(base[1])

		element_exists('class',inst_user_name,'next','') 
		user_name = driver.find_element_by_class_name(inst_user_name)
		print('Username:',user_name.text)

		ins_user_name = user_name.text

		#print('Looking at',ins_user_name)

		element_exists('class',inst_user_details,'next','') 
		user_details = driver.find_elements_by_class_name(inst_user_details)

		user_posts = user_details[0].text
		user_followers = user_details[1].text
		user_following = user_details[2].text

		#print(user_posts)
		#print(user_followers)
		#print(user_following)

		#for elem , value in enumerate(user_details):
			#print(user_details[elem].text)

		#fix_variables

		user_posts = user_posts[:user_posts.find(' ')]
		user_posts = user_posts.replace(',', '')
		user_posts = user_posts.replace('.', '')

		if user_posts.find('m') > 0:
			user_posts = user_posts.replace('m', '')
			user_posts = (int(user_posts) * int(1000000))
		elif user_posts.find('k') > 0:
			user_posts = user_posts.replace('k', '')
			user_posts = (int(user_posts) * int(1000))

		user_posts = int(user_posts)

		user_followers = user_followers[:user_followers.find(' ')]
		user_followers = user_followers.replace(',', '')
		user_followers = user_followers.replace('.', '')

		#print('k?',user_followers.find('k'))
		#print('m?',user_followers.find('m'))
		if user_followers.find('m') > 0:
			user_followers = user_followers.replace('m', '')
			user_followers = (int(user_followers) * int(1000000))
		elif user_followers.find('k') > 0:
			user_followers = user_followers.replace('k', '')
			user_followers = (int(user_followers) * int(1000))

		user_followers = int(user_followers)

		user_following = user_following[:user_following.find(' ')]
		user_following = user_following.replace(',', '')
		user_following = user_following.replace('.', '')

		if user_following.find('m') > 0:
			user_following = user_following.replace('m', '')
			user_following = (int(user_following) * int(1000000))
		elif user_following.find('k') > 0: 
			user_following = user_following.replace('k', '')
			user_following = (int(user_following) * int(1000))

		user_following = int(user_following)

		print('Fixed_User_Posts =',user_posts)
		print('Fixed_User_Followers =',user_followers)
		print('Fixed_User_Following = ',user_following)

		update_ins_user()

		if user_followers < 2000:
			#print('Going to Follow',ins_user_name)
			if instagram_follow_user_switch == 'true':
				follow()

			#pausing()
			#photo_like_button = driver.find_element_by_class_name(instagram_follow_button)
			#photo_like_button.click()

		user_exists = 0	
		
		print('User Window Closed')
		driver.close()



		base = driver.window_handles

		while len(base) > 1:
			base = driver.window_handles

		#pausing()
		driver.switch_to.window(base[0])
		base = driver.window_handles
		focus = driver.current_window_handle
		#print(base,focus)
		#pausing()
	    #print('Closed?')

		#print(user_followers.find('m'))
		#print(user_following.find(' '))
		#user_number = user_followers[:user_followers.find(' ')]
		#user_number_strip = user_number.replace(',', '')

		#print(user_number)
		#print(user_number_strip)

		if user_followers < 2000:

			#Might need to put an upper limit on the number of people someone will follow???

			print('Checking Photo')
			
			#pausing()
			
			#photo_no_likes = driver.find_elements_by_class_name(instagram_photo_no_likes)
			#print('Length of Likes?:',len(photo_no_likes))

			#if len(photo_no_likes) < 1:
			photo_likes = driver.find_elements_by_class_name(instagram_photo_likes)

			print('Photo Present:',len(photo_likes))
			#photo_likes = driver.find_elements_by_class_name('tyrh')
			#photo_likes.click

			if len(photo_likes) < 1:
				print('No Photo, can''t like')


			else:  
				photo_likes = driver.find_element_by_class_name(instagram_photo_likes)
		        
				print('Photo Likes:',photo_likes.text)

				#time.sleep(pause_amount)
				print('Liking Photo')
				button_exists_click(instagram_photo_like_button)
			#photo_like_button = driver.find_element_by_class_name(instagram_photo_like_button)
			#photo_like_button.click()

				likes_hit = likes_hit + 1
		else:
			print('No use liking or following!!!!!!!!!!!!!!!!')

		#pausing()
		#print('Next Photo')

		#try:
			#photo_next_button = driver.find_element_by_class_name(instagram_next_photo) 
		#except NoSuchElementException:
			#driver.find_element_by_class_name(instagram_close_preview)



		photo_next_button = driver.find_elements_by_class_name(instagram_next_photo)
		print(len(photo_next_button))
		if len(photo_next_button) == 1:
			button_exists_click(instagram_next_photo)
			print('Next Photo')
			#photo_next_button = driver.find_element_by_class_name(instagram_next_photo)
			#print('Next:',photo_next_button)
			#photo_next_button.click() 
		else:
			print('Done')
			#button_exists_click(instagram_close_preview)
			#photo_next_button = driver.find_element_by_class_name(instagram_close_preview)
			#print('Exiting:')
			#photo_next_button.click() 
			likes_hit = likes_to_hit + 1
print('End')
driver.quit();
