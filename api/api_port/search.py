import json
from elasticsearch import Elasticsearch, ConnectionError
# import db_tool

error_name = ""

es = Elasticsearch()
# es = Elasticsearch(["http://localhost:9200"])

def get_json(string):
    return json.dumps(string, sort_keys=True, indent=4, separators=(",", ":"))

def json_print(string):
    print(json.dumps(string, sort_keys=True, indent=4, separators=(',', ':')))
    return

with open('api/api_port/MetaData.json','r',encoding='utf8') as fp:
    json_data = json.load(fp)

body = {
    # "settings": {
    #   "index": {
    #   "analysis": {
    #       "filter": {},
    #       "analyzer": {
    #         "keyword_analyzer": {
    #           "filter": [
    #             "lowercase",
    #             "asciifolding",
    #             "trim"
    #           ],
    #           "char_filter": [],
    #           "type": "custom",
    #           "tokenizer": "keyword"
    #         },
    #         "edge_ngram_analyzer": {
    #           "filter": [
    #             "lowercase"
    #           ],
    #           "tokenizer": "edge_ngram_tokenizer"
    #         },
    #         "edge_ngram_search_analyzer": {
    #           "tokenizer": "lowercase"
    #         }
    #       },
    #       "tokenizer": {
    #         "edge_ngram_tokenizer": {
    #           "type": "edge_ngram",
    #           "min_gram": 2,
    #           "max_gram": 5,
    #           "token_chars": [
    #             "letter"
    #           ]
    #         }
    #       }
    #     }
    #   }
    # },
    
    # "mappings" : {
    #   "properties" : {
    #     "date" : {
    #         "type" : "text"
    #     },
    #     "paper_id" : {
    #         "type" : "text",
    #     },
    #     "title" : {
    #         "type" : "text",
    #         "fields": {
    #             "keywordstring":{
    #                 "type": "text",
    #                 "analyzer": "keyword_analyzer"
    #             },
    #             "edgengram": {
    #                 "type" : "text",
    #                 "analyzer" : "edge_ngram_analyzer",
    #                 "search_analyzer": "edge_ngram_search_analyzer"
    #             },
    #             "completion": {
    #                 "type" : "completion"
    #             }
    #         },
    #         "analyzer": "standard"
    #     },
    #     "year" : {
    #       "type" : "long",
    #     },
    #     "authors" :{
    #         "type" : "list",
    #     },
    #     "keywords" : {
    #         "type" : "list",
    #     },
    #     "link" : {
    #         "type" : "text"
    #     },
    #     "first_page" : {
    #         "type" : "long"
    #     }
    #   }
    # }

    "mappings": {
      "properties": {
        "data": {
          "type": "text",  
        },
        "paper_id":{
            "type": "text",
            
        },
        "title": {
            "type": "text",
        },
        "year" : {
          "type" : "long",
        },
        "authors" :{
            "type" : "list",
        },
        "keywords" : {
            "type" : "list",
        },
        "link" : {
            "type" : "text"
        },
        "first_page" : {
            "type" : "long"
        },
        "abstract" : {
            "type" : "text"
        },
        "journal" : {
            "type" : "text"
        },
        "doi" : {
            "type" : "text"
        },
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
abstract = []
journal = []
doi = []

for value in json_data.values():
    date.append(value["date"])
    paper_id.append(value["paper_id"])
    title.append(value["title"])
    year.append(value["year"])
    authors.append(value["author"]["name"])
    keywords.append(value["keywords"])
    link.append(value["link"])
    first_page.append(value["first_page"])
    abstract.append(value["abstract"])
    journal.append(value["journal"])
    doi.append(value["doi"])
try:
    # es.indices.delete(index = 'mydatabase')
    es.indices.create(index ='mydatabase',body=body,ignore=400)
    for i in range(100):
        mapping = {"date":date[i],"paper_id":paper_id[i],"title":title[i],"year":year[i],"authors":authors[i],"keywords":keywords[i],"link":link[i],"first_page":first_page[i],"abstract":abstract[i],"journal":journal[i],"doi":doi[i]}
        # mapping = {"title":title[i]}
        res = es.index(index="mydatabase",id=i,body=mapping)

    def search_title(str):
        query = {
            "query":{
                "wildcard":{
                    "title": "*" + str.lower() + "*"
                },
                
                # "match":{
                #     "title": str
                # }
            }
            ,"sort": [
                {
                    "_score":{
                        "order": "desc"
                    }
                }
            ]
            ,"size":1000
        }
        query2 = {
            "query": {
                "match": {
                    "title": {
                        "query": str,
                        "fuzziness": "2"
                    }
                }
            }
            ,"size":1000
        }
        result = es.search(index="mydatabase",body=query2)
        
        hit = result["hits"]["hits"]
        return hit

    def search_year(time):
        query = {
            "query":{
                "match":{
                    "year": time
                }
            }
            ,"size":1000
        }
        result = es.search(index="mydatabase",body=query)
        hit = result["hits"]["hits"]
        return hit

    def search_author(str):
        query = {
            "query":{
                "wildcard":{
                    "authors": "*" + str.lower() + "*"
                }
                # "match":{
                #     "authors": str
                # }
            }
            ,"sort": [
                {
                    "_score":{
                        "order": "desc"
                    }
                }
            ]
            ,"size":1000
        }
        query2 = {
            "query": {
                "match": {
                    "authors": {
                        "query": str,
                        "fuzziness": "2"
                    }
                }
            },
            "size":1000
        }
        result = es.search(index="mydatabase",body=query2)
        hit = result["hits"]["hits"]
        return hit

    def search_keywords(str):
        query = {
            "query":{
                "wildcard":{
                    "keywords": "*" + str.lower() + "*"
                }
                # "match":{
                #     "keywords": str
                # }
            }
            ,"sort": [
                {
                    "_score":{
                        "order": "desc"
                    }
                }
            ]
            ,"size":1000
        }
        query2 = {
            "query": {
                "match": {
                    "keywords": {
                        "query": str,
                        "fuzziness": "2"
                    }
                }
            }
            ,"size":1000
        }
        result = es.search(index="mydatabase",body=query2)
        hit = result["hits"]["hits"]
        return hit


    def add_search(str):
        if(str.isdigit()):
            return search_year(int(str))
        else:
            hit1 = search_title(str)
            hit2 = search_author(str)
            hit3 = search_keywords(str)
            return hit1+hit2+hit3

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

    # json_print(search_title("tle"))
    # json_print(search_year(1990))
    # json_print(search_author("Carlson"))
    # json_print(search_keywords("try"))
    # json_print(add_search("mentle"))
except ConnectionError:
    print("连接错误:无法连接到Elasticsearch。")
    error_name = "ConnectionError"
except NameError:
    print("输入错误:根据年份查询需要输入数字")
    error_name = "NameError"