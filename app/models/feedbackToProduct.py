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
    def AddFeedbackToProduct(uid, pid, ratings, text, vote):
        #INSERT INTO table xxxxx RETURNING xxid
        try:
            rows = app.db.execute('''
INSERT INTO Product_Feedback(uid, pid, ratings, review, vote)
VALUES (:uid, :pid, :ratings, :review, :vote)
RETURNING pid
''',
        uid=uid, pid=pid, ratings=ratings, review=text, vote=vote)
        
        return rows
    except Exception as e:
        print(str(e))
        return None

    

