from django.shortcuts import render,redirect
from apps.categories.models import CategoryModel
from django.contrib import messages

from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required("categories.view_categorymodel", raise_exception=True)

def category_list(request):
    categories = CategoryModel.objects.all().order_by("-created_at")
    context = {
        "category_key" : categories,
    }

    return render(request, "category_list.html", context)


@login_required
@permission_required("categories.add_categorymodel", raise_exception=True)
def category_create(request):
    if request.method == "POST":
        category = CategoryModel.objects.create(
            name = request.POST.get("user_input_name")
        )
        category.save()
        messages.success(request, "Category Created Successfully!")
        return redirect("cl")

    return render(request, "category_create.html")

@login_required
@permission_required("categories.change_categorymodel", raise_exception=True)
def category_update(request,user_id):
    category = CategoryModel.objects.get(id=user_id)
    if request.method == "POST":
        category.name = request.POST.get("user_input_name")
        category.save()
        messages.warning(request, "Category Updated Successfully!")
        return redirect("cl")

    context = {
            "category_key" : category,
        }
    return render(request, "category_update.html",context)


@login_required
@permission_required("categories.delete_categorymodel", raise_exception=True)
def category_delete(request,user_id):
    category = CategoryModel.objects.get(id=user_id)
    category.delete()
    messages.error(request, "Category Deleted Successfully!")
    return redirect("cl")