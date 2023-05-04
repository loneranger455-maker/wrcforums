from .models import *
def get_profile_image_for_comment(allcomments):
        for x in allcomments:
            x.append(str(UserProfile.objects.get(user_instance=
            User.objects.get(username=x[0])).user_profile_picture))
        return allcomments

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]