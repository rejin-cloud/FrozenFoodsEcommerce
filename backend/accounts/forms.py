from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "First name", "autocomplete": "given-name"})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Last name", "autocomplete": "family-name"})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            self.fields["username"].widget.attrs.update({
                "placeholder": "Choose a username",
                "autocomplete": "username"
            })
        if "password1" in self.fields:
            self.fields["password1"].widget.attrs.update({
                "placeholder": "Create a strong password",
                "autocomplete": "new-password"
            })
            self.fields["password1"].help_text = None
        if "password2" in self.fields:
            self.fields["password2"].widget.attrs.update({
                "placeholder": "Re-enter your password",
                "autocomplete": "new-password"
            })
            self.fields["password2"].help_text = None
        for field in self.fields.values():
            field.widget.attrs["class"] = "auth-input-field"


class CustomUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "city",
            "pincode",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"