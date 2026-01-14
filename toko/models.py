from django.db import models

class Produk(models.Model):
    KATEGORI_CHOICES = [
        ('Pria', 'Fashion Pria'),
        ('Wanita', 'Fashion Wanita'),
        ('Anak', 'Fashion Anak-anak'),
    ]
    nama = models.CharField(max_length=200)
    kategori = models.CharField(max_length=10, choices=KATEGORI_CHOICES)
    harga = models.IntegerField()
    deskripsi = models.TextField()
    gambar_url = models.URLField()
    
    # Checkbox ukuran baju (S, M, L, XL)
    punya_ukuran = models.BooleanField(default=False, help_text="Ceklis jika produk ini butuh pilihan S, M, L, XL")
    
    # Checkbox ukuran sepatu (38 - 45)
    punya_ukuran_sepatu = models.BooleanField(default=False, help_text="Ceklis jika produk ini butuh pilihan angka sepatu/sandal")

    def __str__(self):
        return self.nama