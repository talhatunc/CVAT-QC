
# pip install fpdf => PDF raporları için gereklidir. Terminalden yükleyebilirsiniz.

import xml.etree.ElementTree as ET
import cv2
import numpy as np
import os
import datetime
from tqdm import tqdm
from collections import defaultdict
from fpdf import FPDF

# --- PROJE YOLU ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- AYARLAR ---
CONFIG = {
    "xml_path": os.path.join(BASE_DIR, "PREPROCESSDATA", "ALLOUTPUTSXML", "SWE101_GROUP_2.xml"),   # XML YOLUNUZ
    "images_folder": os.path.join(BASE_DIR, "PREPROCESSDATA", "ALLFRAMES", "GRUP2"),     # RESIMLERIN BULUNDUGU KLASOR
    "output_base_name": "SWE101_GROUP_2",   # TR İSE YAZ101 , ENG İSE SWE101 => ÖRNEK KULLANIM SWE101_GRUP_1  YA DA  YAZ101_GRUP_1
    "fps": 2, 
    "skeleton_color": (255, 255, 255),
    "visible_point_color": (0, 255, 0),
    "occluded_point_color": (0, 165, 255),
    "text_color": (0, 255, 255),
    "jump_threshold": 100  # Piksel cinsinden ziplama esigi
}

# --- YARDIMCI FONKSİYONLAR ---

def safe_imread(path):
    try:
        with open(path, "rb") as f:
            chunk = f.read()
        chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
        img = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
        return img
    except Exception:
        return None

def normalize_text(text):
    """PDF için Türkçe karakter dönüşümü"""
    replacements = {
        'ş': 's', 'Ş': 'S', 'ı': 'i', 'İ': 'I', 'ğ': 'g', 'Ğ': 'G',
        'ü': 'u', 'Ü': 'U', 'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C'
    }
    for src, target in replacements.items():
        text = text.replace(src, target)
    return text

class PDFReport(FPDF):
    def header(self):
        # Rapor Başlığı
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'UST KAMERA KALITE KONTROL RAPORU', 0, 1, 'C')
        
        # Altına bir çizgi çek
        self.set_line_width(0.5)
        self.line(10, 20, 200, 20)
        self.ln(10)

    def footer(self):
        # Sayfa Altı
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(230, 230, 230) # Açık gri arka plan
        self.cell(0, 8, normalize_text(title), 0, 1, 'L', 1)
        self.ln(4)

    def section_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, normalize_text(body))
        self.ln()

    def create_centered_table(self, header, data):
        """
        Tabloyu sayfada ortalar ve hücreleri ortalar.
        header: ['Kolon1', 'Kolon2', ...]
        data: [['v1', 'v2', ...], ['v3', 'v4', ...]]
        """
        # Kolon Genişlikleri
        col_widths = [20, 40, 40, 50] 
        total_width = sum(col_widths)
        
        # Sayfa ortalamak için başlangıç X koordinatı
        # A4 genişliği ~210mm. 
        start_x = (210 - total_width) / 2
        
        # --- BAŞLIK SATIRI ---
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(200, 200, 200) # Başlık için daha koyu gri
        self.set_x(start_x) # Ortaya git
        
        for i, col_name in enumerate(header):
            self.cell(col_widths[i], 8, normalize_text(col_name), 1, 0, 'C', 1)
        self.ln()
        
        # --- VERİ SATIRLARI ---
        self.set_font('Arial', '', 10)
        
        for row in data:
            self.set_x(start_x) # Her satırda tekrar ortaya git
            for i, item in enumerate(row):
                self.cell(col_widths[i], 8, normalize_text(str(item)), 1, 0, 'C')
            self.ln()

def parse_svg_edges(svg_content):
    edges = []
    lines = svg_content.split('<line')
    for line in lines:
        if 'data-node-from' in line and 'data-node-to' in line:
            try:
                part1 = line.split('data-node-from="')[1]
                node_from = part1.split('"')[0]
                part2 = line.split('data-node-to="')[1]
                node_to = part2.split('"')[0]
                edges.append((node_from, node_to))
            except IndexError:
                continue
    return edges

