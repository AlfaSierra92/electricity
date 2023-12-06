import json
from google.cloud import firestore
from datetime import datetime


class Electricity(object):
    def __init__(self):
        self.db = firestore.Client()

    def clean(self):
        consumi = self.db.collection('consumi').get()

        for x in consumi:
            print("Cleaning: {x.id}")
            x.delete()

    def add_consumi(self, date, value):
        consumi_ref = self.db.collection('consumi')
        h = {
            'date': date,
            'value': value
        }
        consumi_ref.document(date).set(h)

    def get_lettura_consumi(self, date):
        consumi = []
        consumi_ref = self.db.collection('consumi')
        consumi_doc = consumi_ref.document(date).get()

        if consumi_doc.exists:
            consumi.append(consumi_doc.get("value"))
            consumi.append(False)
            return consumi
        else:
            # INTERPOLATE!!! TODO
            # consumi_collection = self.db.collection('consumi').get()
            valore = 0
            test = len(self.db.collection('consumi').get())
            if test >= 2:
                query = self.db.collection('consumi').order_by("date", direction=firestore.Query.DESCENDING).limit(2)
                docs = query.get()
                for x in docs:
                    valore = valore + x.get("value")
                valore = valore / 2
            else:
                query = self.db.collection('consumi').order_by("date", direction=firestore.Query.DESCENDING).limit(1)
                docs = query.get()
                for x in docs:
                    valore = valore + x.get("value")
                # valore = valore / 2
            consumi.append(valore)
            consumi.append(True)
            return consumi
