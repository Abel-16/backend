
from django.forms import DecimalField
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, ExpressionWrapper, DecimalField

# Create your views here.
# request -> response
# request handler
# action

def hello(request):
    # query_set = Product.objects.filter(unit_price__range=(20,30))
    # query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # query_set = Product.objects.filter(inventory= F('unit_price'))
    #sorting
    #  query_set = Product.objects.order_by('unit_price','-title').reverse() 
    # query_set = Product.objects.filter(collection__id=1).order_by('unit_price').reverse() 
    # product = Product.objects.order_by('unit_price')[0] 
    # product = Product.objects.earliest('unit_price')
    
    #limiting results
    # query_set = Product.objects.all()[:5]
    # query_set = Product.objects.values('id','title', 'collection__title')  ## return dic
    # query_set = Product.objects.filter(id__in   =OrderItem.objects.values('product_id').distinct() )
    # discounted_price = ExpressionWrapper(
        # F('unit_price') * 0.8, output_field=DecimalField())
    # query_set = Product.objects.annotate(discounted_price=discounted_price)
    # for product in query_set:
    #     print(product)
    return render(request, 'test.html', 
                #   {'name': 'abel', 'products': list(query_set)}
                  )