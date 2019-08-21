from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

'''
Student Profile: it contains info about the user that aren't available in User model.
'''
class StudentProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    telephone_number = models.CharField(max_length=16, null=True, blank=True)
    facebook_page = models.URLField(max_length=200, null=True, blank=True)

    MAJORS_NAMES = (
        ('ING_INF_T', 'Ingegneria informatica triennale'),
        ('ING_INF_M', 'Ingegneria informatica magistrale'),
        ('ING_MEC_T', 'Ingegneria meccanica triennale'),
        ('ING_MEC_M', 'Ingegneria meccanica magistrale'),
        ('ING_GES_T', 'Ingegneria gestionale triennale'),
        ('ING_GES_M', 'Ingegneria gestionale magistrale'),

    )

    major = models.CharField(max_length=10, choices=MAJORS_NAMES)
    year_of_study = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], default=1)
    sold_books_number = models.IntegerField(default=0)
    bought_books_number = models.IntegerField(default=0)
    reports_number = models.IntegerField(default=0)
    cluster_number = models.IntegerField(default=0)

    #It defines the string to return with str(s: StudentProfile)
    def __str__(self):
        return str(self.user)

'''
Title: it contains info about a title, which mustn't be confused 
'''
class Title(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True, unique=True)
    name = models.CharField(max_length=10)
    cover_image = models.ImageField(upload_to='title_covers', height_field=None, width_field=None, max_length=100, blank=True, null=True)
    description = models.TextField(max_length=500)
    description_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='descrizioni')
    creation_datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_edit_datetime = models.DateTimeField(auto_now=True, auto_now_add=False)

    CATEGORIES = (
        ('FIS', 'Fisica'),
        ('MAT', 'Matematica'),
        ('INF', 'Informatica'),
        ('MEC', 'Meccanica'),
        ('ELE', 'Elettronica'),
        ('ECO', 'Economia'),
        ('AUT', 'Automazione'),
    )
    category = models.CharField(max_length=3, choices=CATEGORIES)

    #str(t: Title) returns the name of the title
    def __str__(self):
        return self.name

'''
BookAd: it contains info about ads, which are linked to specific titles
'''
class BookAd(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='annunci_titolo')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='annunci_studente')
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    CLASSES = (
        ('A', 'Classe A'),
        ('B', 'Classe B'),
        ('C', 'Classe C'),
        ('D', 'Classe D')
    )
    quality_class = models.CharField(max_length=1, choices=CLASSES)
    publication_datetime = models.DateTimeField(auto_now_add=True)
    last_edit_datetime = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='ads', height_field=None, width_field=None)

    #str(a: BookAd) return title name and seller's name
    def __str__(self):
        return str(self.title) + ' ' + str(self.seller)

'''
Transaction: it contains info about transactions between users
'''
class Transaction(models.Model):
    seller = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='vendite', null=True)
    buyer = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='acquisti', null=True)
    title = models.OneToOneField(Title, on_delete=models.SET_NULL, related_name='vendite_titolo', null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    transaction_datetime = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.seller) + ' -> ' + str(self.buyer) + ': ' + str(self.title)

'''
Wishlist: it contains info about ads that a student likes particularly
'''
class Wishlist(models.Model):

    ad = models.ForeignKey(BookAd, on_delete=models.CASCADE, related_name='wishlist_students')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_books')

    class Meta:
        unique_together = (("ad", "user"),)

'''
InterestingTitle: it contains info about titles that a student likes particularly
'''
class InterestingTitle(models.Model):

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interesting_titles')

    class Meta:
        unique_together = (("title", "user"),)


'''
ClusteringInfo: it contains info about the runs of the clustering algorhythm
'''
class ClusteringInfo(models.Model):
    run_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    #num_clusters = models.IntegerField()