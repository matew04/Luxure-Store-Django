from django.shortcuts import render, get_object_or_404, redirect
from .models import Produk

def home(request):
    # Mengambil 8 produk secara acak dari database
    produk_acak = Produk.objects.all().order_by('?')[:8]
    return render(request, 'home.html', {'produk': produk_acak})

def kategori(request, kat_nama):
    items = Produk.objects.filter(kategori__iexact=kat_nama)
    return render(request, 'kategori.html', {'items': items, 'kategori': kat_nama})

def detail_produk(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    return render(request, 'detail.html', {'produk': produk})

def tambah_ke_keranjang(request, pk):
    if request.method == 'POST':
        ukuran = request.POST.get('ukuran', 'N/A')
        cart = request.session.get('cart', {})
        if not isinstance(cart, dict): cart = {}
        
        item_key = f"{pk}-{ukuran}"
        if item_key in cart:
            cart[item_key]['qty'] += 1
        else:
            cart[item_key] = {'pk': pk, 'ukuran': ukuran, 'qty': 1}
            
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('form_pesanan')

def tambah_qty(request, item_key):
    cart = request.session.get('cart', {})
    if item_key in cart:
        cart[item_key]['qty'] += 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('form_pesanan')

def kurang_qty(request, item_key):
    cart = request.session.get('cart', {})
    if item_key in cart:
        if cart[item_key]['qty'] > 1:
            cart[item_key]['qty'] -= 1
        else:
            del cart[item_key]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('form_pesanan')

def hapus_item_keranjang(request, item_key):
    cart = request.session.get('cart', {})
    if item_key in cart:
        del cart[item_key]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('form_pesanan')

def form_pesanan(request):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}

    produk_terpilih = []
    total_bayar = 0

    # Ambil kunci yang mau dihapus jika produknya sudah tidak ada di DB
    keys_to_delete = []

    for item_key, data in cart.items():
        if isinstance(data, dict) and 'pk' in data:
            p = Produk.objects.filter(id=int(data['pk'])).first()
            
            if p:
                subtotal = p.harga * data['qty']
                total_bayar += subtotal
                produk_terpilih.append({
                    'produk': p,
                    'ukuran': data.get('ukuran', 'N/A'),
                    'qty': data['qty'],
                    'subtotal': subtotal,
                    'item_key': item_key
                })
            else:
                # Jika produk tidak ada di DB, tandai untuk dihapus dari session
                keys_to_delete.append(item_key)

    # Hapus data sampah dari session
    for key in keys_to_delete:
        del cart[key]
    if keys_to_delete:
        request.session['cart'] = cart
        request.session.modified = True

    if request.method == 'POST':
        konteks = {
            'nama': request.POST.get('nama'),
            'email': request.POST.get('email'),
            'items': produk_terpilih,
            'total': total_bayar,
            'pesan': request.POST.get('pesan'),
        }
        request.session['cart'] = {}
        return render(request, 'form_hasil.html', konteks)
    
    return render(request, 'form.html', {'items': produk_terpilih, 'total': total_bayar})

def about(request): return render(request, 'about.html')
def gallery(request): return render(request, 'gallery.html')
def gallery(request):
    # Mengambil semua produk dari database untuk ditampilkan di galeri
    semua_produk = Produk.objects.all()
    return render(request, 'gallery.html', {'produk': semua_produk})