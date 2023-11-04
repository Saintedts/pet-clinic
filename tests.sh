curl http://localhost:8000/
curl -X POST -H "Content-Type: application/json" -d '{"id": 2, "timestamp": 15}' http://localhost:8000/post
curl "http://localhost:8000/dog?kind=terrier"
curl -X POST -H "Content-Type: application/json" -d '{"pk": 0, "name": "Buddy", "kind": "terrier"}' http://localhost:8000/dog
curl http://localhost:8000/dog/2
curl -X PATCH 'http://localhost:8000/dog/0?name=Buddy&kind=terrier'