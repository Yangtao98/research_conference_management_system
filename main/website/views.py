from ast import Delete, match_case
from weakref import ref
from django.shortcuts import render, redirect
from .admin_controller import *
from .author_controller import *
from .cc_controller import *
from .reviewer_controller import *
from .testfunctions import *
from .populate import *
from .models import *
#from .forms import *
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.core.files.storage import FileSystemStorage

# Create your views here.
class LoginUI:
    def Login(request):
        if 'user_id' not in request.session:
            if request.POST:
                # email = request.POST['email']
                # password = request.POST['password']
                email = request.POST.get('email')
                password = request.POST.get('password')

                new_login_user_account_controller = LoginUserAccountController
                user_id, user_first_name, user_role = new_login_user_account_controller.authenticate_password(email, password)
                if user_role is not None:
                    match user_role:
                            case "System Admin":
                                request.session['user_id'] = user_id
                                request.session['first_name'] = user_first_name
                                request.session['user_role'] = "System Admin"
                                print('admin login')
                                return redirect('admin-home')
                            case "Author":
                                request.session['user_id'] = user_id
                                request.session['first_name'] = user_first_name
                                request.session['user_role'] = "Author"
                                print('author login')
                                return redirect('author-home')
                            case "Reviewer":
                                request.session['user_id'] = user_id
                                request.session['first_name'] = user_first_name
                                request.session['user_role'] = "Reviewer"
                                print('reviewer login')
                                return redirect('reviewer-home')
                            case "Conference Chair":
                                request.session['user_id'] = user_id
                                request.session['first_name'] = user_first_name
                                request.session['user_role'] = "Conference Chair"
                                print('conference login')
                                return redirect('conference_chair-home')
                            case _:
                                messages.error(request, 'Invalid')
                                request.session['user_id'] = user_id
                                request.session['first_name'] = user_first_name
                                request.session['user_role'] = "Misc"
                                return redirect('miscellaneous_user-home') # change to misc home that has access to only papers for view
                                #request.session['loggedin'] = 'logged-in'

                else:
                    messages.error(request, 'Invalid Username or Password')
                    return render(request,'login.html',{})
            else:
                return render(request,'login.html',{})
        else:
            user_role = request.session['user_role']
            match user_role:
                    case "System Admin":
                        print('admin login')
                        return redirect('admin-home')
                    case "Author":
                        print('author login')
                        return redirect('author-home')
                    case "Reviewer":
                        print('reviewer login')
                        return redirect('reviewer-home')
                    case "Conference Chair":
                        print('conference login')
                        return redirect('conference_chair-home')
                    case _:
                        messages.error(request, 'Invalid')
                        return redirect('miscellaneous_user-home') # change to misc home that has access to only papers for view
                        #request.session['loggedin'] = 'logged-in'

class LogoutUI:
    def Logout(request):
        #try:
        del request.session['user_id']
        del request.session['first_name']
        del request.session['user_role']
        request.session.flush()
            
        # except KeyError:
        #     pass
        #     print("error")
        print("logged out")
        messages.success(request, 'You are now logged out.')
        #return HttpResponse("You're now logged out.")
        return redirect('login')

#-----------------------------------------------------------

class AdminHomeUI:
    def AdminHome(request):
        if request.session.get('user_role') == "System Admin":
            print("admin home loaded")
            
            new_adminhome = AdminHomeController

            if request.method == "POST":
                searched = request.POST.get('searched')

                results = new_adminhome.search_user_profile(searched)

                if results:
                    return render(request, 'admin/admin-home.html' ,{'searched' : searched, 'results': results})
                    
                else:
                    return render(request, 'admin/admin-home.html' , {})

            else:

                userprofiles  = new_adminhome.view_all_user_profile
                context = {'userprofiles' : userprofiles}
                context.update()
                return render(request, 'admin/admin-home.html', {'userprofiles' : userprofiles})
        else:

            return redirect('login')

class AdminCreateUserProfileUI:
    def AdminCreateUserProfile(request):
        if request.session.get('user_role') == "System Admin":
            if request.method == 'POST':
                new_createuserprofile = AdminCreateUserProfileController
                user_role = request.POST.get('profile_name')
                user_desc = request.POST.get('profile_desc')

                status = new_createuserprofile.create_user_profile(user_role, user_desc)
                if status is True:
                    messages.success(request, 'User Profile Successfully created')
                    return redirect('admin-home')

                else:
                    messages.error(request, 'Error')

            return render(request, 'admin/admin-create_user_profile.html', {})

        else:
            return redirect('login')

