import os
from .models import *
from .admin_controller import *
from .author_controller import *
from .reviewer_controller import *
from .cc_controller import *
import csv
import os
import pandas as pd
import numpy as np
from django.core.files.base import ContentFile, File

#os.environ.setdefault('DJANGO_SETTINGS_MODULE','ProTwo.settings')

import django
django.setup()

import random
from faker import Faker

# def DumpAccounts():
#     df = pd.read_csv('touchgrass/useraccount.csv', sep=r'\s*,\s*', skip_blank_lines=True, header=0)
#     df = df.reset_index()

#     new_create_user_account_controller = AdminCreateUserAccountController
#     count = 0
#     for index, row in df.iterrows():
#         print(new_create_user_account_controller.create_user_account(row['firstName'], row['lastName'], row['email'], row['password'], row['user_role']))
#         print(row['email'])
#         count += 1
        
#     print(count)

# DumpAccounts()

fakegen = Faker()


# def DumpPapers():
#     author = Author.objects.get(pk=1)


#     newaddpaper = AuthorAddPaperController




#     file = open('blankpdf.pdf', 'rb')
#     djangofile = File(file)

#     count = 0

#     for i in range(0, 100):
#         title = fakegen.name()
#         newaddpaper.add_paper(title, 1, [2], "Mass", djangofile)
#         count +=1

#     print(count)

# DumpPapers()

# def DumpAssign():

#     newaddassign = ccAssignController

#     count = 0

#     for i in range(40, 140):
#         print(i)
#         newaddassign.assign(i,[1])
#         count +=1

#     print(count)
    
# DumpAssign()

# def DumpReviews():
#     reviewer = Reviewer.objects.get(pk=1)


#     newaddreview = ReviewerAddReviewController

#     count = 0

#     for i in range(67, 166):
#         review = fakegen.sentence()
#         print(review)
#         currentreview = Review.objects.get(pk=i)
#         newaddreview.add_review(currentreview.paper.paper_id, 1, i, review,  random.randint(1, 7))
#         count +=1

#     print(count + " reviews created")

# DumpReviews()

# def DumpComments():

#     newaddcomment = ReviewerCreateCommentController

#     count = 0

#     for i in range(0, 100):
#         comment = fakegen.sentence()
#         print(comment)

#         newaddcomment.create_comment(1, 18, 9, 1, comment)
#         count +=1

#     print(count)

# DumpComments()