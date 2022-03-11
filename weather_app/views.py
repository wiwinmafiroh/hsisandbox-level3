import requests
from django.shortcuts import redirect, render
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
  # Use API
  url = 'http://api.openweathermap.org/data/2.5/find?q={}&units=metric&appid=795b80dc92f5c7954f7aa04e1e9a03fe'
  
  # For Message
  err_msg = ''
  message = ''
  message_class =''
  
  # Cek apakah ada request dengan method POST
  if request.method == 'POST':
    form = CityForm(request.POST)
    
    if form.is_valid():
      new_city = form.cleaned_data['name']
      
      # Cek apakah kota yang di input sudah ada atau belum
      existing_city_count = City.objects.filter(name = new_city).count()
      
      if existing_city_count == 0:
        # Cek apakah kota yang dimasukkan sudah benar
        r = requests.get(url.format(new_city)).json()
        
        if r['count'] > 0:
          form.save()
        else:
          err_msg = 'City does not exist in the world!'  
        
      else:
        err_msg = 'City already exists in the database!'
    
    if err_msg:
      message = err_msg
      message_class = 'is-danger'
    else:
      message = 'City added successfully!'
      message_class = 'is-success'
  
  # Tampilkan form kembali
  form = CityForm()
  
  # Urutkan kota dari yang terbaru
  cities = City.objects.order_by('-id')
  # List untuk menyimpan kota
  weather_data = []
  
  # Perulangan untuk menampilkan kota di db
  for city in cities:
    r = requests.get(url.format(city)).json()
    
    # Ambil detail kota
    city_weather = {
      'city': city.name,
      'temperature': r['list'][0]['main']['temp'],
      'description': r['list'][0]['weather'][0]['description'],
      'icon': r['list'][0]['weather'][0]['icon']
    }
    # Masukkan kota kedalam list
    weather_data.append(city_weather)
  
  # Data yang akan dikirim ke template
  context = {
    'weather_data': weather_data, 
    'form': form,
    'message': message,
    'message_class': message_class
  }
  
  return render(request, 'weather_app/weather.html', context)

def delete_city(request, city_name):
  City.objects.get(name= city_name).delete()
  
  return redirect('weather')