class AdminViewUserProfileUI:
    def AdminViewUserProfile(request, user_profile_id):
        if request.session.get('user_role') == "System Admin":
            new_viewuserprofile = AdminViewUserProfileController

            targetprofile = new_viewuserprofile.view_user_profile(user_profile_id)

            return render(request, 'admin/admin-view_user_profile.html', {'results': targetprofile})
        else:
            return redirect('login')

class AdminUpdateUserProfileUI:
    def AdminUpdateUserProfile(request, user_profile_id):
        if request.session.get('user_role') == "System Admin":
            new_updateuserprofile = AdminUpdateUserProfileController

            targetprofile = new_updateuserprofile.view_user_profile(user_profile_id)

            if request.method == 'POST':
                user_role = request.POST.get('profile_name')
                profile_desc = request.POST.get('profile_desc')

                if (new_updateuserprofile.update_user_profile(user_profile_id, user_role, profile_desc) == True):
                    messages.success(request, 'User Profile Successfully updated')
                    return redirect('admin-home')

                else:
                    messages.error(request, 'Error')
                    return redirect('admin-home')

            return render(request, 'admin/admin-edit_user_profile.html', {'results': targetprofile})
        else:
            return redirect('login')

# def AdminDeleteUserProfile(request, user_profile_id):
#     if request.session.get('user_role')  == "System Admin":
#         new_viewuserprofile = ViewUserProfile

#         targetprofile = new_viewuserprofile.view_user_profile(user_profile_id)

#         return render(request, 'admin/admin-delete_user_profile.html', {'results': targetprofile})
#     else:
#         return redirect('login')

# def AdminDeleteUserProfileTrue(request, user_profile_id):
#     if request.session.get('user_role') == "System Admin":
#         new_deleteuserprofile = DeleteUserProfile
#         status = new_deleteuserprofile.delete_user_profile(user_profile_id)

#         if status is True:
#             messages.success(request, 'Successfully deleted profile')
#             return redirect('admin-home')

#         else:
#             messages.error(request, 'Error')
#             return redirect('admin-home')
#     else: 
#         return redirect('login')

# def AdminDeleteUserProfileFalse(request):
#     return redirect('admin-home')

class AdminCreateUserAccountUI:
    def AdminCreateUserAccount(request):
        if request.session.get('user_role') == "System Admin":
            new_createuseraccount = AdminCreateUserAccountController
            userprofiles = new_createuseraccount.get_available_user_profile()

            if request.method == 'POST':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                password = request.POST.get('password')
                user_role = request.POST.get('user_profile')

                status = new_createuseraccount.create_user_account(first_name, last_name, email, password, user_role)
                if status is True:
                    messages.success(request, 'User Account Successfully created')
                    return redirect('admin-home')

                else:
                    messages.error(request, 'Error')


            return render(request, 'admin/admin-create_user_account.html', {'userprofiles' : userprofiles})
        else:
            return redirect('login')

class AdminViewUserAccountUI:
    def AdminViewUserAccount(request, user_role_id, user_account_id):
        if request.session.get('user_role') == "System Admin":
            new_viewuseraccount = AdminViewUserAccountController

            targetprofile = new_viewuseraccount.get_user_account_profile_name(user_role_id)
            results  = new_viewuseraccount.view_user_account(user_account_id, targetprofile.profile_name)

            return render(request, 'admin/admin-view_user_account.html', {'results': results})
        else:
            return redirect('login')

class AdminUpdateUserAccountUI:
    def AdminUpdateUserAccount(request, user_account_id, user_role_id):
        if request.session.get('user_role') == "System Admin":
            new_updateuseraccount = AdminUpdateUserAccountController

            targetprofile = new_updateuseraccount.get_user_account_profile_name(user_role_id)
            results  = new_updateuseraccount.view_user_account(user_account_id, targetprofile.profile_name)

            if request.method == 'POST':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                password = request.POST.get('password')

                new_updateuseraccount = AdminUpdateUserAccountController
                if password:
                    if (new_updateuseraccount.update_user_account(user_account_id, first_name, last_name, email, password, targetprofile.profile_name) == True):
                        messages.success(request, 'Successfully updated')
                        return redirect('admin-home')

                    else:
                        messages.error(request, 'Error')
                        return redirect('admin-home')

                else:
                    if (new_updateuseraccount.update_user_account(user_account_id, first_name, last_name, email, targetprofile.profile_name) == True):
                        messages.success(request, 'Successfully updated')
                        return redirect('admin-home')

                    else:
                        messages.error(request, 'Error')
                        return redirect('admin-home')

            return render(request, 'admin/admin-edit_user_account.html', {'results': results})
        else:
            return redirect('login')

