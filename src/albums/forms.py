from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Album, Artist, Genre
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = '__all__'
        
    artist = AutoCompleteSelectMultipleField('artist', required=False, help_text="Search by name", show_help_text=False, label='Album artist')
    genre = AutoCompleteSelectMultipleField('genre', required=False, help_text="Search by name", show_help_text=False, label='Genre')

    def clean_author(self):
        if not self.cleaned_data['author']:
            return User()
        return self.cleaned_data['author']         