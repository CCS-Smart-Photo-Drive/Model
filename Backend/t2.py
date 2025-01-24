# Test File to check if the database is connected properly or not

from myproject.manager.models import ImageEmbedding, Manager
from myproject import app
with app.app_context():
    a = ImageEmbedding.query.all()
    for i in a :
        print(i)
        print()
    # print(Member.query.all())