# def AdminDeleteUserAccount(request, user_account_id, user_role_id):
#     if request.session.get('user_role') == "System Admin":
#         new_viewuseraccount = ViewUserAccount

#         targetaccount = new_viewuseraccount.get_user_account_profile_name(user_role_id)
#         results  = new_viewuseraccount.view_user_account(user_account_id, targetaccount.profile_name)

#         return render(request, 'admin/admin-delete_user_account.html', {'results': results})
#     else:
#         return redirect('login')

# def AdminDeleteUserAccountTrue(request, user_account_id, user_role_id):
#     if request.session.get('user_role') == "System Admin":
#         new_viewuseraccount = ViewUserAccount

#         targetaccount = new_viewuseraccount.get_user_account_profile_name(user_role_id)

#         new_deleteuseraccount = DeleteUserAccount

#         status = new_deleteuseraccount.delete_user_account(user_account_id, targetaccount.profile_name)

#         if status is True:
#             messages.success(request, 'Successfully deleted account')
#             return redirect('admin-home')

#         else:
#             messages.error(request, 'Error')
#             return redirect('admin-home')
#     else: 
#         return redirect('login')
        
# def AdminDeleteUserAccountFalse(request):
#     return redirect('admin-home')

class AdminSystemAdminUI:
    def AdminSystemAdmin(request):
        if request.session.get('user_role') == "System Admin":
            new_viewuseraccount = AdminViewUserAccountController

            user_role = request.POST.get('user_role')

            if request.method == "POST":
                searched = request.POST['searched']

                new_searchuseraccount = AdminSearchUserAccountController
                results = new_searchuseraccount.search_user_account(searched, "System Admin")

                if results:
                    return render(request, 'admin/admin-system_admin.html' ,{'searched' : searched, 'results': results})
                    
                else:
                    return render(request, 'admin/admin-system_admin.html' , {})

            else:
                u = new_viewuseraccount.view_all_user_account("System Admin") #collect all records from table
                return render(request, 'admin/admin-system_admin.html', {'u':u})
        else:
            return redirect('login')

class AdminAuthorUI:
    def AdminAuthor(request):
        if request.session.get('user_role') == "System Admin":
            new_viewuseraccount = AdminViewUserAccountController

            user_role = request.POST.get('user_role')

            if request.method == "POST":
                searched = request.POST['searched']

                new_searchuseraccount = AdminSearchUserAccountController
                results = new_searchuseraccount.search_user_account(searched, "Author")

                if results:
                    return render(request, 'admin/admin-author.html' ,{'searched' : searched, 'results': results})
                    
                else:
                    return render(request, 'admin/admin-author.html' , {})

            else:
                u = new_viewuseraccount.view_all_user_account("Author") #collect all records from table
                return render(request, 'admin/admin-author.html', {'u':u})
        else:
            return redirect('login')

class AdminReviewerUI:
    def AdminReviewer(request):
        if request.session.get('user_role') == "System Admin":
            new_viewuseraccount = AdminViewUserAccountController

            user_role = request.POST.get('user_role')

            if request.method == "POST":
                searched = request.POST['searched']

                new_searchuseraccount = AdminSearchUserAccountController
                results = new_searchuseraccount.search_user_account(searched, "Reviewer")

                if results:
                    return render(request, 'admin/admin-reviewer.html' ,{'searched' : searched, 'results': results})
                    
                else:
                    return render(request, 'admin/admin-reviewer.html' , {})
            else:
                u = new_viewuseraccount.view_all_user_account("Reviewer") #collect all records from table
                return render(request, 'admin/admin-reviewer.html', {'u':u})
        else:
            return redirect('login')

