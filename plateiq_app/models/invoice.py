from db import db
from datetime import datetime

class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    seller = db.Column(db.String(50), nullable=False)
    buyer = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))
    digitized = db.Column(db.Boolean)
    invoice_datetime = db.Column(db.DateTime, nullable=False)

    def __init__(self, seller, buyer, description=None, digitized=None, invoice_datetime=None):
        self.seller = seller
        self.buyer = buyer
        self.description = description

        if digitized == None:
            digitized = False

        if digitized == True or digitized == 1 or digitized == '1':
            self.digitized = 1      # True
        else:
            self.digitized = 0      # False, for any garbage value also

        if invoice_datetime == None:
            self.invoice_datetime = datetime.now()
        else:
            self.invoice_datetime = invoice_datetime

    @classmethod
    def get_by_id(cls, id):
        invoice = cls.query.filter_by(id=id).first()
        return invoice

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.id

    def _json(self):
        return {'id': self.id,
                'seller': self.seller,
                'buyer': self.buyer,
                'description': self.description,
                'digitized': self.digitized,
                'invoice_datetime': str(self.invoice_datetime)
            }
