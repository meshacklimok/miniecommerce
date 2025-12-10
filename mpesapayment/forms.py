from django import forms

class MpesaPaymentForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        label="Phone Number",
        widget=forms.TextInput(attrs={
            'placeholder': '2547XXXXXXXX',
            'class': 'form-control'
        })
    )
