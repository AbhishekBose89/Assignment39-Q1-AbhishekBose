from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path(
        "product/<int:product_id>/reviews",
        csrf_exempt(GetReviewByProduct.as_view()),
        name="get-reviews-by-product",
    ),
    path(
        "order/<int:order_id>/orderItems",
        csrf_exempt(GetOrderItemsByOrder.as_view()),
        name="get-orderItems-by-order",
    ),
    path(
        "product/search/",
        csrf_exempt(SearchProductApi.as_view()),
        name="search-product",
    ),
    path("product/", csrf_exempt(FilteredProduct.as_view()), name="sorted-product"),
    path(
        "product/page/",
        csrf_exempt(PaginatedProducts.as_view()),
        name="paginated_product",
    ),
    path(
        "product/search/page/",
        csrf_exempt(SearchPaginatedProduct.as_view()),
        name="search-paginated-product",
    ),
    path(
        "product/filter/price",
        csrf_exempt(GetFilterBooksByPrice.as_view()),
        name="filter-by-price",
    ),
    path(
        "product/filter/multiple",
        csrf_exempt(GetMultipleFilterProducts.as_view()),
        name="filter-by-multiple-queries",
    ),
    path(
        "product/match", csrf_exempt(MatchProducts.as_view()), name="get-match-products"
    ),
    path("signup", Signup.as_view(), name="signup"),
    path("signin", Signin.as_view(), name="signin"),
]
