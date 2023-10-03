from django import forms
from .models import Listing, Bids, Comments


class CreateListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'bid', 'image']

        widgets = {
            'title': forms.TextInput(attrs={'id': 'id_title', 'class': 'form-control cl-item', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'id': 'id_description', 'rows': '10', 'class': 'form-control cl-item', 'placeholder': 'Describe your item...'}),
            'bid': forms.NumberInput(attrs={'id': 'id_bid', 'class': 'form-control cl-item', 'placeholder': 'Place your starting bid'}),
            'image': forms.URLInput(attrs={'id': 'id_image', 'class': 'form-control cl-item', 'placeholder': 'Item Image URL'})
        }


class PlaceBid(forms.ModelForm):
    value = forms.CharField(max_length=16, label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Bid'}
        ))
    class Meta:
        model = Bids
        fields = ['value']


class PostComment(forms.ModelForm):
    content = forms.CharField(max_length=300, label="", widget=forms.Textarea(
        attrs={'rows': '10', 'class': 'form-control', 'placeholder': 'Write your comment...'}
        ))
    class Meta:
        model = Comments
        fields = ['content']