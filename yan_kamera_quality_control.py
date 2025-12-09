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
    # Dosya yollarınızı kontrol edin
    "xml_path": os.path.join(BASE_DIR, "PREPROCESSDATA", "ALLOUTPUTSXML", "SWE101_GROUP_X.xml"),      # XML YOLUNUZ
    "images_folder": os.path.join(BASE_DIR, "PREPROCESSDATA", "ALLFRAMES", "GRUPX"),  # RESIMLERIN BULUNDUGU KLASOR
    "output_base_name": "SWE101_GRUP_X",        # TR İSE YAZ101 , ENG İSE SWE101 => ÖRNEK KULLANIM SWE101_GRUP_1  YA DA  YAZ101_GRUP_1
    "fps": 2, 
    "skeleton_color": (255, 255, 255),
    "visible_point_color": (0, 255, 0),
    "occluded_point_color": (0, 165, 255),
    "text_color": (0, 255, 255)
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
    replacements = {'ş':'s','Ş':'S','ı':'i','İ':'I','ğ':'g','Ğ':'G','ü':'u','Ü':'U','ö':'o','Ö':'O','ç':'c','Ç':'C'}
    for src, target in replacements.items():
        text = text.replace(src, target)
    return text



# --- PDF REPORT CLASS ---
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 12, 'YAN KAMERA KALITE KONTROL RAPORU', 0, 1, 'C', 1)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}', 0, 0, 'C')

    # DÜZELTİLEN KISIM: Fonksiyon adı section_title olarak kullanılıyor
    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(220, 220, 220)
        self.cell(0, 8, normalize_text(title), 0, 1, 'L', 1)
        self.ln(4)

    def section_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, normalize_text(body))
        self.ln()

    def create_centered_table(self, header, data):
        col_widths = [20, 40, 40, 50] 
        start_x = (210 - sum(col_widths)) / 2
        
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(180, 180, 180) 
        self.set_x(start_x)
        for i, col_name in enumerate(header):
            self.cell(col_widths[i], 8, normalize_text(col_name), 1, 0, 'C', 1)
        self.ln()
        
        self.set_font('Arial', '', 10)
        for row in data:
            self.set_x(start_x)
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

# YAN KAMERA SVG (18 Noktalı)
SVG_CONTENT = """
<svg viewBox="0 0 100 100">
<line x1="41.03852462768555" y1="64.11571502685547" x2="39.195980072021484" y2="64.95323181152344" stroke="black" data-type="edge" data-node-from="16" stroke-width="0.5" data-node-to="18"/>
<line x1="41.87604522705078" y1="62.60817337036133" x2="40.368507385253906" y2="63.110687255859375" stroke="black" data-type="edge" data-node-from="15" stroke-width="0.5" data-node-to="17"/>
<line x1="48.57621383666992" y1="58.14139938354492" x2="41.03852462768555" y2="64.11571502685547" stroke="black" data-type="edge" data-node-from="5" stroke-width="0.5" data-node-to="16"/>
<line x1="48.57621383666992" y1="58.14139938354492" x2="41.87604522705078" y2="62.60817337036133" stroke="black" data-type="edge" data-node-from="5" stroke-width="0.5" data-node-to="15"/>
<line x1="52.763816833496094" y1="63.780704498291016" x2="50.75376892089844" y2="65.12073516845703" stroke="black" data-type="edge" data-node-from="12" stroke-width="0.5" data-node-to="14"/>
<line x1="53.26633071899414" y1="62.27316665649414" x2="51.088775634765625" y2="62.94318389892578" stroke="black" data-type="edge" data-node-from="11" stroke-width="0.5" data-node-to="13"/>
<line x1="49.413734436035156" y1="62.440670013427734" x2="52.763816833496094" y2="63.780704498291016" stroke="black" data-type="edge" data-node-from="10" stroke-width="0.5" data-node-to="12"/>
<line x1="50.25125503540039" y1="61.10063552856445" x2="53.26633071899414" y2="62.27316665649414" stroke="black" data-type="edge" data-node-from="9" stroke-width="0.5" data-node-to="11"/>
<line x1="52.09379959106445" y1="62.27316665649414" x2="49.413734436035156" y2="62.440670013427734" stroke="black" data-type="edge" data-node-from="8" stroke-width="0.5" data-node-to="10"/>
<line x1="52.763816833496094" y1="61.10063552856445" x2="50.25125503540039" y2="61.10063552856445" stroke="black" data-type="edge" data-node-from="7" stroke-width="0.5" data-node-to="9"/>
<line x1="56.95142364501953" y1="60.765628814697266" x2="52.09379959106445" y2="62.27316665649414" stroke="black" data-type="edge" data-node-from="6" stroke-width="0.5" data-node-to="8"/>
<line x1="56.95142364501953" y1="60.765628814697266" x2="52.763816833496094" y2="61.10063552856445" stroke="black" data-type="edge" data-node-from="6" stroke-width="0.5" data-node-to="7"/>
<line x1="48.57621383666992" y1="58.14139938354492" x2="56.95142364501953" y2="60.765628814697266" stroke="black" data-type="edge" data-node-from="5" stroke-width="0.5" data-node-to="6"/>
<line x1="40.03266143798828" y1="61.904170989990234" x2="48.57621383666992" y2="58.14139938354492" stroke="black" data-type="edge" data-node-from="4" stroke-width="0.5" data-node-to="5"/>
<line x1="40.03266143798828" y1="61.904170989990234" x2="38.36038589477539" y2="61.5697135925293" stroke="black" data-type="edge" data-node-from="4" stroke-width="0.5" data-node-to="3"/>
<line x1="40.03266143798828" y1="61.904170989990234" x2="39.69820785522461" y2="60.06467056274414" stroke="black" data-type="edge" data-node-from="4" stroke-width="0.5" data-node-to="2"/>
<line x1="34.34693145751953" y1="63.57644271850586" x2="40.03266143798828" y2="61.904170989990234" stroke="black" data-type="edge" data-node-from="1" stroke-width="0.5" data-node-to="4"/>
</svg>
"""

