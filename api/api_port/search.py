import json
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError



# import db_tool

error_name = ""

# es = Elasticsearch()
es = Elasticsearch(["http://localhost:9200"])


def get_json(string):
    return json.dumps(string, sort_keys=True, indent=4, separators=(",", ":"))


def json_print(string):
    print(json.dumps(string, sort_keys=True, indent=4, separators=(",", ":")))
    return


with open("api/api_port/MetaData.json", "r", encoding="utf8") as fp:
    json_data = json.load(fp)

body = {
    "mappings": {
        "properties": {
            "data": {
                "type": "text",
            },
            "paper_id": {
                "type": "text",
            },
            "title": {
                "type": "completion",
            },
            "year": {
                "type": "long",
            },
            "authors": {
                "type": "list",
            },
            "keywords": {
                "type": "list",
            },
            "link": {"type": "text"},
            "first_page": {"type": "long"},
        }
    }
}

date = []
paper_id = []
title = []
year = []
authors = []
keywords = []
link = []
first_page = []

for value in json_data.values():
    date.append(value["date"])
    paper_id.append(value["paper_id"])
    title.append(value["title"])
    year.append(value["year"])
    authors.append(value["author"]["name"])
    keywords.append(value["keywords"])
    link.append(value["link"])
    first_page.append(value["first_page"])

# es.indices.delete(index="mydatabase")
try:
    es.indices.create(index="mydatabase", body=body, ignore=400)

    # es.indices.create(index='mydatabase', body=mappings, ignore=400, headers={'Content-Type': 'application/json'}
    for i in range(100):
        mapping = {
            "date": date[i],
            "paper_id": paper_id[i],
            "title": title[i],
            "year": year[i],
            "authors": authors[i],
            "keywords": keywords[i],
            "link": link[i],
            "first_page": first_page[i],
        }
        res = es.index(index="mydatabase", id=i, body=mapping)


    def search_title(str):
        query = {
            "query": {
                "wildcard": {"title": "*" + str.lower() + "*"}
                # "match":{
                #     "title": str
                # }
            },
            "sort": [{"_score": {"order": "desc"}}],
            "size": 1000,
        }
        result = es.search(index="mydatabase", body=query)
        hit = result["hits"]["hits"]
        return hit


    def search_year(time):
        query = {"query": {"match": {"year": time}}, "size": 1000}
        result = es.search(index="mydatabase", body=query)
        hit = result["hits"]["hits"]
        return hit


    def search_author(str):
        query = {
            "query": {
                "wildcard": {"keywords": "*" + str + "*"}
                # "match":{
                #     "authors": str
                # }
            },
            "sort": [{"_score": {"order": "desc"}}],
            "size": 1000,
        }
        result = es.search(index="mydatabase", body=query)
        hit = result["hits"]["hits"]
        return hit


    def search_keywords(str):
        query = {
            "query": {
                "wildcard": {"keywords": "*" + str + "*"}
                # "match":{
                #     "keywords": str
                # }
            },
            "sort": [{"_score": {"order": "desc"}}],
            "size": 1000,
        }
        result = es.search(index="mydatabase", body=query)
        hit = result["hits"]["hits"]
        return hit


    # def title_autocomplete(str):
    #     query = {
    #         "query":{
    #             "match":{
    #                 "title.edgengram":str
    #             }
    #         },
    #         "size":1000
    #     }
    #     res = es.search(index="mydatabase",body=query,filter_path = ['**.hits'])
    #     json_print(res)

    # def title_autocomplete(str):
    #     body = {
    #         "suggest": {
    #             "title_suggest": {
    #                 "text": str,
    #                 "completion": {
    #                     "field": "title",
    #                     "skip_duplicates": True,
    #                     "size": 10
    #                 }
    #             }
    #         }
    #     }
    #     res = es.search(index="mydatabase",body=body)
    #     json_print(res)

    # def title_autosolve(str):
    #     body = {
    #         "completion": {
    #         "field": "title.suggest",
    #         "size": 5,
    #          "fuzzy": {
    #           "fuzziness": 2
    #     }
    #     res = es.search(index="mydatabase",body=body)
    #     json_print(res)

    # json_print(search_title("tle"))
    # json_print(search_year(a))
    # json_print(search_author("Carlson"))
    # json_print(search_keywords("try"))

except ConnectionError:
    print("连接错误:无法连接到Elasticsearch。")
    error_name = "ConnectionError"
except NameError:
    print("输入错误:根据年份查询需要输入数字")
    error_name = "NameError"