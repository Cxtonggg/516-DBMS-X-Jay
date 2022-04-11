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
    def UpdateFeedback(uid, pid, ratings, text):
        try:
            rows = app.db.execute("""
UPDATE Product_Feedback SET ratings=:ratings, text=:text
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

    

    

