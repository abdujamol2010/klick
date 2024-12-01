from django.db.models import Q
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)

from goods.models import Products

def q_search(query):
    # Проверка на числовой запрос (ID)
    if query.isdigit() and len(query) <= 5:
        product = Products.objects.filter(id=int(query))
        return product if product.exists() else Products.objects.none()

    # Подготовка вектора поиска и запроса
    vector = SearchVector("name", "description")
    search_query = SearchQuery(query)

    # Аннотирование с ранжированием и заголовками
    result = (
        Products.objects.annotate(rank=SearchRank(vector, search_query))
        .filter(rank__gt=0)
        .order_by("-rank")
        .annotate(
            headline=SearchHeadline(
                "name",
                search_query,
                start_sel='<span style="background-color: yellow;">',
                stop_sel="</span>"
            ),
            bodyline=SearchHeadline(
                "description",
                search_query,
                start_sel='<span style="background-color: yellow;">',
                stop_sel="</span>"
            )
        )
    )

    return result
