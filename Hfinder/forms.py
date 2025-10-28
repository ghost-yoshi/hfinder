from django import forms
from Hfinder.models import Person

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
    class Meta:
        model = Person
        exclude = ('friends',)