from flask_restful import Resource, request
from models.invoice import Invoice

class InvoiceResource(Resource):
    def get(self, id):
        invoice = Invoice.get_by_id(id)
        if invoice:
            return invoice._json(), 200

        return {'message': 'Error finding invoice with id={}'.format(id)}, 500

    def put(self, id):
        invoice = Invoice.get_by_id(id)
        if not invoice:
            return {'message': 'Error: Invoice with id={} not found'.format(id)}, 404

        data = request.form
        data_keys = [key.lower() for key in data.keys()]

        if 'seller' in data_keys:
            invoice.seller = data['seller']
        if 'buyer' in data_keys:
            invoice.buyer = data['buyer']
        if 'description' in data_keys:
            invoice.description = data['description']
        if 'digitized' in data_keys:
            if data['digitized'] == True or data['digitized'] == 1 or data['digitized'] == '1':
                digitized = 1  # True
            else:
                digitized = 0  # False, for any garbage value also

            invoice.digitized = digitized

        try:
            id = invoice.save()
        except Exception as e:
            return {'message': 'Error: {}'.format(e)}, 500

        return {'message': 'Invoice Updated', 'id': id}, 202


    def delete(self, id):
        invoice = Invoice.get_by_id(id)
        if invoice:
            id = invoice.delete()
            return {'message': 'Success: Invoice Id={} is Deleted'.format(id)}, 200

        return {'message': 'Error finding invoice with id={}'.format(id)}, 500


class InvoicesResource(Resource):
    def get(self):
        invoices = []
        for item in Invoice.query.all():
            invoices.append(item._json())

        return {'invoices': invoices}, 200

    def post(self):
        mimetype = request.mimetype

        data = request.form
        data_keys = [key.lower() for key in data.keys()]

        if 'seller' not in data_keys:
            return {'message': 'seller not provided'}, 404
        if 'buyer' not in data_keys:
            return {'message': 'buyer not provided'}, 404

        seller = data['seller']
        buyer = data['buyer']
        description = data.get('description', None)
        digitized = data.get('digitized', None)

        if 'invoice_datetime' in data_keys:
            invoice_datetime = data['invoice_datetime']
        else:
            invoice_datetime = None

        invoice = Invoice(seller, buyer, description, digitized, invoice_datetime)
        try:
            id = invoice.save()
        except Exception as e:
            return {'message': 'Error: {}'.format(e)}, 500

        return {'message': 'New Invoice Created', 'id':id}, 201



class MarkDigitizedInvoice(Resource):
    def put(self, id):
        invoice = Invoice.get_by_id(id)
        if not invoice:
            return {'message': 'Error: Invoice with id={} not found'.format(id)}, 404

        if invoice.digitized == 1:
            return {'message': 'Invoice Already Digitized', 'id': id}, 200

        invoice.digitized = 1
        try:
            id = invoice.save()
        except Exception as e:
            return {'message': 'Error: {}'.format(e)}, 500

        return {'message': 'Invoice Digitized', 'id':id}, 201


