from django.shortcuts import render, HttpResponseRedirect
from sales.forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import get_object_or_404
from sales import models
#from datetime import datetime, timezone
import numpy as np
from kmeans.kmeans_functions import elbow_kmeans
from background_task import background
import random

# Create your views here.

#View relativa ad homepage
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('login'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


#@background(schedule=10)
def run_kmeans():

    print('Started')

    # Students objects
    students = models.StudentProfile.objects.all()

    # Students' favourite subjects list
    students_matrix = []

    # For each student, we create a numpy array that contains the values referred to the different subjects
    for s in students:
        # Extraction of interesting titles and wishlist books
        s_int_titles = s.user.interesting_titles.all()
        s_wishes = s.user.wishlist_books.all()

        # List for the subject values
        s_values_list = [0, 0, 0, 0, 0, 0, 0, 0]

        # Values update due to interesting titles
        for i in s_int_titles:
            if i.title.category == 'FIS':
                s_values_list[0] += 5
            elif i.title.category == 'MAT':
                s_values_list[1] += 5
            elif i.title.category == 'INF':
                s_values_list[2] += 5
            elif i.title.category == 'MEC':
                s_values_list[3] += 5
            elif i.title.category == 'EN':
                s_values_list[4] += 5
            elif i.title.category == 'ECO':
                s_values_list[5] += 5
            elif i.title.category == 'AUT':
                s_values_list[6] += 5
            elif i.title.category == 'STA':
                s_values_list[7] += 5

        # Values update due to wishlist books
        for w in s_wishes:
            if w.ad.title.category == 'FIS':
                s_values_list[0] += 2
            elif w.ad.title.category == 'MAT':
                s_values_list[1] += 2
            elif w.ad.title.category == 'INF':
                s_values_list[2] += 2
            elif w.ad.title.category == 'MEC':
                s_values_list[3] += 2
            elif w.ad.title.category == 'EN':
                s_values_list[4] += 2
            elif w.ad.title.category == 'ECO':
                s_values_list[5] += 2
            elif w.ad.title.category == 'AUT':
                s_values_list[6] += 2
            elif w.ad.title.category == 'STA':
                s_values_list[7] += 2

        students_matrix.append(s_values_list)

    s_values = np.array(students_matrix, dtype=float)

    prova = s_values.shape

    clusters, _, k = elbow_kmeans(s_values, 10)

    for i in range(len(students)):
        students[i].cluster_number=clusters[i]
        students[i].save()


def first_page(request, username):
    #User who is entering the page
    c = get_object_or_404(User, username=username)

    current = c.profile

    #Get info about the previous clustering algorithm runs
    clustering_runs = models.ClusteringInfo.objects.all()

    #If the clustering algorithm has never been run, then run it
    if(clustering_runs.count() == 0):
        # A new clustering run object is saved in order to avoid new runs by other users
        new_run = models.ClusteringInfo()
        new_run.save()
        # Elbow k-means
        run_kmeans()

    #If the last execution of the algorithm was more than 1h ago, then run the algorithm
    elif(((timezone.now()-clustering_runs.latest('run_time').run_time).total_seconds())>3600):
        # A new clustering run object is saved in order to avoid new runs by other users
        new_run = models.ClusteringInfo()
        new_run.save()
        # Elbow k-means
        run_kmeans()

    #Cluster number of the current student
    c_number = current.cluster_number

    #Students of the same cluster
    #same_cluster_entries = models.Cluster.objects.filter(cluster_number=c_number)
    similar_students = models.StudentProfile.objects.filter(cluster_number=c_number)

    #Lists for similar students' interesting titles and wishlist books
    int_titles = {}
    wish_ads = {}

    for student in similar_students:

        wishes = student.user.wishlist_books.all()
        interests = student.user.interesting_titles.all()

        #Wishes selection
        #if(wishes.count() != 0):
        for wish in wishes:

            if wish in wish_ads.keys():
                wish_ads[wish] += 1
            else:
                wish_ads[wish] = 1

        #Interests selection
        for interest in interests:

            if interest in int_titles.keys():
                int_titles[interest] += 1
            else:
                int_titles[interest] = 1

    #Wishes and interests sorting


    try:
        ordered_wishes = list(sorted(wish_ads, key=wish_ads.__getitem__, reverse=True))
        ordered_interests = list(sorted(int_titles, key=int_titles.__getitem__, reverse=True))
    except:
        ordered_wishes = None
        ordered_interests = None

    #Wishes and interests mix
    final_wishes = []

    #For the first 10 interests, the first ad is chosen
    int_wishes_count = 0
    for i in range(min(10, len(ordered_interests))):
        final_wishes.append(ordered_interests[i].title.annunci_titolo.all()[0])
        int_wishes_count += 1
    for j in range(min(20-int_wishes_count, len(ordered_wishes))):
        final_wishes.append(ordered_wishes[j].ad)

    #The selected ads are passed to the home template
    return render(request, 'first_page.html', {'ads': final_wishes, 'count': len(final_wishes)})

'''
def first_page(request, username):
    #User who is entering the page
    c = get_object_or_404(User, username=username)

    current = c.profile

    #Get info about the previous clustering algorithm runs
    clustering_runs = models.ClusteringInfo.objects.all()

    #If the clustering algorithm has never been run, then run it
    if(clustering_runs.count() == 0):
        # A new clustering run object is saved in order to avoid new runs by other users
        new_run = models.ClusteringInfo()
        new_run.save()
        # Elbow k-means
        run_kmeans()

        #Check user's wishlist
        c_wishlist = c.wishlist_books.all()
        c_int_titles = c.interesting_titles.all()

        if len(c_wishlist) >= 10:
            # The selected ads are passed to the home template
            return render(request, 'first_page.html', {'ads': c_wishlist})

        elif len(c_int_titles) > 0:

            final_wishes = []

            for i in range(min(5, len(c_int_titles))):

                for ad in c_int_titles[i].title.annunci_titolo.all():
                    final_wishes.append(ad)

            # The selected ads are passed to the home template
            return render(request, 'first_page.html', {'ads': final_wishes})

        else:

            final_wishes = []

            for wish in c_wishlist:
                final_wishes.append(wish)

            other_ads = models.BookAd.objects.all()

            while len(final_wishes) < 10:

                obj = other_ads[random.randint(0, len(other_ads)-1)]

                if obj not in final_wishes:
                    final_wishes.append(obj)

            # The selected ads are passed to the home template
            return render(request, 'first_page.html', {'ads': final_wishes})


    #If the last execution of the algorithm was more than 1h ago, then run the algorithm
    if(((timezone.now()-clustering_runs.latest('run_time').run_time).total_seconds())>3600):
        # A new clustering run object is saved in order to avoid new runs by other users
        new_run = models.ClusteringInfo()
        new_run.save()
        # Elbow k-means
        run_kmeans()

    #Cluster number of the current student
    c_number = current.cluster_number

    #Students of the same cluster
    #same_cluster_entries = models.Cluster.objects.filter(cluster_number=c_number)
    similar_students = models.StudentProfile.objects.filter(cluster_number=c_number)

    #Lists for similar students' interesting titles and wishlist books
    int_titles = {}
    wish_ads = {}

    for student in similar_students:

        wishes = student.user.wishlist_books.all()
        interests = student.user.interesting_titles.all()

        #Wishes selection
        #if(wishes.count() != 0):
        for wish in wishes:

            if wish in wish_ads.keys():
                wish_ads[wish] += 1
            else:
                wish_ads[wish] = 1

        #Interests selection
        for interest in interests:

            if interest in int_titles.keys():
                int_titles[interest] += 1
            else:
                int_titles[interest] = 1

    #Wishes and interests sorting
    try:
        ordered_wishes = list(sorted(wishes, key=wishes.__getitem__, reverse=True))
        ordered_interests = list(sorted(interests, key=interests.__getitem__, reverse=True))
    except:
        ordered_wishes = wishes
        ordered_interests = interests

    #Wishes and interests mix
    final_wishes = []

    #For the first 10 interests, the first ad is chosen
    int_wishes_count = 0
    for i in range(min(10, len(ordered_interests))):
        final_wishes.append(ordered_interests[i].title.annunci_titolo.first())
        int_wishes_count += 1
    for j in range(min(20-int_wishes_count, len(ordered_wishes))):
        final_wishes.append(ordered_wishes[j])

    #The selected ads are passed to the home template
    return render(request, 'first_page.html', {'ads': final_wishes})
'''










