from django import forms
from Hfinder.models import Person
from django.db.models import Q

class LoginForm(forms.Form):
    email = forms.EmailField(label='Courriel', 
                             required=True,
                             widget=forms.EmailInput(attrs={
                                 'placeholder':'',
                             }) 
                            )
    password = forms.CharField(label='Mot de Passe', widget=forms.PasswordInput, required=True)

    
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:

            result = Person.objects.filter(password=password, email=email)
            if len(result) != 1:
                raise forms.ValidationError("Adresse de courriel ou mot de passe érroné")
        return cleaned_data
    
class userProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget = forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Person
        exclude = ('friends',)
        fields = ['registration_number', 'last_name', 'first_name', 'birth_date', 'email', 'phone_number', 'password']
        
class AddFriendForm(forms.Form):
    name = forms.CharField(label='nom ', max_length=20)
    def clean(self):
        cleaned_data = super(AddFriendForm, self).clean()
        name = cleaned_data.get('name')

        #verification du name
        if name:
            result = Person.objects.filter(Q(first_name=name) | Q(last_name=name))
            #result.pushPerson.objects.filter(last_name=name))
            print("Dans la base de données se trouve : "+ str(len(result)) + " Occurences")

            if len(result) != 1:
                raise forms.ValidationError('le Nom mentionné est érroné')
    
        return cleaned_data 
    