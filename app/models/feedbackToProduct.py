from flask import current_app as app

class feedbackToProduct():
    def __init__(self, uid, pid, rate, review, time, vote):
        self.uid = uid
        self.pid = pid
        self.rate = rate
        self.review = review
        self.time = time
        self.vote = vote

    @staticmethod
    def AddFeedbackToProduct(uid, pid, ratings, text):
        #INSERT INTO table xxxxx RETURNING xxid
        try:
            rows = app.db.execute('''
INSERT INTO Product_Feedback(uid, pid, ratings, review)
VALUES (:uid, :pid, :ratings, :review)
RETURNING pid
''',
        uid=uid, pid=pid, ratings=ratings, review=text)
        
            return rows
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def VerifyComment(uid, pid):
        try:
        # see if they already commented
            rows = app.db.execute("""
SELECT uid, pid
FROM Product_Feedback
WHERE uid = :uid and pid = :pid
""",
                              uid=uid, pid = pid)
            return rows
        except Exception as e:
            print(str(e))
            return None


    @staticmethod
    def GetFeedback(uid, pid):
        try:
            rows = app.db.execute("""
SELECT ratings, review
FROM Product_Feedback
WHERE uid = :uid and pid = :pid
""",


                                  uid = int(uid), pid = int(pid))
            return rows[0][0], rows[0][1]
        except Exception as e:
            print(str(e))
            return None, None



    @staticmethod
    def UpdateFeedback(uid, pid, ratings, text):
        try:
            rows = app.db.execute("""
UPDATE Product_Feedback SET ratings=:ratings, review =:text
WHERE Product_Feedback.uid = :uid and Product_Feedback.pid = :pid
RETURNING uid
""",
                                  ratings = ratings,
                                  text = text,
                                  uid = uid, pid = pid)
            return rows
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def removeFeedback(uid,pid):
        deletequery = app.db.execute('''
DELETE FROM Product_Feedback
WHERE uid=:uid AND pid=:pid 
''',
                uid=uid, pid=pid)
        return deletequery if deletequery is not None else None

    @staticmethod
    def GetVote(uid, pid):
        try:
            rows = app.db.execute("""
SELECT vote
FROM Product_Feedback
WHERE uid = :uid and pid = :pid
""",


                                  uid = int(uid), pid = int(pid))
            return rows[0][0]
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def vote(uid, pid, vote):
        try:
            rows = app.db.execute("""
UPDATE Product_Feedback SET vote=:vote
WHERE Product_Feedback.uid = :uid and Product_Feedback.pid = :pid
RETURNING vote
""",
                                  vote = vote,
                                  uid = uid, pid = pid)
            return rows[0][0]
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def SummaryRatings(pid):
        try:
            rows = app.db.execute('''
SELECT COUNT(ratings), AVG(ratings)
FROM Product_Feedback
WHERE pid = :pid
GROUP BY pid
''',
                    pid = pid)
            return rows[0][0], rows[0][1]
        except Exception as e:
            print(str(e))
            return None, None