def analyze_and_visualize(config):
    print("--- Yan Kamera Kalite Kontrol Başlatıldı ---")
    
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

    missing_frames = []
    
    w, h = 1920, 1080
    if len(images) > 0:
        w = int(images[0].attrib.get('width', 1920))
        h = int(images[0].attrib.get('height', 1080))
    
    base_name = config["output_base_name"]
    if base_name is None:
        base_name = os.path.splitext(config["xml_path"])[0]
        
    video_name = base_name + "_QC_Video.mp4"
    pdf_name = base_name + "_QC_Report.pdf"
        
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_name, fourcc, config["fps"], (w, h))
    
    print(f"Video oluşturuluyor: {video_name}")

    try:
        for idx, img in tqdm(enumerate(images), total=total_frames, desc="Analiz Ediliyor"):
            full_img_name_from_xml = img.attrib['name']
            img_filename = full_img_name_from_xml.replace("\\", "/").split("/")[-1]
            
            img_path_full = os.path.join(config["images_folder"], img_filename)
            
            frame_img = safe_imread(img_path_full)
            
            if frame_img is None:
                frame_img = np.zeros((h, w, 3), dtype=np.uint8)
                cv2.putText(frame_img, f"Resim Yok: {full_img_name_from_xml}", (50, h//2), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                if frame_img.shape[1] != w or frame_img.shape[0] != h:
                    frame_img = cv2.resize(frame_img, (w, h))

            skeleton = img.find('skeleton')
            points_dict = {}
            
            if skeleton is not None:
                annotated_frames_count += 1
                points_xml = skeleton.findall('points')
                if len(points_xml) == 18: fully_annotated_frames += 1 # Yan kamera 18 nokta
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
                    if occ == 0: cv2.circle(frame_img, center, 6, config["visible_point_color"], -1)
                    else:
                        cv2.circle(frame_img, center, 6, config["occluded_point_color"], 2)
                        cv2.drawMarker(frame_img, center, config["occluded_point_color"], markerType=cv2.MARKER_CROSS, markerSize=12, thickness=2)
                    cv2.putText(frame_img, label, (center[0]+10, center[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, config["text_color"], 2)

                cv2.putText(frame_img, f"Frame: {idx} | File: {img_filename}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, config["text_color"], 2)
            else:
                cv2.putText(frame_img, "ETIKETLENMEMIS", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                missing_frames.append(full_img_name_from_xml)

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
        completeness = (total_points_all / (max(1, annotated_frames_count) * 18)) * 100 # Yan kamera 18 nokta
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
                         f"Tam (18 Noktali) Kareler: {fully_annotated_frames}\n"
                         f"Iskelet Butunlugu: %{completeness:.2f}\n"
                         f"Toplam Isaretlenen Nokta: {total_points_all}\n"
                         f"Gorunur Noktalar: {total_visible_points} (%{vis_rate:.2f})\n"
                         f"Gorunmez (Occluded) Noktalar: {total_occluded_points} (%{occ_rate:.2f})\n"
                         f"Boyut Degisimi (Varyasyon): %{cv_area:.2f}")
            
            if missing_frames:
                 body_text += f"\n\nEtiketlenmemis Kareler ({len(missing_frames)}): " + ", ".join(missing_frames[:10])
                 if len(missing_frames) > 10: body_text += "..."

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

            pdf.output(pdf_name)
            print(f"\nPDF Raporu Olusturuldu: {pdf_name}")
        except Exception as e:
            print(f"\nPDF Olusturma Hatasi: {e}")

        print(f"Video Kaydedildi: {video_name}")

        # --- KONSOL ÇIKTISI ---
        print("\n" + "="*60)
        print(f"KALITE KONTROL TAMAMLANDI (YAN KAMERA)")
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
        
        if missing_frames:
            print("-" * 30)
            print(f"4. ETIKETLENMEMIS KARELER ({len(missing_frames)} Adet)")
            for mf in missing_frames:
                print(f"   -> {mf}")

        print("="*60)

        print(f"Video Kaydedildi: {video_name}")

if __name__ == "__main__":
    analyze_and_visualize(CONFIG)