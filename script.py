import random
from sales.models import StudentProfile, Title, BookAd, Wishlist, InterestingTitle
from django.contrib.auth.models import User

names = ['Andrea', 'Antonio', 'Angelo', 'Angela', 'Anna', 'Alice', 'Arianna', 'Alfredo', 'Aurora', 'Barbara', 'Beatrice', 'Carlo', 'Chiara', 
        'Claudio', 'Claudia', 'Carla', 'Clara', 'Camilla', 'Dario', 'Davide', 'Dania', 'Daniele', 'Daniela', 'Elisa', 'Elena', 'Elisabetta', 
        'Ennio', 'Emma','Ernesto', 'Emanuele', 'Fausto', 'Flavio', 'Flavia', 'Franco', 'Francesco', 'Francesca', 'Federico', 'Federica',
        'Fernando', 'Ferdinando', 'Giulia', 'Giulio', 'Giuseppe', 'Giancarlo', 'Gianfranco', 'Gianluigi', 'Gianni', 'Gabriele',
        'Gabriella', 'Hellen', 'Harry', 'Howard', 'Ilenia', 'Irene', 'Imma', 'Jack', 'James', 'John', 'Jennifer', 'Karen', 'Karim',
        'Kevin', 'Leonardo', 'Leo', 'Laura', 'Lisa', 'Lando', 'Marco', 'Matteo', 'Mirko', 'Mattia', 'Maria', 'Marianna', 'Marta',
        'Miriam', 'Melissa', 'Moira', 'Nicola', 'Nicole', 'Nadia', 'Nicoletta', 'Olmo', 'Paola', 'Paolo', 'Qamar', 'Ryan', 'Rachele',
        'Rachid', 'Rosa', 'Sabrina', 'Sara', 'Sofia', 'Stefano', 'Stefania', 'Selene', 'Sarah', 'Tiziano', 'Tiziana', 'Ubaldo',
        'Ugo', 'Vittorio', 'Virginia', 'Vilma', 'Walter', 'Xi Gin', 'Yolanda', 'Zoe', 'Zaccaria', 'Zara']

surnames = ['Belotti', 'Carminati', 'Carrara', 'Cattaneo', 'Cortinovis', 'Rossi', 'Ferrari', 'Mazzoleni', 'Pesenti', 'Milesi', 
            'Ravasio', 'Rota', 'Pellegrini', 'Pellegrinelli', 'Salvi', 'Vitali', 'Manzoni', 'Gritti', 'Previtali', 'Colombo',
            'Ghilardi', 'Villa', 'Carissimi', 'Fustinoni', 'Valsecchi', 'Piffari', 'Calegari', 'Pasotti', 'Pelizzari', 'Polver', 
            'Bianchini', 'Olivieri', 'Fumagalli', 'Rossi', 'De Luca', 'Del Prete', 'Trevisan', 'Zanini', 'Zanetti', 'Trevisan',
            'Sabato', 'Calogiuri', 'Russo', 'Rizzo', 'Izzo']

base_strings = ['mat', 'inf', 'mec', 'ele', 'eco', 'aut', 'sta']
majors = ['ING_INF_T', 'ING_INF_M', 'ING_MEC_T', 'ING_MEC_M', 'ING_GES_T', 'ING_GES_M']
letters = ['A', 'B', 'C', 'D', 'E']
classes = ['A', 'B', 'C', 'D']
description_base = 'Prova'
categories = ['FIS','MAT','INF','MEC','ELE','ECO','AUT','STA']

image_path = 'ads/book.jpg'
seller = User.objects.filter(username='marco').first()

#--------------------------------------------------------------------------------------------------------------

#Creazione utenti
for i in range(800):

    selected_major = majors[random.randint(0, len(majors)-1)]
    user = User(username=selected_major+str(i))
    user.save()
    year = 1

    if 'TRI' in selected_major:
        year = random.randint(1,3)
    else:
        year = random.randint(1,2)

    student = StudentProfile(user=user, name=names[random.randint(0, len(names)-1)], 
                            surname=surnames[random.randint(0, len(surnames)-1)],
                            major=selected_major, year_of_study = year)

    student.save()

#---------------------------------------------------------------------------------------------------

#Creazione titoli
counter = 0
students = StudentProfile.objects.all()

for i in range(150):

    nome = 'Titolo_' + str(counter)
    counter = counter + 1

    titolo = Title(isbn=str(counter), name=nome, description='Titolo', 
                description_author=students[random.randint(0, len(students)-1)].user,
                category = categories[random.randint(0, len(categories)-1)])
    
    titolo.save()

#Creazione annunci
titoli = Title.objects.all()

#Creo dai 10 ai 50 annunci per titolo
for t in titoli:

    numero = random.randint(10, 50)

    for i in range(numero):

        prezzo = random.randint(5, 20)

        ad = BookAd(title=t, seller=students[random.randint(0, len(students)-1)].user,
                    description='Annuncio', price=prezzo, 
                    quality_class=classes[random.randint(0, len(classes)-1)],
                    photo=image_path)

        ad.save()

