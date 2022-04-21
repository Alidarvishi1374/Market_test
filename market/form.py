#download flask_wtf for import FlaskForm
from ast import Str
import email
from click import confirm
from flask_wtf import FlaskForm

#download wtforms for import StringField, PasswordField, SubmitField
from wtforms import StringField, SubmitField, PasswordField, IntegerField

#import from wtforms.validators Email,Length,Datarequirer(),..
# pip install email_validator
from wtforms.validators import Length, Email, DataRequired, EqualTo, ValidationError

from market.models import User




class Registerform(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(name=username_to_check.data).first()
        if user:
            raise ValidationError("نام کاربری موجود می باشد")

    def validate_Email(self, Email_to_check):
        user = User.query.filter_by(Email=Email_to_check.data).first()
        if user:
            raise ValidationError("این ایمیل موجود می باشد")

    def validate_Phone(self, Phone_to_check):
        user = User.query.filter_by(Phone=Phone_to_check.data).first()
        if user:
            raise ValidationError("این تلفن موجود می باشد")

    username = StringField(label="نام کاربری", validators=[Length(min=4, max=25), DataRequired()])
    Email = StringField(label="ایمیل", validators=[Email(), DataRequired()])
    Phone = StringField(label="شماره همراه", validators=[Length(min=11, max=11) ,DataRequired()])
    Home_Address = StringField(label="آدرس", validators=[DataRequired()])
    Coin = IntegerField(label="مقدار موجودی")
    password1 = PasswordField(label="رمز", validators=[Length(min=4), DataRequired()])
    password2 = PasswordField(label="تکرار رمز", validators=[EqualTo("password1"), DataRequired()])
    Submit = SubmitField(label="ایجاد حساب کاربری")

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    Signin = SubmitField(label="ورود")

class PurchaseItem(FlaskForm):
    Submit = SubmitField(label="برای خرید کلیک نمایید")

class SellItem(FlaskForm):
    Submit = SubmitField(label="برای حذف از سبد کلیک نمایید ")

class ResetRequForm(FlaskForm):
      Phone = StringField(validators=[DataRequired()])
      Submit = SubmitField(label="ارسال کد اعتبارسنجی")

class ForgetPassword(FlaskForm):
    password1 = PasswordField(validators=[Length(min=4), DataRequired()])
    password2 = PasswordField(validators=[EqualTo('password1'), DataRequired()])
    Submit = SubmitField(label="تغییر رمز عبور")

class TaideCode(FlaskForm):
    Code = StringField(validators=[DataRequired()])
    password1 = PasswordField(validators=[Length(min=4), DataRequired()])
    password2 = PasswordField(validators=[EqualTo('password1'), DataRequired()])
    Submit = SubmitField(label="تایید")
