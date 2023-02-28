import profile
from .models import *

import sys
import os
import hashlib
import uuid
from django.db.models import Q
from django.utils import timezone
from multipledispatch import dispatch

class AdminHomeController:
    def view_all_user_profile():
        profiles = UserProfile.objects.filter()
        print(profiles.values())

        return profiles

    def search_user_profile(text):
        find_profile_name = UserProfile.objects.filter(Q(profile_name__icontains=text))

        if find_profile_name is not None:
            print("Found: " + text)
            return find_profile_name

        else:
            print("Cannot find: " + text)
            return None

class AdminCreateUserProfileController:

    def create_user_profile(profile_name,profile_desc):
        find_profile_name = UserProfile.objects.filter(profile_name=profile_name).first()

        if find_profile_name is None:
            new_user_profile = UserProfile(profile_name=profile_name, profile_desc=profile_desc)

            new_user_profile.save() #save into db 
            print("Successfully created profile: " + profile_name)
            return True

        else:
            print("Failed to create profile: " + profile_name)
            return False

# class SearchUserProfile:

#     def search_user_profile(text):
#         find_profile_name = UserProfile.objects.filter(Q(profile_name__icontains=text))

#         if find_profile_name is not None:
#             print("Found: " + text)
#             return find_profile_name

#         else:
#             print("Cannot find: " + text)
#             return None

# class ViewAllUserProfile:

#     def view_all_user_profile():
#         profiles = UserProfile.objects.filter()
#         print(profiles.values())

#         return profiles

class AdminViewUserProfileController:
    def view_user_profile(id):
        target_profile = UserProfile.objects.get(pk=id)
        print(target_profile)
        return target_profile

class AdminUpdateUserProfileController:
    def view_user_profile(id):
        target_profile = UserProfile.objects.get(pk=id)
        print(target_profile)
        return target_profile

    def update_user_profile(id, profile_name, profile_desc):
        target_profile = UserProfile.objects.get(pk = id)

        target_profile.profile_name = profile_name
        target_profile.profile_desc = profile_desc
        target_profile.save()

        return True

# class DeleteUserProfile:

#     def delete_user_profile(id):
#         target_profile = UserProfile.objects.get(pk = id)
#         target_profile.delete()

#         return True

# class CreateUserAccount:
   
#     def salting():
#         salt = uuid.uuid4().hex

#         return salt

#     def encrypt(text):
#         salt = CreateUserAccount.salting()
#         hash = hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt

#         return hash

#     def get_available_user_profile():
#         account_profiles = UserProfile.objects.all()

#         return account_profiles

#     def create_user_account(first_name, last_name, email, password, user_role):
        
#         #select statement to check if this user alr exists in db
#         account_email = UserAccount.objects.filter(email=email).first()

#         if account_email is None: 

#             #create object
#             user = UserAccount(first_name = first_name, 
#                         last_name = last_name,
#                         email = email,
#                         password = CreateUserAccount.encrypt(password),
#                         user_role = UserProfile.objects.get(pk=user_role))

#             user.save() #save into db 
            
#             return print('create success user account')

#         else:
#             return print('username taken')

class AdminCreateUserAccountController:
   
    def salting():
        salt = uuid.uuid4().hex

        return salt

    def encrypt(text):
        salt = AdminCreateUserAccountController.salting()
        hash = hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt

        return hash

    def get_available_user_profile():
        account_profiles = UserProfile.objects.all()

        return account_profiles

    def create_user_account(first_name, last_name, email, password, user_role):
        
        match user_role:
                case "System Admin":
                    new_user_account = SystemAdmin
                    print("Creating system admin for: " + first_name + " " + last_name + ", " + email)
                case "Author":
                    new_user_account = Author
                    print("Creating author for: " + first_name + " " + last_name + ", " + email)
                case "Reviewer":
                    new_user_account = Reviewer
                    print("Creating reviewer for: " + first_name + " " + last_name + ", " + email)
                case "Conference Chair":
                    new_user_account = ConferenceChair
                    print("Creating conference for: " + first_name + " " + last_name + ", " + email)
                case _:
                    new_user_account = MiscUser
                    print("Creating miscelleneous user for: " + first_name + " " + last_name + ", " + email)

        #select statement to check if this user alr exists in db
        account_email = new_user_account.objects.filter(email=email).first()

        if account_email is None: 

            #create object
            user = new_user_account(first_name = first_name, 
                        last_name = last_name,
                        email = email,
                        password = AdminCreateUserAccountController.encrypt(password),
                        user_role = UserProfile.objects.get(profile_name=user_role))

            user.save() #save into db 
            print("Successfully created: " + first_name + " " + last_name)
            return True

        else:
            print("Failed to create: " + first_name + " " + last_name)
            return False

# class LoginUserAccount:
#     def salting():
#         salt = uuid.uuid4().hex

