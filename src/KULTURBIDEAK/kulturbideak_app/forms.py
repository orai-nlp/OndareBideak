from django.forms import *
from django.core.validators import validate_email
from django.forms.extras.widgets import SelectDateWidget
import django.forms.extras
from django.db.models import Q
from django.contrib.auth.models import User


HIZKUNTZA_CHOICES = (
    (1, 'Euskera'),
    (2, 'Gaztelania'),
    (3, 'Ingelesa'),
)
class LoginForm(Form):
    """Earbiltzaile bat logeatzeko formularioa kargatzen du"""
    erabiltzailea=CharField(max_length=150,required=True, widget=TextInput(attrs={"placeholder":"erabiltzailea","type":"text", "class":"form-control"}))
    pasahitza=CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":"pasahitza","type":"password", "class":"form-control"}),required=True)

    def clean_erabiltzailea(self):
        """Erabiltzailea existitzen den konprobatzen da"""
        try:
            e=User.objects.get(username=self.cleaned_data["erabiltzailea"])
            return self.cleaned_data["erabiltzailea"]
        except:
            raise forms.ValidationError("Erabiltazilea ez dago erregistratua")

    def clean_pasahitza(self):
        """Erabiltzailea eta pasahitza egokia diren konrpobatzen da"""
        try:
            e=User.objects.get(username=self.cleaned_data["erabiltzailea"])
            if e.check_password(self.cleaned_data["pasahitza"]):
                return self.cleaned_data["pasahitza"]
            else:
                raise forms.ValidationError("Pasahitza ez da zuzena")
        except:
            raise forms.ValidationError("Pasahitza ez da zuzena")
        
 #    https://docs.djangoproject.com/en/1.8/ref/forms/fields/#multiplechoicefield   
class ItemGehituForm(Form):
    """Item berri bat gehitzeko formularioa kargatzen du"""
    titulua=CharField(max_length=500,required=True, widget=TextInput(attrs={"placeholder":"titulua","type":"text", "class":"form-control"}))
    #  sortzailea: logeatuta dagoen erabiltzailea
    deskribapena=CharField(max_length=150,required=True, widget=TextInput(attrs={"placeholder":"deskribapena","type":"text", "class":"form-control"}))
    # date : momentukoa
    gaia=CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":"gaia","type":"text", "class":"form-control"}))
    eskubideak=CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":"eskubideak","type":"text", "class":"form-control"}))
    irudia=ImageField(max_length=32,required=False)
    hizkuntza=ChoiceField(required=False,  choices=HIZKUNTZA_CHOICES)