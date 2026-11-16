from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from .extensions import db
from .models import Product, StockMovement, User

main_bp = Blueprint("main", __name__)
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.index"))
        flash("Usuário ou senha inválidos.", "error")
    return render_template("login.html")

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@main_bp.route("/")
@login_required
def index():
    term = request.args.get("q", "").strip()
    query = Product.query
    if term:
        query = query.filter(or_(Product.name.ilike(f"%{term}%"), Product.code.ilike(f"%{term}%")))
    products = query.order_by(Product.name).all()
    return render_template("index.html", products=products, term=term)

@main_bp.route("/products/new", methods=["GET", "POST"])
@login_required
def new_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        code = request.form.get("code", "").strip().upper()
        price = parse_money(request.form.get("price", ""))
        quantity = parse_int(request.form.get("quantity", ""))
        minimum = parse_int(request.form.get("minimum_stock", ""))
        if not name or not code or price is None or quantity is None or minimum is None:
            flash("Preencha os campos corretamente. Quantidades e preço não podem ser negativos.", "error")
        elif Product.query.filter_by(code=code).first():
            flash("Já existe um produto com esse código.", "error")
        else:
            db.session.add(Product(name=name, code=code, price_cents=price, quantity=quantity, minimum_stock=minimum))
            db.session.commit()
            flash("Produto cadastrado com sucesso.", "success")
            return redirect(url_for("main.index"))
    return render_template("product_form.html")

@main_bp.route("/movements/new", methods=["GET", "POST"])
@login_required
def new_movement():
    products = Product.query.order_by(Product.name).all()
    if request.method == "POST":
        product = db.session.get(Product, parse_int(request.form.get("product_id", "")) or -1)
        kind = request.form.get("movement_type", "")
        quantity = parse_int(request.form.get("quantity", ""))
        note = request.form.get("note", "").strip()
        if not product or kind not in ("entrada", "saida") or quantity is None or quantity <= 0:
            flash("Selecione um produto e informe uma quantidade inteira maior que zero.", "error")
        elif kind == "saida" and quantity > product.quantity:
            flash("Estoque insuficiente: a saída não pode deixar saldo negativo.", "error")
        else:
            # O movimento e o saldo são persistidos na mesma transação.
            product.quantity += quantity if kind == "entrada" else -quantity
            db.session.add(StockMovement(product=product, movement_type=kind, quantity=quantity, note=note))
            db.session.commit()
            flash("Movimentação registrada. Saldo atualizado.", "success")
            return redirect(url_for("main.index"))
    return render_template("movement_form.html", products=products)

def parse_int(value):
    try:
        number = int(value)
        return number if number >= 0 else None
    except (TypeError, ValueError):
        return None

def parse_money(value):
    try:
        normalized = value.strip()
        if "," in normalized:
            normalized = normalized.replace(".", "").replace(",", ".")
        amount = float(normalized)
        if amount < 0:
            return None
        return round(amount * 100)
    except (AttributeError, ValueError):
        return None
