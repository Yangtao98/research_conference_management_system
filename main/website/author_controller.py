import profile
from .models import *

from django.db.models import Q
from django.utils import timezone
from multipledispatch import dispatch
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


class AuthorViewPaperController:

    def view_all_paper_by_author(id):
        target_author = Author.objects.get(pk=id)
        target_papers = Paper.objects.filter(submitting_author=target_author)

        if target_papers is not None:
            print(target_papers)
            return target_papers
        else:
            print("Nothing found")
            return None

    def view_paper(id):
        target_paper = Paper.objects.get(pk=id)

        if target_paper is not None:
            print(target_paper)
            return target_paper
        else:
            print("Nothing found")
            return None
        
    def viewpapercoauthor(id):
        target_paper = Paper.objects.get(pk=id)
        target_coauthor = PaperAuthor.objects.filter(paper = target_paper)
        
        if target_coauthor is not None:
            print(target_coauthor)
            return target_coauthor
        else:
            print("Nothing found")
            return None
        
    

class AuthorSearchPaperController:
    def search_paper(text, author):

        find_paper = Paper.objects.filter(
        Q(title__icontains=text)|
        Q(category__icontains=text)|
        Q(submitting_author__first_name__icontains=text)|
        Q(submitting_author__last_name__icontains=text))
        
        find_paper = find_paper.filter(submitting_author=author)
        if find_paper is not None:

            print(find_paper.values())
            return find_paper

        else:
            print("Nothing found")
            return None

class AuthorAddPaperController:

    def add_paper(title, submitting_author, co_authors, category, file):
        current_author = Author.objects.get(pk=submitting_author)
        print(current_author)
        new_paper = Paper(title=title, submitting_author=current_author, category=category, status=0)
        new_paper.save()
        print(new_paper.title)

        current_paper = Paper.objects.get(pk=new_paper.paper_id)
        current_paper.upload = file
        current_paper.save()
        new_paperauthor = PaperAuthor(paper=current_paper, author=current_author)
        print(new_paperauthor)
        new_paperauthor.save()
        
        # parent_dir = "touchgrass/Papers/"
        # paper_dir_name = str(current_paper.paper_id)
        # filename = str(file)

        # os.path.join(parent_dir, paper_dir_name)
        # os.makedirs(os.path.dirname(str(file)), exist_ok=True)
        # destination = open(os.path, 'wb+')
        # for chunk in file.chunks():
        #     destination.write(chunk)
        # destination.close()

        if not co_authors:
            print("Created paper with no co authors")
            return True

        else:
            for co_author in co_authors:
                current_author = Author.objects.get(pk=co_author)
                print(current_author)
                new_paperauthor = PaperAuthor(paper=current_paper, author=current_author)
                print(new_paperauthor)
                new_paperauthor.save()
            print("Created paper with co authors")
            return True            

    def get_available_coauthors(id):
        allauthors = Author.objects.exclude(pk=id).order_by('first_name')
        return allauthors

class AuthorUpdatePaperController:
    def current_paper(id):
        target_paper = Paper.objects.get(pk = id)

        return target_paper

    def update_paper(id, title, submitting_author, co_authors, category, file):
        target_paper = Paper.objects.get(pk = id)

        target_paper.title = title
        target_paper.category = category

        if file is not None:
            target_paper.upload = file
        
        target_paper.save()
        
        PaperAuthor.objects.filter(paper=target_paper).delete()
        target_author = Author.objects.get(pk = submitting_author)
        new_paperauthor = PaperAuthor(paper=target_paper, author=target_author)
        new_paperauthor.save()

        #new_paperauthor = PaperAuthor(author=current_author, paper=target_paper)
        #print(new_paperauthor)
        #new_paperauthor.save()

        if not co_authors:
            print("Updated paper with no co authors")
            return True

        else:
            for co_author in co_authors:
                current_author = Author.objects.get(pk=co_author)
                print(current_author)
                new_paperauthor = PaperAuthor(paper=target_paper, author=current_author)
                print(new_paperauthor)
                new_paperauthor.save()
            print("Created paper with co authors")
            return True            

    def get_available_coauthors(id):
        allauthors = Author.objects.exclude(pk=id).order_by('first_name')
        return allauthors


class AuthorDeletePaperController:
    def current_paper(id):
        target_paper = Paper.objects.get(pk = id)
        return target_paper
    
    def delete_paper(id):
        target_paper = Paper.objects.get(pk = id)
        # target_paperatable = PaperAuthor.objects.filter(paper=target_paper)
        
        if target_paper is not None:
            target_paper.delete()
            return True
        else:
            return False

class AuthorReviewedController:
    def getreviewd(user_id):
        revs = Review.objects.filter(paper__submitting_author__user_id=user_id)
        revs = revs.exclude(rating=0)
        
        if revs is not None:
            return revs
        else:
            return None
        
class AuthorRateController:
    def rate(rating, reviewid):
        targetreview = Review.objects.get(pk=reviewid)
        targetreview.evaluation = rating
        targetreview.save()
        
        return True