"""
Gelişmiş Gemini Fine-Tuning Betiği

Bu betik, Google Generative AI (Gemini) üzerinde bir ince ayar (fine-tuning)
işlemini başlatmak, izlemek ve yönetmek için kullanılır.

Özellikler:
- Komut satırından yapılandırılabilir parametreler.
- JSON Lines (.jsonl) formatındaki eğitim verisini yükler.
- Aynı ID'ye sahip bir modelin varlığını kontrol eder.
- İşlem adımlarını detaylı bir şekilde loglar.
- API hatalarını ve diğer istisnaları yönetir.

Komut Satırı Kullanımı:
python advanced_finetune.py \
    --data_file "data/egitim_verisi.jsonl" \
    --model_id "rapor-html-donusturucu-v2" \
    --display_name "Rapor HTML Donusturucu v2" \
    --epochs 15
"""

import argparse
import logging
import os
import sys
import time
import google.generativeai as genai

# Sabit olarak temel modelimizi belirliyoruz.
# İleride bu da bir argüman olarak eklenebilir.
BASE_MODEL = "gemini-1.0-pro-001"

def setup_logging():
    """Loglama yapılandırmasını ayarlar."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )

def parse_arguments():
    """Komut satırı argümanlarını tanımlar ve ayrıştırır."""
    parser = argparse.ArgumentParser(description="Gemini modeli için gelişmiş fine-tuning betiği.")
    parser.add_argument(
        "--data_file",
        type=str,
        required=True,
        help="Eğitim için kullanılacak .jsonl formatındaki veri dosyasının yolu."
    )
    parser.add_argument(
        "--model_id",
        type=str,
        required=True,
        help="Oluşturulacak ayarlanmış model için benzersiz ID (küçük harf, rakam, tire)."
    )
    parser.add_argument(
        "--display_name",
        type=str,
        required=True,
        help="Model için kullanıcı dostu, görünen ad."
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=10,
        help="Eğitim döngüsü (epoch) sayısı."
    )
    return parser.parse_args()

def check_api_key():
    """Google API anahtarının ortam değişkenlerinde ayarlı olup olmadığını kontrol eder."""
    if "GOOGLE_API_KEY" not in os.environ:
        logging.error("HATA: GOOGLE_API_KEY ortam değişkeni ayarlanmamış.")
        sys.exit(1)
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    logging.info("Google API anahtarı başarıyla yapılandırıldı.")

def check_if_model_exists(model_id: str) -> bool:
    """Verilen ID ile bir modelin zaten var olup olmadığını kontrol eder."""
    try:
        # tunedModels/model_id formatı gerekiyor
        full_model_name = f"tunedModels/{model_id}"
        genai.get_tuned_model(name=full_model_name)
        logging.warning(f"'{full_model_name}' ID'li model zaten mevcut. İşlem durduruluyor.")
        return True
    except Exception as e:
        # 'Not Found' hatası beklenen durumdur, modelin olmadığını gösterir.
        if "404" in str(e) and "was not found" in str(e):
             logging.info(f"'{model_id}' ID'li bir model bulunamadı, yeni model oluşturulabilir.")
             return False
        # Diğer beklenmedik hatalar
        logging.error(f"Model kontrolü sırasında beklenmedik bir hata oluştu: {e}")
        raise

def upload_training_file(file_path: str) -> genai.File:
    """Eğitim dosyasını API'ye yükler ve işlenmesini bekler."""
    if not os.path.exists(file_path):
        logging.error(f"Veri dosyası bulunamadı: {file_path}")
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {file_path}")

    logging.info(f"'{file_path}' dosyası yükleniyor...")
    training_file = genai.upload_file(path=file_path)
    
    logging.info(f"Dosya '{training_file.name}' adıyla yüklendi. İşlenmesi bekleniyor...")
    while training_file.state.name == "PROCESSING":
        time.sleep(5)
        training_file = genai.get_file(training_file.name)
        logging.info("Dosya durumu: PROCESSING...")
    
    if training_file.state.name == "FAILED":
        logging.error("Dosya yükleme ve işleme başarısız oldu.")
        raise ValueError("Dosya yüklenemedi.")

    logging.info("Dosya başarıyla işlendi ve kullanıma hazır.")
    return training_file

def launch_and_monitor_tuning(model_id, display_name, training_file, epochs):
    """Fine-tuning işlemini başlatır ve tamamlanana kadar izler."""
    logging.info(f"'{model_id}' ID'li model için fine-tuning işlemi başlatılıyor...")
    logging.info(f"Temel Model: {BASE_MODEL}, Epoch Sayısı: {epochs}")

    try:
        operation = genai.create_tuned_model(
            id=model_id,
            display_name=display_name,
            source_model=BASE_MODEL,
            training_data=training_file,
            epoch_count=epochs,
        )

        logging.info("Eğitim arka planda başladı. İlerleme durumu izleniyor...")
        for status in operation.wait_bar():
            # İlerleme çubuğu, bekleme sırasında görsel geri bildirim sağlar.
            pass

        tuned_model = operation.result
        logging.info("Eğitim başarıyla tamamlandı!")
        logging.info(f"Model Adı: {tuned_model.name}")
        logging.info(f"Görünen Ad: {tuned_model.display_name}")
        logging.info(f"Durum: {tuned_model.state}")
        return tuned_model

    except Exception as e:
        logging.error(f"Fine-tuning işlemi sırasında bir hata oluştu: {e}")
        raise

def main():
    """Ana betik akışını yönetir."""
    setup_logging()
    args = parse_arguments()
    
    try:
        check_api_key()
        
        if check_if_model_exists(args.model_id):
            sys.exit(0)
            
        training_file = upload_training_file(args.data_file)
        
        launch_and_monitor_tuning(
            model_id=args.model_id,
            display_name=args.display_name,
            training_file=training_file,
            epochs=args.epochs
        )
        
        logging.info("\nTüm işlemler başarıyla tamamlandı.")

    except (FileNotFoundError, ValueError, Exception) as e:
        logging.error(f"Program bir hata nedeniyle sonlandırıldı: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()