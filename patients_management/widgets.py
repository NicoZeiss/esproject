from django import forms


class CustomTextInput(forms.TextInput):
    template_name = 'patients_management/widgets/custom_text_input.html'
