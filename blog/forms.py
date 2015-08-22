from django import forms
from .models import Post, Item

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title',)


class ItemForm(forms.ModelForm):
	
	class Meta:
		model = Item
		fields = ('abstract', 'note', 'status')



		
