import warnings
import numpy as np
from kmeans.kmeans_functions import elbow_kmeans
from sales import models
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **options):

        new_run = models.ClusteringInfo()
        new_run.save()

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