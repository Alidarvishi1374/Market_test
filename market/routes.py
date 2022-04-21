
from itertools import count
import random
from flask_bcrypt  import Bcrypt
import bcrypt
from market import app,db
from flask import redirect, render_template, url_for, flash, request
from market import form
from market.models import Item, User
from market.form import PurchaseItem, Registerform, LoginForm, SellItem, ForgetPassword, ResetRequForm, TaideCode
from flask_login import login_user, logout_user, login_required, current_user
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import secrets
from kavenegar import *



#create route
@app.route('/')
def Home_page():
    return render_template('Home_page.html')

#create route wellcom
@app.route('/Wellcom')
def Wellcom():
    return render_template('Wellcom.html')

@app.route('/login', methods=["POST", "GET"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(name=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_pass=form.password.data):
            login_user(attempted_user)
            flash(f"ورود شما با موفقیت انجام شد ", category="success")
            return redirect(url_for('Market_page'))
        else:
            flash(f'نام کاربری یا رمز ورود شما اشتباه است',category="danger")

    return render_template('login.html', form=form)
    


@app.route('/market', methods=['GET','POST'])
@login_required
def Market_page():
    form_purchase = PurchaseItem()
    from_sell = SellItem()
    if request.method == "POST":
        purchased_item = request.form.get('form_purchase')
        selles_item = request.form.get('form_sell')
        s_Item_obj = Item.query.filter_by(name=selles_item).first()
        p_Item_obj = Item.query.filter_by(name=purchased_item).first()
        if p_Item_obj:
            if current_user.can_buy(p_Item_obj):
                p_Item_obj.buy(current_user)
                flash('خرید با موفقیت صورت گرفت',category="success")
            else:
                flash('موجودی حساب شما کافی نیست',category="danger")
        if selles_item:
            if current_user.can_sell(s_Item_obj):
                s_Item_obj.sell(current_user)
                flash('به فروشگاه برگشت داده شد',category="success")
        return redirect(url_for('Market_page'))

    if request.method == "GET":
        items=Item.query.all()
        owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template('market_page.html',items=items, form_purchase=form_purchase, owned_items=owned_items, form_sell=from_sell)


@app.route('/register', methods=['POST', 'GET'])
def register_page():
    form = Registerform()
    if form.validate_on_submit():
        create_to_user = User(name=form.username.data,
                                Address = form.Home_Address.data,
                                Email = form.Email.data,
                                password = form.password1.data,
                                coin = form.Coin.data,
                                Phone = form.Phone.data)
        db.session.add(create_to_user)
        db.session.commit()
        login_user(create_to_user)
        flash(f" حساب کاربری شما یجاد شده و وارد صفحه خرید فروشگاه شدید {create_to_user.name}", category="success")
        return redirect(url_for('Market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
              flash(f'ایجاد حساب کاربری با خطا مواجه شده شرح خطا: {err_msg}', category="danger")  
    return render_template('register.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f"با موفقیت خارج شدید", category="success")
    return redirect(url_for('Home_page'))

# def send_mail(user):
#     serial = Serializer(app.config['SECRET_KEY'], expires_in=300)
#     token=serial.dumps({'user_id':user.id}).decode('utf-8')
#     msg = Message('درخواست رمز جدید', recipients=[user.Email], sender='noreply@codejana.com')
#     msg.body=f''' برای تغیر رمز بر روی لینک زیر بزنید:
#     {url_for('reset_token',token=token,_external=True)}

#      '''


API_KEY = "6D756C62446F683446515A315A6E484B69426E4A4F4F6350527253594A35464C426F76485858784D52586B3D"
url = "https://api.kavenegar.com/v1/{API_KEY}/verify/lookup.json"

def send_pm():
    pass

@app.route('/reset_pass', methods=['GET', 'POST'])
def reset_req():
    form = ResetRequForm()
    if form.validate_on_submit:
        user = User.query.filter_by(Phone=form.Phone.data).first()
        if user:
            flash('کاربر پیدا شد', category='success')
            print(user.Phone)
            #return redirect(url_for('Taid'))
            # Phone_number = str(user.Phone)
            # try:
            #     send_pm
            #     secrest = secrets.SystemRandom()
            #     Code = random.randrange(100000,999999)
            #     print(Code)
            #     api = KavenegarAPI(API_KEY)
            #     params = {
            #               'sender': '10008663',
            #               'receptor': Phone_number,
            #               'message': Code
            #                }
            #     api.sms_send(params)
                # flash('کد اعتبارسنجی برای شما ارسال شد', category='seccess')
                # if Code != None:
                #    form = TaideCode()
                #    if form.validate_on_submit:
                #        Code_User = form.Code.data
                #        print(Code_User)
                #        if Code_User == None:
                #            password_hash = Bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
                #            db.session.commit()
                #            flash('پسورد شما با موفقیت تغییر کرد', category="successs")
                #        print(Code_User)
                #        return render_template('Taide_Code.html', form = form)
                # print(Code_User)
                # if Code == Code_User :
                #     form = ForgetPassword()
                #     return render_template('change_password.html', form=form)
                # return render_template('Taide_Code.html', form = form)

            # except Exception as ex:
            #     flash(f"خطایی در ارسال پیام رخ داه است  ممکن است مشکل از پنل ارسال پیام باشد {ex}", category='danger')
              #  return redirect(url_for('reset_req'))
            # form = ForgetPassword()
            # if form.validate_on_submit:
            #     password_hash = Bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
            #     db.session.commit()
            #     flash('پسورد شما با موفقیت تغییر کرد', category="successs")
            # return render_template('change_password.html', form = form)
        if user is None:
            flash('کاربر مرد نظر پیدا نشد')
    return render_template('Request_reset.html', form=form)

@app.route('/reset_pass/<token>', methods=['GET', 'POST'])
def reset_token(token):
    serial = Serializer(app.config['SECRET_KEY'])
    user_id = serial.loads(token)['user_id']
    user=User.query.get(user_id)
    if user is None:
        flash('توکن نامعتبر می باشد یا زمان استفاده از آن به اتمام رسیده است لطفا دوباره تلاش نمایید', category='warning')
        return redirect(url_for('reset_requ'))

    form = ForgetPassword()
    if form.validate_on_submit:
        hash_password = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
        db.session.commit()
        flash('پسورد تغیر کرد', 'success')
    return render_template('change_password.html', form = form)


    










                         