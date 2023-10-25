from app import db
from sqlalchemy import Enum

class OrgModel(db.Model):
    __tablename__ = 'org'

    org_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    org_name = db.Column(db.String(100), nullable=False)
    org_address = db.Column(db.String(255))
    org_contactno = db.Column(db.String(15))

class RoleModel(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(40), nullable=False)
    description_role = db.Column(db.String(100))
    org_id = db.Column(db.Integer, db.ForeignKey('org.org_id'), nullable=False)

    # Define the back reference to the Org table
    org = db.relationship('OrgModel', backref='roles')

class UserModel(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    uname = db.Column(db.String(50), unique=True)
    password = db.Column(db.VARBINARY(120))  # Ideally, this should be hashed
    email = db.Column(db.String(100), unique=True)
    phoneno = db.Column(db.String(15), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    org_id = db.Column(db.Integer, db.ForeignKey('org.org_id'), nullable=False)

    # Define foreign key relationships
    role = db.relationship('RoleModel', foreign_keys=[role_id])
    org = db.relationship('OrgModel', foreign_keys=[org_id])

    def __repr__(self) -> str:
        return f'<User: {self.email}>'
    
class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('OrgModel.org_id'), nullable=False)

class ItemModel(db.Model):
    __tablename__ = 'item'

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(25), nullable=False)
    descriptions = db.Column(db.String(100), nullable=False)
    time_used = db.Column(db.Integer, nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    item_address = db.Column(db.String(100), nullable=False)
    image_info = db.Column(db.String(2000), nullable=False)
    specification = db.Column(db.String(100), nullable=False)
    item_check = db.Column(db.Boolean, nullable=False, default=False)
    status_item = db.Column(db.Enum('open', 'closed', 'expired'), nullable=False, default='open')
    org_id = db.Column(db.Integer, db.ForeignKey('org.org_id'), nullable=False)

    category = db.relationship('Category', backref='categ_item', foreign_keys=[category_id])

class ImageModel(db.Model):
    __tablename__ = 'images'
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_data = db.Column(db.LargeBinary)
    org_id = db.Column(db.Integer, db.ForeignKey('org.org_id'), nullable=False)

    org = db.relationship('OrgModel', backref='images')
