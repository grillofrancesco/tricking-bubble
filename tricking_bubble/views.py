from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from typing import Any, Dict
from .models import Utente, Trick, Progression, Comment

class AuthenticateView(TemplateView):
    template_name = "authenticate.html"         # Collegamento a pagina html da richiamare
    title = ""                                  # Titolo pagina
    POSSIBLE_GET_ERR = {'1':'Per continuare è necessario accedere.'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        # Dizionario riportato nella funzione render
        context['type'] = self.request.path.replace("/",'')

        context['title'] = 'Accedi' if context['type'] != 'register' else 'Registrati'
        context['active'] = 'profile'
        return context

    def get(self, request) -> HttpResponse:
        print(f"request.user: {request.user}")                                 # Riconosce se l'utente è loggato.
        context = self.get_context_data()

        context['img_profilo'] = get_img_profilo(request)

        if request.user.is_authenticated:
            return redirect('profile')
        
        # Riceve informazioni da pagine come profilo o trick_tree, che necessitano l'utente loggato.
        err = request.GET.get('err', '')                # Vede se ci sono errori riportati nella get
        if err != '':
            errore = self.POSSIBLE_GET_ERR.get(err, '') # Prende stringa corrispondente se è un caso specifico
            if errore != '':
                context['blocked_access'] = True        # Mostra alla pagina che esiste
                context['err_string'] = errore  

        return render(request, self.template_name, context)                     
            
    def post(self, request):
        context = self.get_context_data()
        user_post = request.POST.get('username')
        psw_post = request.POST.get('password1')
        # Non viene usato make_password, a quanto pare django cripta da sè, e non è necessario.
        if context['type'] == 'register':
            try:
                djangoUser = User.objects.create_user(username=user_post, password= psw_post)

                email = request.POST.get('email')
                new_user = Utente.objects.create(user=djangoUser, nickname=str(djangoUser), mail=email, foto_profilo="")
                new_user.save()
                djangoUser.save()
                """ with open('credenziali_salvate.txt','a') as file:                   # Utilizzato in fase di testing
                    file.write(f"utente: {new_user} | psw_post: {psw_post} \n") """

            except Exception:
                context['err_utente'] = 'Utente già registrato.'
                print("Utente già registrato.")
        
        if context.get('err_utente') is not None:
            return render(request, self.template_name, context)
        
        utente = authenticate(request, username=user_post, password=psw_post)

        if utente is None:
            if context.get('err_utente') is None:
                context['err_utente'] = 'Credenziali inserite non corrette.'
            return render(request, self.template_name, context)
            
        login(request, utente)


        print(f"user_post: {user_post} | psw_post: {psw_post} | utente: {utente}")
        

        return redirect('profile')
        
class Trick_TreeView(TemplateView):
    template_name = "trick_tree.html"
    title = "Trick Tree"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['active'] = 'trick_tree'
        return context
    
    def __get_trick_information__(self, cat):
        return Trick.objects.filter(categoria=cat)
    
    def __get_trick_category__(self, request):
        category = request.GET.get('cat', '')
        try:
            if int(category) > 3:
                category = ''
            else:
                return int(category)
        except ValueError:
            return ''
        
    def __get_category_name__(self, cat):
        match cat:
            case 1:
                return 'Power Moves'
            case 2:
                return 'Caricamenti'
            case 3:
                return 'Avvitamenti'

    def __get_list_of_completed__(self,request):
        utente = Utente.objects.get(nickname=request.user)
        list_of_progressions = Progression.objects.filter(user_id=utente)

        return [
            progression.salto.id
            for progression in list_of_progressions
            if progression.completato == True
        ]
    
    def __get_progressioni__(self, utente, trick):
        progressione = list(Progression.objects.filter(user_id=utente, salto=trick))
        if not progressione:
            progressione = Progression.objects.create(
                salto=trick, user_id=utente
            )
            progressione.save()
        else:
            progressione = progressione[0]

        return progressione
    
    def get(self, request) -> HttpResponse:
        context = self.get_context_data()

        context['img_profilo'] = get_img_profilo(request)

        if not request.user.is_authenticated:
            return redirect('/login/?err=1')                        # REDIRECT TO LOGIN IF NOT AUTHENTICATED

        context['user'] = request.user

        category = self.__get_trick_category__(request)
        if not category:                                                               # GET CATEGORY INDEX
            return redirect('category_choice')
        context['categoria'] = self.__get_category_name__(category)

        tricks = self.__get_trick_information__(category)
        context['tricks'] = tricks                                                    # GET TRICK INFO
        context['indici_tricks'] = list(range(len(tricks)))
    
        context['list_of_completed'] = self.__get_list_of_completed__(request)     
        

        return render(request, 'trick_tree.html', context)
    
    def post(self, request):
        context = self.get_context_data()

        # form_uses = {0: 'CheckCompletedTrick', 1: 'Ratings', 2: 'Comments'}
        # print(request.POST)

        match request.POST.get('form_use'):
            case '0':
                # CheckCompletedTrick
                trick_selected = request.POST.get('trick_selezionato')

                utente = Utente.objects.get(nickname=request.user)
                trick_instance = Trick.objects.get(id=trick_selected)
                # print(f"{utente, trick_instance}")

                progressione = self.__get_progressioni__(utente, trick_instance)

                progressione.completato = not progressione.completato
                progressione.save()

            case '1':
                # Ratings
                # print("Trick: "+request.POST.get('trick_selezionato'))
                # print("Valore: "+request.POST.get('valore_selezionato'))
                # Seleziona istanza di progresso tra utente e salto, assegna valore.
                # Se istanza non esiste, creala.
                valore = int(request.POST.get('valore_selezionato'))
                utente = Utente.objects.get(nickname=request.user)
                trick_instance = Trick.objects.get(id=request.POST.get('trick_selezionato'))

                progressione = self.__get_progressioni__(utente, trick_instance)

                progressione.valutazione = valore
                progressione.save()

            case '2':
                # Comments
                utente = Utente.objects.get(nickname=request.user)
                trick_instance = Trick.objects.get(id=request.POST.get('trick_selezionato'))
                testo = request.POST.get('commento') 
                testo = testo.replace("'","\\u0027")
                testo = testo.replace('"',"\\u0027")

                # registra commento in db
                new_commento = Comment.objects.create(salto=trick_instance, user_id=utente, testo=testo)
                new_commento.save()



        context['list_of_completed'] = self.__get_list_of_completed__(request)
        return render(request, self.template_name, context)
     
class Choice_CategoryView(TemplateView):
    template_name = "category_choice.html"
    title = "Seleziona Categoria"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['active'] = 'trick_tree'
        return context
    
    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        context['img_profilo'] = get_img_profilo(request)
        return render(request, self.template_name, context)

    def post(self, request):
        context = self.get_context_data()
        categoria = request.POST.get('category', '')

        if categoria != '':
            context['categoria'] = categoria
            return redirect(f'/trick_tree/?cat={categoria}')
        return render(request, self.template_name, context)
    
class HomeView(TemplateView):
    template_name = "home.html"
    title = "Home Page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['active'] = 'home'
        return context
    
    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        context['img_profilo'] = get_img_profilo(request)
        if request.user.username == "admin":
            logout(request)
            return redirect('home')
        return render(request, self.template_name, context)
    
    def post(self, request):
        context = self.get_context_data()
        categoria = request.POST.get('category', '')

        if categoria != '':
            context['categoria'] = categoria
            return redirect(f'/trick_tree/?cat={categoria}')
        return render(request, self.template_name, context)

class LogoutView(TemplateView):
    template_name = 'logout.html'
    title = 'Logout'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['active'] = 'profile'
        return context
    
    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        context['img_profilo'] = get_img_profilo(request)
        logout(request)
        return render(request, self.template_name, context)

class ProfileView(TemplateView):
    template_name = "profile.html"
    title = "Profilo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = self.title
        
        return context
    
    def get(self, request) -> HttpResponse:
        # sourcery skip: use-contextlib-suppress
        context = self.get_context_data()
        if not request.user.is_authenticated:
            return redirect('/login/?err=1')
        else:
            context['title'] = f'@{request.user}'
        
        context['user'] = request.user

        if request.user.username == "admin":
            logout(request)
            return redirect('login')

        pageType = request.GET.get('type')
        context['type'] = pageType if pageType == 'progress' else 'profile'

        utente = Utente.objects.filter(user = request.user)[0]
        context['img_profilo'] = get_img_profilo(request)
        if context['type'] == 'profile':
            context['active'] = 'profile'

            context['email'] = utente.mail
            context['data_primo_login'] = request.user.date_joined.strftime("%d-%m-%Y")
            context['data_nascita'] = utente.data_nascita if utente.data_nascita is not None else 'Sconosciuta' 

        elif context['type'] == 'progress':
            context['active'] = 'progress'
            # Get progress information:
            # num : tot = % : 100%

            number_of_tricks = []                                       # [n_powerMoves, n_caricamenti, n_avvitamenti]
            number_of_completed_tricks = []
            percentages = []

            for i in range(1,4):
                tricks_i = Trick.objects.filter(categoria=i)
                n_tricks = len(tricks_i)
                number_of_tricks.append(n_tricks)

                conta_trick = 0
                for trick in tricks_i:
                    try:
                        progression = Progression.objects.filter(user_id=utente, salto=trick)[0]
                        if progression.completato:
                            conta_trick += 1
                    except IndexError:
                        pass
                    
                number_of_completed_tricks.append(conta_trick)

                percentages.append(int(conta_trick*100/n_tricks))       # percentuale di completamento
            
            context['number_of_tricks'] = number_of_tricks
            context['number_of_completed_tricks'] = number_of_completed_tricks
            context['percentages'] = percentages
            context['indici_categorie'] = [0,1,2]

            # print(f"number_of_tricks {number_of_tricks} \nnumber_of_completed_tricks {number_of_completed_tricks} \npercentages {percentages}")

        return render(request, self.template_name, context)

class Edit_CredentialsView(TemplateView):
    template_name = "edit_credentials.html"
    title = "Modifica profilo"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data()
        context['active'] = 'profile'
        context['title'] = self.title
        return super().get_context_data()
    
    def get(self, request,) -> HttpResponse:
        context = self.get_context_data()
        context['img_profilo'] = get_img_profilo(request)

        if not request.user.is_authenticated:
            return redirect('/login/?err=1')
        
        if request.user.username == "admin":
            logout(request)
            return redirect('login')
        
        utente = Utente.objects.filter(user = request.user)[0]

        context['email'] = utente.mail
        context['data_nascita'] = ""
        if utente.data_nascita:
            context['data_nascita'] = utente.data_nascita.strftime("%Y-%m-%d")
        return render(request, self.template_name, context)
    
    def post(self,request):
        context = self.get_context_data()
        email = request.POST.get('email')
        data_nascita = request.POST.get('data_nascita', None)

        utente = Utente.objects.filter(user = request.user)[0]
        utente.mail = email
        if data_nascita != '':
            utente.data_nascita = data_nascita
        try:
            immagine_profilo = request.FILES['img_profilo']
        except Exception:
            immagine_profilo = ""    
        utente.foto_profilo = immagine_profilo

        utente.save()

        return redirect('profile')

def get_img_profilo(request):
    try:
        utente = Utente.objects.filter(user = request.user)[0]
        return utente.foto_profilo.url
    except Exception:
        return ""

def test(request):
    return HttpResponse("This is a test.")

def toProgress(request):
    return redirect('/my_profile/?type=progress')

def toHome(request):
    return redirect('home')

def to404Page(request, exception):
    return render(request, '404.html', {})
def to403Page(request, exception):
    return render(request, '403.html', {})
def to400Page(request, exception):
    return render(request, '400.html', {})


# redirect(nomeUrl) -> reindirizza sul nome che si dà nella variabile url
# return super().get(request) -> richiama la pagina stessa