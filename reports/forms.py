from django import forms


class DashboardForm(forms.Form):
    """
    Dashboard to filter on the Dashboard
    """

    search: forms.CharField = forms.CharField(
        max_length=100, required=False
    )
    start: forms.DateField = forms.DateField(required=False)
    end: forms.DateField = forms.DateField(required=False)
