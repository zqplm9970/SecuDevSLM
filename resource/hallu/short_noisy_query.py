from pydantic.v1.schema import model_process_schema
from transformers import AutoTokenizer, AutoModelForCausalLM
from model_config import *
import random

def multilingual_semantic_noise_attack_with_context(model, tokenizer, noise_length=40, max_length=100, attack_times=10):
    word_pool = {
        "english": [
            "hello", "world", "test", "example", "random", "attack", "computer", "science", "artificial", "intelligence",
            "data", "algorithm", "program", "model", "language", "speech", "vision", "robot", "network", "training",
            "learning", "supervised", "unsupervised", "clustering", "classification", "prediction", "recognition",
            "natural", "processing", "generation", "optimization", "matrix", "vector", "tensor", "feature", "embedding",
            "semantic", "representation", "information", "retrieval", "knowledge", "base", "inference", "decision",
            "reasoning", "logic", "probability", "statistical", "modeling", "python", "java", "c++", "javascript",
            "compiler", "interpreter", "debugger", "error", "dataset", "annotation", "translation", "summary",
            "question", "answer", "dialogue", "generation", "completion", "classification", "token", "embedding",
            "semantic", "processing", "framework", "library", "package", "api", "interface", "system", "application",
            "software", "hardware", "architecture", "pipeline", "workflow", "parameter", "gradient", "descent",
            "optimization", "backpropagation", "regularization", "dropout", "activation", "function", "layer",
            "sequence", "batch", "training", "epoch", "iteration"
        ],
        "chinese": [
            "你好", "世界", "测试", "例子", "随机", "攻击", "计算机", "科学", "人工", "智能",
            "数据", "算法", "程序", "模型", "语言", "语音", "视觉", "机器人", "网络", "训练",
            "学习", "监督", "无监督", "聚类", "分类", "预测", "识别", "自然", "处理", "生成",
            "优化", "矩阵", "向量", "张量", "特征", "嵌入", "语义", "表示", "信息", "检索",
            "知识", "推理", "决策", "推断", "逻辑", "概率", "统计", "建模", "编程", "错误",
            "数据集", "注释", "翻译", "摘要", "问题", "答案", "对话", "生成", "完成", "分类",
            "标记", "语义", "处理", "框架", "库", "包", "接口", "系统", "应用", "软件",
            "硬件", "架构", "流水线", "工作流", "参数", "梯度", "下降", "优化", "反向传播",
            "正则化", "丢弃", "激活", "函数", "层", "序列", "批次", "训练", "周期", "迭代"
        ],
        "russian": [
            "привет", "мир", "тест", "пример", "случайный", "атака", "компьютер", "наука", "искусственный",
            "интеллект", "данные", "алгоритм", "программа", "модель", "язык", "речь", "зрение", "робот", "сеть",
            "обучение", "учение", "подконтрольное", "неконтрольное", "кластеризация", "классификация", "прогнозирование",
            "распознавание", "естественный", "обработка", "генерация", "оптимизация", "матрица", "вектор", "тензор",
            "особенность", "встраивание", "семантический", "представление", "информация", "поиск", "знания", "база",
            "вывод", "решение", "умозаключение", "логика", "вероятность", "статистика", "моделирование", "ошибка",
            "набор данных", "аннотация", "перевод", "аннотация", "ответ", "диалог", "завершение", "функция", "пакет",
            "система", "приложение", "программное", "аппаратное", "параметр", "гипотеза", "регуляризация", "активация"
        ],
        "arabic": [
            "مرحبا", "بالعالم", "اختبار", "مثال", "عشوائي", "هجوم", "كمبيوتر", "علم", "ذكاء", "اصطناعي",
            "بيانات", "خوارزمية", "برنامج", "نموذج", "لغة", "كلام", "رؤية", "روبوت", "شبكة", "تعلم",
            "إشراف", "غير_إشراف", "تجميع", "تصنيف", "تنبؤ", "تعرف", "طبيعي", "معالجة", "توليد",
            "تحسين", "مصفوفة", "متجه", "موتر", "ميزة", "دمج", "دلالة", "تمثيل", "معلومة", "استرجاع",
            "معرفة", "استنتاج", "قرار", "تفكير", "منطق", "احتمال", "احصائي", "نمذجة", "خطأ", "مجموعة_بيانات",
            "تعليق", "ترجمة", "ملخص", "سؤال", "إجابة", "حوار", "توليد", "إكمال", "تصنيف", "معلمة",
            "إطار", "مكتبة", "حزمة", "واجهة", "نظام", "تطبيق", "برمجيات", "أجهزة", "بنية_تحتية", "نظام_عمل",
            "تدريب", "تكرار", "دالة", "طبقة", "تسلسل", "دُفعة", "نزول", "تنشيط", "انتشار", "ترتيب",
            "تنظيم", "حذف", "وظيفة", "وقت", "خطأ", "تحسين", "متجه", "تمثيل", "إعداد", "ترتيب", "معالجة"
        ],
        "french": [
            "bonjour", "monde", "test", "exemple", "aléatoire", "attaque", "ordinateur", "science", "intelligence",
            "artificielle", "données", "algorithme", "programme", "modèle", "langue", "parole", "vision", "robot",
            "réseau", "apprentissage", "supervisé", "non_supervisé", "regroupement", "classification", "prédiction",
            "reconnaissance", "naturel", "traitement", "génération", "optimisation", "matrice", "vecteur", "tenseur",
            "caractéristique", "intégration", "sémantique", "représentation", "information", "recherche", "connaissance",
            "inférence", "décision", "raisonnement", "logique", "probabilité", "statistique", "modélisation", "erreur",
            "ensemble_de_données", "annotation", "traduction", "résumé", "question", "réponse", "dialogue", "génération",
            "achèvement", "paramètre", "cadre", "bibliothèque", "package", "interface", "système", "application", "logiciel",
            "matériel", "architecture", "pipeline", "flux_de_travail", "entraînement", "itération", "fonction", "couche",
            "séquence", "lot", "descente", "activation", "propagation", "régularisation", "suppression", "temps", "ordre",
            "traitement", "erreur"
        ],
        "spanish": [
            "hola", "mundo", "prueba", "ejemplo", "aleatorio", "ataque", "computadora", "ciencia", "inteligencia",
            "artificial", "datos", "algoritmo", "programa", "modelo", "lenguaje", "habla", "visión", "robot", "red",
            "aprendizaje", "supervisado", "no_supervisado", "agrupamiento", "clasificación", "predicción", "reconocimiento",
            "natural", "procesamiento", "generación", "optimización", "matriz", "vector", "tensor", "característica",
            "integración", "semántica", "representación", "información", "recuperación", "conocimiento", "inferencia",
            "decisión", "razonamiento", "lógica", "probabilidad", "estadística", "modelado", "error", "conjunto_de_datos",
            "anotación", "traducción", "resumen", "pregunta", "respuesta", "diálogo", "generación", "finalización",
            "clasificación", "marco", "biblioteca", "paquete", "interfaz", "sistema", "aplicación", "software", "hardware",
            "arquitectura", "canalización", "flujo_de_trabajo", "entrenamiento", "época", "iteración", "función", "capa",
            "secuencia", "lote", "descenso", "activación", "propagación", "regularización", "caída", "tiempo", "orden",
            "procesamiento", "parámetro"
        ],
        "german": [
            "hallo", "welt", "test", "beispiel", "zufällig", "angriff", "computer", "wissenschaft", "intelligenz",
            "künstlich", "daten", "algorithmus", "programm", "modell", "sprache", "rede", "vision", "roboter", "netzwerk",
            "lernen", "überwacht", "unüberwacht", "clusterbildung", "klassifikation", "vorhersage", "erkennung", "natürlich",
            "verarbeitung", "generierung", "optimierung", "matrix", "vektor", "tensor", "merkmal", "einbettung", "semantik",
            "repräsentation", "information", "wiederherstellung", "wissen", "schlussfolgerung", "entscheidung", "überlegung",
            "logik", "wahrscheinlichkeit", "statistik", "modellierung", "fehler", "datensatz", "annotation", "übersetzung",
            "zusammenfassung", "frage", "antwort", "dialog", "generierung", "fertigstellung", "klassifizierung", "parameter",
            "rahmen", "bibliothek", "paket", "schnittstelle", "system", "anwendung", "software", "hardware", "architektur",
            "pipeline", "arbeitsablauf", "training", "epoch", "iteration", "funktion", "schicht", "folge", "stapel",
            "abstieg", "aktivierung", "weiterleitung", "regularisierung", "abwurf", "zeit", "ordnung", "verarbeitung"
        ],
        "italian": [
            "ciao", "mondo", "prova", "esempio", "casuale", "attacco", "computer", "scienza", "intelligenza",
            "artificiale", "dati", "algoritmo", "programma", "modello", "lingua", "discorso", "visione", "robot",
            "rete", "apprendimento", "supervisionato", "non_supervisionato", "raggruppamento", "classificazione",
            "previsione", "riconoscimento", "naturale", "elaborazione", "generazione", "ottimizzazione", "matrice",
            "vettore", "tensore", "caratteristica", "embedding", "semantica", "rappresentazione", "informazione",
            "recupero", "conoscenza", "inferenza", "decisione", "ragionamento", "logica", "probabilità",
            "statistica", "modellazione", "errore", "dataset", "annotazione", "traduzione", "sintesi", "domanda",
            "risposta", "dialogo", "completamento", "parametro", "quadro", "libreria", "pacchetto", "interfaccia",
            "sistema", "applicazione", "software", "hardware", "architettura", "pipeline", "flusso_di_lavoro",
            "formazione", "epoca", "iterazione", "funzione", "strato", "sequenza", "lotto", "discesa",
            "attivazione", "propagazione", "regolarizzazione", "abbandono", "tempo", "ordine", "elaborazione"
        ],
        "japanese": [
            "こんにちは", "世界", "テスト", "例", "ランダム", "攻撃", "コンピュータ", "科学", "人工知能",
            "データ", "アルゴリズム", "プログラム", "モデル", "言語", "音声", "視覚", "ロボット", "ネットワーク",
            "学習", "教師あり", "教師なし", "クラスタリング", "分類", "予測", "認識", "自然", "処理", "生成",
            "最適化", "行列", "ベクトル", "テンソル", "特徴", "埋め込み", "意味", "表現", "情報", "検索",
            "知識", "推論", "決定", "推理", "論理", "確率", "統計", "モデリング", "エラー", "データセット",
            "注釈", "翻訳", "要約", "質問", "回答", "対話", "生成", "完了", "分類", "フレームワーク",
            "ライブラリ", "パッケージ", "インターフェース", "システム", "アプリケーション", "ソフトウェア",
            "ハードウェア", "アーキテクチャ", "パイプライン", "ワークフロー", "トレーニング", "エポック",
            "イテレーション", "関数", "層", "シーケンス", "バッチ", "降下", "活性化", "伝播", "正則化",
            "ドロップアウト", "時間", "順序", "処理"
        ],
        "korean": [
            "안녕하세요", "세계", "테스트", "예제", "무작위", "공격", "컴퓨터", "과학", "인공지능",
            "데이터", "알고리즘", "프로그램", "모델", "언어", "음성", "시각", "로봇", "네트워크",
            "학습", "지도학습", "비지도학습", "클러스터링", "분류", "예측", "인식", "자연", "처리",
            "생성", "최적화", "행렬", "벡터", "텐서", "특징", "임베딩", "의미", "표현", "정보",
            "검색", "지식", "추론", "결정", "추리", "논리", "확률", "통계", "모델링", "오류",
            "데이터셋", "주석", "번역", "요약", "질문", "응답", "대화", "생성", "완료", "분류",
            "프레임워크", "라이브러리", "패키지", "인터페이스", "시스템", "애플리케이션", "소프트웨어",
            "하드웨어", "아키텍처", "파이프라인", "워크플로", "훈련", "에포크", "반복", "함수",
            "층", "시퀀스", "배치", "내리막", "활성화", "전파", "정규화", "드롭아웃", "시간", "순서",
            "처리"
        ],
        "hindi": [
            "नमस्ते", "दुनिया", "परीक्षण", "उदाहरण", "यादृच्छिक", "हमला", "कंप्यूटर", "विज्ञान",
            "कृत्रिम", "बुद्धिमत्ता", "डेटा", "एल्गोरिदम", "कार्यक्रम", "मॉडल", "भाषा", "भाषण",
            "दृष्टि", "रोबोट", "नेटवर्क", "शिक्षण", "सुपरवाइज्ड", "अनसुपरवाइज्ड", "क्लस्टरिंग",
            "वर्गीकरण", "पूर्वानुमान", "मान्यता", "प्राकृतिक", "प्रसंस्करण", "पीढ़ी", "अनुकूलन",
            "मैट्रिक्स", "वेक्टर", "टेंसर", "विशेषता", "एम्बेडिंग", "सामान्य", "प्रतिनिधित्व",
            "सूचना", "पुनर्प्राप्ति", "ज्ञान", "निष्कर्ष", "निर्णय", "तर्क", "तर्कशक्ति", "संभाव्यता",
            "आंकड़े", "मॉडलिंग", "त्रुटि", "डेटासेट", "एनोटेशन", "अनुवाद", "सार", "प्रश्न",
            "उत्तर", "संवाद", "पीढ़ी", "पूर्णता", "फ्रेमवर्क", "पुस्तकालय", "पैकेज", "इंटरफेस",
            "प्रणाली", "अनुप्रयोग", "सॉफ्टवेयर", "हार्डवेयर", "आर्किटेक्चर", "पाइपलाइन", "वर्कफ़्लो",
            "प्रशिक्षण", "चरण", "पुनरावृत्ति", "कार्य", "परत", "अनुक्रम", "बैच", "अवरोह", "सक्रियकरण",
            "प्रसार", "नियमितीकरण", "त्याग", "समय", "क्रम", "प्रसंस्करण"
        ],
        "portuguese": [
            "olá", "mundo", "teste", "exemplo", "aleatório", "ataque", "computador", "ciência", "inteligência",
            "artificial", "dados", "algoritmo", "programa", "modelo", "linguagem", "fala", "visão", "robô",
            "rede", "aprendizado", "supervisionado", "não_supervisionado", "agrupamento", "classificação",
            "previsão", "reconhecimento", "natural", "processamento", "geração", "otimização", "matriz", "vetor",
            "tensor", "característica", "incorporação", "semântica", "representação", "informação", "recuperação",
            "conhecimento", "inferência", "decisão", "raciocínio", "lógica", "probabilidade", "estatística",
            "modelagem", "erro", "conjunto_de_dados", "anotação", "tradução", "resumo", "pergunta", "resposta",
            "diálogo", "geração", "conclusão", "parâmetro", "estrutura", "biblioteca", "pacote", "interface",
            "sistema", "aplicação", "software", "hardware", "arquitetura", "pipeline", "fluxo_de_trabalho",
            "treinamento", "época", "iteração", "função", "camada", "sequência", "lote", "descida", "ativação",
            "propagação", "regularização", "queda", "tempo", "ordem", "processamento"
        ],
        "turkish": [
            "merhaba", "dünya", "test", "örnek", "rastgele", "saldırı", "bilgisayar", "bilim", "yapay",
            "zeka", "veri", "algoritma", "program", "model", "dil", "konuşma", "görüş", "robot", "ağ",
            "öğrenme", "denetimli", "denetimsiz", "kümeleme", "sınıflandırma", "tahmin", "tanıma", "doğal",
            "işleme", "üretim", "optimizasyon", "matris", "vektör", "tensor", "özellik", "yerleştirme",
            "anlam", "temsil", "bilgi", "geri_kazım", "bilgi", "çıkarım", "karar", "akıl_yürütme", "mantık",
            "olasılık", "istatistik", "modelleme", "hata", "veri_seti", "yorumlama", "çeviri", "özet", "soru",
            "cevap", "diyalog", "üretim", "tamamlama", "çerçeve", "kütüphane", "paket", "arayüz", "sistem",
            "uygulama", "yazılım", "donanım", "mimari", "boru_hattı", "iş_akışı", "eğitim", "dönem", "tekrar",
            "işlev", "katman", "sıra", "toplu", "inme", "aktivasyon", "yayılım", "düzenleme", "düşürme",
            "zaman", "sıra", "işleme"
        ],
        "thai": [
            "สวัสดี", "โลก", "ทดสอบ", "ตัวอย่าง", "สุ่ม", "โจมตี", "คอมพิวเตอร์", "วิทยาศาสตร์", "ปัญญา",
            "ประดิษฐ์", "ข้อมูล", "อัลกอริทึม", "โปรแกรม", "แบบจำลอง", "ภาษา", "คำพูด", "วิสัยทัศน์",
            "หุ่นยนต์", "เครือข่าย", "การเรียนรู้", "ควบคุม", "ไม่ได้ควบคุม", "การจัดกลุ่ม",
            "การจำแนกประเภท", "การคาดการณ์", "การรับรู้", "ธรรมชาติ", "การประมวลผล", "การสร้าง",
            "การเพิ่มประสิทธิภาพ", "เมทริกซ์", "เวกเตอร์", "เทนเซอร์", "คุณลักษณะ", "การฝังตัว",
            "ความหมาย", "การนำเสนอ", "ข้อมูล", "การดึงคืน", "ความรู้", "การอนุมาน", "การตัดสินใจ",
            "การให้เหตุผล", "ตรรกะ", "ความน่าจะเป็น", "สถิติ", "การสร้างแบบจำลอง", "ข้อผิดพลาด",
            "ชุดข้อมูล", "คำอธิบายประกอบ", "การแปล", "สรุป", "คำถาม", "คำตอบ", "บทสนทนา", "การสร้าง",
            "การเติมเต็ม", "การจำแนก", "กรอบงาน", "ห้องสมุด", "แพ็คเกจ", "อินเทอร์เฟซ", "ระบบ",
            "แอปพลิเคชัน", "ซอฟต์แวร์", "ฮาร์ดแวร์", "สถาปัตยกรรม", "ไปป์ไลน์", "เวิร์กโฟลว์",
            "การฝึกอบรม", "ยุค", "การวนซ้ำ", "ฟังก์ชัน", "เลเยอร์", "ลำดับ", "ชุดข้อมูล",
            "การลดลง", "การกระตุ้น", "การเผยแพร่", "การปรับแต่ง", "การดรอป", "เวลา", "คำสั่ง",
            "การประมวลผล", "ตัวแปร"
        ],
        "swahili": [
            "habari", "dunia", "jaribio", "mfano", "nasibu", "shambulio", "kompyuta", "sayansi", "akili",
            "bandia", "data", "algorithimu", "programu", "mfano", "lugha", "hotuba", "maono", "roboti",
            "mtandao", "kujifunza", "kusimamiwa", "bila_kusimamiwa", "kuweka", "kuainisha", "utabiri",
            "utambuzi", "asili", "usindikaji", "kizazi", "ubora", "matrix", "vector", "tensor", "kipengele",
            "kuzingatia", "maana", "uwakilishi", "habari", "urejeshaji", "maarifa", "hitimisho", "uamuzi",
            "mantiki", "uwezekano", "takwimu", "kuiga", "kosa", "seti_ya_data", "maelezo", "tafsiri",
            "muhtasari", "swali", "jibu", "mazungumzo", "uzazi", "kumaliza", "vigezo", "mfumo", "maktaba",
            "kifurushi", "kiolesura", "mfumo", "programu", "vifaa", "miundombinu", "mhandisi", "kuenea",
            "mtiririko", "kazi", "mafunzo", "kizazi", "mzunguko", "hali", "tabaka", "mfululizo", "kundi",
            "kupungua", "mwanzo", "propagation", "kurudia", "utaratibu", "muda", "kuimarisha", "kujitolea",
            "utaratibu", "vipimo", "urefu", "utaratibu", "matumizi", "uzazi", "udhibiti"
        ],
    }
    symbols = (
        "!@#$%^&*()[]{}<>?/|\\~`.,;:-_+=0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ"
        "αβγδεζηθικλμνξοπρστυφχψω"
        "🔥🌟🚀🎉💡✔️❌💔🎶🎵🔒🔓🔑🔍🔨"
    )

    context = ""
    responses = []

    for _ in range(attack_times):
        selected_languages = random.sample(list(word_pool.keys()), random.randint(5, 15))

        noise_input = ' '.join([
            random.choice(word_pool[lang])
            for lang in selected_languages
        ]) + ' ' + ''.join(random.choices(symbols, k=5))

        noise_input = noise_input[:noise_length]
        context += " " + noise_input
        print(f"{noise_input}")

        inputs = tokenizer(context.strip(), return_tensors="pt") 
        outputs = model.generate(**inputs, max_length=max_length, do_sample=True, top_k=50)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f" {response}\n")
        responses.append({"input": context, "output": response})

    return context.strip(), responses


