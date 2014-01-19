import os, pymongo, sendgrid, lob, stripe

bin_dir = os.environ['bin_dir']
lob.api_key = os.environ['lob_api_key']
s = sendgrid.Sendgrid(os.environ['s_user'], os.environ['s_pass'], secure=True)
stripe.api_key = "sk_test_qnFVxzNRQbpEKusxV5DCa2CI"
client = pymongo.MongoClient(os.environ['db'])
db = client.postpushr
users = db.users
letters = db.letters
postcards = db.postcards