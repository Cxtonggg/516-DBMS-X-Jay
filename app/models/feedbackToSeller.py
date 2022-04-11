from flask import current_app as app

class feedbackToSeller():
    def __init__(self, uid, sid, rate, review, time, vote):
        self.uid = uid
        self.sid = sid
        self.rate = rate
        self.review = review
        self.time = time
        self.vote = vote

    @staticmethod
    def AddFeedbackToSeller(uid, sid, ratings, text):
        #INSERT INTO table xxxxx RETURNING xxid
        try:
            rows = app.db.execute('''
INSERT INTO Seller_Feedback(uid, sid, ratings, review)
VALUES (:uid, :sid, :ratings, :review)
RETURNING sid
''',
        uid=uid, sid=sid, ratings=ratings, review=text)
        
            return rows
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def VerifyPurchase(uid, sid):
        try:
            rows1 = app.db.execute("""
SELECT uid, sid
FROM Purchases
WHERE uid = :uid and sid = :sid
""",
                              uid=uid, sid = sid)
        # see if they already commented
            rows2 = app.db.execute("""
SELECT uid, sid
FROM Seller_Feedback
WHERE uid = :uid and sid = :sid
""",
                              uid=uid, sid = sid)
            return rows1, rows2
        except Exception as e:
            print(str(e))
            return None, None

    @staticmethod
    def UpdateFeedback(uid, sid, ratings, text):
        try:
            rows = app.db.execute("""
UPDATE Seller_Feedback SET ratings=:ratings, text=:text
WHERE Seller_Feedback.uid = :uid and Seller_Feedback.sid = :sid
RETURNING id ?
""",
                                  ratings = ratings,
                                  text = text,
                                  uid = uid, sid = sid)
            return rows
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def vote(uid, sid, ratings):
        try:
            rows = app.db.execute("""
UPDATE Seller_Feedback SET vote=:ratings, text=:text
WHERE Seller_Feedback.uid = :uid and Seller_Feedback.sid = :sid
RETURNING id
""",
                                  ratings = ratings,
                                  text = text,
                                  uid = uid, sid = sid)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            print(str(e))
            return None

        

    

    

