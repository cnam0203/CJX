from django import forms
from .models import Touchpoint
from .models import Channel_Type
from .models import Traffic_Source_Type
from .models import Device_Browser
from .models import Device_Category
from .models import Device_OS
from .models import Interact_Item_Type
from .models import Experience_Emotion
from .models import Action_Type
from .models import Journey_Customer
from .models import Matching_Report
from .models import Matching_Column

class Touchpoint_Form(forms.ModelForm):
    class Meta:
        model = Touchpoint
        fields = '__all__'

class Channel_Type_Form(forms.ModelForm):
    class Meta:
        model = Channel_Type
        fields = '__all__'

class Source_Type_Form(forms.ModelForm):
    class Meta:
        model = Traffic_Source_Type
        fields = '__all__'

class Device_Category_Form(forms.ModelForm):
    class Meta:
        model = Device_Category
        fields = '__all__'

class Device_Browser_Form(forms.ModelForm):
    class Meta:
        model = Device_Browser
        fields = '__all__'

class Device_OS_Form(forms.ModelForm):
    class Meta:
        model = Device_OS
        fields = '__all__'

class Action_Type_Form(forms.ModelForm):
    class Meta:
        model = Action_Type
        fields = '__all__'

class Journey_Customer_Form(forms.ModelForm):
    class Meta:
        model = Journey_Customer
        fields = '__all__'

class Matching_Report_Form(forms.ModelForm):
    class Meta:
        model = Matching_Report
        fields = '__all__'

class Matching_Column_Form(forms.ModelForm):
    class Meta:
        model = Matching_Column
        fields = '__all__'

class Interact_Item_Type_Form(forms.ModelForm):
    class Meta:
        model = Interact_Item_Type
        fields = '__all__'

class Experience_Emotion_Form(forms.ModelForm):
    class Meta:
        model = Experience_Emotion
        fields = '__all__'