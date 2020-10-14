from django import forms
from django_countries.fields import CountryField

PAYMENT_OPTIONS = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '1234 Main St', 'class': 'form-control'}))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Apartment or Suit', 'class': 'form-control'}))
    country = CountryField(blank_label='(select country)').formfield(attrs={'class': 'custom-select d-block w-100'})
    zip = forms.CharField()
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(),required=False )
    payment_options = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_OPTIONS)