class AdminConferenceChairUI:
    def AdminConferenceChair(request):
        if request.session.get('user_role') == "System Admin":
            new_viewuseraccount = AdminViewUserAccountController

            user_role = request.POST.get('user_role')

            if request.method == "POST":
                searched = request.POST['searched']

                new_searchuseraccount = AdminSearchUserAccountController
                results = new_searchuseraccount.search_user_account(searched, "Conference Chair")

                if results:
                    return render(request, 'admin/admin-conference_chair.html' ,{'searched' : searched, 'results': results})
                    
                else:
                    return render(request, 'admin/admin-conference_chair.html' , {})
            else: 
                u = new_viewuseraccount.view_all_user_account("Conference Chair") #collect all records from table
                return render(request, 'admin/admin-conference_chair.html', {'u':u})
        else: 
            return redirect('login')

class AdminMiscellaneousUserUI:
    def AdminMiscellaneousUser(request):
        if request.session.get('user_role') == "System Admin":
            new_viewuseraccount = AdminViewUserAccountController

            user_role = request.POST.get('user_role')

            if request.method == "POST":
                searched = request.POST['searched']

                new_searchuseraccount = AdminSearchUserAccountController
                results = new_searchuseraccount.search_user_account(searched, "Misc")

                if results:
                    return render(request, 'admin/admin-miscellaneous_user.html' ,{'searched' : searched, 'results': results})
                    
                else:
                    return render(request, 'admin/admin-miscellaneous_user.html' , {})
            else: 
                u = new_viewuseraccount.view_all_user_account("Miscellaneous User") #collect all records from table
                return render(request, 'admin/admin-miscellaneous_user.html', {'u':u})
        else:
            return redirect('login')


# def AdminUserProfile(request):
#     return render(request, 'admin/admin-user_profile.html', {})
  
#-----------------------------------------------------------
class AuthorHomeUI:
    def AuthorHome(request):
        if request.session.get('user_role') == "Author":
            print("author home loaded")
            
            new_viewpaper = AuthorViewPaperController

            if request.method == "POST":
                searched = request.POST.get('searched')

                new_searchpaper = AuthorSearchPaperController
                results = new_searchpaper.search_paper(searched, request.session.get('user_id'))

                if results:
                    return render(request, 'author/author-home.html' ,{'searched' : searched, 'results': results})
                    
                else:
                    return render(request, 'author/author-home.html' , {})

            else:
                authorpapers  = new_viewpaper.view_all_paper_by_author(request.session.get('user_id'))
                context = {'authorpapers' : authorpapers}
                context.update()
                return render(request, 'author/author-home.html', {'authorpapers' : authorpapers})

        else:
            return redirect('login')
    
#see papers that have been reviewed 
class AuthorReviewedUI:
    def AuthorReviewed(request):
        if request.session.get('user_role') == "Author":
            revcontroller = AuthorReviewedController
            reviews = revcontroller.getreviewd(request.session.get('user_id'))
            
            if request.method=='POST':
                rating = request.POST.get('arating')
                print(rating)
                reviewid = request.POST.get('reviewid')
                print("review_id: ",reviewid)
                
                ratecontroller = AuthorRateController
                status = ratecontroller.rate(rating, reviewid)
                
                if status is True:
                    messages.success(request, 'Successfully rated review')
                    return redirect('author-reviewed')

                else:
                    messages.error(request, 'Error')
            
            return render(request, 'author/author-reviewed.html' , {'reviews':reviews})
        
        else:
            return redirect('login')

class AuthorAddPaperUI:
    def AuthorAddPaper(request):
        if request.session.get('user_role') == "Author":
            newpaper = AuthorAddPaperController
            authors = newpaper.get_available_coauthors(request.session.get('user_id'))

            if request.method == "POST" and request.FILES['file_name']:
                file = request.FILES['file_name']

                papername = request.POST.get('paper_name')
                category = request.POST.get('category')
                coauthors = request.POST.getlist('coauthor')
                print(coauthors)

                new_addpaper = AuthorAddPaperController

                status = new_addpaper.add_paper(papername, request.session.get('user_id'), coauthors, category, file)
                if status is True:
                    messages.success(request, 'Successfully uploaded paper')
                    return redirect('author-home')

                else:
                    messages.error(request, 'Error')
                    #return redirect('author-home')

            else:
                return render(request, 'author/author-add_paper.html', {'authors' : authors})
        else:
            return redirect('login')
    