#         return salt

#     def encrypt(text):
#         salt = LoginUserAccount.salting()
#         hash = hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt

#         return hash

#     def decrypt(encrypted, text):
#         hash, salt = encrypted.split(':') 
#         #print(hash)
#         #print(hashlib.sha256(salt.encode() + text.encode()).hexdigest())

#         return hash == hashlib.sha256(salt.encode() + text.encode()).hexdigest()

#     def authenticate_password(email, input_password):

#         queryset = UserAccount.objects.filter(email=email).values_list('password','user_role').first()

#         if queryset is None:
#             return False

#         else:
#             if (LoginUserAccount.decrypt(queryset[0], input_password) == True):
#                 return True, queryset[1]
            
#             else:
#                 return False

class LoginUserAccountController:
    def salting():
        salt = uuid.uuid4().hex

        return salt

    def encrypt(text):
        salt = LoginUserAccountController.salting()
        hash = hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt

        return hash

    def decrypt(encrypted, text):
        hash, salt = encrypted.split(':') 
        #print(hash)
        #print(hashlib.sha256(salt.encode() + text.encode()).hexdigest())

        return hash == hashlib.sha256(salt.encode() + text.encode()).hexdigest()

    def authenticate_password(email, input_password):

        queryset1 = SystemAdmin.objects.filter(email=email).first()

        queryset2 = Author.objects.filter(email=email).first()

        queryset3 = Reviewer.objects.filter(email=email).first()

        queryset4 = ConferenceChair.objects.filter(email=email).first()

        queryset5 = MiscUser.objects.filter(email=email).first()
        print(email)
        if queryset1 is not None:
            if (LoginUserAccountController.decrypt(queryset1.password, input_password) == True):
                queryset1.last_login = timezone.now()
                queryset1.save()
                auserprofile = UserProfile.objects.filter(pk = queryset1.user_role.user_profile_id).first()
                return queryset1.user_id, queryset1.first_name, auserprofile.profile_name
            
            else:
                print("Invalid login details")
                return None, None, None

        if queryset2 is not None:
            if (LoginUserAccountController.decrypt(queryset2.password, input_password) == True):
                queryset2.last_login = timezone.now()
                queryset2.save()
                auserprofile = UserProfile.objects.filter(pk = queryset2.user_role.user_profile_id).first()
                print(auserprofile.profile_name)
                return queryset2.user_id, queryset2.first_name, auserprofile.profile_name
            
            else:
                print("Invalid login details")
                return None, None, None

        if queryset3 is not None:
            if (LoginUserAccountController.decrypt(queryset3.password, input_password) == True):
                queryset3.last_login = timezone.now()
                queryset3.save()                
                auserprofile = UserProfile.objects.filter(pk = queryset3.user_role.user_profile_id).first()
                print(auserprofile.profile_name)
                return queryset3.user_id, queryset3.first_name, auserprofile.profile_name
            
            else:
                print("Invalid login details")
                return None, None, None

        if queryset4 is not None:
            if (LoginUserAccountController.decrypt(queryset4.password, input_password) == True):
                queryset4.last_login = timezone.now()
                queryset4.save()
                auserprofile = UserProfile.objects.filter(pk = queryset4.user_role.user_profile_id).first()
                print(auserprofile.profile_name)
                return queryset4.user_id, queryset4.first_name, auserprofile.profile_name
            
            else:
                print("Invalid login details")
                return None, None, None

        if queryset5 is not None:
            if (LoginUserAccountController.decrypt(queryset5.password, input_password) == True):
                queryset5.last_login = timezone.now()
                queryset5.save()
                auserprofile = UserProfile.objects.filter(pk = queryset5.user_role.user_profile_id).first()
                print(auserprofile.profile_name)
                return queryset5.user_id, queryset5.first_name, auserprofile.profile_name
            
            else:
                print("Invalid login details")
                return None, None, None

        else:
            print("How do you even get here")
            return None, None, None


# class SearchUserAccount:
#     def search_user_account(text):
#         find_user_account = UserAccount.objects.filter(
#         Q(first_name__icontains=text)|
#         Q(last_name__icontains=text)|
#         Q(email__icontains=text)|
#         Q(created__icontains=text)|
#         Q(last_login__contains=text))

#         if find_user_account is not None:

#             # for item in find_user_account:
#             #     print(item)

#             return find_user_account.values()

#         else:
#             return print("error")

class AdminSearchUserAccountController:
    def search_user_account(text, user_role):
        match user_role:
            case "System Admin":
                targetuseraccounttype = SystemAdmin
            case "Author":
                targetuseraccounttype = Author
            case "Reviewer":
                targetuseraccounttype = Reviewer
            case "Conference Chair":
                targetuseraccounttype = ConferenceChair
            case _:
                targetuseraccounttype = MiscUser
                
        find_user_account = targetuseraccounttype.objects.filter(
        Q(first_name__icontains=text)|
        Q(last_name__icontains=text)|
        Q(email__icontains=text)|
        Q(created_at__icontains=text)|
        Q(last_login__contains=text))

        if find_user_account is not None:

            # for item in find_user_account:
            #     print(item)
            print(find_user_account.values())
            return find_user_account.values()

        else:
            print("Nothing found")
            return None

