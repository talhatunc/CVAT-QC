<div align="center">

[![Türkçe](https://img.shields.io/badge/lang-Türkçe-red.svg)](#tr)
[![English](https://img.shields.io/badge/lang-English-blue.svg)](#en)

</div>

---

<div id="tr"></div>

# 🛠️ Kalite Kontrol Scriptleri Kullanım Kılavuzu

Merhaba arkadaşlar! Bu repo, işinizi kolaylaştırmak adına hazırladığım **3 adet kalite kontrol scriptini** içermektedir. Bu scriptleri kullanarak etiketleme süreçlerinizi otomatik olarak kontrol edebilir ve raporlayabilirsiniz.

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

<br>
<br>

---

<div id="en"></div>

# 🛠️ Quality Control Scripts User Guide

Hello friends! This repo contains **3 quality control scripts** prepared to make your work easier. You can use these scripts to automatically check and report your labeling processes.

## 🚀 Getting Started

There are two ways to run the scripts:

1.  **Local Environment (Recommended):** You can run the codes directly in your own Python editor (VS Code, PyCharm, etc.).
2.  **Google Colab:** You can transfer the codes to Colab.
    * *Note:* If you use Colab, you must mount Google Drive and update the file path settings in the code according to the Colab environment. (You may need to pull images and the XML file from Drive.)

## ⚙️ Setup and Configuration

Before running the script, do not forget to modify the **CONFIG** lines in the code according to your own file paths.

### Required Inputs
The files you need to provide to the program are:
* `XML File`: The output you exported from CVAT.
* `Frames`: The image frames belonging to the video.

### Expected Outputs
When the script completes successfully, it will generate the following outputs:
* 📹 **Video File (.mp4):** The processed video output.
* 📄 **PDF Report:** The document containing analysis results.
* 💻 **Console Output:** (For local verification only, no need to share this.)

---

## 📂 Submission and Upload Instructions

The generated outputs must be uploaded to the **"KALİTE KONTROL"** (Quality Control) folder on Drive according to the rules below.

| Output Type | Destination Folder | Naming Example |
| :--- | :--- | :--- |
| **PDF Report** | `ALL REPORTS` | `YAZ101_GROUP4.pdf` |
| **Video** | `ALL VİDEOS` | `YAZ101_GROUP4.mp4` |

> **⚠️ Important Note:** Please make sure to write your group name correctly in the file names.

---

## 💡 Tips and Troubleshooting

* **Review the Code:** Make sure to read and consider the **comment lines** inside the codes.
* **Debugging:** The codes have been tested and are working. However, if you encounter errors due to your own data, please try to solve the error yourself by understanding the logic of the code first.

Good luck!

**Yakuphan BİLMEZ**