class AuthorUpdatePaperUI:
    def AuthorUpdatePaper(request, paper_id):
        if request.session.get('user_role') == "Author":
            newupdatepaper = AuthorUpdatePaperController
            currentpaper = newupdatepaper.current_paper(paper_id)

            if currentpaper.submitting_author.user_id == request.session.get('user_id'):

                authors = newupdatepaper.get_available_coauthors(request.session.get('user_id'))
                vp = AuthorViewPaperController
                currentCA = vp.viewpapercoauthor(paper_id)

                if request.method == "POST":
                    file = request.FILES['file_name']

                    print(file)
                    papername = request.POST.get('paper_name')
                    category = request.POST.get('category')
                    coauthors = request.POST.getlist('coauthor')
                    print(coauthors)
                    status = newupdatepaper.update_paper(paper_id, papername, request.session.get('user_id'), coauthors, category, file)

                    if status is True:
                        messages.success(request, 'Successfully updated paper')
                        return redirect('author-home')

                    else:
                        messages.error(request, 'Error')

                else:
                    return render(request, 'author/author-edit_paper.html', {'currentpaper' : currentpaper, 'authors' : authors, 'currentCA':currentCA})

            else:
                return redirect('login')
        else:
            return redirect('login')

class AuthorDeletePaperUI:
    def AuthorDeletePaper(request, paper_id):
        if request.session.get('user_role') == "Author":
            dltpaper = AuthorDeletePaperController
            currentpaper = dltpaper.current_paper(paper_id)

            if currentpaper.submitting_author.user_id == request.session.get('user_id'):
                new_viewpaper = AuthorViewPaperController
                targetpaper = new_viewpaper.view_paper(paper_id)
                targetca = new_viewpaper.viewpapercoauthor(paper_id)
                
                return render(request, 'author/author-delete_paper.html', {'results': targetpaper, 'authors': targetca})
            else:
                return redirect('login')
        
        else:
            return redirect('login')

    def AuthorDeletePaperTrue(request, paper_id):
        if request.session.get('user_role') == "Author":
            dltpaper = AuthorDeletePaperController
            currentpaper = dltpaper.current_paper(paper_id)

            if currentpaper.submitting_author.user_id == request.session.get('user_id'):
                newdeletepaper = AuthorDeletePaperController
                status = newdeletepaper.delete_paper(paper_id)
                
                if status is True:
                    messages.success(request, 'Successfully deleted paper')
                    return redirect('author-home')

                else:
                    messages.error(request, 'Error')
                    return redirect('author-home')

            else:
                return redirect('login')
                    
        else:
            return redirect('login')

    def AuthorDeletePaperFalse(request):
        return redirect('author-home')

class AuthorViewPaperUI:
    def AuthorViewPaper(request, paper_id):
        if request.session.get('user_role') == "Author":
            vpcontroller = AuthorViewPaperController
            currentpaper = vpcontroller.view_paper(paper_id)
            coauthors = vpcontroller.viewpapercoauthor(paper_id)
            
            
            return render(request, 'author/author-view_paper.html',{'currentpaper':currentpaper, 'coauthors':coauthors})
        else:
            return redirect('login')

#-----------------------------------------------------------
class ConferenceChairHomeUI:
    def ConferenceChairHome(request):
        if request.session.get('user_role') == "Conference Chair":
            print("cc home loaded")
            
            pp = ccHomeController
            
            if request.method == "POST":
                searched = request.POST.get('searched')
                results = pp.searchPaper(searched)
                
                if results:
                    return render(request, 'conference_chair/conference_chair-home.html', {'searched':searched, 'results':results})
            else:
                papers = pp.getPaper()
                return render(request, 'conference_chair/conference_chair-home.html', {'papers':papers})
        else:
            return redirect('login')

#page to see reviewer name, max workload, current workload 
class ConferenceChairReviewerUI:
    def ConferenceChairReviewer(request):
        if request.session.get('user_role') == "Conference Chair":
            newWL = viewReviewersController
            rev = newWL.getReviewers()
            
            if rev is not None:
                return render(request, 'conference_chair/conference_chair-reviewer.html', {'rev':rev})
            else:
                return render(request, 'conference_chair/conference_chair-reviewer.html', {})
        else:
            return redirect('login')

