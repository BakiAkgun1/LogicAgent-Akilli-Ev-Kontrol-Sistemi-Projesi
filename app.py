import json
import datetime
import requests  # Added for API requests
from typing import Dict, List, Set, Tuple, Union, Optional

class LogicAgent:
    """
    Akıllı ev kontrolü için Logic-of-Thought yaklaşımını kullanan mantıksal bir ajan.
    Bu ajan doğal dil komutlarını yorumlar ve önerme mantığı kullanarak
    yürütülebilir eylemlere dönüştürür.
    """
    
    def __init__(self, api_key: str = None, llm_endpoint: str = None):
        """LogicAgent'i başlat."""
        self.facts: Set[str] = set()
        self.rules: Dict[str, str] = {}
        self.api_key = api_key
        self.llm_endpoint = llm_endpoint or "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
        # Cihazları Türkçeleştir
        self.devices = {
            "ısıtıcı": False,  # False = kapalı, True = açık
            "kapı": False,     # False = kapalı, True = açık
            "perde": False,    # False = kapalı, True = açık
            "televizyon": False, # False = kapalı, True = açık
            "ışık": False,     # False = kapalı, True = açık
        }
        self.device_temps = {"ısıtıcı": 22.0}  # Float olarak tanımla
        
        # Kullanıcı davranış takibi
        self.user_patterns = {
            "sabah_rutini": [],
            "akşam_rutini": [],
            "sık_kullanılan_cihazlar": {},
            "sıcaklık_tercihleri": []
        }
        
        # Temel bağlamsal gerçekler ve kurallar ile başlat
        self._setup_initial_facts()
        self._setup_initial_rules()
        self._setup_advanced_rules()
    
    def _setup_initial_facts(self):
        """Çevre hakkında ilk gerçekleri kur."""
        current_time = datetime.datetime.now()
        
        # Zamanla ilgili gerçekler
        if 5 <= current_time.hour < 12:
            self.tell_fact("zaman_sabah")
        elif 12 <= current_time.hour < 17:
            self.tell_fact("zaman_öğle")
        elif 17 <= current_time.hour < 22:
            self.tell_fact("zaman_akşam")
        else:
            self.tell_fact("zaman_gece")
            
        # Varsayılan gerçekler
        self.tell_fact("kişi_evde")
    
    def _setup_initial_rules(self):
        """Mantıksal ajan için ilk kuralları kur."""
        # Cihaz kontrolü için temel kurallar
        basic_rules = [
            "kişi_üşüyor -> ısıtıcı_aç",
            "zaman_gece & kişi_evde & ışık_isteği -> ışık_aç",
            "televizyon_isteği -> televizyon_aç",
            "kişi_çıkıyor -> kapı_kapat",
            "zaman_sabah & kişi_evde & perde_isteği -> perde_aç",
            "ısıtıcı_aç_isteği -> ısıtıcı_aç",
            "ısıtıcı_kapat_isteği -> ısıtıcı_kapat",
            "kapı_aç_isteği -> kapı_aç",
            "kapı_kapat_isteği -> kapı_kapat",
            "ışık_aç_isteği -> ışık_aç",
            "ışık_kapat_isteği -> ışık_kapat",
            "perde_aç_isteği -> perde_aç",
            "perde_kapat_isteği -> perde_kapat",
            "televizyon_aç_isteği -> televizyon_aç",
            "televizyon_kapat_isteği -> televizyon_kapat"
        ]
        
        for rule in basic_rules:
            self.tell_rule(rule)
    
    def _setup_advanced_rules(self):
        """Bağlam farkındalığı ve konfor için gelişmiş kurallar kur."""
        advanced_rules = [
            "zaman_gece & !kişi_evde -> ışık_kapat",
            "zaman_sabah & !perde_açık & kişi_uyanıyor -> perde_aç",
            "yüksek_sıcaklık & kişi_evde -> soğutma_öner",
            "zaman_gece & kişi_uyuma_hazırlığı -> gece_modu",
            "(zaman_sabah | zaman_akşam) & kişi_evde & !televizyon_açık & eğlence_isteği -> televizyon_aç",
            "kullanıcı_duygu_mutlu & zaman_akşam -> mutlu_ortam_ışığı",
            "kullanıcı_duygu_üzgün -> neşeli_müzik_çal",
            "kullanıcı_duygu_yorgun & zaman_akşam -> uyku_ortamı_hazırla"
        ]
        
        for rule in advanced_rules:
            self.tell_rule(rule)
    
    def tell_fact(self, fact: str):
        """Ajan'ın bilgi tabanına yeni bir gerçek ekle."""
        self.facts.add(fact)
        print(f"Gerçek eklendi: {fact}")
        
        # Yeni bir gerçek ekledikten sonra, tetiklenmesi gereken kurallar var mı diye kontrol et
        self._evaluate_rules()
    
    def retract_fact(self, fact: str):
        """Bir gerçeği ajan'ın bilgi tabanından kaldır."""
        if fact in self.facts:
            self.facts.remove(fact)
            print(f"Gerçek kaldırıldı: {fact}")
    
    def tell_rule(self, rule: str):
        """Ajan'ın bilgi tabanına yeni bir kural ekle."""
        if "->" not in rule:
            raise ValueError("Kural 'koşul -> eylem' formatında olmalıdır")
        
        condition, action = rule.split("->")
        condition = condition.strip()
        action = action.strip()
        
        self.rules[condition] = action
        print(f"Kural eklendi: {condition} -> {action}")
    
    def _parse_condition(self, condition: str) -> bool:
        """Mantıksal bir koşulu ayrıştır ve değerlendir."""
        # AND koşullarını ele al
        if "&" in condition:
            subconditions = [c.strip() for c in condition.split("&")]
            return all(self._parse_condition(subcond) for subcond in subconditions)
        
        # OR koşullarını ele al
        if "|" in condition:
            subconditions = [c.strip() for c in condition.split("|")]
            return any(self._parse_condition(subcond) for subcond in subconditions)
        
        # NOT koşullarını ele al
        if condition.startswith("!"):
            return not self._parse_condition(condition[1:].strip())
        
        # Temel durum: koşulun gerçeklerde olup olmadığını kontrol et
        return condition.strip() in self.facts
    
    def _evaluate_rules(self):
        """Mevcut gerçeklere dayalı tüm kuralları değerlendir ve eylemleri yürüt."""
        for condition, action in self.rules.items():
            if self._parse_condition(condition):
                self._execute_action(action)
    
    def _execute_action(self, action: str):
        """Tetiklenen bir kurala dayalı bir eylemi yürüt."""
        print(f"Eylem yürütülüyor: {action}")
        
        # Cihaz kontrolleri (Türkçeleştirilmiş)
        if action == "ısıtıcı_aç":
            self._turn_on_device("ısıtıcı")
        elif action == "ısıtıcı_kapat":
            self._turn_off_device("ısıtıcı")
        elif action == "kapı_aç":
            self._turn_on_device("kapı")
        elif action == "kapı_kapat":
            self._turn_off_device("kapı")
        elif action == "perde_aç":
            self._turn_on_device("perde")
        elif action == "perde_kapat":
            self._turn_off_device("perde")
        elif action == "televizyon_aç":
            self._turn_on_device("televizyon")
        elif action == "televizyon_kapat":
            self._turn_off_device("televizyon")
        elif action == "ışık_aç":
            self._turn_on_device("ışık")
        elif action == "ışık_kapat":
            self._turn_off_device("ışık")
        # Gelişmiş konfor eylemleri
        elif action == "mutlu_ortam_ışığı":
            self._turn_on_device("ışık")
            print("Mutlu ortam ışığı ayarlanıyor: parlak, sıcak tonlar")
        elif action == "neşeli_müzik_çal":
            print("Moral yükseltici müzik çalınıyor...")
        elif action == "uyku_ortamı_hazırla":
            self._turn_off_device("televizyon")
            self._turn_off_device("ışık")
            self._turn_off_device("perde")
            print("Uyku ortamı hazırlanıyor: perdeler kapatılıyor, ışıklar söndürülüyor.")
    
    def _turn_on_device(self, device: str):
        """Bir cihazı aç."""
        if device in self.devices:
            self.devices[device] = True
            print(f"{device.capitalize()} AÇILDI")
    
    def _turn_off_device(self, device: str):
        """Bir cihazı kapat."""
        if device in self.devices:
            self.devices[device] = False
            print(f"{device.capitalize()} KAPATILDI")
    
    def _adjust_heater_temp(self, delta: float):
        """Isıtıcı sıcaklığını ayarla."""
        self.device_temps["ısıtıcı"] += delta
        print(f"Isıtıcı sıcaklığı {self.device_temps['ısıtıcı']}°C olarak ayarlandı")
    
    def update_time_facts(self):
        """Günün saatiyle ilgili gerçekleri güncelle"""
        current_time = datetime.datetime.now()
        current_hour = current_time.hour
        
        # Mevcut tüm zaman gerçeklerini kaldır
        for time_fact in ["zaman_sabah", "zaman_öğle", "zaman_akşam", "zaman_gece"]:
            self.retract_fact(time_fact)
        
        # Mevcut zaman gerçeğini ekle
        if 5 <= current_hour < 12:
            self.tell_fact("zaman_sabah")
        elif 12 <= current_hour < 17:
            self.tell_fact("zaman_öğle")
        elif 17 <= current_hour < 22:
            self.tell_fact("zaman_akşam")
        else:
            self.tell_fact("zaman_gece")
    
    def detect_emotion(self, command: str):
        """Kullanıcı komutlarından duyguları algıla"""
        command_lower = command.lower()
        
        # Türkçe'de duygusal anahtar kelimeleri tanımla
        emotion_keywords = {
            "mutlu": ["mutlu", "sevinçli", "neşeli", "harika", "güzel", "memnun"],
            "üzgün": ["üzgün", "mutsuz", "kötü", "kederli", "sıkıntılı"],
            "kızgın": ["kızgın", "sinirli", "öfkeli", "kızmış", "sinirlendim"],
            "yorgun": ["yorgun", "yoruldum", "bitkin", "tükendim", "uykulu"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in command_lower for keyword in keywords):
                emotion_fact = f"kullanıcı_duygu_{emotion}"
                self.tell_fact(emotion_fact)
                return emotion
        
        return None
    
    def learn_from_command(self, command, facts_added):
        """Davranış kalıpları oluşturmak için kullanıcı komutlarından öğren"""
        current_time = datetime.datetime.now()
        current_hour = current_time.hour
        
        # Cihaz kullanım sıklığını takip et
        for fact in facts_added:
            if fact.endswith("_isteği"):
                device = fact.replace("_isteği", "").split("_")[0]
                if device in self.devices:
                    if device not in self.user_patterns["sık_kullanılan_cihazlar"]:
                        self.user_patterns["sık_kullanılan_cihazlar"][device] = 0
                    self.user_patterns["sık_kullanılan_cihazlar"][device] += 1
        
        # Sabah/akşam rutinlerini öğren
        if 5 <= current_hour < 10:
            for fact in facts_added:
                if fact not in self.user_patterns["sabah_rutini"]:
                    self.user_patterns["sabah_rutini"].append(fact)
        elif 18 <= current_hour < 23:
            for fact in facts_added:
                if fact not in self.user_patterns["akşam_rutini"]:
                    self.user_patterns["akşam_rutini"].append(fact)
        
        # Sıcaklık tercihlerini öğren
        if "kişi_üşüyor" in facts_added or "sıcaklık_artır_isteği" in facts_added:
            self.user_patterns["sıcaklık_tercihleri"].append("daha_sıcak_tercih")
        elif "sıcaklık_azalt_isteği" in facts_added:
            self.user_patterns["sıcaklık_tercihleri"].append("daha_serin_tercih")
    
    def call_gemini_api(self, prompt: str) -> str:
        """Gemini API'sini çağır ve yanıt al"""
        if not self.api_key:
            print("API anahtarı tanımlanmamış!")
            return "API anahtarı gerekiyor"
        
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 800
                }
            }
            
            # API endpoint'ine API anahtarını ekle
            endpoint = f"{self.llm_endpoint}?key={self.api_key}"
            
            response = requests.post(endpoint, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                # API yanıtını ayrıştır
                if "candidates" in result and len(result["candidates"]) > 0:
                    if "content" in result["candidates"][0] and "parts" in result["candidates"][0]["content"]:
                        return result["candidates"][0]["content"]["parts"][0]["text"]
                    
                return "API yanıtı ayrıştırılamadı"
            else:
                print(f"API hatası: {response.status_code}")
                print(f"Hata detayı: {response.text}")
                return f"API hatası: {response.status_code}"
                
        except Exception as e:
            print(f"API çağrısı sırasında hata: {str(e)}")
            return f"Hata: {str(e)}"
    
    def process_command_with_gemini(self, command: str):
        """Doğal dil komutunu Gemini API ile işle"""
        if not self.api_key:
            print("Gemini API anahtarı tanımlanmamış!")
            return self.process_command(command)
        
        prompt = f"""
        Ben bir akıllı ev sistemi için mantıksal bir ajanım. Aşağıdaki komutu analiz edip eyleme dönüştürmeme yardım et:
        
        Komut: "{command}"
        
        Aşağıdaki eylemlerden hangisinin uygun olduğunu belirt:
        - ısıtıcı_aç_isteği
        - ısıtıcı_kapat_isteği
        - kapı_aç_isteği
        - kapı_kapat_isteği
        - perde_aç_isteği
        - perde_kapat_isteği
        - televizyon_aç_isteği
        - televizyon_kapat_isteği
        - ışık_aç_isteği
        - ışık_kapat_isteği
        - sıcaklık_artır_isteği
        - sıcaklık_azalt_isteği
        - kişi_çıkıyor
        - kişi_uyuma_hazırlığı
        - kişi_üşüyor
        
        Hangi eylem(ler) gerçekleştirilmeli? Sadece eylem adlarını liste halinde döndür, açıklama ekleme.
        """
        
        api_response = self.call_gemini_api(prompt)
        
        # API yanıtından eylemleri çıkar
        actions = [line.strip() for line in api_response.split('\n') if line.strip() and '_isteği' in line.strip() or line.strip() in ["kişi_çıkıyor", "kişi_uyuma_hazırlığı", "kişi_üşüyor"]]
        
        if not actions:
            print(f"Gemini API'den uygun eylem bulunamadı. Normal işlemeye devam ediliyor.")
            return self.process_command(command)
        
        # Zaman gerçeklerini güncelle
        self.update_time_facts()
        
        # Duyguları algıla
        detected_emotion = self.detect_emotion(command)
        
        # Komut işlemeden önce gerçekleri takip et
        facts_before = set(self.facts)
        
        # API'den gelen eylemleri uygula
        for action in actions:
            action = action.strip()
            if action:
                self.tell_fact(action)
            
        # Bu komuttan öğren
        facts_added = self.facts - facts_before
        self.learn_from_command(command, facts_added)
        
        return detected_emotion
    
    def process_command(self, command: str):
        """Doğal dil komutunu işle."""
        # Zaman gerçeklerini güncelle
        self.update_time_facts()
        
        # Duyguları algıla
        detected_emotion = self.detect_emotion(command)
        
        # Komutu kolay eşleştirme için küçük harfe çevir
        command = command.lower()
        
        # Komut işlemeden önce gerçekleri takip et
        facts_before = set(self.facts)
        
        # Türkçe komutlar için desen eşleştirme
        if any(phrase in command for phrase in ["klimayı aç", "ısıtıcıyı aç", "ısıtıcı aç"]):
            self.tell_fact("ısıtıcı_aç_isteği")
        elif any(phrase in command for phrase in ["klimayı kapat", "ısıtıcıyı kapat", "ısıtıcı kapat"]):
            self.tell_fact("ısıtıcı_kapat_isteği")
        elif any(phrase in command for phrase in ["üşüyorum", "soğuk", "çok soğuk"]):
            self.tell_fact("kişi_üşüyor")
        elif any(phrase in command for phrase in ["kapıyı aç", "kapı aç"]):
            self.tell_fact("kapı_aç_isteği")
        elif any(phrase in command for phrase in ["kapıyı kapat", "kapı kapat"]):
            self.tell_fact("kapı_kapat_isteği")
        elif any(phrase in command for phrase in ["perdeyi aç", "perdeleri aç", "perde aç"]):
            self.tell_fact("perde_aç_isteği")
        elif any(phrase in command for phrase in ["perdeyi kapat", "perdeleri kapat", "perde kapat"]):
            self.tell_fact("perde_kapat_isteği")
        elif any(phrase in command for phrase in ["televizyonu aç", "tv aç", "tv'yi aç"]):
            self.tell_fact("televizyon_aç_isteği")
        elif any(phrase in command for phrase in ["televizyonu kapat", "tv kapat", "tv'yi kapat"]):
            self.tell_fact("televizyon_kapat_isteği")
        elif any(phrase in command for phrase in ["ışıkları aç", "lambayı aç", "ışık aç"]):
            self.tell_fact("ışık_aç_isteği")
        elif any(phrase in command for phrase in ["ışıkları kapat", "lambayı kapat", "ışık kapat"]):
            self.tell_fact("ışık_kapat_isteği")
        elif any(phrase in command for phrase in ["sıcaklığı arttır", "daha sıcak"]):
            self.tell_fact("sıcaklık_artır_isteği")
            self._adjust_heater_temp(1.0)
        elif any(phrase in command for phrase in ["sıcaklığı azalt", "daha soğuk"]):
            self.tell_fact("sıcaklık_azalt_isteği")
            self._adjust_heater_temp(-1.0)
        elif "çıkıyorum" in command or "gidiyorum" in command:
            self.tell_fact("kişi_çıkıyor")
        elif "uyumak" in command:
            self.tell_fact("kişi_uyuma_hazırlığı")
        else:
            print(f"Anlaşılamadı: {command}")
        
        # Bu komuttan öğren
        facts_added = self.facts - facts_before
        self.learn_from_command(command, facts_added)
        
        return detected_emotion
    
    def get_device_status(self):
        """Tüm cihazların mevcut durumunu döndür."""
        status = {}
        for device, is_on in self.devices.items():
            status[device] = "AÇIK" if is_on else "KAPALI"
        
        # Isıtıcı için sıcaklık ekle
        if "ısıtıcı" in self.device_temps:
            status["ısıtıcı_sıcaklığı"] = f"{self.device_temps['ısıtıcı']}°C"
            
        return status
    
    def display_facts(self):
        """Tüm mevcut gerçekleri görüntüle."""
        print("\nMevcut Gerçekler:")
        for fact in sorted(self.facts):
            print(f"- {fact}")

    def display_rules(self):
        """Tüm kuralları görüntüle."""
        print("\nMevcut Kurallar:")
        for condition, action in self.rules.items():
            print(f"- EĞER {condition} İSE {action}")


def run_demo():
    """LogicAgent'in basit bir interaktif demosunu çalıştır."""
    print("Akıllı Ev Mantık Ajanı")
    print("=" * 50)
    
    # Ajanı Gemini API anahtarı ile başlat
    gemini_api_key = "Lütfen Buraya Kendi APInizi giriniz"
    agent = LogicAgent(api_key=gemini_api_key)
    
    print("\nMevcut cihaz durumları:")
    print(json.dumps(agent.get_device_status(), indent=2, ensure_ascii=False))
    
    print("\nKomutları Türkçe olarak giriniz. 'çıkış' yazarak programdan çıkabilirsiniz.")
    print("Gelişmiş NLP analizi için Gemini API entegre edilmiştir.")
    
    while True:
        command = input("\nKomut: ")
        
        if command.lower() in ['çıkış', 'exit', 'quit']:
            print("Programdan çıkılıyor...")
            break
        
        if command.lower() == 'durum':
            print("\nCihaz Durumları:")
            print(json.dumps(agent.get_device_status(), indent=2, ensure_ascii=False))
            agent.display_facts()
            continue
            
        if command.lower() == 'kurallar':
            agent.display_rules()
            continue
        
        # İleri doğal dil işleme için Gemini API kullan
        emotion = agent.process_command_with_gemini(command)
        
        # Algılanan duyguyu onayla
        if emotion:
            print(f"Duygusal durumunuz anlaşıldı: {emotion}")
        
        # Mevcut durumu göster
        print("\nGüncel Cihaz Durumları:")
        print(json.dumps(agent.get_device_status(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    run_demo()
