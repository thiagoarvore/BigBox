import json
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Case, IntegerField, Sum, When
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from bigbox.forms import (
    CategoryModelForm,
    KitModelForm,
    ProductModelForm,
    ProductSelectionForm,
)
from bigbox.models import Category, Kit, Product


@login_required(login_url="login")
def dashboard_view(request):
    raw_days = request.GET.get("days", "30")
    try:
        days = int(raw_days)
    except (TypeError, ValueError):
        days = 30

    if days < 1:
        days = 1
    if days > 365:
        days = 365

    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)

    kits_in_period = Kit.objects.filter(created_at__gte=start_date).prefetch_related(
        "content"
    )
    products_in_period = Product.objects.filter(created_at__gte=start_date)

    kit_signature_stats = {}
    product_usage = {}
    product_profit_estimated = {}

    for kit in kits_in_period:
        content_ids = tuple(sorted(kit.content.values_list("id", flat=True)))
        signature = (kit.label, content_ids)
        stats = kit_signature_stats.get(signature)
        if stats is None:
            stats = {
                "label": kit.label,
                "count": 0,
                "profit_total": 0.0,
                "latest_created_at": kit.created_at,
                "latest_pk": kit.pk,
                "profit_max": kit.profit,
            }
        stats["count"] += 1
        stats["profit_total"] += float(kit.profit or 0)
        if kit.created_at and kit.created_at > stats["latest_created_at"]:
            stats["latest_created_at"] = kit.created_at
            stats["latest_pk"] = kit.pk
        if kit.profit is not None and kit.profit > stats["profit_max"]:
            stats["profit_max"] = kit.profit
        kit_signature_stats[signature] = stats

        content_list = list(kit.content.all())
        split_profit = float(kit.profit or 0) / max(len(content_list), 1)
        for product in content_list:
            product_usage[product.pk] = product_usage.get(product.pk, 0) + 1
            product_profit_estimated[product.pk] = product_profit_estimated.get(
                product.pk, 0.0
            ) + split_profit

    top_kits_by_count = sorted(
        kit_signature_stats.values(),
        key=lambda x: (x["count"], x["latest_created_at"]),
        reverse=True,
    )[:5]

    top5_kits_chart_labels = [k["label"] for k in top_kits_by_count]
    top5_kits_chart_data = [k["count"] for k in top_kits_by_count]

    most_profitable_kit = kits_in_period.order_by("-profit", "-created_at").first()
    most_profitable_kit_total = None
    if kit_signature_stats:
        most_profitable_kit_total = max(
            kit_signature_stats.values(),
            key=lambda x: (x["profit_total"], x["latest_created_at"]),
        )

    most_used_product = None
    if product_usage:
        most_used_product_id = max(product_usage.items(), key=lambda x: x[1])[0]
        most_used_product = Product.objects.filter(pk=most_used_product_id).first()

    most_profitable_product = None
    if product_profit_estimated:
        most_profitable_product_id = max(
            product_profit_estimated.items(), key=lambda x: x[1]
        )[0]
        most_profitable_product = Product.objects.filter(
            pk=most_profitable_product_id
        ).first()

    kits_profit_total = kits_in_period.aggregate(total=Sum("profit"))["total"] or 0
    kits_profit_avg = kits_in_period.aggregate(avg=Avg("profit"))["avg"] or 0
    kits_price_avg = kits_in_period.aggregate(avg=Avg("price"))["avg"] or 0

    context = {
        "days": days,
        "start_date": start_date,
        "end_date": end_date,
        "products_count": products_in_period.count(),
        "kits_count": kits_in_period.count(),
        "categories_count": Category.objects.count(),
        "top5_kits_chart_labels": json.dumps(top5_kits_chart_labels),
        "top5_kits_chart_data": json.dumps(top5_kits_chart_data),
        "most_profitable_kit": most_profitable_kit,
        "most_profitable_kit_total": most_profitable_kit_total,
        "most_used_product": most_used_product,
        "most_used_product_count": product_usage.get(
            getattr(most_used_product, "pk", None), 0
        ),
        "most_profitable_product": most_profitable_product,
        "most_profitable_product_profit": product_profit_estimated.get(
            getattr(most_profitable_product, "pk", None), 0.0
        ),
        "kits_profit_total": kits_profit_total,
        "kits_profit_avg": kits_profit_avg,
        "kits_price_avg": kits_price_avg,
    }
    return render(request, "dashboard.html", context)


