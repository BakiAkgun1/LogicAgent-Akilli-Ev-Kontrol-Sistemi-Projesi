# LogicAgent - Akıllı Ev Kontrol Sistemi

LogicAgent, "Logic-of-Thought" yaklaşımını kullanarak doğal dil komutlarını mantıksal çerçevede değerlendiren ve Türkçe dil desteği ile akıllı ev sistemlerini kontrol eden yapay zeka ajanıdır.

## Özellikler

- **Türkçe Doğal Dil İşleme**: Günlük konuşma dilinde verilen komutları anlayabilir
- **Mantık Tabanlı Karar Verme**: IF-THEN kuralları ile akıllı davranış sergileyebilir
- **Google Gemini API Entegrasyonu**: Gelişmiş doğal dil anlama kapasitesi
- **Öğrenme Mekanizması**: Kullanıcı davranışlarını öğrenir ve duygu analizi yapar
- **Akıllı Ev Cihaz Kontrolü**: Isıtıcı, kapı, perde, televizyon ve ışık kontrolü
- **Bağlamsal Farkındalık**: Zaman dilimlerine göre otomatik kural güncelleme
- **Sıcaklık Yönetimi**: Hassas sıcaklık kontrolü ve otomatik ayarlama

## Sistem Mimarisi

### Mantıksal Çerçeve
LogicAgent üç temel bileşen üzerine kurulmuştur:

1. **Gerçekler (Facts)**: Sistem durumu ve çevre hakkında bilinen doğrular
   - Örnek: `person_at_home`, `time_morning`

2. **Kurallar (Rules)**: "IF [koşul] THEN [eylem]" formatında mantıksal kurallar
   - AND, OR, NOT operatörleri ile koşul değerlendirmesi

3. **Eylemler (Actions)**: Cihaz kontrolü için çalıştırılabilir komutlar

### Ana Bileşenler

**Gerçek Yönetimi**
- `tell_fact()`: Sisteme yeni gerçekler ekler
- `retract_fact()`: Gerçekleri sistemden kaldırır

**Kural Yönetimi**
- `tell_rule()`: Sisteme yeni kurallar ekler  
- `_parse_condition()`: Mantıksal koşulları değerlendirir
- `_evaluate_rules()`: Mevcut gerçeklere dayalı tüm kuralları değerlendirir

**Cihaz Kontrolü**
- 5 temel cihaz: ısıtıcı, kapı, perde, televizyon, ışık
- `_turn_on_device()`, `_turn_off_device()`: Cihaz durumunu değiştirir
- `_adjust_heater_temp()`: Isıtıcı sıcaklığını ayarlar

**Doğal Dil İşleme**
- `process_command()`: Kalıp eşleştirme ile kullanıcı komutlarını işler
- `process_command_with_gemini()`: Gemini API entegrasyonu ile gelişmiş NLP

## Kurulum

### Sistem Gereksinimleri

| Gereksinim | Açıklama |
|------------|----------|
| Python Sürümü | Python 3.7 veya üzeri (önerilen 3.8.10) |
| İnternet Bağlantısı | API kullanımı için aktif bağlantı gerekli |
| Kütüphaneler | requests, datetime, json |
| API Anahtarı | Google AI Studio'dan alınmalı |

### Kurulum Adımları

1. **Python Paketlerini Yükleme**
```bash
pip install requests
```

2. **Proje Dosyalarını İndirme**
```bash
git clone https://github.com/yourusername/logicagent.git
cd logicagent
```