class ConferenceChairViewPaperUI:
    def ConferenceChairViewPaper(request, paper_id):
        if request.session.get('user_role') == "Conference Chair":
            newviewpaper = ccViewPaperController
            currentpaper = newviewpaper.getPaper(paper_id)
            info = newviewpaper.getRevWhoBidOnPaper(paper_id)
            arev = newviewpaper.getAssignedTo(paper_id)
            
            newallocate = ccAssignController
            allrev = newallocate.getReviewers()     #display rev in dropdown list

            reviewcomments = newviewpaper.comments(paper_id)
            
            if request.method == "POST": 
                revs = request.POST.getlist('assigned')
                
                status = newallocate.assign(paper_id, revs)
                if status is True:
                    messages.success(request, 'Successfully assigned paper to reviewer(s)')
                    return redirect('conference_chair-home')
                else:
                    messages.error(request, "Error")
                
            else:
                return render(request, 'conference_chair/conference_chair-viewpaper.html', {'currentpaper':currentpaper, 'allrev':allrev, 'info':info, 'arev':arev, 'reviewcomments':reviewcomments})
        else:
            return redirect('login')
    
# page showing list of reviewed papers + cc can accept/decline
class ConferenceChairReviewDoneUI:
    def ConferenceChairReviewDone(request):
        if request.session.get('user_role') == "Conference Chair":
            print("cc reviewed loaded")
            newcon = ccReviewDoneListController
            donelist = newcon.getdone()
            
            if request.method=='POST':
                paper_id = request.POST.get('paper_id')
                print(paper_id)
                pstatus = request.POST.get('pstatus')
                print(pstatus)
                
                ccratecon = ccAcceptDeclineController
                status = ccratecon.rate(paper_id, pstatus)

                if status is True:
                    messages.success(request, 'Successfully accepted/declined paper')
                    return redirect('conference_chair-reviewdone')

                else:
                    messages.error(request, 'Error')
                
            return render(request, 'conference_chair/conference_chair-reviewdone.html', {'donelist':donelist})
            
        else:
            return redirect('login')

#page showing list of accepted/declined papers
class ConferenceChairDoneUI:
    def ConferenceChairDone(request):
        if request.session.get('user_role') == "Conference Chair":
            newcc = ccSeeADController
            done = newcc.getAD()
            
            if done is not None:
                return render(request, 'conference_chair/conference_chair-done.html', {'done':done})
            else:
                return render(request, 'conference_chair/conference_chair-done.html', {})
        else:
            return redirect('login')

#-----------------------------------------------------------
class ReviewerHomeUI:
    def ReviewerHome(request):
        if request.session.get('user_role') == "Reviewer":
            newviewpaper = ReviewerDisplayPapersController
            allpaper = newviewpaper.view_all_paper()
            
            currentid = request.session.get('user_id')
            currentWL = newviewpaper.getmaxwl(currentid)
            
            if request.method == "POST":
                searched = request.POST.get('searched')
                
                searchcontroller = ReviewerSearchPaperController
                results = searchcontroller.searchpaper(searched)
            
                if results:
                    context = {'searched' : searched, 'results': results,'allpaper':allpaper,'currentWL':currentWL}
                    context.update()
                    return render(request, 'reviewer/reviewer-home.html', context)
                else:
                    return render(request, 'reviewer/reviewer-home.html', {})
            else:
                return render(request, 'reviewer/reviewer-home.html', {'currentWL':currentWL, 'allpaper':allpaper})
            
        else:
            return redirect('login')

#see papers reviewer bid on
class ReviewerBidUI:
    def ReviewerBid(request):
        if request.session.get('user_role') == "Reviewer":
            print("reviewer-bid page loaded")
            newviewbid = ReviewerBidController
            allbid = newviewbid.view_all_bids(request.session.get('user_id'))

            currentWL = newviewbid.getmaxwl(request.session.get('user_id'))
            print(currentWL)
            
            if request.method == "POST":
                searched = request.POST.get('searched')
                
                searchcontroller = ReviewerSearchPaperController
                results = searchcontroller.searchpaper2(searched, request.session.get('user_id'))
            
                if results:
                    context = {'searched' : searched, 'results': results, 'allbid':allbid, 'currentWL':currentWL}
                    context.update()
                    return render(request, 'reviewer/reviewer-bid.html', context)
                else:
                    return render(request, 'reviewer/reviewer-bid.html', {})
            else:
                context = {'allbid':allbid, 'currentWL':currentWL}
                context.update()
                return render(request, 'reviewer/reviewer-bid.html', context)
            
        else:
            return redirect('login')