SVG_CONTENT = """
<svg viewBox="0 0 100 100">
<line x1="50.9" y1="47.8" x2="51.7" y2="46.5" data-type="edge" data-node-from="14" data-node-to="16"/>
<line x1="54.7" y1="49.9" x2="55.7" y2="49.0" data-type="edge" data-node-from="13" data-node-to="15"/>
<line x1="51.4" y1="52.2" x2="50.9" y2="47.8" data-type="edge" data-node-from="5" data-node-to="14"/>
<line x1="51.4" y1="52.2" x2="54.7" y2="49.9" data-type="edge" data-node-from="5" data-node-to="13"/>
<line x1="52.5" y1="57.9" x2="53.2" y2="56.7" data-type="edge" data-node-from="9" data-node-to="11"/>
<line x1="47.9" y1="57.9" x2="47.0" y2="56.7" data-type="edge" data-node-from="10" data-node-to="12"/>
<line x1="48.7" y1="58.9" x2="47.9" y2="57.9" data-type="edge" data-node-from="8" data-node-to="10"/>
<line x1="51.4" y1="59.1" x2="52.5" y2="57.9" data-type="edge" data-node-from="7" data-node-to="9"/>
<line x1="50.4" y1="60.9" x2="48.7" y2="58.9" data-type="edge" data-node-from="6" data-node-to="8"/>
<line x1="50.4" y1="60.9" x2="51.4" y2="59.1" data-type="edge" data-node-from="6" data-node-to="7"/>
<line x1="51.4" y1="52.2" x2="50.4" y2="60.9" data-type="edge" data-node-from="5" data-node-to="6"/>
<line x1="54.4" y1="47.5" x2="51.4" y2="52.2" data-type="edge" data-node-from="4" data-node-to="5"/>
<line x1="54.4" y1="47.5" x2="54.0" y2="45.5" data-type="edge" data-node-from="4" data-node-to="3"/>
<line x1="54.4" y1="47.5" x2="56.2" y2="47.2" data-type="edge" data-node-from="4" data-node-to="2"/>
<line x1="57.1" y1="43.8" x2="54.4" y2="47.5" data-type="edge" data-node-from="1" data-node-to="4"/>
</svg>
"""

