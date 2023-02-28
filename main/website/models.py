from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils.timezone import now
# from model_utils.managers import InheritanceManager
# from polymorphic.models import PolymorphicModel

#create models/class/entity here
parent_dir = "touchgrass/touchgrass/Papers/"

class UserProfile(models.Model):
    user_profile_id = models.BigAutoField(primary_key=True)
    profile_name = models.CharField(max_length=255)
    profile_desc = models.TextField()

    # def __str__(self):
    #     return self.profile_id

    class Meta:
        db_table = 'user_profile'
        managed = True
        #managed = True
    

class UserAccount(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)

    email = models.CharField(max_length=255)

    password = models.CharField(max_length=255)

    user_role = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(default=now, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    #last_login = models.DateTimeField(null=True, blank=True, default=now)

    #objects = InheritanceManager()

    class Meta:
        abstract = True
        #db_table = 'user_account'
        managed = True

    # def __init__(self, first_name, last_name, email, password, user_role):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.email = email
    #     self.password = password
    #     self.user_role = user_role


    # def get_user_role_text(self, user_role):
    #     user_profile = UserProfile
    #     queryset = user_profile.filter(profile_id=user_role).first()
    #     return queryset[1]

    def __str__(self):
        return self.first_name + " " + self.last_name #+ " (" + self.get_user_role + ")"



class SystemAdmin(UserAccount):

    class Meta:
        db_table = 'user_account_system_admin'
        managed = True
        #managed = True


class Author(UserAccount):

    class Meta:
        db_table = 'user_account_author'
        managed = True
        #managed = True


class Reviewer(UserAccount):
    max_workload = models.IntegerField(default=0)
    current_workload = models.IntegerField(default=0)

    class Meta:
        db_table = 'user_account_reviewer'
        managed = True
        #managed = True


class ConferenceChair(UserAccount):

    class Meta:
        db_table = 'user_account_conference_chair'
        managed = True
        #managed = True
        
class MiscUser(UserAccount):

    class Meta:
        db_table = 'user_account_miscellaneous'
        managed = True
        #managed = True

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'touchgrass/Papers/paper_{0}/{1}'.format(instance.paper_id, filename)

class Paper(models.Model):
    paper_id = models.BigAutoField(primary_key=True)
    submitting_author = models.ForeignKey(Author, null = True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    status = models.IntegerField(default=0)

    def status_text(self):
        match self.status:
            case 0:
                return "Pending"
            case 1:
                return "Rejected"
            case 2:
                return "Accepted"

    created_at = models.DateTimeField(default=now, blank=True)
    upload = models.FileField(upload_to=user_directory_path)

    class Meta:
        db_table = 'paper'

class PaperAuthor(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'paper_author'

class Bid(models.Model):
    bid_id = models.BigAutoField(primary_key=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE)
    bid_value = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=now, blank=True)
  
    def bid_value_text(self):
        match self.bid_value:
            case 1:
                return "Somewhat Want"
            case 2:
                return "Want"
            case 3:
                return "Strong Want"

    def status_text(self):
        match self.status:
            case 0:
                return "Pending"
            case 1:
                return "Rejected"
            case 2:
                return "Accepted"
            case 3:
                return "Reviewed"

    class Meta:
        db_table = 'bid'

class Review(models.Model):
    review_id = models.BigAutoField(primary_key=True)
    #bid = models.ForeignKey(Bid, on_delete=models.DO_NOTHING)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='child_review')
    reviewer = models.ForeignKey(Reviewer, on_delete=models.DO_NOTHING)
    review = models.TextField(default="", blank=True)
    rating = models.IntegerField(default=0)
    evaluation = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=now, blank=True)

    def rating_text(self):
        match self.rating:
            case 0:
                return "Unrated"
            case 1:
                return "Strong Reject"
            case 2:
                return "Reject"
            case 3:
                return "Weak Reject"
            case 4:
                return "Borderline Paper"
            case 5:
                return "Weak Accept"
            case 6:
                return "Accept"
            case 7:
                return "Strong Accept"

    def evaluation_text(self):
        match self.evaluation:
            case 0:
                return "Unrated"
            case 1:
                return "*"
            case 2:
                return "**"
            case 3:
                return "***"
            case 4:
                return "****"
            case 5:
                return "*****"



    class Meta:
        db_table = 'review'


class Comment(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    parent_review = models.ForeignKey(Review, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="replies")

    reviewer = models.ForeignKey(Reviewer, on_delete=models.DO_NOTHING)

    comment_text = models.TextField(default="", blank=True)
    rating = models.IntegerField(default=-1, blank=True, null=True)

    created_at = models.DateTimeField(default=now, blank=True)

    def rating_text(self):
        match self.rating:
            case -1:
                return ""
            case 0:
                return ""
            case 1:
                return "Strong Reject"
            case 2:
                return "Reject"
            case 3:
                return "Weak Reject"
            case 4:
                return "Borderline Paper"
            case 5:
                return "Weak Accept"
            case 6:
                return "Accept"
            case 7:
                return "Strong Accept"

    class Meta:
        db_table = 'comment'

# class PaperReview(models.Model): 
#     paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
#     review = models.ForeignKey(Review, on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'paper_review'


# class Comment(models.Model):
#     post = models.ForeignKey(PaperReview,on_delete=models.CASCADE,related_name='comments')
#     name = models.CharField(max_length=80)
#     email = models.EmailField()
#     body = models.TextField()
#     created_on = models.DateTimeField(auto_now_add=True)
#     active = models.BooleanField(default=False)

#     class Meta:
#         ordering = ['created_on']

#     def __str__(self):
#         return 'Comment {} by {}'.format(self.body, self.name)