# see papers allocate to me to review
class ReviewerReviewUI:
    def ReviewerReview(request):
        if request.session.get('user_role') == "Reviewer":
            print("reviewer-review page loaded")
            revcontroller = ReviewerReviewController
            currentWL = revcontroller.getmaxwl(request.session.get('user_id'))
            print(currentWL)
            
            mybids = revcontroller.getmybids(request.session.get('user_id'))
        
            if request.method == "POST":
                searched = request.POST.get('searched')
                
                searchcontroller = ReviewerSearchPaperController
                results = searchcontroller.searchpaper3(searched, request.session.get('user_id'))
            
                if results:
                    context = {'searched' : searched, 'results': results, 'mybids':mybids, 'currentWL':currentWL}
                    context.update()
                    return render(request, 'reviewer/reviewer-review.html', context)
                else:
                    return render(request, 'reviewer/reviewer-review.html', {})
            else:
                context = {'mybids':mybids, 'currentWL':currentWL}
                context.update()
                return render(request, 'reviewer/reviewer-review.html', context)
        else:
            return redirect('login')
    
#update reviewer workload page
class ReviewerWorkloadUI:
    def ReviewerWorkload(request):
        if request.session.get('user_role') == "Reviewer":
            
            currentR = request.session.get('user_id')
            updatewl = ReviewerUpdateWorkloadControler
            currentWL = updatewl.getmaxwl(currentR)
            print(currentWL)
            
            if request.method == "POST":
                workload = request.POST.get('maxworkload')
                status = updatewl.updateWL(currentR, workload)
                
                if status is True:
                    messages.success(request, "Successfully updated max workload")
                    return redirect('reviewer-home')
                else:
                    messages.error(request, "error")
                    
            return render(request, 'reviewer/reviewer-workload.html', {'currentWL':currentWL})
        else:
            return redirect('login')
    
