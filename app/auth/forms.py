#encoding: utf-8

from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

Province_choice = [('北京市', '北京市'), ('天津市', '天津市'), ('上海市', '上海市'), ('天津市', '天津市'), ('重庆市', '重庆市'), ('河北', '河北'),
                   ('山东', '山东'), ('辽宁', '辽宁'), ('黑龙江', '黑龙江'), ('吉林', '吉林'), ('甘肃', '甘肃'), ('青海', '青海'),
                   ('河南', '河南'), ('江苏', '江苏'), ('湖北', '湖北'), ('湖南', '湖南'), ('江西', '江西'), ('浙江', '浙江'),
                   ('广东', '广东'), ('云南', '云南'), ('福建', '福建'), ('台湾', '台湾'), ('海南', '海南省'), ('山西', '山西'),
                   ('四川', '四川'), ('陕西', '陕西'), ('贵州', '贵州'), ('安徽', '安徽'), ('广西', '广西'), ('内蒙古', '内蒙古'),
                   ('西藏', '西藏'), ('新疆', '新疆'), ('宁夏', '宁夏'), ('澳门', '澳门'), ('香港', '香港')]


class LoginForm(Form):
    username = StringField('用户名', validators=[Required(), Length(1, 64)])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登录')


class RegistrationForm(Form):
    name = StringField('姓名', render_kw={'placeholder':u'请输入姓名'}, validators=[Required(),
        Length(1, 20), Regexp('^[a-zA-Z\u4e00-\u9fa5]*$', 0, '只能输入英文和中文')])
    telephone = StringField('电话', render_kw={'placeholder':u'请输入手机号码'},
        validators=[Required(), Length(1, 32), Regexp('^[0-9+-.]*$', 0, '请输入正确的手机号码')])
    email = StringField('邮箱', render_kw={'placeholder':u'请输入邮箱地址'},
        validators=[Required(), Length(1, 64), Email()])
    username = StringField('用户名', render_kw={'placeholder':u'请输入用户名'},
        validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '支持英文和字母下划线')])
    password = PasswordField('密码', render_kw={'placeholder':u'请输入密码，字母、数字和特殊符号组合'},
        validators=[Required(), Length(6, 20, message='长度位于6~20之间'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '支持英文和字母下划线'), EqualTo('password2',
            message='两次密码不一致')])
    password2 = PasswordField('确认密码', render_kw={'placeholder':u'请再次输入密码'},
        validators=[Required()])
    about_me = TextAreaField('备注')
    submit = SubmitField('立即注册')

    def validate_email(self, field):
        if User.query.filter(User.email==field.data).first():
            raise ValidationError('邮箱已被注册.')

    def validate_username(self, field):
        if User.query.filter(User.username==field.data).first():
            raise ValidationError('用户名已被注册.')

    def validate_telephone(self, field):
        if User.query.filter(User.telephone==field.data).first():
            raise ValidationError('手机号已被注册.')


class PasswordResetRequestForm(Form):
    email = StringField('邮箱地址', render_kw={'placeholder':u'请输入邮箱地址'},
        validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if not User.query.filter(User.email==field.data).first():
            raise ValidationError('邮箱不存在,请重新确认')


class PasswordResetForm(Form):
    password = PasswordField('密码', render_kw={'placeholder':u'请输入密码，字母、数字和特殊符号组合'},
        validators=[Required(), Length(6, 20, message='长度位于6~20之间'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '支持英文和字母下划线'), EqualTo('password2',
            message='两次密码不一致')])
    password2 = PasswordField('确认密码', render_kw={'placeholder':u'请再次输入密码'},
        validators=[Required()])
    submit = SubmitField('修改')


class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='两次密码不一致.')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('修改')


class ChangeEmailForm(Form):
    email = StringField('新邮箱地址', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('修改')

    def validate_email(self, field):
        pass
        # if MongoClient().blog.User.find_one({'temp': field.data}) is not None:
            # raise ValidationError('此邮箱已经注册.')

class EditProfileForm(Form):
    name = StringField('姓名', validators=[Length(1, 20)])
    telephone = StringField('电话', validators=[Length(1, 32)])
    email = StringField('邮箱', validators=[Length(0, 64)])
    username = StringField('用户名', validators=[Length(0, 64)])
    about_me = TextAreaField('备注')
    submit = SubmitField('提交')


class EditProfileAdminForm(Form):
    choices = [('Administrator', '管理员'), ('Moderator', '协管员'), ('User', '用户')]

    name = StringField('姓名', render_kw={'placeholder':u'请输入姓名'}, validators=[Required(),
        Length(1, 20), Regexp('^[a-zA-Z\u4e00-\u9fa5]*$', 0, '只能输入英文和中文')])
    telephone = StringField('电话', render_kw={'placeholder':u'请输入手机号码'},
        validators=[Required(), Length(1, 32), Regexp('^[0-9+-.]*$', 0, '请输入正确的手机号码')])
    email = StringField('邮箱', render_kw={'placeholder':u'请输入邮箱地址'},
        validators=[Required(), Length(1, 64), Email()])
    username = StringField('用户名', render_kw={'placeholder':u'请输入用户名'},
        validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '支持英文和字母下划线')])
    password = PasswordField('密码', render_kw={'placeholder':u'请输入密码，字母、数字和特殊符号组合'},
        validators=[Required(), Length(6, 20, message='长度位于6~20之间'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '支持英文和字母下划线'), EqualTo('password2',
            message='两次密码不一致')])
    password2 = PasswordField('确认密码', render_kw={'placeholder':u'请再次输入密码'},
        validators=[Required()])
    about_me = TextAreaField('备注')

    activate = BooleanField('账户激活状态')
    role = SelectField('权限', choices=choices)
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_email(self, field):
        if field.data == self.user.username:
            return
        if User.query.filter(User.email==field.data).first():
            raise ValidationError('邮箱已被注册.')

    def validate_username(self, field):
        if field.data == self.user.username:
            return
        if User.query.filter(User.username==field.data).first():
            raise ValidationError('用户名已被注册.')

    def validate_telephone(self, field):
        if field.data == self.user.telephone:
            return
        if User.query.filter(User.telephone==field.data).first():
            raise ValidationError('手机已被注册.')