def analyze_and_visualize(config):
    print("--- Detaylı Kalite Kontrol ve Raporlama Başlatıldı ---")
    
    try:
        tree = ET.parse(config["xml_path"])
        root = tree.getroot()
    except FileNotFoundError:
        print("HATA: XML dosyası bulunamadı.")
        return

    skeleton_edges = parse_svg_edges(SVG_CONTENT)
    images = root.findall('image')
    total_frames = len(images)
    
    annotated_frames_count = 0
    fully_annotated_frames = 0 
    
    total_points_all = 0
    total_visible_points = 0
    total_occluded_points = 0
    
    keypoint_stats = defaultdict(lambda: {'visible': 0, 'occluded': 0})
    areas = []
    
    # Anomali Tespiti
    prev_points_dict = None
    anomalies = [] # (frame_idx, label, distance)
    JUMP_THRESHOLD = config.get("jump_threshold", 50)

    
    # Video Writer
    first_img = images[0]
    w = int(first_img.attrib['width'])
    h = int(first_img.attrib['height'])
    
    base_name = config["output_base_name"]
    if base_name is None:
        base_name = os.path.splitext(config["xml_path"])[0]

    video_name = base_name + "_QC_Video.mp4"
    pdf_name = base_name + "_QC_Report.pdf"
        
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_name, fourcc, config["fps"], (w, h))
    
    print(f"Video oluşturuluyor: {video_name} ({config['fps']} FPS)")

    try:
        for idx, img in tqdm(enumerate(images), total=total_frames, desc="Analiz Ediliyor"):
            # XML'den gelen isim "GRUP2/002322.jpg" formatında olabilir
            # Sadece dosya adını almak için split yapıyoruz
            full_img_name_from_xml = img.attrib['name']
            img_filename = full_img_name_from_xml.replace("\\", "/").split("/")[-1]
            
            img_path_full = os.path.join(config["images_folder"], img_filename)
            
            frame_img = safe_imread(img_path_full)
            
            if frame_img is None:
                frame_img = np.zeros((h, w, 3), dtype=np.uint8)
                cv2.putText(frame_img, f"Resim Yok: {img_name}", (50, h//2), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            skeleton = img.find('skeleton')
            points_dict = {}
            
            if skeleton is not None:
                annotated_frames_count += 1
                points_xml = skeleton.findall('points')
                
                if len(points_xml) == 16:
                    fully_annotated_frames += 1
                    
                x_coords = []
                y_coords = []

                for pt in points_xml:
                    label = pt.attrib['label']
                    coords = pt.attrib['points'].split(',')
                    x, y = float(coords[0]), float(coords[1])
                    occluded = int(pt.attrib.get('occluded', 0))
                    
                    points_dict[label] = (x, y, occluded)
                    
                    total_points_all += 1
                    if occluded == 1:
                        total_occluded_points += 1
                        keypoint_stats[label]['occluded'] += 1
                    else:
                        total_visible_points += 1
                        keypoint_stats[label]['visible'] += 1
                        x_coords.append(x)
                        y_coords.append(y)

                if x_coords and y_coords:
                    area = (max(x_coords) - min(x_coords)) * (max(y_coords) - min(y_coords))
                    areas.append(area)

                # Çizim
                for edge in skeleton_edges:
                    p1_label, p2_label = edge
                    if p1_label in points_dict and p2_label in points_dict:
                        pt1 = (int(points_dict[p1_label][0]), int(points_dict[p1_label][1]))
                        pt2 = (int(points_dict[p2_label][0]), int(points_dict[p2_label][1]))
                        cv2.line(frame_img, pt1, pt2, config["skeleton_color"], 2)

                for label, data in points_dict.items():
                    x, y, occ = data
                    center = (int(x), int(y))
                    
                    if occ == 0: 
                        cv2.circle(frame_img, center, 6, config["visible_point_color"], -1)
                    else:
                        cv2.circle(frame_img, center, 6, config["occluded_point_color"], 2)
                        cv2.drawMarker(frame_img, center, config["occluded_point_color"], markerType=cv2.MARKER_CROSS, markerSize=12, thickness=2)

                    cv2.putText(frame_img, label, (center[0]+10, center[1]-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, config["text_color"], 2)

                # --- ANOMALI KONTROLU (YENI) ---
                frame_anomalies = []
                if prev_points_dict is not None:
                    for label, data in points_dict.items():
                        if label in prev_points_dict:
                            x1, y1, _ = data
                            x2, y2, _ = prev_points_dict[label]
                            dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                            
                            if dist > JUMP_THRESHOLD:
                                frame_anomalies.append((label, dist))
                                anomalies.append([idx, label, f"{dist:.1f}"])
                
                if frame_anomalies:
                    # Ekrana uyari yaz
                    cv2.putText(frame_img, f"DIKKAT: {len(frame_anomalies)} ADET ZIPLAMA!", (30, 100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    y_off = 140
                    for lbl, dist in frame_anomalies[:3]: # Ekrana en fazla 3 tanesini yaz
                        text = f"{lbl}: {dist:.1f} px"
                        cv2.putText(frame_img, text, (30, y_off), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        y_off += 30

                prev_points_dict = points_dict
                
                cv2.putText(frame_img, f"Frame: {idx} | Pts: {len(points_dict)}/16", (30, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, config["text_color"], 2)
            else:
                prev_points_dict = None # Etiket yoksa gecmisi sifirla
                cv2.putText(frame_img, "ETIKETLENMEMIS", (30, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            video_writer.write(frame_img)
            
    except KeyboardInterrupt:
        print("\n\n!!! İŞLEM DURDURULDU !!!")
    except Exception as e:
        print(f"\n\n!!! HATA: {e}")
    finally:
        video_writer.release()
        
        # --- HESAPLAMALAR ---
        safe_total_frames = max(1, total_frames)
        safe_total_points = max(1, total_points_all)
        
        labeling_rate = (annotated_frames_count / safe_total_frames) * 100
        completeness = (total_points_all / (max(1, annotated_frames_count) * 16)) * 100
        vis_rate = (total_visible_points / safe_total_points) * 100
        occ_rate = (total_occluded_points / safe_total_points) * 100
        
        cv_area = 0
        if len(areas) > 0:
            std_dev_area = np.std(areas)
            mean_area = np.mean(areas)
            cv_area = (std_dev_area / mean_area) * 100 

        # --- PDF RAPOR OLUŞTURMA ---
        try:
            pdf = PDFReport()
            pdf.add_page()
            
            # Bilgi Bloğu
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 5, f"Dosya Adi: {os.path.basename(config['xml_path'])}", 0, 1)
            pdf.cell(0, 5, f"Tarih: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
            pdf.ln(5)
            
            # Bölüm 1
            pdf.section_title("1. GENEL OZET")
            body_text = (f"Toplam Kare Sayisi: {total_frames}\n"
                         f"Etiketlenen Kare Sayisi: {annotated_frames_count} (%{labeling_rate:.2f})\n"
                         f"Tam (16 Noktali) Kareler: {fully_annotated_frames}\n"
                         f"Iskelet Butunlugu: %{completeness:.2f}\n"
                         f"Toplam Isaretlenen Nokta: {total_points_all}\n"
                         f"Gorunur Noktalar: {total_visible_points} (%{vis_rate:.2f})\n"
                         f"Gorunmez (Occluded) Noktalar: {total_occluded_points} (%{occ_rate:.2f})\n"
                         f"Boyut Degisimi (Varyasyon): %{cv_area:.2f}")
            pdf.section_body(body_text)
            
            # Bölüm 2: Tablo
            pdf.section_title("2. UZUV BAZLI GORUNMEZLIK ANALIZI")
            
            table_header = ['ID', 'Gorunur', 'Gorunmez', 'Oran %']
            table_data = []
            
            sorted_keys = sorted(keypoint_stats.keys(), key=lambda x: int(x) if x.isdigit() else x)
            for label in sorted_keys:
                vis = keypoint_stats[label]['visible']
                occ = keypoint_stats[label]['occluded']
                total = vis + occ
                pt_occ_rate = (occ / total * 100) if total > 0 else 0
                
                rate_str = f"%{pt_occ_rate:.2f}"
                if pt_occ_rate > 70:
                    rate_str += " (!)"
                
                table_data.append([label, vis, occ, rate_str])
            
            pdf.create_centered_table(table_header, table_data)

            # Bölüm 3: Anomali
            pdf.ln(10)
            pdf.section_title("3. SUPHELI KARELER (ANOMALI TESPITI)")
            pdf.section_body(f"Eşik Değeri (Threshold): {JUMP_THRESHOLD} piksel. Bu değerin üzerindeki ani keypoint hareketleri listelenir.")
            
            if anomalies:
                anomaly_header = ['Kare No', 'Uzuv', 'Mesafe (px)']
                # En yüksek 25 anomaliyi göster
                sorted_anomalies = sorted(anomalies, key=lambda x: float(x[2]), reverse=True)[:30]
                pdf.create_centered_table(anomaly_header, sorted_anomalies)
            else:
                pdf.section_body("Herhangi bir ziplama (anomali) tespit edilemedi.")


            pdf.output(pdf_name)
            print(f"\nPDF Raporu Olusturuldu: {pdf_name}")
        except Exception as e:
            print(f"\nPDF Olusturma Hatasi: {e}")

        print(f"Video Kaydedildi: {video_name}")

        # --- KONSOL ÇIKTISI ---
        print("\n" + "="*60)
        print(f"KALITE KONTROL TAMAMLANDI")
        print("="*60)
        print(f"1. GENEL DURUM")
        print(f"   Toplam Kare     : {total_frames}")
        print(f"   Etiketli Kare   : {annotated_frames_count} (%{labeling_rate:.2f})")
        print("-" * 30)
        print(f"2. NOKTA ANALIZI")
        print(f"   Toplam Nokta    : {total_points_all}")
        print(f"   Görünür         : {total_visible_points} (%{vis_rate:.2f})")
        print(f"   Kapalı          : {total_occluded_points} (%{occ_rate:.2f})")
        print("-" * 30)
        print(f"3. UZUV DETAYLARI")
        print(f"{'ID':<5} | {'Görünür':<10} | {'Görünmez':<10} | {'Oran %':<10}")
        for row in table_data:
             print(f"{row[0]:<5} | {row[1]:<10} | {row[2]:<10} | {row[3]:<10}")
        print("="*60)
        
        print(f"4. ANOMALI OZETI (Threshold: {JUMP_THRESHOLD} px)")
        if anomalies:
            print(f"   Toplam Supheli Hareket: {len(anomalies)}")
            print(f"   En Yuksek 5 Anomali:")
            sorted_anomalies = sorted(anomalies, key=lambda x: float(x[2]), reverse=True)[:5]
            for item in sorted_anomalies:
                print(f"   - Kare: {item[0]} | Uzuv: {item[1]} | Mesafe: {item[2]}")
        else:
            print("   Temiz. Ziplama yok.")
        print("="*60)

if __name__ == "__main__":
    analyze_and_visualize(CONFIG)
