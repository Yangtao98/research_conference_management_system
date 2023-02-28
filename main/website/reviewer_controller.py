import profile
from .models import *

from django.db.models import Q
from django.utils import timezone
from multipledispatch import dispatch
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class ReviewerDisplayPapersController:
    
    def view_all_paper():
        papers = Paper.objects.filter(status=0)
        
        if papers is not None: 
            return papers
        else:
            return None
        
    def view_authors_of_paper(id):
        target_paper = Paper.objects.get(pk = id)
        target_paperatable = PaperAuthor.objects.filter(paper=target_paper)
        if target_paperatable is not None: 
            return target_paperatable
        else:
            return None
        
    def view_paper(id):
        targetpaper = Paper.objects.filter(pk=id)
        
        if targetpaper is not None:
            print(targetpaper)
            return targetpaper
        else:
            return None
        
    def getmaxwl(id):
        wl = Reviewer.objects.filter(pk = id).values_list("max_workload", flat=True)
        wl = wl[0]
        
        if wl is not None:
            return wl
        else:
            return None

class ReviewerViewPaperController:
    def view_paper(id):
        target_paper = Paper.objects.get(pk=id)

        if target_paper is not None:
            print(target_paper)
            return target_paper
        else:
            print("Nothing found")
            return None
        
    def getmaxwl(id):
        wl = Reviewer.objects.filter(pk = id).values_list("max_workload", flat=True)
        wl = wl[0]
        
        if wl is not None:
            return wl
        else:
            return None

    def allocated_anot(paper_id, reviewer_id):
        targetpaper = Paper.objects.get(pk=paper_id)
        targetreviewer = Reviewer.objects.get(pk=reviewer_id)
        targetreview = Review.objects.filter(paper=targetpaper, reviewer=targetreviewer).first()
        print("allocated anot")
        print(targetreview)
        
        if targetreview:
            print("allocated liao")
            return targetreview
        
        else:
            print("havent allocate")
            return None

    def bid_before_not(paper_id, reviewer_id):
        targetpaper = Paper.objects.get(pk=paper_id)
        targetreviewer = Reviewer.objects.get(pk=reviewer_id)

        bid = Bid.objects.filter(paper=targetpaper, reviewer=targetreviewer).first()
        if bid is None:

            return True, 0
        
        else:
            return False, bid.bid_value
        
    # def reviewed_anot(paper_id, reviewer_id):
    #     targetpaper = Paper.objects.get(pk=paper_id)
    #     targetreviewer = Reviewer.objects.get(pk=reviewer_id)
    #     targetreview = Review.objects.filter(paper=targetpaper, reviewer=targetreviewer).first()
    #     print("reviewed anot")
    #     print(targetreview)
        
    #     if targetreview.rating > 0:
    #         print("review liao")
    #         return targetreview
    #     else:
    #         print("havent review")
    #         return None

    def comments(paper_id):
        targetpaper = Paper.objects.get(pk=paper_id)
        targetcomments = Comment.objects.filter(paper=targetpaper).exclude(rating=0).order_by('-created_at')

        return targetcomments

    def childcomments(comment_id):
        targetcomment = Comment.objects.get(pk=comment_id)
        childcomments = Comment.objects.filter(parent=targetcomment).order_by('-created_at')

        return childcomments

class ReviewerAddBidPaperController:


    def add_bid(paper_id, reviewer_id, bid_value):
        targetpaper = Paper.objects.get(pk=paper_id)
        reviewer = Reviewer.objects.get(pk=reviewer_id)

        bid = Bid(paper=targetpaper, reviewer=reviewer, bid_value=bid_value)
        bid.save()

        print("Successfully made bid")
        return True

class ReviewerUpdateBidPaperController:
    def update_bid(paper_id, reviewer_id, bid_value):
        targetpaper = Paper.objects.get(pk=paper_id)
        reviewer = Reviewer.objects.get(pk=reviewer_id)

        bid = Bid.objects.filter(paper=targetpaper, reviewer=reviewer).first()
        bid.bid_value = bid_value
        bid.save()

        print("Successfully updated bid")
        return True

class ReviewerDeleteBidPaperController:
    def delete_bid(paper_id, reviewer_id, bid_value):
        targetpaper = Paper.objects.get(pk=paper_id)
        reviewer = Reviewer.objects.get(pk=reviewer_id)

        bid = Bid.objects.filter(paper=targetpaper, reviewer=reviewer).first()
        bid.delete()

        print("Successfully deleted bid")
        return True

class ReviewerUpdateWorkloadControler:
    
    def updateWL(id, max_wl):
        target_acc = Reviewer.objects.get(user_id = id)
        target_acc.max_workload = max_wl
        
        target_acc.save()
        
        return True
    
    def getmaxwl(id):
        wl = Reviewer.objects.filter(pk = id).values_list("max_workload", flat=True)
        wl = wl[0]
        
        if wl is not None:
            return wl
        else:
            return None

# view my bids page 
class ReviewerBidController:
    
    def view_all_bids(id):
        target_reviewer = Reviewer.objects.get(pk=id)
        bids = Bid.objects.filter(reviewer=target_reviewer)
        
        if bids is not None: 
            return bids
        else:
            return None
        
        
    def getmaxwl(id):
        wl = Reviewer.objects.filter(pk = id).values_list("max_workload", flat=True)
        wl = wl[0]
        
        if wl is not None:
            return wl
        else:
            return None