@method_decorator(login_required(login_url="login"), name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryModelForm
    template_name = "new_category.html"
    success_url = "/products_list/"


@method_decorator(login_required(login_url="login"), name="dispatch")
class ProductsListView(ListView):
    model = Product
    template_name = "products_list.html"
    context_object_name = "products"
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset().order_by("name")
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class Test(View):

    def get(self, request, *args, **kwargs):
        return render(template_name="test.html", request=request)


@method_decorator(login_required(login_url="login"), name="dispatch")
class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"


@method_decorator(login_required(login_url="login"), name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductModelForm
    template_name = "new_product.html"
    success_url = "/products_list/"


@method_decorator(login_required(login_url="login"), name="dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    form_model = ProductModelForm
    template_name = "product_update.html"
    success_url = "/product_detail/"
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"pk": self.object.pk})


@method_decorator(login_required(login_url="login"), name="dispatch")
class ProductDeleteView(DeleteView):
    model = Product
    form_model = ProductModelForm
    template_name = "product_delete.html"
    success_url = "products_list"

    def get_success_url(self):
        return reverse_lazy("products_list")


@method_decorator(login_required(login_url="login"), name="dispatch")
class ProductLogListView(DetailView):
    model = Product
    template_name = "product_log.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        audit_logs = product.history.all()
        parsed_logs = []
        for log in audit_logs:
            changes_dict = json.loads(log.changes)
            parsed_logs.append({"timestamp": log.timestamp, "changes": changes_dict})

        context["product"] = self.object
        context["audit_logs"] = (
            parsed_logs  # history é o campo do model Product e audit_logs é o que passa para o template
        )
        context["username"] = self.request.user.username
        return context


@method_decorator(login_required(login_url="login"), name="dispatch")
class KitListView(ListView):
    model = Kit
    template_name = "kit_list.html"
    context_object_name = "kits"
    paginate_by = 30

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .prefetch_related("content")
            .order_by("label", "-created_at")
        )
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(label__icontains=search)

        seen = set()
        keep_ids = []
        for kit in queryset:
            content_ids = tuple(sorted(kit.content.values_list("id", flat=True)))
            signature = (kit.label, content_ids)
            if signature in seen:
                continue
            seen.add(signature)
            keep_ids.append(kit.pk)

        if not keep_ids:
            return Kit.objects.none()

        ordering = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(keep_ids)],
            output_field=IntegerField(),
        )
        return (
            Kit.objects.filter(pk__in=keep_ids)
            .annotate(_order=ordering)
            .order_by("_order")
        )


@method_decorator(login_required(login_url="login"), name="dispatch")
class KitDetailView(DetailView):
    model = Kit
    template_name = "kit_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = self.object.content.all()

        return context


def create_kit(request):
    allproducts = Product.objects.all()
    if request.method == "POST":
        form = ProductSelectionForm(request.POST or None)
        if form.is_valid():
            selected_products = []
            all_products = Product.objects.all()

            for product in all_products:
                field_name = f"product_{product.id}"
                if form.cleaned_data.get(field_name):
                    selected_products.append(product)
            price = 27.99
            cost = (
                sum(product.price for product in selected_products)
                + 1.50
                + (price * 6 / 100)
            )
            profit = round(price - cost, 2)
            label = form.cleaned_data.get("label", "")

            kit = Kit.objects.create(cost=cost, price=27.99, profit=profit, label=label)
            kit.content.set(selected_products)

            return redirect("kit_list")
    else:
        form = ProductSelectionForm()

    context = {
        "form": form,
        "allproducts": allproducts,
    }
    return render(request, "new_kit.html", context)


class KitDeleteView(DeleteView):
    model = Kit
    form_model = KitModelForm
    template_name = "kit_delete.html"
    success_url = "kit_list"

    def get_success_url(self):
        return reverse_lazy("kit_list")


def create_identical_kit(request, pk):
    actual_date_time = datetime.now()
    original_kit = get_object_or_404(Kit, pk=pk)
    new_kit = Kit.objects.create(
        cost=original_kit.cost,
        price=original_kit.price,
        profit=original_kit.profit,
        label=original_kit.label,
        created_at=actual_date_time,
    )
    new_kit.content.set(original_kit.content.all())

    return HttpResponseRedirect(reverse("kit_list"))