class ReviewerViewPaperUI:
    def ReviewerViewPaper(request, paper_id):
        if request.session.get('user_role') == "Reviewer":
            newviewpaper = ReviewerViewPaperController
            currentpaper = newviewpaper.view_paper(paper_id)
            currentWL = newviewpaper.getmaxwl(request.session.get('user_id'))

            reviewcomments = newviewpaper.comments(paper_id)

            allocated = newviewpaper.allocated_anot(paper_id, request.session.get('user_id'))

            if allocated:
                if allocated.rating > 0:
                    print("review before liao")
                    if request.method == "POST" and 'updatereview' in request.POST:
                        editreview = ReviewerUpdateReviewController
                        reviewtext = request.POST.get('review_text')
                        print(reviewtext)
                        reviewrate = request.POST.get('rating_value')
                        print(reviewrate)


                        status = editreview.update_review(paper_id, request.session.get('user_id'), allocated.review_id, reviewtext, reviewrate)
                        print(status)
                        if status is True:
                            messages.success(request, "Successfully updated review")
                            return redirect('reviewer-home')
                        else:
                            messages.error(request, "error")

                    if request.method == "POST" and 'deletereview' in request.POST:
                        newdeletereview = ReviewerDeleteReviewController
                        status = newdeletereview.delete_review(paper_id, request.session.get('user_id'), allocated.review_id)
                        if status is True:
                            messages.success(request, "Successfully deleted review")
                            return redirect('reviewer-home')
                        else:
                            messages.error(request, "error")

                    if request.method == "POST" and 'postreply' in request.POST:
                        newcreatecomment = ReviewerCreateCommentController
                        print("creating reply")
                        review_id = request.POST.get('review_id')
                        comment_id = request.POST.get('comment_id')
                        comment_text = request.POST.get('comment_text')

                        print(review_id)
                        print(comment_id)
                        print(comment_text)

                        status = newcreatecomment.create_comment(paper_id, review_id, comment_id, request.session.get('user_id'), comment_text)
                        if status is True:
                            messages.success(request, "Successfully created a reply")
                            return HttpResponseRedirect("#")
                        else:
                            messages.error(request, "error")

                    if request.method == "POST" and 'deletereply' in request.POST:
                        newdeletecomment = ReviewerDeleteCommentController
                        print("deleting reply")
                        comment_id = request.POST.get('comment_id')

                        print(comment_id)

                        status = newdeletecomment.delete_comment(comment_id)
                        if status is True:
                            messages.success(request, "Successfully deleted a reply")
                            return HttpResponseRedirect("#")
                        else:
                            messages.error(request, "error")

                    if request.method == "POST" and 'editreply' in request.POST:
                        neweditcomment = ReviewerUpdateCommentController
                        print("editting reply")
                        comment_id = request.POST.get('comment_id')
                        comment_text = request.POST.get('comment_text')

                        print(comment_id)
                        print(comment_text)

                        status = neweditcomment.update_comment(comment_id, comment_text)
                        if status is True:
                            messages.success(request, "Successfully editted a reply")
                            return HttpResponseRedirect("#")
                        else:
                            messages.error(request, "error")


                    
                    else:   
                        return render(request, 'reviewer/reviewer-view_paper.html', {'currentpaper':currentpaper,'currentWL':currentWL, 'allocated':allocated, 'reviewcomments':reviewcomments})
                
                elif allocated.rating is 0:
                    print("havent review")
                    if request.method == "POST" and 'submitreview' in request.POST:
                        newaddreview = ReviewerAddReviewController
                        reviewtext = request.POST.get('review_text')
                        print(reviewtext)
                        reviewrate = request.POST.get('rating_value')
                        print(reviewrate)

                        status = newaddreview.add_review(paper_id, request.session.get('user_id'), allocated.review_id, reviewtext, reviewrate)
                        print(status)
                        if status is True:
                            messages.success(request, "Successfully submitted review")
                            return redirect('reviewer-home')
                        else:
                            messages.error(request, "error")

                    if request.method == "POST" and 'deletereview' in request.POST:
                        newdeletereview = ReviewerDeleteReviewController

                        status = newdeletereview.delete_review(paper_id, request.session.get('user_id'), allocated.review_id)

                        if status is True:
                            messages.success(request, "Successfully deleted review")
                            return redirect('reviewer-home')
                        else:
                            messages.error(request, "error")

                    else:   
                        return render(request, 'reviewer/reviewer-view_paper.html', {'currentpaper':currentpaper,'currentWL':currentWL, 'allocated':allocated})
                        
            else:
                bidbeforenot, bidvalue = newviewpaper.bid_before_not(paper_id, request.session.get('user_id'))

                if request.method == "POST" and 'createbid' in request.POST:
                    bidvalue = request.POST.get('bid_value')
                    newaddbid = ReviewerAddBidPaperController
                    status = newaddbid.add_bid(paper_id, request.session.get('user_id'), bidvalue)

                    if status is True:
                        messages.success(request, "Successfully made a bid")
                        return redirect('reviewer-home')
                    else:
                        messages.error(request, "error")


                if request.method == "POST" and 'updatebid' in request.POST:
                    bidvalue = request.POST.get('bid_value')

                    newupdatebidpaper = ReviewerUpdateBidPaperController
                    status = newupdatebidpaper.update_bid(paper_id, request.session.get('user_id'), bidvalue)

                    if status is True:
                        messages.success(request, "Successfully updated bid")
                        return redirect('reviewer-home')
                    else:
                        messages.error(request, "error")

                if request.method == "POST" and 'deletebid' in request.POST:

                    newdeletebidpaper = ReviewerDeleteBidPaperController
                    status = newdeletebidpaper.delete_bid(paper_id, request.session.get('user_id'), bidvalue)

                    if status is True:
                        messages.success(request, "Successfully deleted bid")
                        return redirect('reviewer-home')
                    else:
                        messages.error(request, "error")

                else:   

                    return render(request, 'reviewer/reviewer-view_paper.html', {'currentpaper':currentpaper,'currentWL':currentWL,'bidbeforenot':bidbeforenot, 'bidvalue':bidvalue, 'allocated':allocated})
            
        else:
            return redirect('login')

# def ReviewerComments(request):
#     if request.session.get('user_role') == "Reviewer":
#         return render(request, 'reviewer/reviewer-comments.html', {})
#     else:
#         return redirect('login')

#-----------------------------------------------------------
class MiscellaneousUserHomeUI:
    def MiscellaneousUserHome(request):
        if request.session.get('user_role') == "Misc":
            return render(request, 'miscellaneous_user/miscellaneous_user-home.html', {})
        else:
            return redirect('login')