#------------------------------------------------------------------------------------------------------

#Divido i gruppi di studenti
inf_tri = StudentProfile.objects.all().filter(major='ING_INF_T')
inf_mag = StudentProfile.objects.all().filter(major='ING_INF_M')
mec_tri = StudentProfile.objects.all().filter(major='ING_MEC_T')
mec_mag = StudentProfile.objects.all().filter(major='ING_MEC_M')
ges_tri = StudentProfile.objects.all().filter(major='ING_GES_T')
ges_mag = StudentProfile.objects.all().filter(major='ING_GES_M')

#categories = ['FIS','MAT','INF','MEC','ELE','ECO','AUT','STA']
fis_titles = Title.objects.all().filter(category='FIS')
mat_titles = Title.objects.all().filter(category='MAT')
inf_titles = Title.objects.all().filter(category='INF')
mec_titles = Title.objects.all().filter(category='MEC')
ele_titles = Title.objects.all().filter(category='ELE')
eco_titles = Title.objects.all().filter(category='ECO')
aut_titles = Title.objects.all().filter(category='AUT')
sta_titles = Title.objects.all().filter(category='STA')

ads = BookAd.objects.all()

#--------------------------------------------------------------

#Interesting titles per studenti triennali informatici (da 0 a 10)
for it in inf_tri:

    #User
    utente = it.user

    #Numero di interesting titles
    num_int = random.randint(0,10)

    int_titles = []

    while len(int_titles) < num_int:

        fis = fis_titles[random.randint(0, len(fis_titles)-1)]
        mat = mat_titles[random.randint(0, len(mat_titles)-1)]
        inf = inf_titles[random.randint(0, len(inf_titles)-1)]
        ele = ele_titles[random.randint(0, len(ele_titles)-1)]
        aut = aut_titles[random.randint(0, len(aut_titles)-1)]
        sta = sta_titles[random.randint(0, len(sta_titles)-1)]

        number = random.random()*6

        if number <= 1.5:
            int_titles.append(mat)
        elif number <= 3:
            int_titles.append(inf)
        elif number <= 4:
            int_titles.append(fis)
        elif number <= 5:
            int_titles.append(sta)
        elif number <= 5.5:
            int_titles.append(aut)
        else:
            int_titles.append(ele)

    for t in int_titles:

        if len(InterestingTitle.objects.filter(user=utente).filter(title=t))==0:

            interesse = InterestingTitle(title=t, user=utente)
            interesse.save()

    
    #wishlist

    #Numero di wishes
    num_wishes = random.randint(0,20)

    wishes = []

    while len(wishes) < num_wishes:

        wishes.append(ads[random.randint(0, len(ads)-1)])
    
    for w in wishes:

        if len(Wishlist.objects.filter(user=utente).filter(ad=w))==0:

            wish = Wishlist(ad=w, user=utente)
            wish.save()

#Interesting titles per studenti magistrali informatici (da 0 a 10)
for im in inf_mag:

    #User
    utente = im.user

    #Numero di interesting titles
    num_int = random.randint(0,10)

    int_titles = []

    while len(int_titles) < num_int:

        mec = mec_titles[random.randint(0, len(mec_titles)-1)]
        inf = inf_titles[random.randint(0, len(inf_titles)-1)]
        ele = ele_titles[random.randint(0, len(ele_titles)-1)]
        aut = aut_titles[random.randint(0, len(aut_titles)-1)]
        sta = sta_titles[random.randint(0, len(sta_titles)-1)]

        number = random.random()*5

        if number <= 1.5:
            int_titles.append(sta)
        elif number <= 3:
            int_titles.append(inf)
        elif number <= 3.75:
            int_titles.append(ele)
        elif number <= 4.5:
            int_titles.append(aut)
        else:
            int_titles.append(mec)

    for t in int_titles:

        if len(InterestingTitle.objects.filter(user=utente).filter(title=t))==0:
            interesse = InterestingTitle(title=t, user=utente)
            interesse.save()

    
    #wishlist

    #Numero di wishes
    num_wishes = random.randint(0,20)

    wishes = []

    while len(wishes) < num_wishes:

        wishes.append(ads[random.randint(0, len(ads)-1)])
    
    for w in wishes:

        if len(Wishlist.objects.filter(user=utente).filter(ad=w))==0:

            wish = Wishlist(ad=w, user=utente)
            wish.save()