class ReviewerReviewController:
    
    def getmybids(id):
        mybids = Review.objects.filter(reviewer=id)
        
        if mybids is not None: 
            return mybids
        else:
            return None
        
        
    def getmaxwl(id):
        wl = Reviewer.objects.filter(pk = id).values_list("max_workload", flat=True)
        wl = wl[0]
        
        if wl is not None:
            return wl
        else:
            return None
        
class ReviewerSearchPaperController:
    
    # homepage search
    def searchpaper(text):
        find_paper = Paper.objects.filter(
        Q(title__icontains=text)|
        Q(category__icontains=text)|
        Q(submitting_author__first_name__icontains=text)|
        Q(submitting_author__last_name__icontains=text))

        if find_paper is not None:
            
            print(find_paper.values())
            return find_paper

        else:
            print("Nothing found")
            return None
        
    # my reviews page search 
    def searchpaper2(text, rid):
        find_paper = Paper.objects.filter(
        Q(title__icontains=text)|
        Q(category__icontains=text)|
        Q(submitting_author__first_name__icontains=text)|
        Q(submitting_author__last_name__icontains=text))

        find_paper = find_paper.filter(bid__reviewer=rid)
        
        if find_paper is not None:
            print(find_paper.values())
            return find_paper

        else:
            print("Nothing found")
            return None    
    
    # my reviews page search 
    def searchpaper3(text, rid):
        find_paper = Paper.objects.filter(
        Q(title__icontains=text)|
        Q(category__icontains=text)|
        Q(submitting_author__first_name__icontains=text)|
        Q(submitting_author__last_name__icontains=text))

        find_paper = find_paper.filter(review__reviewer=rid)
        
        if find_paper is not None:
            print(find_paper.values())
            return find_paper

        else:
            print("Nothing found")
            return None

class ReviewerAddReviewController:

    def add_review(paper_id, reviewer_id, review_id, review, rating):
        targetpaper=Paper.objects.get(pk=paper_id)
        targetreview=Review.objects.get(pk=review_id)
        targetreviewer=Reviewer.objects.get(pk=reviewer_id)

        if targetreview.reviewer == targetreviewer:
            targetreview.review = review
            targetreview.rating = rating
            targetreview.created_at = timezone.now()
            targetreview.save()
            
            targetreviewer.current_workload = targetreviewer.current_workload - 1
            targetreviewer.save()

            new_comment = Comment(paper=targetpaper, parent_review=targetreview, parent=None, reviewer=targetreviewer, comment_text=review, rating=rating)
            new_comment.save()

            return True

        else:
            return False
        
class ReviewerUpdateReviewController:
    
    def update_review(paper_id, reviewer_id, review_id, review, rating):
        targetpaper=Paper.objects.get(pk=paper_id)
        targetreview=Review.objects.get(pk=review_id)
        targetreviewer=Reviewer.objects.get(pk=reviewer_id)
        
        if targetreview.reviewer == targetreviewer:
            targetreview.review = review
            targetreview.rating = rating
            targetreview.created_at = timezone.now()
            targetreview.save()
            
            targetreviewer.save()

            targetcomment=Comment.objects.filter(parent_review=targetreview).first()
            if targetcomment:
                targetcomment.comment_text=review
                targetcomment.rating = rating
                targetcomment.save()

            else:
                new_comment = Comment(paper=targetpaper, parent_review=targetreview, parent=None, reviewer=targetreviewer, comment_text=review, rating=rating)
                new_comment.save()

            return True
        else:
            return False

class ReviewerDeleteReviewController:

    def delete_review(paper_id, reviewer_id, review_id):
        targetreview=Review.objects.get(pk=review_id)
        targetreview.review = ""
        targetreview.rating = 0
        targetreview.save()
        
        targetreviewer=Reviewer.objects.get(pk=reviewer_id)
        targetreviewer.current_workload = targetreviewer.current_workload + 1
        targetreviewer.save()

        targetcomment=Comment.objects.filter(parent_review=targetreview).first()
        if targetcomment:
            targetcomment.delete()

        return True

class ReviewerCreateCommentController:

    def create_comment(paper_id, review_id, parent_comment_id, reviewer_id, comment_text):
        targetpaper=Paper.objects.get(pk=paper_id)
        targetreview=Review.objects.filter(review_id=review_id).first()
        targetparent=Comment.objects.filter(comment_id=parent_comment_id).first()
        print(targetpaper)
        targetreviewer=Reviewer.objects.get(pk=reviewer_id)

        new_comment = Comment(paper=targetpaper, parent_review=targetreview, parent=targetparent, reviewer=targetreviewer, comment_text=comment_text)
        new_comment.save()

        return True

class ReviewerUpdateCommentController:

    def update_comment(comment_id, comment_text):
        targetcomment=Comment.objects.get(pk=comment_id)

        targetcomment.comment_text = comment_text
        targetcomment.created_at = timezone.now()

        targetcomment.save()

        return True

class ReviewerDeleteCommentController:

    def delete_comment(comment_id):
        targetcomment=Comment.objects.get(pk=comment_id)

        targetcomment.delete()

        return True