from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from rest_framework import filters, status, views, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import CategoryGenreModelMixin, TitleModelMixin
from .permissions import (AdminOnlyPermission,
                          AdminPermissionOrReadOnlyPermission,
                          AuthorAdminModeratorObjectPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer,
                          UserSerializer, UserSerializerOrReadOnly,
                          UserSignupSerializer)
from .validators import email_validator


@api_view(['POST'])
def send_confirmation_code(request):
    """Отправка письма с кодом подтверждения на почту."""
    email = request.data.get('email')
    email_validator(email)
    email_split = email.split('@')
    username = email_split[0]
    user = User.objects.get_or_create(
        is_active=False,
        email=email,
        username=username,

    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Подтверждение регистрации',
        (f'Для получения токена и подтверждения регистрации сделайте '
         f'post-запрос со следующими параметрами:\n'
         f'Ваш email : {email}\n'
         f'Код подтверждения: {confirmation_code}'),
        f'{settings.CONTACT_EMAIL}',
        [email],
        fail_silently=False,
    )

    return Response({'email': email})


class UserSignupViewset(views.APIView):
    """Регистрация нового пользователя, получение кода."""
    permission_classes = (AllowAny,)

    def tokensend(self, user, username, email):
        token = default_token_generator.make_token(user)
        send_mail('confirmation_code',
                  token,
                  'admin@yamdb.ru',
                  [email])

    def post(self, request):
        try:
            username = request.data['username']
            email = request.data['email']
            user = User.objects.get(username=username, email=email)
            self.tokensend(user, username, email)
        except (KeyError, User.DoesNotExist):
            serializer = UserSignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            username = request.data['username']
            email = request.data['email']
            if username == 'me':
                return Response(
                    {'Использовать имя "me" в качестве username запрещено.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = serializer.save()
            self.tokensend(user, username, email)
        return Response(
            {'username': username, 'email': email},
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
def get_token(request):
    """Получение токена."""
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    if not confirmation_code or not username:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=username)
    result = {'info': 'Введите правильный confirmation_code'}
    if default_token_generator.check_token(
            user=user,
            token=confirmation_code
    ):
        user.is_active = True
        user.save()

        def get_tokens_for_user(current_user):
            refresh = RefreshToken.for_user(current_user)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        result = get_tokens_for_user(user)
    return Response(result, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    """API для работы с моделью отзывов"""

    serializer_class = ReviewSerializer
    permission_classes = (
        AuthorAdminModeratorObjectPermission,
        IsAuthenticatedOrReadOnly
    )

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        queryset = title.reviews.order_by('id')
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    """API для работы с моделью комментариев"""

    permission_classes = (
        AuthorAdminModeratorObjectPermission,
        IsAuthenticatedOrReadOnly
    )
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        queryset = review.comments.order_by('id')
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )


class CategoryViewSet(CategoryGenreModelMixin):
    """API для работы с моделью категорий"""

    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminPermissionOrReadOnlyPermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class GenreViewSet(CategoryGenreModelMixin):
    """API для работы с моделью жанров"""

    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminPermissionOrReadOnlyPermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class TitleViewSet(TitleModelMixin):
    """API для работы произведений"""

    queryset = Title.objects.order_by('id').annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (AdminPermissionOrReadOnlyPermission,)
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    """API для работы пользователями"""

    lookup_field = 'username'
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (AdminOnlyPermission,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """
        Запрос и возможность редактирования
         информации профиля пользователя.
        """
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        if request.method == 'PATCH':
            serializer = UserSerializerOrReadOnly(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