class AdminViewUserAccountController:

    def get_user_account_profile_name(id):
        target_profile = UserProfile.objects.get(pk=id)

        return target_profile

    def view_all_user_account(user_role):
        match user_role:
            case "System Admin":
                targetuseraccounttype = SystemAdmin
            case "Author":
                targetuseraccounttype = Author
            case "Reviewer":
                targetuseraccounttype = Reviewer
            case "Conference Chair":
                targetuseraccounttype = ConferenceChair
            case _:
                targetuseraccounttype = MiscUser

        target_accounts = targetuseraccounttype.objects.all().order_by('first_name')

        if target_accounts is not None:
            return target_accounts

        else:
            return None

    def view_user_account(id, user_role):
        match user_role:
            case "System Admin":
                targetuseraccounttype = SystemAdmin
            case "Author":
                targetuseraccounttype = Author
            case "Reviewer":
                targetuseraccounttype = Reviewer
            case "Conference Chair":
                targetuseraccounttype = ConferenceChair
            case _:
                targetuseraccounttype = MiscUser

        target_account = targetuseraccounttype.objects.filter(pk = id).first()

        if target_account is not None:
            return target_account

        else:
            return None
        
    


class AdminUpdateUserAccountController:

    def get_user_account_profile_name(id):
        target_profile = UserProfile.objects.get(pk=id)

        return target_profile

    def view_user_account(id, user_role):
        match user_role:
            case "System Admin":
                targetuseraccounttype = SystemAdmin
            case "Author":
                targetuseraccounttype = Author
            case "Reviewer":
                targetuseraccounttype = Reviewer
            case "Conference Chair":
                targetuseraccounttype = ConferenceChair
            case _:
                targetuseraccounttype = MiscUser

        target_account = targetuseraccounttype.objects.filter(pk = id).first()

        if target_account is not None:
            return target_account

        else:
            return None
            
    def salting():
        salt = uuid.uuid4().hex

        return salt

    def encrypt(text):
        salt = AdminUpdateUserAccountController.salting()
        hash = hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt

        return hash

    def update_user_account(id, first_name, last_name, email, password, user_role):
        match user_role:
            case "System Admin":
                target_account = SystemAdmin.objects.get(pk = id)
            case "Author":
                target_account = Author.objects.get(pk = id)
            case "Reviewer":
                target_account = Reviewer.objects.get(pk = id)
            case "Conference Chair":
                target_account = ConferenceChair.objects.get(pk = id)
            case _:
                target_account = MiscUser.objects.get(pk = id)

        target_account.first_name = first_name
        target_account.last_name = last_name
        target_account.email = email
        target_account.password = AdminUpdateUserAccountController.encrypt(password)
        target_account.save()

        return True

    def update_user_account(id, first_name, last_name, email, user_role):
        match user_role:
            case "System Admin":
                target_account = SystemAdmin.objects.get(pk = id)
            case "Author":
                target_account = Author.objects.get(pk = id)
            case "Reviewer":
                target_account = Reviewer.objects.get(pk = id)
            case "Conference Chair":
                target_account = ConferenceChair.objects.get(pk = id)
            case _:
                target_account = MiscUser.objects.get(pk = id)

        target_account.first_name = first_name
        target_account.last_name = last_name
        target_account.email = email
        target_account.save()

        return True

class AdminDeleteUserAccountController:

    def delete_user_account(id, user_role):
        match user_role:
            case "System Admin":
                target_account = SystemAdmin.objects.get(pk = id)
            case "Author":
                target_account = Author.objects.get(pk = id)
            case "Reviewer":
                target_account = Reviewer.objects.get(pk = id)
            case "Conference Chair":
                target_account = ConferenceChair.objects.get(pk = id)
            case _:
                target_account = MiscUser.objects.get(pk = id)

        if target_account is not None:
            target_account.delete()
            return True

        else:
            return False

# class DeleteUserAccount:

#     def delete_user_account(id, user_role):
#         match user_role:
#                 case '1':
#                     target_account = SystemAdmin.objects.get(pk = id)
#                 case '2':
#                     target_account = Author.objects.get(pk = id)
#                 case '3':
#                     target_account = Reviewer.objects.get(pk = id)
#                 case '4':
#                     target_account = ConferenceChair.objects.get(pk = id)
#                 case _:
#                     target_account = MiscUser.objects.get(pk = id)

#         if target_account is not None:
#             target_account.delete()
#             return True

#         else:
#             return print("Error")