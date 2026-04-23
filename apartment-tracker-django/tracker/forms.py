from django import forms
from .models import Apartment, Roommate, Rating
import re

URL_RE = re.compile(r'^https?://', re.IGNORECASE)


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = [
            'name', 'listing_url', 'image_url', 'address',
            'bedrooms', 'bathrooms', 'monthly_rent',
            'has_parking', 'is_pet_friendly', 'has_in_unit_laundry',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Cozy Downtown Studio'}),
            'listing_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://... (optional)'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123 Main St, Seattle WA'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0.5, 'step': 0.5}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'step': 50}),
            'has_parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_pet_friendly': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_in_unit_laundry': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_listing_url(self):
        url = self.cleaned_data.get('listing_url', '')
        if not URL_RE.match(url):
            raise forms.ValidationError('Listing URL must start with http:// or https://')
        return url

    def clean_image_url(self):
        url = self.cleaned_data.get('image_url', '')
        if url and not URL_RE.match(url):
            raise forms.ValidationError('Image URL must start with http:// or https://')
        return url

    def clean_bedrooms(self):
        beds = self.cleaned_data.get('bedrooms')
        if beds is not None and beds < 1:
            raise forms.ValidationError('Bedrooms must be at least 1.')
        return beds

    def clean_bathrooms(self):
        baths = self.cleaned_data.get('bathrooms')
        if baths is not None and baths < 0.5:
            raise forms.ValidationError('Bathrooms must be at least 0.5.')
        return baths

    def clean_monthly_rent(self):
        rent = self.cleaned_data.get('monthly_rent')
        if rent is not None and rent <= 0:
            raise forms.ValidationError('Monthly rent must be greater than $0.')
        return rent


class RoommateForm(forms.ModelForm):
    class Meta:
        model = Roommate
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Alex Smith'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'alex@email.com'}),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['apartment', 'roommate', 'score', 'comment']
        widgets = {
            'apartment': forms.Select(attrs={'class': 'form-select'}),
            'roommate': forms.Select(attrs={'class': 'form-select'}),
            'score': forms.Select(
                choices=[(1, '1 — Not interested'), (2, '2 — Below average'),
                         (3, "3 — It's okay"), (4, '4 — Pretty good'), (5, '5 — Love it!')],
                attrs={'class': 'form-select'}
            ),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'What did you like or dislike?'
            }),
        }

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score not in range(1, 6):
            raise forms.ValidationError('Score must be between 1 and 5.')
        return score