#Interesting titles per studenti triennali gestionali (da 0 a 10)
for gt in ges_tri:

    #User
    utente = gt.user

    #Numero di interesting titles
    num_int = random.randint(0,10)

    int_titles = []

    while len(int_titles) < num_int:

        fis = fis_titles[random.randint(0, len(fis_titles)-1)]
        mat = mat_titles[random.randint(0, len(mat_titles)-1)]
        inf = inf_titles[random.randint(0, len(inf_titles)-1)]
        eco = eco_titles[random.randint(0, len(eco_titles)-1)]
        sta = sta_titles[random.randint(0, len(sta_titles)-1)]

        number = random.random()*5

        if number <= 1.5:
            int_titles.append(mat)
        elif number <= 3:
            int_titles.append(eco)
        elif number <= 4:
            int_titles.append(fis)
        elif number <= 4.5:
            int_titles.append(inf)
        else:
            int_titles.append(sta)

    for t in int_titles:

        if len(InterestingTitle.objects.filter(user=utente).filter(title=t))==0:
            interesse = InterestingTitle(title=t, user=utente)
            interesse.save()

    #wishlist

    #Numero di wishes
    num_wishes = random.randint(0,20)

    wishes = []

    while len(wishes) < num_wishes:

        wishes.append(ads[random.randint(0, len(ads)-1)])
    
    for w in wishes:

        if len(Wishlist.objects.filter(user=utente).filter(ad=w))==0:

            wish = Wishlist(ad=w, user=utente)
            wish.save()

#Interesting titles per studenti magistrali gestionali (da 0 a 10)
for gm in ges_mag:

    #User
    utente = gm.user

    #Numero di interesting titles
    num_int = random.randint(0,10)

    int_titles = []

    while len(int_titles) < num_int:

        inf = inf_titles[random.randint(0, len(inf_titles)-1)]
        eco = eco_titles[random.randint(0, len(eco_titles)-1)]
        sta = sta_titles[random.randint(0, len(sta_titles)-1)]

        number = random.random()*6

        if number <= 2.5:
            int_titles.append(eco)
        elif number <= 5:
            int_titles.append(sta)
        else:
            int_titles.append(inf)

    for t in int_titles:

        if len(InterestingTitle.objects.filter(user=utente).filter(title=t))==0:
            interesse = InterestingTitle(title=t, user=utente)
            interesse.save()

    #wishlist

    #Numero di wishes
    num_wishes = random.randint(0,20)

    wishes = []

    while len(wishes) < num_wishes:

        wishes.append(ads[random.randint(0, len(ads)-1)])
    
    for w in wishes:

        if len(Wishlist.objects.filter(user=utente).filter(ad=w))==0:

            wish = Wishlist(ad=w, user=utente)
            wish.save()

#Interesting titles per studenti triennali meccanica (da 0 a 10)
for mt in mec_tri:

    #User
    utente = mt.user

    #Numero di interesting titles
    num_int = random.randint(0,10)

    int_titles = []

    while len(int_titles) < num_int:

        fis = fis_titles[random.randint(0, len(fis_titles)-1)]
        mat = mat_titles[random.randint(0, len(mat_titles)-1)]
        inf = inf_titles[random.randint(0, len(inf_titles)-1)]
        mec = mec_titles[random.randint(0, len(mec_titles)-1)]
        ele = ele_titles[random.randint(0, len(ele_titles)-1)]

        number = random.random()*5

        if number <= 2:
            int_titles.append(fis)
        elif number <= 3:
            int_titles.append(mat)
        elif number <= 4:
            int_titles.append(mec)
        elif number <= 4.5:
            int_titles.append(inf)
        else:
            int_titles.append(ele)

    for t in int_titles:

        if len(InterestingTitle.objects.filter(user=utente).filter(title=t))==0:
            interesse = InterestingTitle(title=t, user=utente)
            interesse.save()

    #wishlist

    #Numero di wishes
    num_wishes = random.randint(0,20)

    wishes = []

    while len(wishes) < num_wishes:

        wishes.append(ads[random.randint(0, len(ads)-1)])
    
    for w in wishes:

        if len(Wishlist.objects.filter(user=utente).filter(ad=w))==0:

            wish = Wishlist(ad=w, user=utente)
            wish.save()

#Interesting titles per studenti magistrali meccanica (da 0 a 10)
for mm in mec_mag:

    #User
    utente = mm.user

    #Numero di interesting titles
    num_int = random.randint(0,10)

    int_titles = []

    while len(int_titles) < num_int:

        aut = aut_titles[random.randint(0, len(aut_titles)-1)]
        mec = mec_titles[random.randint(0, len(mec_titles)-1)]
        ele = ele_titles[random.randint(0, len(ele_titles)-1)]

        number = random.random()*5

        if number <= 2:
            int_titles.append(mec)
        elif number <= 3:
            int_titles.append(aut)
        else:
            int_titles.append(ele)

    for t in int_titles:

        if len(InterestingTitle.objects.filter(user=utente).filter(title=t))==0:
            interesse = InterestingTitle(title=t, user=utente)
            interesse.save()

    #wishlist

    #Numero di wishes
    num_wishes = random.randint(0,20)

    wishes = []

    while len(wishes) < num_wishes:

        wishes.append(ads[random.randint(0, len(ads)-1)])
    
    for w in wishes:

        if len(Wishlist.objects.filter(user=utente).filter(ad=w))==0:

            wish = Wishlist(ad=w, user=utente)
            wish.save()










        


