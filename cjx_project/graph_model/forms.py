from django import forms
from .models import Journey_Cluster_Model, Journey_Process_Graph, Clustered_Customer, Clustered_Journey_Graph

class Journey_Cluster_Model_Form(forms.ModelForm):
    class Meta:
        model = Journey_Cluster_Model
        fields = '__all__'


class Journey_Process_Graph_Form(forms.ModelForm):
    class Meta:
        model = Journey_Process_Graph
        fields = '__all__'

class Clustered_Customer_Form(forms.ModelForm):
    class Meta:
        model = Clustered_Customer
        fields = '__all__'

class Clustered_Journey_Graph_Form(forms.ModelForm):
    class Meta:
        model = Clustered_Journey_Graph
        fields = '__all__'