3. **API Anahtarı Alma ve Entegrasyonu**
   - [Google AI Studio](https://aistudio.google.com/)'ya gidin
   - Google hesabınızla giriş yapın
   - "Create API Key" butonunu kullanarak yeni anahtar oluşturun
   - `logic_agent.py` dosyasında şu satırı güncelleyin:
   ```python
   gemini_api_key = "BURAYA_API_ANAHTARINIZI_GIRIN"
   ```
   ![image](https://github.com/user-attachments/assets/c22bd232-5eea-4033-aa0b-7351774d4ec6)

## Proje Çalıştırma

### Uygulamayı Başlatma
```bash
python app.py
```

### Başlangıç Ekranı
Uygulama başarıyla çalıştırıldığında şu ekran görünecektir:

```
Smart Home Logic Agent
==================================================
Current device statuses:
{
  "heater": "OFF",
  "door": "CLOSED", 
  "curtain": "CLOSED",
  "television": "OFF",
  "light": "OFF",
  "heater_temperature": "22.0°C"
}
Command:
```
![image](https://github.com/user-attachments/assets/63c374ac-d674-4f80-bc19-a5ab5896e8fc)

### Test Komutları
Sistemin düzgün çalıştığını test etmek için:
```
ışıkları aç
televizyonu aç  
sıcaklığı arttır
üşüyorum
durum
```

## Kullanım Kılavuzu

### Temel Cihaz Komutları
| Komut | Açıklama |
|-------|----------|
| `ısıtıcıyı aç` | Isıtıcıyı açar |
| `ısıtıcıyı kapat` | Isıtıcıyı kapatır |
| `kapıyı aç / kapıyı kapat` | Kapıyı açar/kapatır |
| `perdeyi aç / perdeleri kapat` | Perdeleri kontrol eder |
| `televizyonu aç / tv kapat` | TV'yi açar veya kapatır |
| `ışıkları aç / lambayı kapat` | Işıkları kontrol eder |

### Sıcaklık Kontrolü
| Komut | Etki |
|-------|------|
| `sıcaklığı arttır` | 1 derece arttırır |
| `sıcaklığı azalt` | 1 derece azaltır |  
| `üşüyorum` | Isıtıcıyı açar |
| `soğuk` | Isıtıcıyı açar |

### Sistem Komutları
| Komut | Açıklama |
|-------|----------|
| `durum` | Tüm cihaz durumlarını listeler |
| `kurallar` | Tanımlı tüm kuralları gösterir |
| `çıkış` | Programdan çıkar |
| `çıkıyorum` | Evden çıkma durumu olarak algılanır |
| `uyumak istiyorum` | Uyku modunu başlatır |

### Duygusal Komutlar
| Duygu | Örnek Komutlar |
|-------|----------------|
| Mutlu | "Bugün çok mutluyum", "Harika hissediyorum" |
| Üzgün | "Moralim bozuk", "Kendimi kötü hissediyorum" |
| Kızgın | "Sinirliyim", "Çok öfkeliyim" |
| Yorgun | "Çok yoruldum", "Bitkinim" |

## Gemini API Entegrasyonu

### Entegrasyon Amacı
Gemini API entegrasyonu, LogicAgent'ın doğal dil anlama kapasitesini artırmak için eklenmiştir. Basit kalıp eşleştirmesi yerine Google'ın güçlü dil modelini kullanarak daha karmaşık ve belirsiz kullanıcı komutlarını yorumlayabilir.

### Teknik Detaylar
- **API İletişimi**: `call_gemini_api()` HTTP istekleri gönderir
- **İstek Formatı**: JSON formatında prompt ve konfigürasyon içerir
- **Yanıt İşleme**: API yanıtlarını ayrıştırır ve metin içeriğini çıkarır
- **Hata Yönetimi**: API anahtarı eksik veya API yanıtı alınamadığında yedek işleme mekanizması

### Performans Etkileri
- **Doğruluk**: Özellikle karmaşık komutlar için doğruluk oranını artırır
- **Esneklik**: Farklı komut formülasyonlarını anlama yeteneği geliştirildi
- **Gecikme**: API çağrıları nedeniyle yanıt süresinde hafif artış olabilir

## Sorun Giderme

### API Bağlantı Sorunları
**Belirti**: API hata mesajları
**Çözüm**:
- İnternet bağlantınızı kontrol edin
- API anahtarınızın geçerli olduğundan emin olun
- Google API servis durumunu kontrol edin
- Kotalarınızı aşmadığınızı doğrulayın

### Komut Anlama Sorunları  
**Belirti**: Komutlar algılanmıyor
**Çözüm**:
- Daha açık ifadeler kullanın
- Gemini API çalışmıyorsa sistem basit eşleştirmeye geri döner

### Python Hataları
**Belirti**: SyntaxError, ImportError gibi Python hataları
**Çözüm**:
- Python sürümünüzün 3.7+ olduğunu doğrulayın
- Gerekli paketlerin yüklü olduğundan emin olun
- Kodu değiştirdiyseniz sözdizimini kontrol edin

### Sıcaklık Sorunları
**Belirti**: Sıcaklık değeri artmıyor veya azalmıyor
**Çözüm**:
- Sıcaklık değişkeninin float olduğundan emin olun
- `_adjust_heater_temp()` fonksiyonunda değerlerin doğru işlendiğini kontrol edin

## Geliştirme Notları

### Sıcaklık Değeri Düzeltmesi
Sistemde tespit edilen sıcaklık değeri hatası şu şekilde düzeltilmiştir:
1. **Float Tanımlama**: `self.device_temps["heater"]` değeri integer (22) yerine decimal (22.0) olarak tanımlandı
2. **Tutarlı Hesaplama**: Sıcaklık artırma/azaltma işlemleri 1.0 veya -1.0 değerleriyle yapılır

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
