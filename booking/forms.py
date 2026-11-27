from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')

        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError(
                    "Image size must be less than 2 MB."
                )

            if image.content_type not in ['image/jpeg', 'image/png']:
                raise forms.ValidationError(
                    "Only JPG and PNG images are allowed."
                )

        return image