from django.shortcuts import render, get_object_or_404
from .models import Car
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from .forms import  CompareForm
from django.http import HttpResponse

# Create your views here.
@login_required(login_url = 'login')
def cars(request):
    cars = Car.objects.order_by('-created_date')
    paginator = Paginator(cars, 4)
    page = request.GET.get('page')
    paged_cars = paginator.get_page(page)

    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()

    data = {
        'cars': paged_cars,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    return render(request, 'cars/cars.html', data)

@login_required(login_url = 'login')
def car_detail(request, id):
    single_car = get_object_or_404(Car, pk=id)

    data = {
        'single_car': single_car,
    }
    return render(request, 'cars/car_detail.html', data)

@login_required(login_url = 'login')
def search(request):
    cars = Car.objects.order_by('-created_date')

    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    transmission_search = Car.objects.values_list('transmission', flat=True).distinct()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            cars = cars.filter(description__icontains=keyword)

    if 'model' in request.GET:
        model = request.GET['model']
        if model:
            cars = cars.filter(model__iexact=model)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            cars = cars.filter(city__iexact=city)

    if 'year' in request.GET:
        year = request.GET['year']
        if year:
            cars = cars.filter(year__iexact=year)

    if 'body_style' in request.GET:
        body_style = request.GET['body_style']
        if body_style:
            cars = cars.filter(body_style__iexact=body_style)

    if 'min_price' in request.GET:
        min_price = request.GET['min_price']
        max_price = request.GET['max_price']
        if max_price:
            cars = cars.filter(price__gte=min_price, price__lte=max_price)

    data = {
        'cars': cars,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
        'transmission_search': transmission_search,
    }
    return render(request, 'cars/search.html', data)

@login_required(login_url = 'login')
def compare(request):

    form = CompareForm(request.POST or None)
    if request.method == 'POST':
        car1 = int(request.POST['car1'])
        car2 = int(request.POST['car2'])

        car1 = Car.objects.get(pk=car1)
        car2 = Car.objects.get(pk=car2)

        data = {
            
           'car1_pic': car1.car_photo.url,
            'car1_car': car1.car_title,
           'car1_model': car1.model,
            'car1_c': car1.color,
           'car1_fuel_type': car1.fuel_type,
            'car1_body_style': car1.body_style,
            'car1_price': car1.price,
            'car1_features': car1.features,
            'car1_m': car1.milage,
            'car1_e': car1.engine,
            'car1_i': car1.interior,
            'car1_transmission': car1.transmission,
            
            
            'car2_pic': car2.car_photo.url,
            'car2_car': car2.car_title,
            'car2_body_style': car2.body_style,
            'car2_model': car2.model,
            'car2_c': car2.color,
            'car2_fuel_type': car2.fuel_type,
            'car2_m': car2.milage,
            'car2_e': car2.engine,
            'car2_price': car2.price,
            'car2_features': car2.features,
           'car2_i': car2.interior,
            'car2_transmission': car2.transmission,
           
        }

        html = '''
        <table class="table table-bordered" id="cmpTable">
            <tbody>
            
                
           <tr>
                <td>
                        Photo
                </td>
                <td>
                    <img class="img-fluid" src="{car1_pic}" alt="">
                </td>
                <td>
                    <img class="img-fluid" src="{car2_pic}" alt="">
                </td>
            </tr>

             <tr>
                <td>
                     Car Name
                </td>
                <td>
                    {car1_car}
                </td>
                <td>
                    {car2_car}
                </td>
            </tr>
            <tr>
                <td>
                    Price (in &#8377;)
                </td>
                <td>
                    {car1_price}
                </td>
                <td>
                    {car2_price}
                </td>
            </tr>

             <tr>
                <td>
                      Body style
                </td>
                <td>
                    {car1_body_style}
                </td>
                <td>
                    {car2_body_style}
                </td>
            </tr>

             <tr>
                <td>
                      Color
                </td>
                <td>
                    {car1_c}
                </td>
                <td>
                    {car2_c}
                </td>
            </tr>

             <tr>
                <td>
                          Model
                </td>
                <td>
                    {car1_model}
                </td>
                <td>
                    {car2_model}
                </td>
            </tr>

             <tr>
                <td>
                      Features
                </td>
                <td>
                    {car1_features}
                </td>
                <td>
                    {car2_features}
                </td>
            </tr>

            
         

            <tr>
                <td>
                      Engine
                </td>
                <td>
                    {car1_e}
                </td>
                <td>
                    {car2_e}
                </td>
            </tr>
            
             <tr>
                <td>
                      Milage
                </td>
                <td>
                    {car1_m}
                </td>
                <td>
                    {car2_m}
                </td>
            </tr>

            <tr>
                <td>
                      Interior
                </td>
                <td>
                    {car1_i}
                </td>
                <td>
                    {car2_i}
                </td>
            </tr>
            
            
            <tr>
                <td>
                    Transmission type
                </td>
                <td>
                    {car1_transmission}
                </td>
                <td>
                    {car2_transmission}
                </td>
            </tr>

             <tr>
                <td>
                     Fuel type
                </td>
                <td>
                    {car1_fuel_type}
                </td>
                <td>
                    {car2_fuel_type}
                </td>
            </tr>
            
            
            </tbody>
        </table>
        '''.format(**data)

        return HttpResponse(html)

    context = {
        'form': form
    }

    return render(request, 'cars/compare.html', context)