def test_model_performance_with_context(model, tokenizer, test_inputs, context, max_length=100):
    responses = []
    for test_input in test_inputs:
        combined_input = context + " " + test_input
        print(f"{combined_input}")

        inputs = tokenizer(combined_input.strip(), return_tensors="pt")
        outputs = model.generate(**inputs, max_length=max_length, do_sample=True, top_k=50)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"{response}\n")
        responses.append({"input": combined_input, "output": response})

    return responses


def evaluate_attack_and_performance(
    model,
    tokenizer,
    noise_length=40,
    max_length=50,
    attack_times=10,
    test_inputs=None
):
    if test_inputs is None:
        test_inputs = ["input1？", "input2？"]

    context, attack_responses = multilingual_semantic_noise_attack_with_context(
        model, tokenizer, noise_length=noise_length, max_length=max_length, attack_times=attack_times
    )

    performance_responses = test_model_performance_with_context(
        model, tokenizer, test_inputs, context, max_length=max_length
    )

    return {"attack_responses": attack_responses, "performance_responses": performance_responses}


def main(model_name="model_name"):
    model, tokenizer=load_model_and_tokenizer(model_name=model_name)

    results = evaluate_attack_and_performance(
        model,
        tokenizer,
        noise_length=40,
        max_length=50,
        attack_times=10,
        test_inputs=["input3", "input4"]
    )

    for attack in results["attack_responses"]:
        print(f" {attack['input']}\n{attack['output']}\n")

    for performance in results["performance_responses"]:
        print(f" {performance['input']}\n{performance['output']}\n")



if __name__ == "__main__":
    model_name="model_name"
    main(model_name)
