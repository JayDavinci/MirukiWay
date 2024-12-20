import streamlit as st
import pandas as pd
from datetime import date

if "products" not in st.session_state:
    st.session_state.products = {}

def add_product(product_type, product_name):
    if product_type not in st.session_state.products:
        st.session_state.products[product_type] = {}
    if product_name not in st.session_state.products[product_type]:
        st.session_state.products[product_type][product_name] = []

st.title("SCM-MIRUKI WAY")
st.image("Mirukiwaylogo.png", use_container_width=True)

st.sidebar.header("Tambahkan Produk")
product_type = st.sidebar.text_input("Jenis Produk")
product_name = st.sidebar.text_input("Nama Produk")

if st.sidebar.button("Tambahkan"):
    if product_type and product_name:
        add_product(product_type, product_name)
        st.sidebar.success(f"Produk {product_name} dalam jenis {product_type} berhasil ditambahkan!")
    else:
        st.sidebar.error("Mohon isi Jenis Produk dan Nama Produk.")

st.header("Daftar Produk")
if st.session_state.products:
    product_type_selected = st.selectbox(
        "Pilih Jenis Produk:", options=list(st.session_state.products.keys())
    )
    if product_type_selected:
        product_name_selected = st.selectbox(
            "Pilih Produk:", options=list(st.session_state.products[product_type_selected].keys())
        )
        if st.button("Lihat Produk"):
            st.session_state.selected_product = (product_type_selected, product_name_selected)
else:
    st.write("Belum ada produk yang ditambahkan.")

if "selected_product" in st.session_state:
    product_type, product_name = st.session_state.selected_product
    st.header(f"Detail Produk: {product_name} ({product_type})")

    with st.form("add_record_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            quantity = st.number_input("Jumlah", min_value=1, value=1)
        with col2:
            price = st.number_input("Harga per unit", min_value=0, value=0, step=1000.0)
        with col3:
            record_date = st.date_input("Tanggal", value=date.today())

        if st.form_submit_button("Tambahkan Pengeluaran"):
            total_cost = quantity * price
            st.session_state.products[product_type][product_name].append(
                {"quantity": quantity, "price": price, "total_cost": total_cost, "date": record_date}
            )
            st.success("Pengeluaran berhasil ditambahkan!")

    st.subheader("Pengeluaran")
    records = st.session_state.products[product_type][product_name]
    if records:
        df = pd.DataFrame(records)

        df['date'] = pd.to_datetime(df['date'])

        st.subheader("Filter Pengeluaran berdasarkan Bulan")
        month_selected = st.selectbox(
            "Pilih Bulan:", options=["Semua"] + sorted(df['date'].dt.strftime('%B %Y').unique())
        )
        if month_selected != "Semua":
            df = df[df['date'].dt.strftime('%B %Y') == month_selected]

        st.table(df)
    else:
        st.write("Belum ada pengeluaran untuk produk ini.")
