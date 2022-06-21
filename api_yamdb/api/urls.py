from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserSignupViewset,
                    UserViewSet, get_token, send_confirmation_code)

app_name = 'api'

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comment'
)
router.register('users', UserViewSet, basename='User')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'auth/email/',
        send_confirmation_code,
        name='send_confirmation_code'
    ),
    path('auth/signup/', UserSignupViewset.as_view(), name='signup'),
    path(
        'auth/token/',
        get_token,
        name='token_obtain_pair'
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
