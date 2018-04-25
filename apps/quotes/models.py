from __future__ import unicode_literals
from django.db import models
import bcrypt, datetime

# Create your models here.

class User_Manager(models.Manager):
    def validate_reg(self, pack):
        errors = []
        checkName = pack['full_name']
        checkAlias = pack['alias']
        checkEmail = pack['email']
        checkPassword = pack['password']
        checkConfirm = pack['confirm']
        checkBDate = pack['birthdate']
        print(checkBDate)
        datetime.datetime.strptime(checkBDate, "%Y-%m-%d")
        today = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
        print(checkBDate)
        print(today)
        preExisting = User.objects.filter(email=checkEmail)
        if len(checkName) < 2:
            errors.append('Your nane must be at least 2 characters long.')
        if len(checkAlias) > 25:
            errors.append("The length of your alias is far to large!")
        if len(preExisting) > 0:
            errors.append("Your email has already been taken! :( sorry... not " + checkEmail + ", Ah-ha.")
        elif '.com' not in checkEmail:
            errors.append("What are you doing? Your email has to have a .com or .org. It is almost as if you don't care!")
        if len(checkPassword) < 8:
            errors.append("Your password needs to be at least 8 characters long. It isn't hard, " \
                                 "you are just stupid.")
        if checkPassword != checkConfirm:
            errors.append("Oh my god. Your fingers must look like all the wires behind your tv set. " \
                                "So first, untangle yourself. Then try again.")
        if today <= checkBDate:
            errors.append("The Date is wrong and so are you.")
        # if errors == []:
        #     hashed_pass = bcrypt.hashpw(checkPassword.encode(), bcrypt.gensalt())
        #     errors.append("your hashed password looks like this! {}".format(hashed_pass))
        #     result = bcrypt.checkpw(checkPassword.encode(), hashed_pass.encode())
        #     errors.append('Lets check the result! Here: {}'.format(result))
        # (Except for now...) this can return an empty dict, or one filled with error messages.
        return errors

    def validate_log(self, pack):
        print('The login validator has been hit!')
        error = "Username or Password does not exists or was typed incorrectly."
        checkEmail = pack['email']
        checkEmail = checkEmail.lower()
        print("You typed in {} as your email.".format(checkEmail))
        checkPassword = pack['password']
        existingUserCheck = User.objects.filter(email=checkEmail)
        print("Length of existing user search is: {}".format(len(existingUserCheck)))
        if len(existingUserCheck) > 0:
            userPass = User.objects.get(email=checkEmail).hashedPassword
            resultPass = bcrypt.checkpw(checkPassword.encode(), userPass.encode())
            print(resultPass)
            if resultPass:
                error = ""
                return error
        # returns error as a string * I-F * errors exist.
        return error


class Quote_Manager(models.Manager):
    def validate_quote(self, pack):
        existing = Quote.objects.filter(desc=pack['desc'])
        if len(existing) > 0:
            existing = True
        else:
            existing = False
        return existing


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField()
    hashedPassword = models.CharField(max_length=255)
    birthdate = models.DateField()
    objects = User_Manager()

    def __repr__(self):
        return "\n##########################\n" \
               "NAME: {}\nALIAS: {}\nEMAIL: {}\n" \
               "HASHED-PASSWORD: {}\nBIRTHDATE: {}\n##########################\n" \
               "".format(self.name, self.alias, self.email, self.hashedPassword, self.birthdate)


class Quote(models.Model):
    by_person = models.CharField(max_length=255)
    desc = models.TextField()
    posted_by = models.ForeignKey(User, related_name="posted")
    favorited_by = models.ManyToManyField(User, related_name="favorite_quotes")
    objects = Quote_Manager()

    def __repr__(self):
        return "\n##########################\n" \
               "By: {}\nDESC: {}\n##########################\n".format(self.by_person, self.desc, )