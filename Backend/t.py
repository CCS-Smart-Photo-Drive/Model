# Test File to check if the database is connected properly or not

from myproject.manager.models import Manager
from myproject.member.models import Member

from myproject import app
with app.app_context():
    print(Manager.query.all())
    print(Member.query.all())