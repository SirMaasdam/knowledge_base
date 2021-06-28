from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(label=False,
                             widget=forms.TextInput(attrs={'class': "uk-search-input uk-form-large uk-border-rounded",
                                                           'placeholder': "Задайте свой вопрос",
                                                           'autocomplete': "off",
                                                           'data-minchars': "1",
                                                           'type': "search"}))

