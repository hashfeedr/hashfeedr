from django import forms

class FilterForm(forms.Form):
	query = forms.CharField(max_length=100, initial="#djangodash")
	