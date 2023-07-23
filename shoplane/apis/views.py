import json
from django.http import JsonResponse
from django.views import View
from .serializer import (
    OrderSerializer,
    ProductSerializer,
    SigninSerializer,
    SignupSerializer,
)
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class GetReviewByProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if product:
            reviews = Review.objects.filter(product=product.id)
            review_list = []
            for review in reviews:
                review_data = {
                    "review_id": review.id,
                    "user_id": review.user,
                    "rate": review.rate,
                    "comment": review.review,
                    "active": review.active,
                    "created": review.created,
                }
                review_list.append(review_data)
            response_data = {
                "product_id": product.id,
                "product_name": product.name,
                "product_image": product.image,
                "product_brand": product.brand,
                "shipping": product.shipping,
                "description": product.description,
                "price": product.price,
                "category": product.category,
                "featured": product.featured,
                "active": product.active,
                "created": product.created,
                "reviews": review_list,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({"msg": "product not found"})


# class GetReviewByProduct(View):
# permission_classes = [IsAuthenticated]
#     def get(self, request, product_id):
#         product = Product.objects.filter(id=product_id).first()
#         if product:
#             reviews = Review.objects.filter(product=product.id).values()
#             serialized_product = ProductSerializer(product).data
#             serialized_product["reviews"] = list(reviews)
#             return JsonResponse(serialized_product, safe=False)
#         else:
#             return JsonResponse({"msg": "Product not found"})


class GetOrderItemsByOrder(View):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()
        if order:
            order_items = OrderItem.objects.filter(order=order.id)
            order_items_list = []
            for order_item in order_items:
                order_item_data = {
                    "product_id": order_item.product,
                    "quantity": order_item.quantity,
                    "price": order_item.price,
                }
                order_items_list.append(order_item_data)
            response_data = {
                "order_id": order.id,
                "order_no": order.order_number,
                "order_date": order.order_date,
                "order_items": order_items_list,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({"msg": "order not found"})


# class GetOrderItemsByOrder(View):
#   permission_classes = [IsAuthenticated]
#     def get(self,request,order_id):
#         order=Order.objects.filter(id=order_id).first()
#         if order:
#             order_items=OrderItem.objects.filter(order=order.id).values()
#             serialized_order=OrderSerializer(order).data
#             serialized_order["order_items"]=list(order_items)
#             return JsonResponse(serialized_order,safe=False)
#         else:
#             return JsonResponse({"msg":"Order not found"})


class SearchProductApi(View):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get("query", "")
        products = Product.objects.filter(name__icontains=query)
        if products:
            serialized_products = ProductSerializer(products, many=True).data
            return JsonResponse(serialized_products, safe=False)
        else:
            return JsonResponse({"msg": "Search product not found"})


class FilteredProduct(View):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brand = request.GET.get("brand", "")
        min_price = request.GET.get("min", 0)
        max_price = request.GET.get("max", 0)
        products = Product.objects.all()
        if brand:
            products = products.filter(brand__icontains=brand)
        if min_price:
            products = products.filter(price__gte=int(min_price))
        if max_price:
            products = products.filter(price__lte=int(max_price))
        serialized_products = ProductSerializer(products, many=True).data
        return JsonResponse(serialized_products, safe=False)


class PaginatedProducts(View):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page_num = request.GET.get("page", 1)
        products = Product.objects.all().order_by("id")
        paginator = Paginator(products, 5)
        page = paginator.get_page(page_num)
        product_obj = page.object_list
        serialized_products = ProductSerializer(product_obj, many=True).data
        return JsonResponse(
            {
                "data": serialized_products,
                "total_product": products.count(),
                "total_pages": paginator.num_pages,
            }
        )


class SearchPaginatedProduct(View):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = request.GET.get("name", "")
        page_num = request.GET.get("page", 1)
        products = Product.objects.filter(name__icontains=name)
        if products:
            paginator = Paginator(products, 5)
            page = paginator.get_page(page_num)
            product_obj = page.object_list
            serialized_products = ProductSerializer(product_obj, many=True).data
            return JsonResponse(
                {
                    "data": serialized_products,
                    "total_pages": paginator.num_pages,
                    "total_products": products.count(),
                }
            )
        else:
            return JsonResponse({"msg": "Product not found"})


class GetFilterBooksByPrice(View):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        min_price = request.GET.get("min", 0)
        max_price = request.GET.get("max", 0)
        if min_price and max_price:
            products = Product.objects.filter(
                Q(price__gte=min_price) & Q(price__lte=max_price)
            )
            serialized_product = ProductSerializer(products, many=True).data
            return JsonResponse(serialized_product, safe=False)
        else:
            return JsonResponse({"msg": "Please provide min and max both"})


class GetMultipleFilterProducts(View):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category = request.GET.get("category", None)
        brand = request.GET.get("brand", None)
        active = request.GET.get("active", None)
        if category and brand and active:
            products = Product.objects.filter(
                Q(category__iexact=category)
                & Q(brand__iexact=brand)
                & Q(active__in=[bool(int(active))])
            )
            # print(products)
            serialized_product = ProductSerializer(products, many=True).data
            return JsonResponse(serialized_product, safe=False)
        else:
            return JsonResponse({"msg": "Please provide the valid queries"})


class MatchProducts(View):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get("query", None)
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        serialized_products = ProductSerializer(products, many=True).data
        return JsonResponse(serialized_products, safe=False)


class Signup(APIView):
    def post(self, request):
        data = json.loads(request.body)
        exist_user = User.objects.filter(username=data["username"]).first()
        if not exist_user:
            serialized_user = SignupSerializer(data=data)
            if serialized_user.is_valid():
                user = serialized_user.save()
                refresh = RefreshToken.for_user(user)
                return JsonResponse(
                    {"refresh": str(refresh), "access": str(refresh.access_token)},
                    status=status.HTTP_201_CREATED,
                )
            return JsonResponse(
                {"msg": "unsuccessful registration"}, status=status.HTTP_400_BAD_REQUEST
            )
        return JsonResponse({"msg": "username is already exist"})


class Signin(APIView):
    def post(self, request):
        data = json.loads(request.body)
        serialized = SigninSerializer(data=data)
        if serialized.is_valid():
            user = serialized.validated_data
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )
        return JsonResponse(
            serialized.errors, safe=False, status=status.HTTP_401_UNAUTHORIZED
        )
