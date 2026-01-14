from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kategori/<str:kat_nama>/', views.kategori, name='kategori'),
    path('produk/<int:pk>/', views.detail_produk, name='detail_produk'),
    path('cart/add/<int:pk>/', views.tambah_ke_keranjang, name='tambah_ke_keranjang'),
    path('cart/add-qty/<str:item_key>/', views.tambah_qty, name='tambah_qty'),
    path('cart/minus-qty/<str:item_key>/', views.kurang_qty, name='kurang_qty'),
    path('cart/remove/<str:item_key>/', views.hapus_item_keranjang, name='hapus_item_keranjang'),
    path('pesan/', views.form_pesanan, name='form_pesanan'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
]