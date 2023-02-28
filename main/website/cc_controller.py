import profile
from .models import *

from django.db.models import Q, Count
from django.utils import timezone
from multipledispatch import dispatch
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.db.models import Case, When, IntegerField

from django.core.mail import send_mail

class viewReviewersController:
    def getReviewers():
        targets = Reviewer.objects.all().order_by('first_name')
        
        if targets is not None:
            return targets
        else:
            return None
        
class ccHomeController:
    def getPaper():
        targets = Paper.objects.all().order_by('status')
        
        if targets is not None:
            return targets
        else:
            return None
        
    # function not working anyway
    def searchPaper(text):
        findpaper = Paper.objects.filter(
        Q(title__icontains=text)|
        Q(category__icontains=text)|
        Q(submitting_author__first_name__icontains=text)|
        Q(submitting_author__last_name__icontains=text))
        
        if findpaper is not None: 
            print(findpaper.values())
            return findpaper
        else:
            print("Nothing found")
            return None
        
class ccViewPaperController:
    def getPaper(id):
        target_paper = Paper.objects.get(pk=id)

        if target_paper is not None:
            print(target_paper)
            return target_paper
        else:
            print("Nothing found")
            return None
        
    def getRevWhoBidOnPaper(paperid):
        thispaper = Paper.objects.get(pk=paperid)
        bids = Bid.objects.filter(paper=thispaper)
        
        if bids is not None:
            return bids
        else:
            return None
        
    def getAssignedTo(paperid):
        thispaper = Paper.objects.get(pk=paperid)
        arev = Review.objects.filter(paper=thispaper)
        
        if arev is not None:
            return arev
        else:
            return None

    def comments(paper_id):
        targetpaper = Paper.objects.get(pk=paper_id)
        targetcomments = Comment.objects.filter(paper=targetpaper).exclude(rating=0).order_by('-created_at')

        return targetcomments

    def childcomments(comment_id):
        targetcomment = Comment.objects.get(pk=comment_id)
        childcomments = Comment.objects.filter(parent=targetcomment).order_by('-created_at')

        return childcomments
        
class ccAssignController:
    def getReviewers():
        allrev = Reviewer.objects.all().order_by('first_name')
        
        if allrev is not None:
            return allrev
        else:
            return None
        
    def assign(paper_id, reviewers):
        currentpaper = Paper.objects.get(pk=paper_id)
        
        for r in reviewers:
            currentreviewer = Reviewer.objects.get(pk=r) 
            print(currentreviewer)
            
            if not Review.objects.filter(paper=currentpaper, reviewer=currentreviewer).exists():
                newallocation = Review(paper=currentpaper, reviewer=currentreviewer)
                print(newallocation)
                newallocation.save()
                
                currentreviewer.current_workload = currentreviewer.current_workload + 1
                currentreviewer.save()
            
        return True
    
class ccReviewDoneListController:
    def getdone():
        #show only rated and yet to accept/decline papers
        #donelist = Review.objects.exclude(~Q(rating__gt=0, paper__status=0))
        
        donelist = Paper.objects.annotate(
                num_sr=Count(Case(
                    When(child_review__rating=1, then=1),
                    output_field=IntegerField()
                )
                )
                ).annotate(
                num_r=Count(Case(
                    When(child_review__rating=2, then=1),
                    output_field=IntegerField()
                )
                )
                ).annotate(
                num_wr=Count(Case(
                    When(child_review__rating=3, then=1),
                    output_field=IntegerField()
                )
                )
                ).annotate(
                num_bp=Count(Case(
                    When(child_review__rating=4, then=1),
                    output_field=IntegerField()
                )
                )
                ).annotate(
                num_wa=Count(Case(
                    When(child_review__rating=1, then=1),
                    output_field=IntegerField()
                )
                )
                ).annotate(
                num_a=Count(Case(
                    When(child_review__rating=6, then=1),
                    output_field=IntegerField()
                )
                )
                ).annotate(
                num_sa=Count(Case(
                    When(child_review__rating=7, then=1),
                    output_field=IntegerField()
                )
                )
                )

        donelist = donelist.exclude(~Q(child_review__rating__gt=0, status=0))
        
        print(donelist)
        
        # for item in donelist:
        #     print(item)
        #     print(item.num_sr)
        #     print(item.num_r)
        #     print(item.num_wr)
        #     print(item.num_bp)
        #     print(item.num_wa)
        #     print(item.num_a)
        #     print(item.num_sa)


        return donelist

        
class ccAcceptDeclineController:

    def rate(paper_id, ad):
        targetpaper = Paper.objects.get(pk=paper_id)

        targetpaper.status = ad
        targetpaper.save()

        targetauthor = targetpaper.submitting_author
        status = targetpaper.status
        thetext = ""
        if status == 1:
            thetext = "Rejected"
        elif status ==2:
            thetext = "Accepted"

        ccAcceptDeclineController.notify_author_email(targetauthor.email, thetext)
        
        return True
    
    def notify_author_email(email, status_text):
        send_mail(
            'Paper Acceptance/Declination',
            'Your paper has been ' + status_text,
            os.getenv('EMAIL_HOST_USER'),
            [email],
            fail_silently=False,
        )
        print("email sent")     
class ccSeeADController():
    def getAD():
        papers = Paper.objects.filter(status__gt=0).order_by("status").reverse()
        
        if papers is not None:
            return papers
        else:
            return None
