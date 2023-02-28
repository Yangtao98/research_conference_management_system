from django.test import TestCase
from .models import *
from .admin_controller import *

class UserProfileTestCase(TestCase):
    def setUp(self):
        print("creating profiles")
        newadmincreateuserprofile = AdminCreateUserProfileController
        newadmincreateuserprofile.create_user_profile("System Admin", "Ability to create/update user profile and accounts")
        newadmincreateuserprofile.create_user_profile("Author", "Ability to submit papers")
        newadmincreateuserprofile.create_user_profile("Reviewer", "Reviews papers submitted by authors and accepts/rejects them")
        newadmincreateuserprofile.create_user_profile("Conference Chair", "Allocates papers by authors to reviewers for review, then accept/reject based on reviews")
        newadmincreateuserprofile.create_user_profile("Regular", "")
        newadmincreateuserprofile.create_user_profile("Test", "")

        print("end of creating profiles")

    def test_profile(self):
        print("viewing profiles")
        sp = UserProfile.objects.get(profile_name="System Admin")
        ap = UserProfile.objects.get(profile_name="Author")
        rp = UserProfile.objects.get(profile_name="Reviewer")
        cp = UserProfile.objects.get(profile_name="Conference Chair")
        rgp = UserProfile.objects.get(profile_name="Regular")

        self.assertEqual(sp.profile_name, 'System Admin')
        self.assertEqual(ap.profile_name, 'Author')
        self.assertEqual(rp.profile_name, 'Reviewer')
        self.assertEqual(cp.profile_name, 'Conference Chair')
        self.assertEqual(rgp.profile_name, 'Regular') #all pass
        print('all should pass')
        print("end of viewing profiles")

    def test_edit_profile(self):
        print("updating profiles")
        pf1 = UserProfile.objects.get(profile_name="Test")

        newadminedituserprofile = AdminUpdateUserProfileController

        newadminedituserprofile.update_user_profile(pf1.user_profile_id, "NewName", "")

        self.assertEqual(pf1.profile_name, 'Test') 
        print('should fail')#fail

        self.assertEqual(pf1.profile_name, 'NewName')         
        print('should pass')#fail  

        print("end of updating profiles")

class UserAccountTestCase(TestCase):
    def setUp(self):
        print("creating user accounts")
        newadmincreateuseraccount = AdminCreateUserAccountController
        newadmincreateuseraccount.create_user_account('Gabriel', 'White', 'Gabriel@touchgrass.com', '91124201gab', "System Admin")
        newadmincreateuseraccount.create_user_account('Blaire', 'White', 'Blaire@touchgrass.com', '91124201gab', "Author")
        newadmincreateuseraccount.create_user_account('Hailey', 'Lai', 'Haile@touchgrass.com', '91124201gab', "Reviewer")
        newadmincreateuseraccount.create_user_account('Cecilia', 'Lai', 'Cecilia@touchgrass.com', '91124201gab', "Conference Chair")
        newadmincreateuseraccount.create_user_account('Cecilia', 'Lai', 'Cecilia@touchgrass.com', '91124201gab', "Conference Chair")

        newadmincreateuseraccount.create_user_account('Lumine', '', 'Lumine@touchgrass.com', '243f78n5', "Regular")
        #newadmincreateuseraccount.create_user_account('Aether', '', 'Cecilia@touchgrass.com', '5635567h5h6', "Traveler")
        print("end of creating user accounts")


    def test_user_account(self):
        print("viewing user accounts")
        ac1 = SystemAdmin.objects.get(pk=1)
        ac2 = Author.objects.get(pk=1)
        ac3 = Reviewer.objects.get(pk=1)
        ac4 = ConferenceChair.objects.get(pk=1)


        print(ac1.user_id, ac1.user_role.profile_name, ac1.first_name)
        self.assertEqual(ac1.first_name, 'Gabriel')

        print(ac2.user_id, ac2.user_role.profile_name, ac2.first_name)
        self.assertEqual(ac2.first_name, 'Blaire')

        print(ac3.user_id, ac3.user_role.profile_name, ac3.first_name)
        self.assertEqual(ac3.first_name, 'Hailey')    

        print(ac4.user_id, ac4.user_role.profile_name, ac4.first_name)
        self.assertEqual(ac4.first_name, 'Cecilia')
        print('all should pass')
        print("end of viewing user accounts")

    def test_update_user_account(self):
        print("updating user accounts")
        ac2 = Author.objects.get(pk=1)

        newadminedituseraccount = AdminUpdateUserAccountController

        newadminedituseraccount.update_user_account(ac2.user_id, ac2.first_name, ac2.last_name, "gabesojk@gmail.com", "Author")
        
        self.assertEqual(ac2.email, 'Blaire@touchgrass.com') #should fail
        print('should fail')
        self.assertEqual(ac2.email, 'gabesojk@gmail.com') #should pass
        print('should pass')
        print("updating user accounts")

    def test_login_account(self):
        print("login user accounts")
        ac1 = SystemAdmin.objects.get(pk=1)
        ac2 = Author.objects.get(pk=1)
        ac3 = Reviewer.objects.get(pk=1)
        ac4 = ConferenceChair.objects.get(pk=1)

        newloginuseraccountcontroller = LoginUserAccountController

        qr1, qr2, qr3 = newloginuseraccountcontroller.authenticate_password(ac1.email, "91124201gab")
        self.assertEqual(qr1, 1) #should pass
        print('should pass')

        self.assertEqual(qr2, 'Gabriel') #should pass
        print('should pass')

        self.assertEqual(qr3, 'System Admin') #should pass
        print('should pass')

        qr1, qr2, qr3 = newloginuseraccountcontroller.authenticate_password(ac2.email, "91124201gab")
        self.assertEqual(qr1, 1) #should pass
        print('should pass')

        self.assertEqual(qr2, 'Blaire') #should pass
        print('should pass')

        self.assertEqual(qr3, 'Author') #should pass
        print('should pass')
        
        qr1, qr2, qr3 = newloginuseraccountcontroller.authenticate_password(ac2.email, "newpassword")
        self.assertEqual(qr1, 1) #should fail
        print('should fail')

        self.assertEqual(qr2, 'Blaire') #should fail
        print('should fail')

        self.assertEqual(qr3, 'Author') #should fail
        print('should fail')

        print("end of login user accounts")

    
    # def test(self):
    #     self.Test_create_profile()
    #     self.Test_profile()
    #     self.Test_edit_profile

    #     self.Test_create_user_account()
    #     self.Test_user_account()
    #     self.Test_update_user_account()
    #     self.Test_login_account()


