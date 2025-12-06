# 🛠️ Kalite Kontrol Scriptleri Kullanım Kılavuzu

Merhaba arkadaşlar! Bu repo, işinizi kolaylaştırmak adına hazırladığım 3 adet kalite kontrol scriptini içermektedir. Bu scriptleri kullanarak etiketleme süreçlerinizi otomatik olarak kontrol edebilir ve raporlayabilirsiniz.

## 🚀 Başlangıç

Scriptleri çalıştırmak için iki yönteminiz var:

1.  **Yerel Ortam (Önerilen):** Kodları direkt olarak kendi bilgisayarınızdaki Python editöründe (VS Code, PyCharm vb.) çalıştırabilirsiniz.
2.  **Google Colab:** Kodları Colab'e aktarabilirsiniz.
    * *Dikkat:* Colab kullanacaksanız, Drive bağlantısı yapmalı ve kod içerisindeki dosya yolu (path) ayarlarını Colab ortamına göre güncellemelisiniz. (Resimleri ve XML dosyasını Drive'dan çekmeniz gerekebilir.)

## ⚙️ Kurulum ve Ayarlar

Scripti çalıştırmadan önce kod içerisindeki **CONFIG** satırlarını kendi dosya yollarınıza göre düzenlemeyi unutmayın.

### Gerekli Girdiler (Inputs)
Programa sağlamanız gereken dosyalar şunlardır:
* `XML Dosyası`: CVAT üzerinden aldığınız çıktı.
* `Frameler`: Videoya ait görüntü kareleri.

### Beklenen Çıktılar (Outputs)
Script başarıyla tamamlandığında aşağıdaki çıktıları üretecektir:
* 📹 **Video Dosyası (.mp4):** İşlenmiş video çıktısı.
* 📄 **PDF Raporu:** Analiz sonuçlarını içeren belge.
* 💻 **Konsol Çıktısı:** (Sadece yerel kontrol içindir, paylaşılmasına gerek yoktur.)

---

## 📂 Teslim ve Yükleme Talimatları

Oluşturulan çıktıların Drive üzerindeki **"KALİTE KONTROL"** klasörüne, aşağıdaki kurallara göre yüklenmesi gerekmektedir.

| Çıktı Türü | Yükleneceği Klasör | Örnek İsimlendirme Formatı |
| :--- | :--- | :--- |
| **PDF Raporu** | `ALL REPORTS` | `YAZ101_GRUP4.pdf` |
| **Video** | `ALL VİDEOS` | `YAZ101_GRUP4.mp4` |

> **⚠️ Önemli Not:** Lütfen dosya isimlendirmelerinde grup adınızı doğru yazdığınızdan emin olun.

---

## 💡 Tavsiyeler ve Sorun Giderme

* **Kodu İnceleyin:** Kodların içerisinde yer alan **yorum satırlarını** mutlaka okuyun ve dikkate alın.
* **Hata Ayıklama:** Kodlar test edilmiş ve çalışır durumdadır. Ancak kendi verilerinizden kaynaklı hatalar alırsanız, lütfen önce kodun mantığını anlayarak hatayı kendiniz çözmeye çalışın.

Başarılar!

**Yakuphan BİLMEZ**
