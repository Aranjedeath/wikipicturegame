from django.shortcuts import render
# from game.wikipediaclient import generateQuestion
from django.http import HttpResponse
from game.models import WikipediaCategory, RowCounts
import json


_INITIAL_REQUEST_SIZE = 2


def home(request):
    if request.method == "GET":
        if request.is_ajax():
            categoryRequestSize = int(request.GET['amount'])
        else:
            categoryRequestSize = _INITIAL_REQUEST_SIZE

        rowCount = RowCounts.objects.get(tablename='game_wikipediacategory').rowcount
        # Query paraphrased from
        # https://www.periscope.io/blog/how-to-sample-rows-in-sql-273x-faster.html
        random_category_query = "select id, title from game_wikipediacategory " \
                                "where id in ( " \
                                "select round(random() * {0})::integer as id " \
                                "from generate_series(1, {1}) " \
                                "group by id) " \
                                "limit {2} ".format(rowCount,
                                                    categoryRequestSize * 10,
                                                    categoryRequestSize)

        randomCategorySet = WikipediaCategory.objects.raw(random_category_query)
        categories = []
        for m in randomCategorySet:
            categories.append(m.title)

        if request.is_ajax():
            return HttpResponse(json.dumps(categories), content_type='application/json')
        else:
            context = {"categories": json.dumps(categories)}
            return render(request, 'game/game.html', context)

    # if request.method == "POST":
    #     if request.is_ajax():
    #         data = json.loads(request.body.decode('utf-8'))
    #         category = data['category']
    #         try:
    #             question = generateQuestion(category)
    #             data = json.dumps(question)
    #         except ValueError as e:
    #             print(str(e))
    #             raise Exception
    #         return HttpResponse(data, content_type='application/json')
