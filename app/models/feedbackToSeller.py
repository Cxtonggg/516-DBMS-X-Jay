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
    def GetFeedback(uid, sid):
        try:
            rows = app.db.execute("""
SELECT ratings, review
FROM Seller_Feedback
WHERE uid = :uid and sid = :sid
""",


                                  uid = int(uid), sid = int(sid))
            return rows[0][0], rows[0][1]
        except Exception as e:
            print(str(e))
            return None, None


    @staticmethod
    def UpdateFeedback(uid, sid, ratings, text):
        try:
            rows = app.db.execute("""
UPDATE Seller_Feedback SET ratings=:ratings, review=:text
WHERE Seller_Feedback.uid = :uid and Seller_Feedback.sid = :sid
RETURNING sid 
""",
                                  ratings = ratings,
                                  text = text,
                                  uid = uid, sid = sid)
            return rows
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def GetVote(uid, sid):
        try:
            rows = app.db.execute("""
SELECT vote
FROM Seller_Feedback
WHERE uid = :uid and sid = :sid
""",


                                  uid = int(uid), sid = int(sid))
            return rows[0][0]
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def vote(uid, sid, vote):
        try:
            rows = app.db.execute("""
UPDATE Seller_Feedback SET vote=:vote
WHERE Seller_Feedback.uid = :uid and Seller_Feedback.sid = :sid
RETURNING vote
""",
                                  vote = vote,
                                  uid = uid, sid = sid)
            return rows[0][0]
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def removeFeedback(uid,sid):
        deletequery = app.db.execute('''
DELETE FROM Seller_Feedback
WHERE uid=:uid AND sid=:sid 
''',
                uid=uid, sid=sid)
        return deletequery if deletequery is not None else None

    @staticmethod
    def SummaryRatings(sid):
        try:
            rows = app.db.execute('''
SELECT COUNT(ratings), AVG(ratings)
FROM Seller_Feedback
WHERE sid = :sid
GROUP BY sid
''',
                    sid = sid)
            return rows[0][0], rows[0][1]
        except Exception as e:
            print(str(e))
            return None, None


