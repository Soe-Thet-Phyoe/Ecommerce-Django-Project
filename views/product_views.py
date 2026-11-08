from django.shortcuts import render,redirect, get_object_or_404
from apps.products.models import ProductModel
from apps.categories.models import CategoryModel

from django.contrib import messages

from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required("products.view_productmodel", raise_exception=True)
def product_list(request):
    product = ProductModel.objects.all()

    context = {
        "product_key" : product
    }

    return render(request, "product_list.html", context)

@login_required
@permission_required("products.add_productmodel", raise_exception=True)
def product_create(request):
    category_data = CategoryModel.objects.all()

    context = {
        "category_data_key" : category_data
    }
    if request.method == "POST":
        product = ProductModel.objects.create(
            title = request.POST.get("user_input_title"),
            price = request.POST.get("user_input_price"),
            qty = request.POST.get("user_input_qty"),
            image = request.FILES.get("user_input_img"), #File type
            description = request.POST.get("user_input_des"),
            category_id = request.POST.get("user_input_category"))

        messages.success(request, "Product Created Successfully!")

        return redirect("pl")
       
        
    return render(request, "product_create.html", context)

@login_required
@permission_required("products.change_productmodel", raise_exception=True)
def product_update(request, user_id):

    category_data = CategoryModel.objects.all()
    
    item = get_object_or_404(ProductModel, id = user_id)
    if request.method == "POST":
        item.title = request.POST.get("user_input_title")
        item.price = request.POST.get("user_input_price")
        item.qty = request.POST.get("user_input_qty")
        item.category_id = request.POST.get("user_input_category")
        item.description = request.POST.get("user_input_des")

        if request.FILES.get("user_input_img"):
            item.image.delete(save=False)
            item.image = request.FILES.get("user_input_img")

        item.save()

        messages.warning(request, "Product Updated Successfully!")
        return redirect("pl")

    context = {
        "item_key" : item,
        "category_data_key" : category_data
    }

    return render(request, "product_update.html", context)

@login_required
@permission_required("products.delete_productmodel", raise_exception=True)
def product_delete(request, user_id):
    item = get_object_or_404(ProductModel, id = user_id)
    if item.image:
        item.image.delete(save=False)
    item.delete()

    messages.error(request, "Product Deleted Successfully!")

    return redirect("pl")