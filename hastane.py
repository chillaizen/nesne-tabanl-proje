import tkinter as tk
from tkinter import messagebox


class Hasta:
    def __init__(self, isim, tc):
        self.isim = isim
        self.tc = tc
        self.randevu_gecmisi = []


class Doktor:
    def __init__(self, isim, uzmanlik):
        self.isim = isim
        self.uzmanlik = uzmanlik
        self.musait = True


class Randevu:
    def __init__(self, tarih, doktor, hasta):
        self.tarih = tarih
        self.doktor = doktor
        self.hasta = hasta


class RandevuSistemi:
    def __init__(self):
        self.doktorlar = []
        self.hastalar = []
        self.randevular = []

    def doktor_ekle(self, doktor):
        self.doktorlar.append(doktor)

    def hasta_ekle(self, hasta):
        self.hastalar.append(hasta)

    def randevu_al(self, hasta_tc, doktor_isim, tarih):
        hasta = next((h for h in self.hastalar if h.tc == hasta_tc), None)
        doktor = next((d for d in self.doktorlar if d.isim == doktor_isim), None)

        if not hasta:
            return "Hasta bulunamadı."

        if not doktor:
            return "Doktor bulunamadı."

        if not doktor.musait:
            return "Doktor şu anda müsait değil."

        randevu = Randevu(tarih, doktor, hasta)
        self.randevular.append(randevu)
        hasta.randevu_gecmisi.append(randevu)
        doktor.musait = False
        return "Randevu başarıyla alındı."

    def randevu_iptal(self, hasta_tc, doktor_isim):
        randevu = next(
            (r for r in self.randevular if r.hasta.tc == hasta_tc and r.doktor.isim == doktor_isim),
            None
        )

        if not randevu:
            return "Randevu bulunamadı."

        self.randevular.remove(randevu)
        randevu.doktor.musait = True
        return "Randevu başarıyla iptal edildi."

    def randevulari_listele(self):
        if not self.randevular:
            return "Henüz randevu yok."
        return "\n".join(
            [f"{r.tarih}: {r.hasta.isim} ile {r.doktor.isim}" for r in self.randevular]
        )



sistem = RandevuSistemi()
sistem.doktor_ekle(Doktor("Dr. Ayşe", "Dahiliye"))
sistem.doktor_ekle(Doktor("Dr. Mehmet", "Ortopedi"))
sistem.hasta_ekle(Hasta("Ahmet Yılmaz", "12345678900"))
sistem.hasta_ekle(Hasta("Fatma Demir", "98765432100"))

root = tk.Tk()
root.title("Hastane Randevu Sistemi")


tk.Label(root, text="Hasta TC:").grid(row=0, column=0)
tc_entry = tk.Entry(root)
tc_entry.grid(row=0, column=1)

tk.Label(root, text="Doktor İsmi:").grid(row=1, column=0)
doktor_entry = tk.Entry(root)
doktor_entry.grid(row=1, column=1)

tk.Label(root, text="Randevu Tarihi:").grid(row=2, column=0)
tarih_entry = tk.Entry(root)
tarih_entry.grid(row=2, column=1)


def randevu_al():
    tc = tc_entry.get()
    doktor = doktor_entry.get()
    tarih = tarih_entry.get()
    sonuc = sistem.randevu_al(tc, doktor, tarih)
    messagebox.showinfo("Bilgi", sonuc)


def randevu_iptal():
    tc = tc_entry.get()
    doktor = doktor_entry.get()
    sonuc = sistem.randevu_iptal(tc, doktor)
    messagebox.showinfo("Bilgi", sonuc)


def randevulari_goster():
    liste = sistem.randevulari_listele()
    messagebox.showinfo("Randevu Listesi", liste)



tk.Button(root, text="Randevu Al", command=randevu_al).grid(row=3, column=0, pady=10)
tk.Button(root, text="Randevu İptal", command=randevu_iptal).grid(row=3, column=1, pady=10)
tk.Button(root, text="Randevuları Listele", command=randevulari_goster).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
s