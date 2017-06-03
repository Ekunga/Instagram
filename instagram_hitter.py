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
########################################################################################
from selenium import webdriver
import time
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException 
#import mysqlclient
import pymysql


HOST="instagram.lukerussell.com"     #The host you want to connect to.
USER="lukerussell"    # The database username. 
PASSWORD="Anna1234"    # The database password. 
DATABASE="lr_instagram"    # The database name.

db = pymysql.connect(HOST,USER,PASSWORD,DATABASE,autocommit=True)

cur = db.cursor(pymysql.cursors.DictCursor)
update = db.cursor(pymysql.cursors.DictCursor)
search_term = db.cursor(pymysql.cursors.DictCursor)

User_To_Run = '1'



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

	button_to_click = driver.find_elements_by_class_name(web_element)
	#print('Length:',len(button_to_click))
	while len(button_to_click) < 1:
		#print('Looking for Element')
		button_to_click = driver.find_elements_by_class_name(web_element)

	if len(button_to_click) >= 1:
		button_to_click = driver.find_element_by_class_name(web_element)
		#print('Next:',button_to_click)
		button_to_click.click() 

def pausing():
	print('Pause')
	time.sleep(pause_amount)

def unfollowing_all():
	sql = 'Select * from lr_instagram.instagram_user_follows Where User_ID = 1 and Date_Followed < curdate() and Date_Unfollowed is null'
	cur.execute(sql)


	for row in cur:
		print('Unfollowing:',row['Username'])
		Record_To_Unfollow = row['Record_Number']
		#time.sleep(pause_amount)
		#search_button = driver.find_element_by_class_name(instagram_search_button)
		#search_button.click()

		#print('Entering Search:',row['Username'])
		#time.sleep(pause_amount)
		#search_input = driver.find_element_by_class_name(instagram_search_input)
		#search_input.send_keys(row['Username'])
		#time.sleep(pause_amount)
		#search_input.send_keys(u'\ue007')
		time.sleep(pause_amount)
		user_name = row['Username'] 
		user_url = 'https://www.instagram.com/'+str(user_name)
		print(user_url)
		driver.get(user_url)

		user_unfollow = driver.find_element_by_class_name(instagram_follow_button)
		user_unfollow.click()

		sql = "UPDATE lr_instagram.instagram_user_follows SET Date_Unfollowed=,curdate(), WHERE Record_Number="+str(Record_To_Unfollow)
		update.execute(sql)
		print('SQL Updated',sql)

pause_amount = 2

url = 'https://www.instagram.com/?hl=en'
driver=webdriver.Chrome()
#driver = webdriver.PhantomJS()

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

#Instagram - Minutes before like? Like a photo after 60 mins?
#


instagram_first_photo_link = '_8mlbc'   # _8mlbc _vbtk2 _t5r8b
instagram_photo_username = '_4zhc5'  #_4zhc5 notranslate _ook48
instagram_photo_no_likes = '_kkf84' # _kkf84 _oajsw
instagram_photo_likes = '_tf9x3'  # _tf9x3   div-_iuf51 _oajsw  If Views Section - _tfkbw _d39wz   Div - _iuf51 _3sst1
instagram_photo_like_button = '_1tv0k'  #_ebwb5 _1tv0k
instagram_next_photo = 'coreSpriteRightPaginationArrow'   #_de018 coreSpriteRightPaginationArrow

inst_user_name = '_i572c' #_i572c 
inst_user_details = '_s53mj' #_s53mj _13vpi
global ins_user_exists_len
ins_user_exists_len = 0

Keys_Control = '\ue009'
Keys_Enter = '\ue007'
Keys_Shift = '\ue008'

if login_method == 'Username':
	print('Logging In')
	button_exists_click('_fcn8k')
	#login_button = driver.find_element_by_class_name('_fcn8k')
	#login_button.click()

	print('Entering Username')
	username_input = driver.find_element_by_name('username')
	username_input.send_keys(username)

	print('Entering Password')
	password_input = driver.find_element_by_name('password')
	password_input.send_keys(password)

	print('Pressing Login')
	#time.sleep(pause_amount)
	button_exists_click(username_login_button)
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

print('Unfollowing')
unfollowing_all()

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

	#pausing()
	print('Clicking First Image')
	button_exists_click(instagram_first_photo_link)
	#first_photo = driver.find_element_by_class_name(instagram_first_photo_link)
	#first_photo.click()




	likes_hit = 0

	while likes_hit <= likes_to_hit:

		print('***********************',likes_hit,'/',likes_to_hit,'****************************************')
		#time.sleep(pause_amount)
		#print('Looking at Photo Details')

		photo_user = driver.find_elements_by_class_name(instagram_photo_username)
		#print('Checking User Exists:',instagram_photo_username)


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

		#print('Windows:',len(base))
		while len(base) < 2:
			base = driver.window_handles

		driver.switch_to.window(base[1])

		user_name = driver.find_element_by_class_name(inst_user_name)
		print('Username:',user_name.text)

		ins_user_name = user_name.text

		#print('Looking at',ins_user_name)


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
			follow()

			#pausing()
			#photo_like_button = driver.find_element_by_class_name(instagram_follow_button)
			#photo_like_button.click()

		user_exists = 0	
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
			
			photo_no_likes = driver.find_elements_by_class_name(instagram_photo_no_likes)
			print('No Likes:',len(photo_no_likes))


			if len(photo_no_likes) < 1:
				photo_likes = driver.find_elements_by_class_name(instagram_photo_likes)

				print('Photo Present:',len(photo_likes))
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
