"""touchgrass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website import views
from django.conf import settings
from django.conf.urls.static import static  


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.index, name='index'),
    path('', views.LoginUI.Login, name='login'),
    path('logout/', views.LogoutUI.Logout, name='logout'),
    path('admin-home/', views.AdminHomeUI.AdminHome, name='admin-home'),
    path('admin-create_user_profile/', views.AdminCreateUserProfileUI.AdminCreateUserProfile, name='admin-create_user_profile'),
    path('admin-view_user_profile/<int:user_profile_id>', views.AdminViewUserProfileUI.AdminViewUserProfile, name='admin-view_user_profile'),
    path('admin-edit_user_profile/<int:user_profile_id>', views.AdminUpdateUserProfileUI.AdminUpdateUserProfile, name='admin-edit_user_profile'),
    # path('admin-delete_user_profile/<int:user_profile_id>', views.AdminDeleteUserProfile, name='admin-delete_user_profile'),
    # path('admin-delete_user_profile_true/<int:user_profile_id>', views.AdminDeleteUserProfileTrue, name='admin-delete_user_profile_true'),
    # path('admin-delete_user_profile_false/', views.AdminDeleteUserProfileFalse, name='admin-delete_user_profile_false'),    

    path('admin-create_user_account/', views.AdminCreateUserAccountUI.AdminCreateUserAccount, name='admin-create_user_account'),
    path('admin-view_user_account/<int:user_role_id>/<int:user_account_id>', views.AdminViewUserAccountUI.AdminViewUserAccount, name='admin-view_user_account'),    
    path('admin-edit_user_account/<int:user_role_id>/<int:user_account_id>', views.AdminUpdateUserAccountUI.AdminUpdateUserAccount, name='admin-edit_user_account'),
    # path('admin-delete_user_account/<int:user_role_id>/<int:user_account_id>', views.AdminDeleteUserAccount, name='admin-delete_user_account'),
    # path('admin-delete_user_account_true/<int:user_role_id>/<int:user_account_id>', views.AdminDeleteUserAccountTrue, name='admin-delete_user_account_true'),
    # path('admin-delete_user_account_false/', views.AdminDeleteUserAccountFalse, name='admin-delete_user_account_false'),  

    path('admin-system_admin/', views.AdminSystemAdminUI.AdminSystemAdmin, name='admin-system_admin'),
    path('admin-author/', views.AdminAuthorUI.AdminAuthor, name='admin-author'),
    path('admin-reviewer/', views.AdminReviewerUI.AdminReviewer, name='admin-reviewer'),
    path('admin-conference_chair/', views.AdminConferenceChairUI.AdminConferenceChair, name='admin-conference_chair'),
    path('admin-miscellaneous_user/', views.AdminMiscellaneousUserUI.AdminMiscellaneousUser, name='admin-miscellaneous_user'),

    path('author-home/', views.AuthorHomeUI.AuthorHome, name='author-home'),

    path('author-add_paper/', views.AuthorAddPaperUI.AuthorAddPaper, name='author-add_paper'),
    path('author-view_paper/<int:paper_id>', views.AuthorViewPaperUI.AuthorViewPaper, name='author-view_paper'),   
    path('author-edit_paper/<int:paper_id>', views.AuthorUpdatePaperUI.AuthorUpdatePaper, name='author-edit_paper'),    
    path('author-delete_paper/<int:paper_id>', views.AuthorDeletePaperUI.AuthorDeletePaper, name='author-delete_paper'),   
    path('author-delete_paper_true/<int:paper_id>', views.AuthorDeletePaperUI.AuthorDeletePaperTrue, name='author-delete_paper_true'), 
    path('author-delete_paper_false/', views.AuthorDeletePaperUI.AuthorDeletePaperFalse, name='author-delete_paper_false'), 
    path('author-reviewed/', views.AuthorReviewedUI.AuthorReviewed, name='author-reviewed'), 
    
    path('reviewer-home/', views.ReviewerHomeUI.ReviewerHome, name='reviewer-home'),
    path('reviewer-bid/', views.ReviewerBidUI.ReviewerBid, name='reviewer-bid'),
    path('reviewer-review/', views.ReviewerReviewUI.ReviewerReview, name='reviewer-review'),
    path('reviewer-workload/', views.ReviewerWorkloadUI.ReviewerWorkload, name='reviewer-workload'),
    path('reviewer-view_paper/<int:paper_id>', views.ReviewerViewPaperUI.ReviewerViewPaper, name='reviewer-view_paper'),
    #path('reviewer-comments/', views.ReviewerComments, name='reviewer-comments'),
    
    path('conference_chair-home/', views.ConferenceChairHomeUI.ConferenceChairHome, name='conference_chair-home'),
    path('conference_chair-reviewer/', views.ConferenceChairReviewerUI.ConferenceChairReviewer, name='conference_chair-reviewer'),
    path('conference_chair-reviewdone/', views.ConferenceChairReviewDoneUI.ConferenceChairReviewDone, name='conference_chair-reviewdone'),
    path('conference_chair-viewpaper/<int:paper_id>', views.ConferenceChairViewPaperUI.ConferenceChairViewPaper, name='conference_chair-viewpaper'),
    path('conference_chair-done/', views.ConferenceChairDoneUI.ConferenceChairDone, name='conference_chair-done'),
    
    
    path('miscellaneous_user-home/', views.MiscellaneousUserHomeUI.MiscellaneousUserHome, name='miscellaneous_user-home'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

