# from sqlalchemy import Column, UnicodeText, Integer
#
# from models.base_model import SQLMixin, db
# from models.user import User
#
#
# class Reply(SQLMixin, db.Model):
#     content = Column(UnicodeText, nullable=False)
#     topic_id = Column(Integer, nullable=False)
#     user_id = Column(Integer, nullable=False)
#
#     @classmethod
#     def new(cls, form, user_id):
#         form['user_id'] = user_id
#         m = super().new(form)
#         return m
#
#     def user(self):
#         u = User.one(id=self.user_id)
#         return
