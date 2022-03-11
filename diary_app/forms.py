from django.forms import ModelForm
# import the model
from .models import Entry

# Create the form from the model
class EntryForm(ModelForm):
  class Meta:
    model = Entry
    # display in the form
    fields = ('text', )
    
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['text'].widget.attrs.update({'class': 'textarea', 'placeholder': 'What\`s on your mind?'})
