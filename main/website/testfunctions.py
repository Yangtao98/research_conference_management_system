from .models import *
from .admin_controller import *
import csv
import os
import pandas as pd

# new_create_profile_controller = CreateUserProfile
# new_create_profile_controller.create_user_profile('System Admin')
# new_create_profile_controller.create_user_profile('Author')
# new_create_profile_controller.create_user_profile('Reviewer')
# new_create_profile_controller.create_user_profile('Conference Chair')
# new_create_profile_controller.create_user_profile('Regular')


# new_create_user_account_controller = AdminCreateUserAccountController
# new_create_user_account_controller.create_user_account('Gabriel', 'White', 'Gabriel@touchgrass.com', '91124201gab', "System Admin")
# new_create_user_account_controller.create_user_account('Blaire', 'White', 'Blaire@touchgrass.com', '91124201gab', "Author")
# new_create_user_account_controller.create_user_account('Hailey', 'Lai', 'Haile@touchgrass.com', '91124201gab', "Reviewer")
# new_create_user_account_controller.create_user_account('Cecilia', 'Lai', 'Cecilia@touchgrass.com', '91124201gab', "Conference Chair")


# def DumpAccounts():
#     df = pd.read_csv('touchgrass/useraccount.csv', sep=r'\s*,\s*', skip_blank_lines=True, header=0)
#     df = df.reset_index()

#     new_create_user_account_controller = AdminCreateUserAccountController
#     count = 0
#     for index, row in df.iterrows():
#         print(new_create_user_account_controller.create_user_account(row['firstName'], row['lastName'], row['email'], row['password'], row['user_role']))
#         print(row['email'])
#         count += 1
        
#     print(count + " accounts created")

# DumpAccounts()






# new_create_user_account_controller.create_user_account('Hailey', 'Lai', 'Haile@touchgrass.com', '91124201g', "System Admin")
# new_create_user_account_controller.create_user_account('Gabriel', 'White', 'Gabriel@touchgrass.com', '91124201gab', "System Admin")
# new_create_user_account_controller.create_user_account('Blaire', 'White', 'Blaire@touchgrass.com', '91124201gab', "Author")

# new_create_user_account_controller.create_user_account('Misc', 'Test', 'misctest@touchgrass.com', 'misc123', "_") #doesnt work this way 


# # new_create_user_account_controller.create_user_account('Gabriel', 'White', 'Gabriel1@touchgrass.com', 'password123', 2)
# # new_create_user_account_controller.create_user_account('Gabriel', 'White', 'Gabriel2@touchgrass.com', 'password1234', 5) 

# new_create_user_account_controller.create_user_account('Bruce', 'Wayne', 'bw123@touchgrass.com', '12bw34', "Author")
# new_create_user_account_controller.create_user_account('Tom', 'H', 'thom@touchgrass.com', 'tomtom123', "Reviewer")
# new_create_user_account_controller.create_user_account('Sun', 'Lee', 'slee@touchgrass.com', 'sleepy123', "Conference Chair")
# new_create_user_account_controller.create_user_account('Tan', 'Jon', 'tjon@touchgrass.com', 'jon123', "System Admin")

# new_create_user_account_controller.create_user_account('Bruce2', 'Wayne', 'bw1233@touchgrass.com', '12bw343', "Author")
# new_create_user_account_controller.create_user_account('Tom2', 'H', 'thom2@touchgrass.com', 'tomtom1232', "Reviewer")
# new_create_user_account_controller.create_user_account('Sun3', 'Lee', 'slee3@touchgrass.com', 's3leepy123', "Conference Chair")
# new_create_user_account_controller.create_user_account('Tan1', 'Jon', '1tjon@touchgrass.com', '2jon123', "System Admin")
# new_create_user_account_controller.create_user_account('Bruce13', 'Wayne', '222bw123@touchgrass.com', '12312bw34', "Author")
# new_create_user_account_controller.create_user_account('Tom', 'H', 'thom123@touchgrass.com', 'tomtom123', "Reviewer")
# new_create_user_account_controller.create_user_account('Sun12', 'Lee', 'slee124@touchgrass.com', '12sleepy123', "Conference Chair")
# new_create_user_account_controller.create_user_account('Tan4', 'Jon', 'tjon444@touchgrass.com', '4jon123', "System Admin")
# new_create_user_account_controller.create_user_account('Bruce24', 'Wayne', 'bw1234@touchgrass.com', '12bw34', "Author")
# new_create_user_account_controller.create_user_account('Tom54', 'H', 'thom45@touchgrass.com', 'tomtom123', "Reviewer")
# new_create_user_account_controller.create_user_account('Sunv', 'Lee', 'sleev@touchgrass.com', 'sleepyv123', "Conference Chair")
# new_create_user_account_controller.create_user_account('Tan7', 'Jon', 'tjon8@touchgrass.com', '8jon123', "System Admin")
# new_create_user_account_controller.create_user_account('Bruce8', 'Wayne', 'bw12398@touchgrass.com', '12bw34', "Author")
# new_create_user_account_controller.create_user_account('Tom9', 'H', 'thom@touchgrass.com', 'tomtom12398', "Reviewer")
# new_create_user_account_controller.create_user_account('Sun98', 'Lee', 'slee98@touchgrass.com', 'sleepy123', "Conference Chair")
# new_create_user_account_controller.create_user_account('Tan0', 'Jon', 'tjon000@touchgrass.com', '0jon123', "System Admin")

# nv = ViewUserProfile
# print(nv.view_user_profile(1))

# new_login_user_account_controller = LoginUserAccount
# print(new_login_user_account_controller.authenticate_password('Gabriel@touchgrass.com', '91124201gab'))
# print(new_login_user_account_controller.authenticate_password('Gabriel1@touchgrass.com', 'password123', '1'))
# print(new_login_user_account_controller.authenticate_password('Gabriel1@touchgrass.com', 'password1234', '1'))
# print(new_login_user_account_controller.authenticate_password('Gabriel1@touchgrass.com', 'password123', '2'))
# print(new_login_user_account_controller.authenticate_password('Gabriel2@touchgrass.com', 'password1234', '1'))
# print(new_login_user_account_controller.authenticate_password('Gabriel2@touchgrass.com', 'password1234', '5'))

# new_login_user_account_controller = LoginUserAccount
# print(new_login_user_account_controller.authenticate_password('Gabriel@touchgrass.com', 'password123'))
# print(new_login_user_account_controller.authenticate_password('Gabriel1@touchgrass.com', 'password123'))
# print(new_login_user_account_controller.authenticate_password('Gabriel1@touchgrass.com', 'password1234'))
# print(new_login_user_account_controller.authenticate_password('Gabriel1@touchgrass.com', 'password123'))
# print(new_login_user_account_controller.authenticate_password('Gabriel2@touchgrass.com', 'password1234'))
# print(new_login_user_account_controller.authenticate_password('Gabriel2@touchgrass.com', 'password1234'))

# new_delete_user_account_controller = DeleteUserAccount

# print(new_delete_user_account_controller.delete_user_account(2))


# new_search_user_profile = SearchUserProfile
# print(SearchUserProfile.search_user_profile('System Admin'))


# new_search_user_account_controller = SearchUserAccount
# print(new_search_user_account_controller.search_user_account("Gabriel"))


# new_submitpaper = SubmitPaper
# new_submitpaper.submit_paper("The First Paper", 1, [], "Inglis")