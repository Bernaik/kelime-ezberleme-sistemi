import sqlite3

# Veritabanına bağlanıyoruz
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# 50 Adet Hazır Kelime Listesi (İngilizce, Türkçe, Örnek Cümle, Resim Yolu)
hazir_kelimeler = [
    
    ("Brain", "Beyin", "Young and clever Brain is walking in the forest.", "static/uploads/brain.jpeg"),
    ("Night", "Gece", "He began a mysterious journey during the night.", "static/uploads/night.jpeg"),
    ("Tiger", "Kaplan", "A dangerous tiger appeared and changed everything.", "static/uploads/tiger.jpeg"),
    ("Robin", "Ardıç Kuşu / Robin", "A robin bird showed him the safe way out.", "static/uploads/robin.jpeg"),
    ("Noble", "Soylu / Asil", "The robin was remembered as a noble hero.", "static/uploads/noble.jpeg"),
    ("Throw", "Atmak / Fırlatmak", "Do not throw garbage out of the truck window.", "static/uploads/throw.jpeg"),
    ("Arise", "Ortaya Çıkmak", "New opportunities arise when you study hard.", "static/uploads/arise.jpeg"),
    ("Route", "Rota / Yol", "This is the shortest route to the university faculty.", "static/uploads/route.jpeg"),
    ("Rule", "Kural", "We must follow the school rules during the exam.", "static/uploads/rule.jpeg"),
    ("Rebus", "Resimli Bilmece", "Solving a rebus puzzle is very fun and educational.", "static/uploads/rebus.jpeg"),
    ("Achieve", "Başarmak", "You can achieve your goals if you work hard.", "static/uploads/achieve.jpeg"),
    ("Believe", "İnanmak", "Always believe in yourself and your abilities.", "static/uploads/believe.jpeg"),
    ("Create", "Yaratmak / Oluşturmak", "Software developers create useful applications.", "static/uploads/create.jpeg"),
    ("Develop", "Geliştirmek", "We need to develop a new relational database.", "static/uploads/develop.jpeg"),
    ("Explore", "Keşfetmek", "Students love to explore new programming languages.", "static/uploads/explore.jpeg"),
    ("Forget", "Unutmak", "Do not forget to save your code before closing.", "static/uploads/forget.jpeg"),
    ("Growth", "Büyüme / Gelişme", "The company showed a great economic growth.", "static/uploads/growth.jpeg"),
    ("Honest", "Dürüst", "Being honest is the most important value.", "static/uploads/honest.jpeg"),
    ("Improve", "Geliştirmek / İlerletmek", "I practice every day to improve my English.", "static/uploads/improve.jpeg"),
    ("Journey", "Yolculuk", "Learning to code is a long and beautiful journey.", "static/uploads/journey.jpeg"),
    ("Knowledge", "Bilgi", "Books are the main source of human knowledge.", "static/uploads/knowledge.jpeg"),
    ("Listen", "Dinlemek", "Please listen carefully to the teacher's instructions.", "static/uploads/listen.jpeg"),
    ("Manage", "Yönetmek", "Scrum masters manage the software projects smoothly.", "static/uploads/manage.jpeg"),
    ("Notice", "Fark Etmek", "Did you notice the mistake in the database design?", "static/uploads/notice.jpeg"),
    ("Observe", "Gözlemlemek", "Scientists observe the behavior of animals.", "static/uploads/observe.jpeg"),
    ("Protect", "Korumak", "Antivirus programs protect your computer from viruses.", "static/uploads/protect.jpeg"),
    ("Receive", "Almak / Kabul Etmek", "I hope to receive a good grade from the project.", "static/uploads/receive.jpeg"),
    ("Search", "Aramak", "You can search for words using the lookup module.", "static/uploads/search.jpeg"),
    ("Travel", "Seyahat Etmek", "We will travel to Europe for a solidarity project.", "static/uploads/travel.jpeg"),
    ("Understand", "Anlamak", "Do you understand the 6-times repetition logic?", "static/uploads/understand.jpeg"),
    ("Value", "Değer", "Time is a very precious value for students.", "static/uploads/value.jpeg"),
    ("Wonder", "Merak Etmek", "I wonder how many lines of code we wrote.", "static/uploads/wonder.jpeg"),
    ("Accept", "Kabul Etmek", "They decided to accept our transfer application.", "static/uploads/accept.jpeg"),
    ("Behave", "Davranmak", "Children should behave well at the school.", "static/uploads/behave.jpeg"),
    ("Cancel", "İptal Etmek", "The teacher had to cancel the quiz today.", "static/uploads/cancel.jpeg"),
    ("Damage", "Zarar Vermek", "Smoking can damage your physical health.", "static/uploads/damage.jpeg"),
    ("Effect", "Etki", "This project has a big effect on the final grade.", "static/uploads/effect.jpeg"),
    ("Flight", "Uçuş", "Our flight to Paris was delayed for two hours.", "static/uploads/flight.jpeg"),
    ("Gather", "Toplamak / Bir Araya Getirmek", "We will gather the team for a scrum meeting.", "static/uploads/gather.jpeg"),
    ("Impact", "Etki / Darbe", "Technology has a massive impact on education.", "static/uploads/impact.jpeg"),
    ("Leader", "Lider", "A good leader supports his team members.", "static/uploads/leader.jpeg"),
    ("Memory", "Hafıza / Anı", "This word game helps your long-term memory.", "static/uploads/memory.jpeg"),
    ("Object", "Nesne", "C# and Java are object-oriented languages.", "static/uploads/object.jpeg"),
    ("Patient", "Sabırlı", "You need to be patient when debugging code.", "static/uploads/patient.jpeg"),
    ("Refuse", "Reddetmek", "Never refuse a chance to learn something new.", "static/uploads/refuse.jpeg"),
    ("Select", "Seçmek", "Please select a picture for the new word.", "static/uploads/select.jpeg"),
    ("Theory", "Teori", "We learned the normalization theory in class.", "static/uploads/theory.jpeg"),
    ("Unique", "Benzersiz / Eşsiz", "Every user has a unique username in the system.", "static/uploads/unique.jpeg"),
    ("Verify", "Doğrulamak", "The system will verify your password at login.", "static/uploads/verify.jpeg"),
    ("Wealth", "Zenginlik", "Good health is the greatest wealth in life.", "static/uploads/wealth.jpeg")
]

print("🔄 50 kelime veritabanına yükleniyor...")

# Tabloyu temizleyip temiz ekleme yapmak için (Opsiyonel)
# cursor.execute("DELETE FROM words")

for eng, tur, sample, pic in hazir_kelimeler:
    # correct_count=0, learned=0 olarak başlıyorlar (Quizde çıkması için)
    cursor.execute(
        "INSERT INTO words (english, turkish, sample, picture, correct_count, learned) VALUES (?, ?, ?, ?, 0, 0)",
        (eng, tur, sample, pic),
    )

connection.commit()
connection.close()

print("✅ 50 adet harika kelime veritabanına başarıyla yüklendi!")
