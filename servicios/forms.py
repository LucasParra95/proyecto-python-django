from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Cliente, Servicio, Empleado, Coordinador, ReservaServicio

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'numero_legajo', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_legajo': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CoordinadorForm(forms.ModelForm):
    class Meta:
        model = Coordinador
        fields = ['nombre', 'apellido', 'numero_documento', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_documento': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ServicioSelectMultiple(forms.SelectMultiple):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        # Extraer el ID del servicio
        val_id = value.value if hasattr(value, 'value') else value
        if val_id:
            try:
                servicio = Servicio.objects.filter(pk=val_id).first()
                if servicio:
                    option['attrs']['data-precio'] = str(servicio.precio)
            except Exception:
                pass
        return option

class ReservaServicioForm(forms.ModelForm):
    class Meta:
        model = ReservaServicio
        fields = ['cliente', 'servicios', 'empleado', 'coordinador', 'fecha_servicio']
        widgets = { 
            'fecha_servicio': DatePickerInput(
                options={
                    'format': 'DD/MM/YYYY',
                    'locale': 'es',
                    'showTodayButton': True,
                    'showClear': True,
                    'inline': True,
                    'keepOpen': True,
                    'focusOnShow': False,
                }
            ),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'servicios': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'empleado': forms.Select(attrs={'class': 'form-select'}),
            'coordinador': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {  
            'cliente': 'Cliente',
            'servicios': 'Servicios a Contratar (Selección múltiple)',
            'empleado': 'Empleado que toma la reserva',
            'coordinador': 'Coordinador del evento',
            'fecha_servicio': 'Fecha del Evento',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if self.instance and self.instance.pk and self.instance.fecha_servicio:
        #     self.fields['fecha_servicio'].widget.format = '%Y-%m-%d'
            
        self.fields['cliente'].queryset = Cliente.objects.filter(activo=True)
        self.fields['servicios'].queryset = Servicio.objects.filter(activo=True)
        self.fields['empleado'].queryset = Empleado.objects.filter(activo=True)
        self.fields['coordinador'].queryset = Coordinador.objects.filter(activo=True)