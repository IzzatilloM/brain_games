"""Hisob formalari — bitta bola hisobi + ota-ona nazorati."""

from django import forms
from django.contrib.auth import authenticate

from .models import AGE_GROUPS, AVATARS, ParentalControl, User


class StyledFormMixin:
    """Maydonlarga Bootstrap form-control klassini biriktiradi."""

    default_class = "form-control"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " " + self.default_class).strip()


class LoginForm(StyledFormMixin, forms.Form):
    username = forms.CharField(
        label="Login",
        widget=forms.TextInput(attrs={"placeholder": "ali2015", "autofocus": True}),
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={"placeholder": "••••••"}),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get("username")
        password = cleaned.get("password")
        if username and password:
            self.user = authenticate(self.request, username=username, password=password)
            if self.user is None:
                raise forms.ValidationError("Login yoki parol noto'g'ri.")
            if not self.user.is_active:
                raise forms.ValidationError("Bu hisob faolsizlantirilgan.")
        return cleaned

    def get_user(self):
        return self.user


class RegisterForm(StyledFormMixin, forms.Form):
    """Bola o'zi ro'yxatdan o'tadi: login, ism, parol, yosh guruhi, avatar."""

    full_name = forms.CharField(
        label="Ism", max_length=120, required=False,
        widget=forms.TextInput(attrs={"placeholder": "Ali"}),
    )
    username = forms.CharField(
        label="Login", max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "ali2015"}),
    )
    password = forms.CharField(
        label="Parol", min_length=4,
        widget=forms.PasswordInput(attrs={"placeholder": "••••••"}),
    )
    age_group = forms.ChoiceField(
        label="Yoshingiz", choices=AGE_GROUPS, initial="9-11",
        widget=forms.HiddenInput(),
    )
    avatar = forms.ChoiceField(
        label="Avatar", choices=[(a, a) for a in AVATARS], initial=AVATARS[0],
        widget=forms.HiddenInput(),
    )

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Bu login band. Boshqasini tanlang.")
        return username

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"],
        )
        user.full_name = self.cleaned_data.get("full_name", "")
        user.age_group = self.cleaned_data["age_group"]
        user.avatar = self.cleaned_data["avatar"]
        user.save()
        ParentalControl.objects.get_or_create(user=user)
        return user


class ProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "avatar", "age_group", "sound_enabled"]
        widgets = {
            "avatar": forms.HiddenInput(),
            "age_group": forms.Select(),
        }


class ParentalUnlockForm(forms.Form):
    """Ota-ona nazoratiga kirish — PIN tekshiruvi."""

    pin = forms.CharField(
        label="PIN kod", max_length=8,
        widget=forms.PasswordInput(attrs={
            "placeholder": "••••", "inputmode": "numeric",
            "class": "form-control form-control-lg text-center",
        }),
    )


class ParentRegisterForm(StyledFormMixin, forms.ModelForm):
    """Ota-ona ro'yxatdan o'tishi: ism, familiya, yosh, ish joyi, bola, email."""

    parent_type = forms.ChoiceField(
        label="Kim?", choices=ParentalControl.PARENT_TYPES,
        widget=forms.RadioSelect, initial="ota",
    )

    class Meta:
        model = ParentalControl
        fields = [
            "parent_type", "parent_first_name", "parent_last_name",
            "parent_age", "parent_workplace",
            "child_first_name", "child_last_name", "parent_email",
        ]
        widgets = {
            "parent_first_name": forms.TextInput(attrs={"placeholder": "Ism"}),
            "parent_last_name": forms.TextInput(attrs={"placeholder": "Familiya"}),
            "parent_age": forms.NumberInput(attrs={"min": 18, "max": 90, "placeholder": "Yosh"}),
            "parent_workplace": forms.TextInput(attrs={"placeholder": "Ish joyi"}),
            "child_first_name": forms.TextInput(attrs={"placeholder": "Bola ismi"}),
            "child_last_name": forms.TextInput(attrs={"placeholder": "Bola familiyasi"}),
            "parent_email": forms.EmailInput(attrs={"placeholder": "email@gmail.com"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("parent_first_name", "parent_last_name", "parent_age",
                     "parent_workplace", "child_first_name", "child_last_name", "parent_email"):
            self.fields[name].required = True


class ParentalControlForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ParentalControl
        fields = [
            "pin", "daily_limit_minutes", "weekly_goal_minutes",
            "bedtime_start", "bedtime_end",
            "allow_mental", "allow_xotira", "allow_tezoqish",
            "allow_diqqat", "allow_matematika", "is_blocked",
        ]
        widgets = {
            "bedtime_start": forms.TimeInput(attrs={"type": "time"}),
            "bedtime_end": forms.TimeInput(attrs={"type": "time"}),
            "daily_limit_minutes": forms.NumberInput(attrs={"min": 5, "max": 240}),
            "weekly_goal_minutes": forms.NumberInput(attrs={"min": 30, "max": 1200}),
        }
