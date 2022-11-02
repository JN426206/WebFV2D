from django import forms
from .models import VideoFile

# Form for upload video to the server
class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoFile
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super(VideoUploadForm, self).__init__(*args, **kwargs)
        # In html input only accept video uploads
        self.fields['file'].widget.attrs.update({'class': 'form-control border-0', 'accept': 'video/*'})
