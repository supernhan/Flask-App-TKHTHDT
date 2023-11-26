from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://LENHAN\SQLEXPRESS/QUANLYBDS_TEAM040210?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'

db = SQLAlchemy(app)

class FullContract(db.Model):
    __tablename__ = 'Full_Contract'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    full_contract_code = db.Column(db.String(10), nullable=True)
    customer_name = db.Column(db.String(50), nullable=False)
    year_of_birth = db.Column(db.Integer, nullable=True)
    ssn = db.Column(db.String(15), nullable=False)
    customer_address = db.Column(db.String(100), nullable=True)
    mobile = db.Column(db.String(15), nullable=True)
    property_id = db.Column(db.Integer, nullable=False)
    date_of_contract = db.Column(db.Date, nullable=True)
    price = db.Column(db.Numeric(18, 0), nullable=True)
    deposit = db.Column(db.Numeric(18, 0), nullable=True)
    remain = db.Column(db.Numeric(18, 0), nullable=True)
    status = db.Column(db.Boolean, nullable=False)
@app.route('/')
def index():
    contracts = FullContract.query.all()
    return render_template('index.html', contracts=contracts)
@app.route('/add_contract', methods=['GET', 'POST'])
def add_contract():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        customer_name = request.form['customer_name']
        year_of_birth = request.form['year_of_birth']
        ssn = request.form['ssn']
        customer_address = request.form['customer_address']
        mobile = request.form['mobile']
        property_id = request.form['property_id']
        date_of_contract = request.form['date_of_contract']
        price = request.form['price']
        deposit = request.form['deposit']
        remain = request.form['remain']
        status = 'status' in request.form

        # Sử dụng câu lệnh SQL với returning
        sql = text(
            """
            INSERT INTO Full_Contract
            (customer_name, year_of_birth, ssn, customer_address, mobile, property_id, date_of_contract, price, deposit, remain, status)
            VALUES (:customer_name, :year_of_birth, :ssn, :customer_address, :mobile, :property_id, :date_of_contract, :price, :deposit, :remain, :status)
            """
        ).bindparams(
            customer_name=customer_name,
            year_of_birth=year_of_birth,
            ssn=ssn,
            customer_address=customer_address,
            mobile=mobile,
            property_id=property_id,
            date_of_contract=date_of_contract,
            price=price,
            deposit=deposit,
            remain=remain,
            status=status
        )

        # Thực hiện câu lệnh SQL
        db.session.execute(sql)
        db.session.commit()
        # Chuyển hướng đến trang chủ sau khi thêm hợp đồng
        return redirect(url_for('index'))

    # Nếu là yêu cầu GET, render template add_contract.html
    return render_template('add_contract.html')

if __name__ == '__main__':
    app.run(debug=True)