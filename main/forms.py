from django import forms

class UploadFileForm(forms.Form):
	#
	# upload File form
	#
	description = forms.CharField(widget=forms.Textarea(attrs={"rows":3, "cols":40}))
	file = forms.FileField()

class UploadUrlForm(forms.Form):
	#
	# upload URL form
	#
	description = forms.CharField(widget=forms.Textarea(attrs={"rows":3, "cols":40}))
	url = forms.URLField()

class AccessForm(forms.Form):
	#
	# access secured data form
	#
	password = forms.CharField(widget=forms.PasswordInput)