from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {"form": form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {"form": form})


def calculate(request):
    a = request.GET.get("a")
    b = request.GET.get("b")

    if a is not None and b is not None and a.isdigit() and b.isdigit():
        a, b = int(a), int(b)
        addition = a + b
        power = a**b
        context = {"a": a, "b": b, "addition": addition, "power": power, "error": None}
    else:
        context = {"error": "Ошибка: Параметры a и b должны быть целыми числами."}

    return render(request, "blog/calculate.html", context)


def matrix(request):
    if request.method == "POST":
        x = request.POST.get("x")
        y = request.POST.get("y")

        if x and y and x.isdigit() and y.isdigit():
            x, y = int(x), int(y)
            if x > 0 and y > 0:
                matrix = [[f"{i} + {j}" for j in range(y)] for i in range(x)]
                return render(
                    request, "blog/matrix.html", {"matrix": matrix, "x": x, "y": y}
                )

        return render(
            request,
            "blog/matrix.html",
            {"error": "Ошибка: x и y должны быть положительными целыми числами."},
        )

    return render(request, "blog/matrix.html")
