# Plate IQ - Backend Assignment

Ref: [PlateIQ-BackendEngineer-Assignment.pdf] (PlateIQ-BackendEngineer-Assignment.pdf)


#### System Requirements
* Python v3
* virtualenv

### Steps to Execute:
Execute below commands in order:
1) `virtualenv venv`
2) `source venv/bin/activate`
3) `pip install -r requirements.txt`
4) `python migrate.py`      # optional if data.db file exists (with sample data provided)
5) `python app.py`

#### To upload a __*pdf*__ document:
Open any browser and goto http://127.0.0.1:5000/ <br>
PDF's will be uploaded and stored under `./uploads` folder.

### API's:
* `GET /invoices`
```bash
curl --request GET \
  --url http://localhost:5000/invoices \
  --header 'Content-Type: application/json' \
```

* `GET /invoices/<id>`
```bash
curl --request GET \
  --url http://localhost:5000/invoices/1 \
  --header 'Content-Type: application/json' \
```

* `POST /invoices`
```bash
curl --request POST \
  --url http://localhost:5000/invoices \
  --header 'Content-Type: application/json' \
  --header 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  --form 'seller=seller 123' \
  --form 'buyer=buyer 123' \
  --form 'description=some free text desc' \
  --form digitized=0
```

* `PUT /invoices`
```bash
curl --request PUT \
  --url http://localhost:5000/invoices/1 \
  --header 'Content-Type: application/json' \
  --form 'seller=seller 123' \
  --form 'buyer=buyer 456' \
  --form 'description=foo bar' \
  --form digitized=1
```


* `PUT /invoices/<id>/digitize`
```bash
curl --request PUT \
  --url http://localhost:5000/invoices/1/digitize \
  --header 'Content-Type: application/x-www-form-urlencoded' \
```