# coding: utf-8
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, LargeBinary, SmallInteger, String, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'categories'

    categoryid = Column(SmallInteger, primary_key=True)
    categoryname = Column(String(15), nullable=False)
    description = Column(Text)
    picture = Column(LargeBinary)


class Customerdemographic(Base):
    __tablename__ = 'customerdemographics'

    customertypeid = Column(NullType, primary_key=True)
    customerdesc = Column(Text)


class Customer(Base):
    __tablename__ = 'customers'

    customerid = Column(NullType, primary_key=True)
    companyname = Column(String(40), nullable=False)
    contactname = Column(String(30))
    contacttitle = Column(String(30))
    address = Column(String(60))
    city = Column(String(15))
    region = Column(String(15))
    postalcode = Column(String(10))
    country = Column(String(15))
    phone = Column(String(24))
    fax = Column(String(24))

    customerdemographics = relationship('Customerdemographic', secondary='customercustomerdemo')


class Employee(Base):
    __tablename__ = 'employees'

    employeeid = Column(SmallInteger, primary_key=True)
    lastname = Column(String(20), nullable=False)
    firstname = Column(String(10), nullable=False)
    title = Column(String(30))
    titleofcourtesy = Column(String(25))
    birthdate = Column(Date)
    hiredate = Column(Date)
    address = Column(String(60))
    city = Column(String(15))
    region = Column(String(15))
    postalcode = Column(String(10))
    country = Column(String(15))
    homephone = Column(String(24))
    extension = Column(String(4))
    photo = Column(LargeBinary)
    notes = Column(Text)
    reportsto = Column(ForeignKey('employees.employeeid'))
    photopath = Column(String(255))

    parent = relationship('Employee', remote_side=[employeeid])
    territories = relationship('Territory', secondary='employeeterritories')


class Region(Base):
    __tablename__ = 'region'

    regionid = Column(SmallInteger, primary_key=True)
    regiondescription = Column(NullType, nullable=False)


class Shipper(Base):
    __tablename__ = 'shippers'

    shipperid = Column(SmallInteger, primary_key=True)
    companyname = Column(String(40), nullable=False)
    phone = Column(String(24))


class Supplier(Base):
    __tablename__ = 'suppliers'

    supplierid = Column(SmallInteger, primary_key=True)
    companyname = Column(String(40), nullable=False)
    contactname = Column(String(30))
    contacttitle = Column(String(30))
    address = Column(String(60))
    city = Column(String(15))
    region = Column(String(15))
    postalcode = Column(String(10))
    country = Column(String(15))
    phone = Column(String(24))
    fax = Column(String(24))
    homepage = Column(Text)


t_usstates = Table(
    'usstates', metadata,
    Column('stateid', SmallInteger, nullable=False),
    Column('statename', String(100)),
    Column('stateabbr', String(2)),
    Column('stateregion', String(50))
)


t_customercustomerdemo = Table(
    'customercustomerdemo', metadata,
    Column('customerid', ForeignKey('customers.customerid'), primary_key=True, nullable=False),
    Column('customertypeid', ForeignKey('customerdemographics.customertypeid'), primary_key=True, nullable=False)
)


class Order(Base):
    __tablename__ = 'orders'

    orderid = Column(SmallInteger, primary_key=True)
    customerid = Column(ForeignKey('customers.customerid'))
    employeeid = Column(ForeignKey('employees.employeeid'))
    orderdate = Column(Date)
    requireddate = Column(Date)
    shippeddate = Column(Date)
    shipvia = Column(ForeignKey('shippers.shipperid'))
    freight = Column(Float)
    shipname = Column(String(40))
    shipaddress = Column(String(60))
    shipcity = Column(String(15))
    shipregion = Column(String(15))
    shippostalcode = Column(String(10))
    shipcountry = Column(String(15))

    customer = relationship('Customer')
    employee = relationship('Employee')
    shipper = relationship('Shipper')


class Product(Base):
    __tablename__ = 'products'

    productid = Column(SmallInteger, primary_key=True)
    productname = Column(String(40), nullable=False)
    supplierid = Column(ForeignKey('suppliers.supplierid'))
    categoryid = Column(ForeignKey('categories.categoryid'))
    quantityperunit = Column(String(20))
    unitprice = Column(Float)
    unitsinstock = Column(SmallInteger)
    unitsonorder = Column(SmallInteger)
    reorderlevel = Column(SmallInteger)
    discontinued = Column(Integer, nullable=False)

    category = relationship('Category')
    supplier = relationship('Supplier')


class Territory(Base):
    __tablename__ = 'territories'

    territoryid = Column(String(20), primary_key=True)
    territorydescription = Column(NullType, nullable=False)
    regionid = Column(ForeignKey('region.regionid'), nullable=False)

    region = relationship('Region')


t_employeeterritories = Table(
    'employeeterritories', metadata,
    Column('employeeid', ForeignKey('employees.employeeid'), primary_key=True, nullable=False),
    Column('territoryid', ForeignKey('territories.territoryid'), primary_key=True, nullable=False)
)


class OrderDetail(Base):
    __tablename__ = 'order_details'

    orderid = Column(ForeignKey('orders.orderid'), primary_key=True, nullable=False)
    productid = Column(ForeignKey('products.productid'), primary_key=True, nullable=False)
    unitprice = Column(Float, nullable=False)
    quantity = Column(SmallInteger, nullable=False)
    discount = Column(Float, nullable=False)

    order = relationship('Order')
    product = relationship('Product')
