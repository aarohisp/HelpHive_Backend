from app import db
from sqlalchemy import Enum

# class RoleModel(db.Model):
#     __tablename__ = 'role'

#     role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     role_name = db.Column(db.String(40), nullable=False)
#     description_role = db.Column(db.String(100))
#     org_id = db.Column(db.Integer, db.ForeignKey('org.org_id'), nullable=False)

#     org = db.relationship('OrgModel', backref='roles')

class UserModel(db.Model):
    __tablename__ = 'UserModel'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    uname = db.Column(db.String(50), unique=True)
    password = db.Column(db.VARBINARY(120)) 
    email = db.Column(db.String(100), unique=True)
    phoneno = db.Column(db.String(15), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    # role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    # org_id = db.Column(db.Integer, db.ForeignKey('org.org_id'), nullable=False)

    # role = db.relationship('RoleModel', backref='users')
    # org = db.relationship('OrgModel', backref='users')

    def __repr__(self):
        return f'<User: {self.email}>'

class ItemModel(db.Model):
    __tablename__ = 'Item'

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(25), nullable=False)
    descriptions = db.Column(db.String(100), nullable=False)
    time_used = db.Column(db.Integer, nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('UserModel.user_id'), nullable=False)
    category = db.Column(db.Enum('clothes', 'medicine', 'furniture', 'medical supplies', 'school essentials', 'stationery', name='category_enum'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    item_address = db.Column(db.String(100), nullable=False)
    image_info = db.Column(db.ARRAY(db.Integer), nullable=True)
    specification = db.Column(db.String(50), nullable=False)
    item_check = db.Column(db.Boolean, default=False)
    status_item = db.Column(db.Enum('open', 'closed', 'expired', name='status_item_enum'), nullable=False, default='open')
    
    # Define the relationship with UserModel
    donor = db.relationship('UserModel', backref='donated_items', foreign_keys=[donor_id])
    images = db.relationship("ImageModel", secondary="item_image", back_populates="items")

class ImageModel(db.Model):
    __tablename__ = 'images'
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_data = db.Column(db.LargeBinary)

    items = db.relationship("ItemModel", secondary="item_image", back_populates="images")

class ItemImage(db.Model):
    __tablename__ = 'item_image'

    item_id = db.Column(db.Integer, db.ForeignKey('Item.item_id'), primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'), primary_key=True)
    
    items = db.relationship("ItemModel", backref=db.backref("image_assoc"))
    images = db.relationship("ImageModel", backref=db.backref("item_assoc"))
