from django.contrib.auth.models import User
from Users.models import Attachment , Profile
from passlib.hash import pbkdf2_sha256
class UserModel: 
    def __init__(self , dataUser):
        self.id_employee =  dataUser['id_employee']
        self.first_name =  dataUser['name_user']
        self.last_name_user =  dataUser['last_name_user']
        self.username =  dataUser['username']
        self.password =  dataUser['password']
        self.email =  dataUser['email']
        self.tel =  dataUser['tel']
    
    def get_model(self): 
        return {
            "id_employee": self.id_employee,
            "first_name": self.first_name,
            "last_name_user": self.last_name_user,
            "username": self.username,
            "password": self.password,
            "tel": self.tel,
            "email" : self.email

        }
    
    def _find_user_by_email(self,email):
        try:
            return User.objects.get(email=email)
        except expression as identifier:
            return e

    def create_user_data(self):
        try:
            user = User(username=self.username,first_name=self.first_name,last_name=self.last_name_user,email=self.email , employeeID=self.id_employee)
            user.set_password(self.password)
            user.save()
            userCreated = self._find_user_by_email(self.email)
            createProfile = Profile(user=userCreated , tel=self.tel)
            createProfile.save()
            return "create new user successfully."
        except Exception as e:
            return e