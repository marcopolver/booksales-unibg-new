from django.shortcuts import render, HttpResponseRedirect
from sales.forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.generic import ListView, TemplateView
from sales import models

#from datetime import datetime, timezone
import numpy as np
from kmeans.kmeans_functions import elbow_kmeans
from background_task import background
import random
import warnings



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
    warnings.filterwarnings("error")

    #print('Started')

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

    #prova = s_values.shape

    clusters = None

    done = False

    while not done:
        try:
            clusters, _, k = elbow_kmeans(s_values, 10)
            done = True
        except RuntimeWarning:
            print("RuntimeWarning")
            done = False

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
    return render(request, 'first_page.html', {'ads': [final_wishes[:4], final_wishes[4:8], final_wishes[8:12], final_wishes[12:16], final_wishes[16:]], 'count': len(final_wishes)})

def ad_details(request, ad_pk):

    # Ad that is going to be shown
    ad = get_object_or_404(models.BookAd, pk = ad_pk)

    return render(request, 'ads.html', {'ad': ad})

def profile(request, username):

    #Get the student profile
    user = get_object_or_404(User, username=username)
    profile = models.StudentProfile.objects.filter(user=user).all()[0]

    return render(request, 'student_profile.html', {'profile': profile})

def search(request):

    return render(request, 'search.html')


def search_users(request):

    majors = [major[0] for major in models.StudentProfile.MAJORS_NAMES]

    return render(request, 'search_student.html', {'majors': majors, 'years': [1,2,3]})


class SearchUsersResults(ListView):

    model = models.StudentProfile
    template_name = 'search_student_results.html'

    def get_queryset(self):
        username_content = self.request.GET.get('username')
        major = self.request.GET.get('major')
        year_of_study = self.request.GET.get('year_of_study')

        users = User.objects.filter(username__icontains=username_content)
        print(users)

        profiles = models.StudentProfile.objects.filter(user__in=users)
        print(profiles)
        object_list = profiles.filter(major=major).filter(year_of_study=year_of_study)
        print(object_list)

        return object_list

