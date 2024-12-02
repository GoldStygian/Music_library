from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'required':'',
            'class':'user-input',
            
        })
        self.fields["password"].widget.attrs.update({
            'required':'',
            'class':'password-input',
        })
    class Meta:
        model= User
        fields = ["username","password"]