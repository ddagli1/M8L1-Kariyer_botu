import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            # Otomatik artan ID ile kariyer tablosu
            conn.execute('''CREATE TABLE IF NOT EXISTS careers (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                category TEXT NOT NULL,
                                skills TEXT NOT NULL,
                                description TEXT NOT NULL
                            )''')
        print(f"Tablo kontrol edildi/oluşturuldu: {self.database}")
        self.add_default_data()
            
    def add_default_data(self):
        """Eğer veritabanı boşsa örnek kariyer yolları ekler."""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM careers")
        if cursor.fetchone()[0] == 0:
            default_careers = [
                ('Veri Bilimci', 'Teknoloji', 'Python, SQL, İstatistik', 'Veri yığınlarından anlamlı hikayeler çıkaran geleceğin dedektifi.'),
                ('Siber Güvenlik Uzmanı', 'Teknoloji', 'Ağ Güvenliği, Linux, Etik Hackerlık', 'Dijital dünyayı siber saldırılara karşı koruyan bir kale muhafızı.'),
                ('UI/UX Tasarımcı', 'Yaratıcı Sanatlar', 'Figma, Adobe XD, Kullanıcı Psikolojisi', 'Uygulamaların hem güzel görünmesini hem de kolay kullanılmasını sağlayan sanatçı.'),
                ('Dijital İçerik Üreticisi', 'Yaratıcı Sanatlar', 'Video Kurgu, Hikaye Anlatıcılığı', 'Sosyal medya platformlarında kitleleri etkileyen yaratıcı projeler üreten kişi.'),
                ('E-Ticaret Stratejisti', 'İş Dünyası', 'Pazaryeri Yönetimi, Dijital Reklam', 'Ürünlerin online dünyada doğru kitleye ulaşmasını sağlayan satış dehası.')
            ]
            
            cursor.executemany(
                "INSERT INTO careers (name, category, skills, description) VALUES (?, ?, ?, ?)", 
                default_careers
            )
            conn.commit()
            print(f"{len(default_careers)} adet varsayılan veri başarıyla eklendi!")
        else:
            print("Veri tabanı zaten dolu, ekleme yapılmadı.")

    def get_careers_by_category(self, category):
        conn = sqlite3.connect(self.database)
        with conn:
            return conn.execute("SELECT name, description FROM careers WHERE category = ?", (category,)).fetchall()

# --- SCRIPT OLARAK ÇALIŞTIRMA BÖLÜMÜ ---
if __name__ == "__main__":
    # Veri tabanı yöneticisini başlat
    manager = DB_Manager(DATABASE)
    
    # Tabloları oluştur ve varsayılan verileri yükle
    print("Veri tabanı kurulumu başlatılıyor...")
    manager.create_tables()
    print("İşlem tamamlandı!")
